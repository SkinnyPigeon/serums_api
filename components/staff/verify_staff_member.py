from components.jwt.validate import validate_jwt
from components.staff.departments import get_department_of_staff_member


def check_staff_member(jwt: str):
    result = {}
    jwt_response = validate_jwt(jwt)
    if jwt_response['status_code'] == 200 \
            and 'PATIENT' not in jwt_response['groupIDs']:
        staff_response = get_department_of_staff_member(
            jwt_response['hospital_id'].lower(),
            jwt_response['serums_id']
        )
        if staff_response:
            result['id'] = jwt_response['serums_id']
            result['department_id'] = staff_response['department_id']
        else:
            return None
    else:
        return None
    return result
