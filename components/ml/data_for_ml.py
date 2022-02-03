from components.utils.convert_dtypes import convert_decimal_to_float, \
                                            convert_dates_to_string
from components.connection.create_connection import setup_connection
from components.utils.convert_to_dicts import object_as_dict
from components.utils.select_source_id import select_source_patient_id_name, \
                                              select_source_patient_id_value
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative.api import DeclarativeMeta
import pandas as pd


def select_patient_data(
        table_class: DeclarativeMeta,
        patient_id: int,
        key_name: str):
    """
    Selects the data within from a hospital's source system for use \
    by the machine learning algorithm
        Parameters:
            table_class (DeclarativeMeta): The SQLAlchemy Table object \
                                           that will be queried
            patient_id (int): The native patient id within the \
                              hospital's system
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            smart_patient_health_record (dict): A dictionary containing \
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
    connection['session'].close()
    connection['engine'].dispose()
    return df.to_dict('index')


def get_patient_data_for_ml(serums_id: int):
    """
    The main function for selecting the data for the machine \
    learning algorithm. Since it is only for the USTAN use case, \
    there are hard coded values such as the hospital id being set \
    to 'ustan' and the table names. These could easily be dynamically \
    set if needed.
        Parameters:
            serums_id (int): The id of the patient whose data \
                             is being accessed
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
        connection = setup_connection('ustan')
        key_name = select_source_patient_id_name('ustan')
        patient_id = select_source_patient_id_value(
            'ustan',
            serums_id,
            key_name
        )
        if patient_id is None:
            return {"message": "Patient not found with that Serums ID"}, 500
        for table in tables:
            table_class = connection['base'].classes[table]
            data = select_patient_data(
                table_class,
                patient_id,
                key_name
            )
            results[table] = data
        connection['session'].close()
        connection['engine'].dispose()
        return results, 200
    except NoResultFound as n:
        connection['session'].close()
        connection['engine'].dispose()
        return {"message": "Patient not found with that Serums ID"}, 500
    except Exception as e:
        connection['session'].close()
        connection['engine'].dispose()
        return {"error": str(e)}, 500
