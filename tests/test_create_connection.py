import sqlalchemy
from components.connection.create_connection import setup_connection
from sqlalchemy.engine.base import Engine


def test_can_create_connection():
    connection = setup_connection('ustan')
    assert connection['schema'] == 'ustan'
    assert type(connection['engine']) == Engine
    connection['session'].close()
    connection['engine'].dispose()
