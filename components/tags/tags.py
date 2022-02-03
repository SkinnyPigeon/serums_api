from components.connection.create_connection import setup_connection
from sqlalchemy import select


def get_tags(hospital_id):
    """
    Returns a list of tags and translated tags available for an \
    individual hospital
        Parameters:
            body (dict): The request body from the api call
        Returns:
            tags (dict): A dictionary with two keys: tags (a list of the \
                         available tags for a hospital) and translated_tags \
                         (a dictionary where the keys are the tags from the \
                         tag list and the values contain the \
                         translation/human friendly version)
    """

    connection = setup_connection(hospital_id)
    try:
        tags_table = connection['metadata'].\
            tables[f'{hospital_id.lower()}.tags']
        stmt = (select([tags_table.c.tags]))
        tags = connection['engine'].execute(stmt).fetchone()

        translate_tags_table = connection['metadata'].\
            tables[f'{hospital_id.lower()}.translated_tags']
        stmt = (select([translate_tags_table.c.tags]))
        translate_tags = connection['engine'].execute(stmt).fetchone()

        results = {}
        results['tags'] = tags[0]
        results['translated'] = translate_tags[0]
        connection['session'].close()
        connection['engine'].dispose()
        return results
    except Exception as e:
        connection['session'].close()
        connection['engine'].dispose()
        return {"error": str(e)}
