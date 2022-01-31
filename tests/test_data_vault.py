from py import process
from components.data_vaults.data_vault import generate_boilerplate, \
                                              get_id_columns
from components.data_vaults.satellites import process_value
import datetime
import decimal


def test_get_id_columns():
    result_one = get_id_columns('time_person_link')
    result_two = get_id_columns('person_object_link')
    assert result_one == {'id': [], 'time_id': [], 'person_id': []}
    assert result_two == {'id': [], 'person_id': [], 'object_id': []}


def test_generate_boilerplate():
    boilerplate = generate_boilerplate()
    expected = {
        'hubs': {
            'hub_time': {'id': []},
            'hub_person': {'id': []},
            'hub_object': {'id': []},
            'hub_location': {'id': []},
            'hub_event': {'id': []}
        },
        'links': {
            'time_person_link': {
                'id': [],
                'time_id': [],
                'person_id': []
            },
            'time_object_link': {
                'id': [],
                'time_id': [],
                'object_id': []
            },
            'time_location_link': {
                'id': [],
                'time_id': [],
                'location_id': []
            },
            'time_event_link': {
                'id': [],
                'time_id': [],
                'event_id': []
            },
            'person_object_link': {
                'id': [],
                'person_id': [],
                'object_id': []
            },
            'person_location_link': {
                'id': [],
                'person_id': [],
                'location_id': []
            },
            'person_event_link': {
                'id': [],
                'person_id': [],
                'event_id': []
            },
            'object_location_link': {
                'id': [],
                'object_id': [],
                'location_id': []
            },
            'object_event_link': {
                'id': [],
                'object_id': [],
                'event_id': []
            },
            'location_event_link': {
                'id': [],
                'location_id': [],
                'event_id': []
            }
        }
    }
    assert boilerplate == expected


def test_process_value():
    val_one = process_value(datetime.datetime(1984, 8, 7))
    val_two = process_value("Hello     ")
    val_three = process_value(datetime.time(11, 38, 48))
    val_four = process_value(decimal.Decimal(12378.12237823727319))
    assert val_one == '07/08/1984 00:00:00'
    assert val_two == "Hello"
    assert val_three == '11:38:48'
    assert val_four == 12378.122378237273
