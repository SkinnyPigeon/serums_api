import requests
from tests.test_jwt_validation import JWT as patient_jwt
from tests.test_valid_staff_jwt import right_jwt as staff_jwt

admin_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
            "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
            "joxNjQ2MzAyMTM5LCJqdGkiOiI5NTBkYzEzMj"\
            "A1MjQ0N2VhOTQ0YzQ5Mzk5N2JhODE0NiIsInV"\
            "zZXJJRCI6MTIxLCJpc3MiOiJTZXJ1bXNBdXRo"\
            "ZW50aWNhdGlvbiIsImlhdCI6MTY0MzcxMDEzO"\
            "Swic3ViIjoiaG9zcGFkbTFAdXN0YW4uY29tIi"\
            "wiZ3JvdXBJRHMiOlsiSE9TUElUQUxfQURNSU4"\
            "iXSwib3JnSUQiOiJVU1RBTiIsImRlcHRJRCI6"\
            "NSwiZGVwdE5hbWUiOiJIT1NQSVRBTF9BRE1JT"\
            "iIsInN0YWZmSUQiOjEyMSwibmFtZSI6Ik9saX"\
            "ZlciBXaWxzb24iLCJhdWQiOiJodHRwczovL3N"\
            "oY3Muc2VydW1zLmNzLnN0LWFuZHJld3MuYWMu"\
            "dWsvIn0.JAYsr1P5EBO04C7BggojLS8Kvc0en"\
            "eg0H2PrHtvmrqs"

URL = 'http://localhost:8000/'

admin_header = {
    'Authorization': 'Bearer ' + admin_jwt
}

staff_header = {
    'Authorization': 'Bearer ' + staff_jwt
}

patient_header = {
    'Authorization': 'Bearer ' + patient_jwt
}


def test_hello():
    res = requests.get(URL + 'hello/hello')
    assert res.status_code == 200
    assert res.json() == {"hello": "Welcome to the API. The server is on"}


def test_departments():
    body = {
        'hospital_id': 'USTAN'
    }
    res = requests.post(URL + 'staff_tables/departments', json=body)
    assert res.status_code == 200
    assert len(res.json()) > 0
    assert type(res.json()[0])


def test_get_department_of_staff_member():
    header = {
        'Authorization': 'Bearer ' + staff_jwt
    }
    res = requests.get(URL + 'staff_tables/get_department_of_staff_member',
                       headers=header)
    assert res.status_code == 200
    expected = [
        'serums_id',
        'staff_id',
        'name',
        'department_id',
        'department_name'
    ]
    assert sorted(dict(res.json()).keys()) == sorted(expected)
    bad_res = requests.get(URL + 'staff_tables/get_department_of_staff_member')
    assert bad_res.status_code == 403


def test_get_single_hospital_tags():
    body = {
        'hospital_id': 'USTAN'
    }
    res = requests.post(URL + 'tags_tables/tags', json=body)
    assert res.status_code == 200
    expected_keys = ['tags', 'translated']
    assert sorted(dict(res.json()).keys()) == sorted(expected_keys)
    assert len(dict(res.json())['tags']) > 0


def test_get_multi_hospital_tags():
    body = {
        'hospital_ids': [
            'USTAN',
            'FCRB',
            'ZMC'
        ]
    }
    res = requests.post(URL + 'tags_tables/all_tags', json=body)
    print(res.json())
    assert res.status_code == 200
    expected_keys = ['FCRB', 'USTAN', 'ZMC']
    assert sorted(dict(res.json()).keys()) == sorted(expected_keys)


def test_add_user():
    body = {
        "serums_id": 26538,
        "patient_id": 1923893,
        "hospital_id": "USTAN"
    }
    del_body = {
        "serums_id": 26538,
        "hospital_ids": ["USTAN"]
    }
    # Remove user if necessary
    requests.post(URL + 'users/remove_user',
                  json=del_body,
                  headers=admin_header)

    unauthorized_res = requests.post(URL + 'users/add_user',
                                     json=body,
                                     headers=patient_header)
    no_header_res = requests.post(URL + 'users/add_user', json=body)
    authorized_res = requests.post(URL + 'users/add_user',
                                   json=body,
                                   headers=admin_header)
    assert unauthorized_res.status_code == 401
    print(dict(unauthorized_res.json()))
    assert dict(unauthorized_res.json())['message'] == \
        "Only admins can add users"
    assert no_header_res.status_code == 403
    assert dict(no_header_res.json())['detail'] == \
        "Not authenticated"
    assert authorized_res.status_code == 200
    assert dict(authorized_res.json())['message'] == \
        "User added correctly"


