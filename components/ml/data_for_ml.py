from multiprocessing import connection
from components.utils.convert_dtypes import convert_decimal_to_float, \
                                            convert_dates_to_string
from components.connection.create_connection import setup_connection
from components.utils.objects_to_dicts import object_as_dict
from components.utils.select_source_id import select_source_patient_id_name, \
                                              select_source_patient_id_value
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd


def select_patient_data(table_class, patient_id, key_name):
    """
    Selects the data within from a hospital's source system for use \
    by the machine learning algorithm
        Parameters:
            session (Session): The SQLAlchemy session to run the query with
            tables (dict): A dictionary that uses the table names as the \
                           keys and SQLAlchemy table classes as the values
            tag_definition (dict): A tag definition that is based \
                                   on the tags field in the request body
            patient_id (int): The native patient id within the \
                              hospital's system
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            smart_patient_health_record (DataFrame): A DataFrame containing \
                                                     the selected patient data
    """
    connection = setup_connection('ustan')
    results = connection['session'].query(table_class).\
        filter_by(**{key_name: patient_id}).all()
    data = []
    for row in results:
        data.append(object_as_dict(row))

    df = pd.DataFrame([x for x in data])
    df = convert_dates_to_string(df)
    df = convert_decimal_to_float(df)
    connection['engine'].dispose()
    return df.to_dict('index')


def get_patient_data_for_ml(body):
    """
    The main function for selecting the data for the machine \
    learning algorithm
        Parameters:
            body (dict): The request body from the api call
        Returns:
            patient_data (dict): The complete dump of data for a \
                                 single patient
    """
    results = {}
    tables = [
        'cycles',
        'general',
        'intentions',
        'patients',
        'regimes',
        'smr01',
        'smr06'
    ]
    try:
        connection = setup_connection(body)
        id_class = connection['base'].classes.serums_ids
        key_name = select_source_patient_id_name(body)
        patient_id = select_source_patient_id_value(connection['session'],
                                                    id_class,
                                                    body['serums_id'],
                                                    key_name
                                                    )
        for table in tables:
            table_class = connection['base'].classes[table]
            data = select_patient_data(
                table_class,
                patient_id,
                key_name
            )
            results[table] = data
        connection['engine'].dispose()
        return results
    except NoResultFound as n:
        connection['engine'].dispose()
        return {"message": "Patient not found with that Serums ID"}
    except Exception as e:
        connection['engine'].dispose()
        return {"error": str(e)}
