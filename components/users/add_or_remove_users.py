from components.connection.create_connection import setup_connection
# from psycopg2.errors import UniqueViolation
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError


def select_source_patient_id_name(schema):
    """Selects the correct column name for the patient id column. \
       Different hospitals use different names for the patient id \
       column within their systems. This allows the Serums API to \
       retrive this value for use in querying multiple databases

            Parameters:

                body (dict): The request body passed from the frontend
            Returns:
                column_name (str): The correct name for the patient id \
                                   column within a hospital's system

    """
    connection = setup_connection(schema)
    metadata = connection['metadata']
    table_dict = dict.fromkeys(metadata.sorted_tables)
    connection['engine'].dispose()
    for keys, values in table_dict.items():
        if keys.name == 'serums_ids':
            for column in keys.columns:
                if ".serums_id" not in str(column) \
                  and '.id' not in str(column):
                    return str(column).split(".")[1]


def get_id_table_class(schema, base):
    """Selects the class object for the id table

            Parameters:
                schema (str): The schema within the database to search through
                base (Base): The SQLAlchemy Base instance that contains the \
                             relevant metadata to enable the search
            Returns:
                table (obj): A SQLAlchemy Table class object
    """
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') \
          and class_name.__table__.fullname == f"{schema}.serums_ids":
            return class_name


def remove_user(serums_id, hospital_ids):
    """Deletes a user from one or more hospital's serums_ids table.
       This instantly severs the system's ability to access the patient's \
       records even before their medical data is removed during the next \
       nightly ETL process

            Parameters:
                serums_id (int): The Serums ID of the patient who is to be \
                                 removed from the system
                hospital_ids (list): A list of hospital IDs from which to \
                                     remove the patient's link to. This can \
                                     be one of more, and does not have to \
                                     be all of the hospitals they have linked
            Response:
                response (tup): A response message based on whether or not \
                                the action was successful plus a response \
                                status code e.g. 200
    """
    for hospital_id in hospital_ids:
        schema = hospital_id.lower()
        connection = setup_connection(schema)
        try:
            serums_ids_table = connection['metadata'].\
                tables[f'{schema}.serums_ids']
            stmt = serums_ids_table.delete().\
                where(serums_ids_table.c.serums_id == serums_id)
            res = connection['engine'].execute(stmt)
            deleted_user = res.rowcount
            connection['engine'].dispose()
            if deleted_user == 0:
                return {"message": f"User not found in {hospital_id}"}, 500
        except Exception as e:
            connection['engine'].dispose()
            return {
                "message": f"Error removing user from {hospital_id}",
                "error": str(e)
            }, 500
    return {"message": f"User successfully removed from {hospital_ids}"}, 200


def add_user(serums_id, patient_id, hospital_id):
    """Adds a user to a hospital's serums_ids table. This allows their serums \
       id to be linked to any of their available data in the data lake.

            Parameters:
                serums_id (int): The Serums ID of the patient who is to be \
                                 added to the system
                patient_id (int): The patient's id within a hospital's \
                                  internal systems to link to a Serums ID \
                hospital_id (str): The hospital id to which the patient's \
                                   serums ID will be linked
            Response:
                response (tup): A response message based on whether or not \
                                the action was successful plus a response \
                                status code e.g. 200
    """
    schema = hospital_id.lower()
    id_column_name = select_source_patient_id_name(schema)
    connection = setup_connection(schema)
    try:
        serums_ids_table = get_id_table_class(schema, connection['base'])
        stmt = (insert(serums_ids_table).
                values(**{
                    id_column_name: patient_id,
                    'serums_id': serums_id
                }))
        connection['engine'].execute(stmt)
        connection['engine'].dispose()
        return {"message": "User added correctly"}, 200
    except IntegrityError as i:
        connection['engine'].dispose()
        return {
            "message": "User with that Serums ID already exists"
        }, 500
