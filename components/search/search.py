from components.connection.create_connection import setup_connection
from components.utils.class_search import get_class_by_name
from components.utils.convert_dtypes import convert_dates_to_string, \
                                            convert_decimal_to_float
from control_files.search_details.ustan import ustan_patient_details
from control_files.search_details.fcrb import fcrb_patient_details
from control_files.search_details.zmc import zmc_patient_details
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd


def search_field_picker(hospital: str):
    """
    Returns a lowercased hospital id, the table name holding \
    the searchable fields, and a dictionary that maps the search \
    fields to their native names within a hospital's system
        Parameters:
            hospital (str): The internal reference for the hospitals \
            within the Serums system
        Returns:
            patient_details (dict): A dictionary that maps the search \
                                    terms to their native values within a \
                                    hospital's system
    """
    if hospital.lower() == 'ustan':
        return ustan_patient_details
    elif hospital.lower() == 'fcrb':
        return fcrb_patient_details
    elif hospital.lower() == 'zmc':
        return zmc_patient_details


def get_serums_id(hospital_id: str, patient_id: int, key_name: str):
    """
    Searches the system for a particular user's Serums id based \
    on their native patient id number

        Parameters:
            hospital_id (str): The hospital to check the patient \
                               id in
            patient_id (int): The native patient id within the hospital's \
                              system
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            serums_id (int): The id used throughout the serums network \
                             linking a single patient across multiple \
                             hospitals
    """
    connection = setup_connection(hospital_id)
    id_class = connection['base'].classes.serums_ids
    serums_id_column = id_class.serums_id
    try:
        results = connection['session'].query(id_class).\
            with_entities(serums_id_column).\
            filter_by(**{key_name: int(patient_id)}).one()
        connection['session'].close()
        connection['engine'].dispose()
        return results[0]
    except NoResultFound:
        connection['session'].close()
        connection['engine'].dispose()
        return None


def search_for_serums_id(body: dict):
    """
    Search function to find a patient's Serums id based on \
    information provided such as: name, dob, gender, native patient id, etc.
        Parameters:
            body (dict): The request body from the api call
        Returns:
            serums_ids (list): A list of patients who match the search criteria
    """
    if 'hospital_id' not in body.keys() or body['hospital_id'] in ["", None]:
        return {
            "message": "Request body must contain 'hospital_id' and it "
                       "must not be blank"
        }, 500
    schema = body['hospital_id'].lower()
    search_fields = search_field_picker(schema)
    connection = setup_connection(schema)
    table_class = get_class_by_name(
        search_fields['source'],
        connection['base']
    )
    filters = {
        search_fields['fields'][key]: body[key] for key in body
        if key in search_fields['fields']
        and body[key] not in ["", None]
    }
    if len(filters) > 0:
        fields = [*search_fields['fields'].values()]
        entities = [getattr(table_class, field) for field in fields]
        try:
            ids = []
            results = connection['session'].query(table_class).\
                with_entities(*entities).filter_by(**filters).all()
            for result in results:
                data = {
                    field: result[index] for index, field in enumerate(fields)
                }
                df = pd.DataFrame(data, index=[0])
                df = convert_dates_to_string(df)
                df = convert_decimal_to_float(df)
                serums_id = get_serums_id(
                    schema,
                    df[search_fields['fields']['patient_id']][0],
                    search_fields['fields']['patient_id']
                )
                df['serums_id'] = serums_id
                ids.append(df.to_dict('index')[0])
                connection['engine'].dispose()
            if len(ids) > 0:
                return ids, 200
            else:
                return {"message": "No patient found with those details"}, 500
        except NoResultFound:
            connection['engine'].dispose()
            return {"message": "No patient found with those details"}, 500
        except Exception as e:
            connection['engine'].dispose()
            return {"message": str(e)}, 500
    else:
        connection['engine'].dispose()
        return {"message": "Please include at least one search term"}, 500
