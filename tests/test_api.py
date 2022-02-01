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
    assert res.status_code == 200
    expected_keys = ['FCRB', 'USTAN', 'ZMC']
    assert sorted(dict(res.json()).keys()) == sorted(expected_keys)


def test_add_user():
    admin_header = {
        'Authorization': 'Bearer ' + admin_jwt
    }
    unauthorized_header = {
        'Authorization': 'Bearer ' + patient_jwt
    }
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
                                     headers=unauthorized_header)
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
