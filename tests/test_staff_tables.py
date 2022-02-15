from components.staff.departments import get_department_of_staff_member, \
                                         get_departments


def test_should_return_existing_member_of_staff():
    result = get_department_of_staff_member('ustan', 216)
    expected = {
        "serums_id": 216,
        "staff_id": 3006,
        "name": "Ella Murray",
        "department_id": 4,
        "department_name": "MEDICAL_STAFF"
    }
    assert result == expected


def test_should_return_none_if_not_correct_staff_id():
    result = get_department_of_staff_member('ustan', 19283)
    assert result is None


def test_should_return_a_list_of_staff():
    results = get_departments('ustan')
    assert len(results) == 8
    expected_keys = [
        'serums_id',
        'staff_id',
        'name',
        'department_id',
        'department_name'
    ]
    assert list(dict.fromkeys(results[0])) == expected_keys
