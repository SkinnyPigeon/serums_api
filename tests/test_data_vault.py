from py import process
from components.data_vaults.data_vault import generate_boilerplate, \
                                              get_id_columns
from components.data_vaults.satellites import process_value, \
                                              process_satellites
from components.sphr.get_source_data import get_patient_data, \
                                            parse_sphr
from tests.test_valid_staff_jwt import right_jwt as staff_jwt
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


def test_process_satellites():
    data, _ = get_patient_data(
        117,
        ['ustan'],
        ['patient_details', 'medication', 'wearble'],
        staff_jwt
    )
    result = process_satellites(data)
    expected = {
        'USTAN': {
            'ustan.general': {
                'links': [
                    'time_person_link',
                    'time_location_link',
                    'time_event_link',
                    'person_location_link',
                    'person_event_link',
                    'location_event_link'
                ],
                'sat_time_general_details': {
                    'hub': 'hub_time',
                    'data': [
                        {
                            'first_seen_date': '18/04/2017 00:00:00',
                            'dat_death': None
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_person_general_patient': {
                    'hub': 'hub_person',
                    'data': [
                        {
                            'name': 'HERMIONE KOCZUR',
                            'date_of_birth': '10/05/1954 00:00:00',
                            'dob': '10/05/1954 00:00:00',
                            'gender': 2,
                            'religion': 0,
                            'civil_st': 9,
                            'postcode': 'KY953HY'
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_person_general_gp': {
                    'hub': 'hub_person',
                    'data': [{}],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_location_general_details': {
                    'hub': 'hub_location',
                    'data': [
                        {
                            'ref_hospital': 617
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_event_general_details': {
                    'hub': 'hub_event',
                    'data': [
                        {
                            'smid': None,
                            'smid1': None,
                            'death_flag': 0
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                }
            }
        }
    }
    assert type(result) == dict
    assert result == expected
