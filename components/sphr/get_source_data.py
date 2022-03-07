from control_files.tags.ustan import ustan_tags
from control_files.tags.fcrb import fcrb_tags
from control_files.tags.zmc import zmc_tags
from components.utils.class_search import get_class_by_name
from components.connection.create_connection import setup_connection
from components.utils.convert_to_dicts import tuples_as_dict
from sqlalchemy.exc import InvalidRequestError
from components.utils.convert_dtypes import convert_dates_to_string, \
                                            convert_decimal_to_float
from components.jwt.validate import validate_jwt
from components.blockchain.rules import get_valid_tags
from components.blockchain.lineage import create_record
from components.utils.select_source_id import select_source_patient_id_name, \
                                              select_source_patient_id_value
import pandas as pd


def tag_picker(hospital_id: str):
    """
    Returns a lowercased hospital id and tag definitions.
        Parameters:
            hospital_id (str): The internal reference for the hospitals \
                               within the Serums system
        Returns:
            hospital_tags (list): A list of tag definitions. These are \
                                  designed by the hospitals to subset \
                                  their data in ways that the patients can \
                                  intuitively understand when they create \
                                  rules. These definitions show:\n
            - The source table that holds the data
            - The columns within the source table that are governed by the tag
    """
    if hospital_id.lower() == 'ustan':
        return ustan_tags
    elif hospital_id.lower() == 'fcrb':
        return fcrb_tags
    elif hospital_id.lower() == 'zmc':
        return zmc_tags


def select_tags(tags_list: list, request_tags: list):
    """
    Selects the relevant tag definition(s) based on \
    the valid tags for a request
        Parameters:
            tags_list (list): The tag definitions as selected \
                              by tag_picker()
            request_tags (list): The list of valid tags which \
                                 have been requested
        Returns:
            selected_tags (list): A list of the tag definitions that \
                                  is based on the valid tags found \
                                  in the request body
    """
    selected_tags = []
    for request_tag in request_tags:
        for tag_definition in tags_list:
            if tag_definition['tag'] == request_tag:
                selected_tags.append(tag_definition)
    return selected_tags


def select_tabular_patient_data(tag_definition: dict,
                                patient_id: int,
                                key_name: str):
    """
    Selects the tabular data within from a hospital's source system

        Parameters:
            tag_definition (dict): A tag definition that is based on \
                                    the valid tags in the request body
            patient_id (int): The native patient id within \
                                the hospital's system
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            smart_patient_health_record (DataFrame): A DataFrame containing \
                                                     the selected patient \
                                                     data
    """
    data = []
    hospital_id = tag_definition['source'].split('.')[0]
    connection = setup_connection(hospital_id)
    table_class = get_class_by_name(
        tag_definition['source'],
        connection['base']
    )
    fields = tag_definition['fields']
    entities = []
    for field in fields:
        entities.append(getattr(table_class, field))
    try:
        result = connection['session'].query(table_class).\
                with_entities(*entities).\
                filter_by(**{key_name: patient_id}).all()
        for row in result:
            data.append(tuples_as_dict(row, fields))
        connection['session'].close()
        connection['engine'].dispose()
    except InvalidRequestError:
        # This is where foreign key lookups are handled for the FCRB use case.
        # It works by using a special value in the tag definition 'key_lookup'.
        # This is then used to select the patient's native id from a table in
        # which it is found, alongside all the relevant foreign keys in order
        # to join them onto this the table which is missing the patient's id.

        # For instance, there is a staff table which does not have a patient id
        # in it. However, there is another table which has the id of the doctor
        # who treated the patient. We use the patient's id in this table to get
        # the ids of the doctors who treated them and then use those as keys to
        # the table we were originally querying
        foreign_key_table_class = get_class_by_name(
            tag_definition['key_lookup']['table'],
            connection['base']
        )
        foreign_key = tag_definition['key_lookup']['key']
        key_entities = []
        key_entities.append(getattr(foreign_key_table_class, foreign_key))
        key_result = connection['session'].query(foreign_key_table_class).\
            with_entities(*key_entities).\
            filter_by(**{key_name: patient_id}).all()
        for row in key_result:
            result = connection['session'].query(table_class).\
                with_entities(*entities).\
                filter_by(**{foreign_key: row[0]}).all()
            for row in result:
                data.append(tuples_as_dict(row, fields))
        connection['session'].close()
        connection['engine'].dispose()
    return data


