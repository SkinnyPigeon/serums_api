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
