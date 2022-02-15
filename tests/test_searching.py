from components.search.search import search_field_picker, \
                                     get_serums_id, \
                                     search_for_serums_id


def test_can_pick_hospital():
    result = search_field_picker('ustan')
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
    assert result == 215


def test_can_handle_wrong_patient_number():
    result = get_serums_id('ustan', 912389128398, 'chi')
    assert result is None


def test_can_find_specific_patient():
    query = {
        "patient_id": 1005549224,
        "family_name": "HERMIONE KOCZUR",
        "dob": "1954-05-10",
        "hospital_id": "ustan"
    }
    result = search_for_serums_id(query)
    assert len(result[0]) == 1
    assert result[1] == 200
    assert result[0][0]['serums_id'] == 215


def test_can_find_multiple_patients():
    query = {
        "dob": "1969-07-03",
        "hospital_id": "ustan"
    }
    results = search_for_serums_id(query)
    print(results)
    assert len(results[0]) == 2
    assert results[1] == 200


def test_message_for_bad_queries():
    missing_query = {}
    missing_res = search_for_serums_id(missing_query)
    assert missing_res[1] == 500
    assert missing_res[0] == {
        "message": "Request body must contain 'hospital_id' and it "
                   "must not be blank"
    }
    wrong_date_query = {
        "dob": "2022-09-03",
        "hospital_id": "ustan"
    }
    wrong_date_res = search_for_serums_id(wrong_date_query)
    assert wrong_date_res[1] == 500
    assert wrong_date_res[0] == {
        "message": "No patient found with those details"
    }
    missing_query['hospital_id'] = 'ustan'
    missing_fields_res = search_for_serums_id(missing_query)
    assert missing_fields_res[1] == 500
    assert missing_fields_res[0] == {
        "message": "Please include at least one search term"
    }
