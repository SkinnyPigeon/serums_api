from components.search.search import hospital_picker


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
