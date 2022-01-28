from sqlalchemy import select
from components.connection.create_connection import setup_connection


def get_department_of_staff_member(hospital_id: str, serums_id: int):
    """Returns the details about a single staff member \
       for a healthcare provider.

            Parameters:
                body (dict): The response body of the validate_jwt \
                             function
            Returns:
                department_ids (list):  A list of dictionaries containing \
                                        the details of a single staff member \
                                        for a particular healthcare provider
    """
    connection = setup_connection(hospital_id)
    department_table = connection['base'].classes['hospital_doctors']
    query = select([
        department_table.serums_id,
        department_table.staff_id,
        department_table.name,
        department_table.department_id,
        department_table.department_name
    ], department_table.serums_id == serums_id)
    details = connection['engine'].execute(query).fetchone()
    connection['session'].close()
    connection['engine'].dispose()
    if details is not None:
        return {
            'serums_id': details[0],
            'staff_id': details[1],
            'name': details[2].replace("'", ""),
            'department_id': details[3],
            'department_name': details[4]
        }
    else:
        return None


def get_departments():
    pass


def check_staff_member():
    pass
