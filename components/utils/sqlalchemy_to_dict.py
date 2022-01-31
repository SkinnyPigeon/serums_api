def convert_tuples_to_dict(row, fields):
    """
    Converts tuples to dictionaries allowing dynamically selected \
    rows from the database to be stored as JSON

        Parameters:
            row (tuple): Data is returned from SQLAlchemy as a \
                         generator of tuples. This is a single \
                         row from within it
            fields (list): The list of fields from the tags \
                           definition that is used as part of \
                           the query function
        Returns:
            row (dict): A dictionary version of the row that uses \
                        the fields as the keys and the tuple \
                        elements as the values
    """
    result_dict = {}
    for index, column in enumerate(fields):
        result_dict[column] = row[index]
    return result_dict