def setup_for_query(jwt: str, tags: list, serums_id: int, hospital_ids: list):
    """
    Handles some of the necessary preparation for the data to be selected. \
    Specifically, it selects the tags definitions which are valid and \
    begins a new record on the lineage blockchain, returning a reference \
    to this record as well as the valid tags

        Parameters:
            jwt (str): The JWT used to authenticate a user within \
                       the Serums system. This is generated by the \
                       authentication module
            tags (list): The list of tags found in the query request body
            serums_id (int): The id of the patient within the Serums system
            hospital_ids (list): A list of the hospital ids from whom data \
                                 will be selected
        Returns:
            proof_id (str): A unique reference to the newly created \
                            record on the lineage blockchain that \
                            will be used to update the status throughout \
                            the creation and transmission of the SPHR
            valid_tags (list): A list containing the tags which have been \
                               validated as accessible to the requestor
    """
    jwt_response = validate_jwt(jwt)
    proof_id = None
    if 'PATIENT' in jwt_response['user_type']:
        valid_tags = tags
        rule_ids = 'PATIENT-ACCESSING-OWN-RECORD'
    else:
        valid_tags, rule_ids = get_valid_tags(jwt, serums_id)
        valid_tags = list(set(valid_tags).intersection(tags))
    if valid_tags is not None:
        proof_id = create_record(serums_id, rule_ids, hospital_ids)
    return proof_id, valid_tags


def select_patient_data(tags_definitions: list,
                        patient_id: int,
                        key_name: str):
    """
    Loops through the tags and selects the relevant data, collating it \
    ready for returning
        Parameters:
            tag_definitions (list): A list of tag definitions. These are \
                                    designed by the hospitals to subset \
                                    their data in ways that the patients \
                                    can intuitively understand when they \
                                    create rules
            patient_id (int): The native patient id within the \
                              hospital's system
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            smart_patient_health_record (dict): A dictionary containing the \
                                                selected patient data
    """
    results = {}
    for tag_definition in tags_definitions:
        results[tag_definition['source']] = select_tabular_patient_data(
            tag_definition, patient_id, key_name
        )
    return results


def parse_sphr(patient_data):
    """
    Parses the data of the standard Smart Patient Health Record. \
    This converts dates to strings and decimals to floats allowing \
    them to be sent as JSON.
        Parameters:
            patient_data (dict): The patient data that has been \
                                 selected by the API call
        Returns:
            result (dict): The parsed data that is ready for \
                           transmission as JSON

    """
    result = {}
    for hospital in patient_data:
        result[hospital] = {}
        for table in patient_data[hospital]['data']:
            df = pd.DataFrame(
                [x for x in patient_data[hospital]['data'][table]]
            )
            df = convert_dates_to_string(df)
            df = convert_decimal_to_float(df)
            result[hospital][table] = df.to_dict('index')
    return result


def get_patient_data(serums_id: int, hospital_ids: list, tags: list, jwt: str):
    """
    The main function for generating the Smart Patient Health Record
        Parameters:
            serums_id (str): The serums_id of the patient whose data is being \
                             requested
            hospital_ids (list): A list of hospital_ids from which to search \
                                 for patient data in
            tags (list): A list of tags that will be used to select a subset \
                         of data with
            jwt (str): The JavaScript Web Token that is used to verify the \
                       identity of the system user
        Returns:
            smart_patient_health_record (dict): A dictionary containing \
                                                the selected patient data
    """
    results = {}
    proof_id, valid_tags = setup_for_query(jwt,
                                           tags,
                                           serums_id,
                                           hospital_ids)
    if valid_tags is not None:
        for hospital_id in hospital_ids:
            results[hospital_id.upper()] = {}
            results[hospital_id.upper()]['data'] = {}
            tags_list = tag_picker(hospital_id)
            tags = select_tags(tags_list, valid_tags)
            key_name = select_source_patient_id_name(hospital_id)
            patient_id = select_source_patient_id_value(
                hospital_id,
                serums_id,
                key_name
            )
            data = {}
            for tag_definition in tags:
                data[tag_definition['source']] = select_tabular_patient_data(
                    tag_definition, patient_id, key_name
                )
            if len(data) > 0:
                results[hospital_id.upper()]['data'] = data
            elif len(data) == 0:
                results[hospital_id.upper()]['data'] = {}
            results[hospital_id.upper()]['tags'] = tags
        return results, proof_id
    else:
        return False, None
