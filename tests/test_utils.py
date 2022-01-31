from components.utils.class_search import get_class_by_name
from components.connection.create_connection import setup_connection
from sqlalchemy.ext.declarative.api import DeclarativeMeta


def test_can_get_class_by_name():
    connection = setup_connection('ustan')
    result = get_class_by_name('ustan.serums_ids', connection['base'])
    assert type(result) == DeclarativeMeta
    bad_result = get_class_by_name('ustan.fake_table', connection['base'])
    assert bad_result is None