def test_remove_user():
    add_body = {
        "serums_id": 26538,
        "patient_id": 1923893,
        "hospital_id": "USTAN"
    }
    body = {
        "serums_id": 26538,
        "hospital_ids": ["USTAN", "FCRB"]
    }

    # Add user if necessary
    requests.post(URL + 'users/add_user',
                  json=add_body,
                  headers=admin_header)

    unauthorized_res = requests.post(URL + 'users/remove_user',
                                     json=body,
                                     headers=patient_header)
    no_header_res = requests.post(URL + 'users/remove_user', json=body)
    authorized_res = requests.post(URL + 'users/remove_user',
                                   json=body,
                                   headers=admin_header)
    assert unauthorized_res.status_code == 401
    assert dict(unauthorized_res.json())['message'] == \
        "Only admins can remove users"
    assert no_header_res.status_code == 403
    assert dict(no_header_res.json())['detail'] == \
        "Not authenticated"
    assert authorized_res.status_code == 200
    assert dict(authorized_res.json()) == \
        {
            "ustan": {
                "message": "User successfully removed from USTAN"
            },
            "fcrb": {
                "message": "User not found in FCRB"
            }
        }


def test_get_ml():
    unauthorized_res = requests.get(URL + 'machine_learning/analytics',
                                    headers=admin_header)
    no_header_res = requests.get(URL + 'machine_learning/analytics')
    authorized_res = requests.get(URL + 'machine_learning/analytics',
                                  headers=patient_header)
    assert unauthorized_res.status_code == 401
    assert dict(unauthorized_res.json())['message'] == \
        "Only patients can access their own ML data"
    assert no_header_res.status_code == 403
    assert dict(no_header_res.json())['detail'] == \
        "Not authenticated"
    assert authorized_res.status_code == 200
    expected_keys = [
        'cycles',
        'general',
        'intentions',
        'patients',
        'regimes',
        'smr01',
        'smr06'
    ]
    assert sorted(dict(authorized_res.json()).keys()) == sorted(expected_keys)


def test_search():
    good_body = {
        "patient_id": 1005549224,
        "dob": "1954-05-10",
        "hospital_id": "ustan"
    }
    missing_hospital = {
        "patient_id": 1005549224,
        "dob": "1954-05-10",
    }
    wrong_details = {
        "patient_id": 1,
        "dob": "1954-05-10",
        "hospital_id": "ustan"
    }

    unauthorized_res = requests.post(URL + 'search/serums_id',
                                     headers=patient_header,
                                     json=good_body)
    no_header_res = requests.post(URL + 'search/serums_id', json=good_body)
    authorized_res = requests.post(URL + 'search/serums_id',
                                   headers=admin_header,
                                   json=good_body)
    assert unauthorized_res.status_code == 401
    assert dict(unauthorized_res.json())['message'] == \
        "Must be either a medical staff or admin to search for users"
    assert no_header_res.status_code == 403
    assert dict(no_header_res.json())['detail'] == \
        "Not authenticated"
    assert authorized_res.status_code == 200
    expected = [
        {
            "chi": 1005549224,
            "name": "HERMIONE KOCZUR",
            "date_of_birth": "1954-05-10",
            "gender": 2,
            "serums_id": 117
        }
    ]
    assert authorized_res.json() == expected
    missing_hospital_res = requests.post(URL + 'search/serums_id',
                                         headers=admin_header,
                                         json=missing_hospital)
    wrong_details_res = requests.post(URL + 'search/serums_id',
                                      headers=admin_header,
                                      json=wrong_details)
    assert missing_hospital_res.status_code == 422
    assert wrong_details_res.status_code == 500
    assert wrong_details_res.json() == \
        {"message": "Unable to find a patient with those details"}
