from sqlalchemy import inspect


def object_as_dict(obj: object):
    """
    Returns an object as a dictionary by list comprehension
        Parameters:
            obj (obj): The object to be converted into a dictionary
        Returns:
            dict (dict): A dictionary based on the object
    """
    return {
        column.key: getattr(obj, column.key)
        for column in inspect(obj).mapper.column_attrs
    }


def tuples_as_dict(row: tuple, fields: list):
    """
    Converts tuples to dictionaries allowing dynamically selected \
    rows from the database to be stored as JSON
        Parameters:
            row (tuple): Data is returned from SQLAlchemy as a generator of \
                         tuples. This is a single row from within it
            fields (list): The list of fields from the tags definition that \
                           is used as part of the query function
        Returns:
            row (dict): A dictionary version of the row that uses the fields \
                        as the keys and the tuple elements as the values
    """
    row_dict = {}
    if len(row) == len(fields):
        for index, column in enumerate(fields):
            row_dict[column] = row[index]
        return row_dict
    return None
