from components.staff.departments import get_department_of_staff_member


def test_should_return_existing_member_of_staff():
    result = get_department_of_staff_member('ustan', 81)
    expected = {
        'serums_id': 81,
        'staff_id': 81,
        'name': 'Charlotte Wilson',
        'department_id': 4,
        'department_name': 'MEDICAL_STAFF'
    }
    assert result == expected


def test_should_return_none_if_not_correct_staff_id():
    result = get_department_of_staff_member('ustan', 19283)
    assert result is None
