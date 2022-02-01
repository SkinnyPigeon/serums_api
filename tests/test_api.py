import requests
from tests.test_jwt_validation import JWT as patient_jwt
from tests.test_valid_staff_jwt import right_jwt as staff_jwt

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
