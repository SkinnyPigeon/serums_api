from components.jwt.validate import validate_jwt
from components.staff.departments import get_department_of_staff_member


def check_staff_member(jwt: str):
    """
    Validates the JWT and checks that the member of staff belongs \
    to the stated hospital

        Parameters:
            jwt (str): The JWT to be checked and validated
        Returns:

    """
    jwt_response = validate_jwt(jwt)
    if jwt_response['status_code'] == 200 \
            and 'PATIENT' not in jwt_response['user_type']:
        staff_response = get_department_of_staff_member(
            jwt_response['hospital_id'],
            jwt_response['serums_id']
        )
        if staff_response:
            return True
        else:
            return False
    else:
        return False
