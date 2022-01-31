from components.connection.create_connection import setup_connection
from control_files.search_details.ustan import ustan_patient_details
from sqlalchemy.orm.exc import NoResultFound


def hospital_picker(hospital: str):
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
    if hospital == 'ustan':
        return ustan_patient_details


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
