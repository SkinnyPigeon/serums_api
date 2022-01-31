from components.connection.create_connection import setup_connection
from control_files.search_details.ustan import ustan_patient_details


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
