from control_files.tags.ustan import ustan_tags
from components.utils.class_search import get_class_by_name
from components.connection.create_connection import setup_connection
from components.utils.convert_to_dicts import tuples_as_dict
from sqlalchemy.exc import InvalidRequestError


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
    if hospital_id == 'ustan':
        return ustan_tags


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
    table_class = get_class_by_name(tag_definition['source'])
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
            connection['engine'].dispose()
    except InvalidRequestError as i:
        # This is where foreign key lookups are handled for the FCRB use case
        foreign_key_table_class = get_class_by_name(
            tag_definition['key_lookup']['table']
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
        connection['engine'].dispose()
    return data
