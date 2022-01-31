from components.connection.create_connection import setup_connection
from components.utils.convert_to_dicts import object_as_dict
from components.utils.class_search import get_class_by_name
from sqlalchemy.orm.exc import NoResultFound


def select_source_patient_id_name(hospital_id: str):
    """
    Selects the correct column name for the patient id column. \
    Different hospitals use different names for the patient id \
    column within their systems. This allows the Serums API to \
    retrive this value for use in querying multiple databases

        Parameters:
            hospital_id (str): The hospital to check the patient \
                               id in
        Returns:
            column_name (str): The correct name for the patient id \
                               column within a hospital's system

    """
    connection = setup_connection(hospital_id)
    metadata = connection['metadata']
    table_dict = dict.fromkeys(metadata.sorted_tables)
    connection['engine'].dispose()
    for keys, values in table_dict.items():
        if keys.name == 'serums_ids':
            for column in keys.columns:
                if ".serums_id" not in str(column) \
                        and '.id' not in str(column):
                    return str(column).split(".")[1]


def select_source_patient_id_value(hospital_id, serums_id, key_name):
    """
    Selects the patient id within the hospital's source system. \
    Serums uses a generic id that can be used to link multiple \
    hospitals' data, however, when searching a hospital's system \
    we must use their internal patient id.
        Parameters:
            hospital_id (str): The hospital to check the patient \
                               id in
            serums_id (int): The id used throughout the serums network \
                             linking a single patient across multiple \
                             hospitals
            key_name (str): The name of the patient id column within a \
                            hospital's system
        Returns:
            patient_id (int): The native patient id within the \
                              hospital's system
    """
    connection = setup_connection(hospital_id)
    id_class = get_class_by_name(
        hospital_id.lower() + '.serums_ids',
        connection['base']
    )
    try:
        result = connection['session'].query(id_class).\
            filter_by(serums_id=serums_id).one()
        res = object_as_dict(result)
        return res[key_name]
    except NoResultFound:
        return None
