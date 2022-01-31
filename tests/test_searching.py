from components.search.search import hospital_picker, \
                                     get_serums_id
from components.connection.create_connection import setup_connection


def test_can_pick_hospital():
    result = hospital_picker('ustan')
    expected = {
        'source': 'ustan.general',
        'fields': {
            'patient_id': 'chi',
            'first_name': 'name',
            'family_name': 'name',
            'dob': 'date_of_birth',
            'gender': 'gender'
        }
    }
    assert result == expected


def test_can_get_serums_id():
    result = get_serums_id('ustan', 1005549224, 'chi')
    assert result == 117


def test_can_handle_wrong_patient_number():
    result = get_serums_id('ustan', 912389128398, 'chi')
    assert result is None
