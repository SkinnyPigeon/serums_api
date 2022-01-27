import jwt
import os

JWT_KEY = os.getenv('JWT_KEY')


def validate_jwt(encoded_jwt: str):
    """
    Validates and decodes the JWT that is passed between the various \
    modules. The token is generated by the authentication \
    module, but the data lake validates this itself to \
    minimise the number of calls between the components

        Parameters:
            encoded_jwt (str): The JWT that is to be validated \
                               and decoded

        Returns:
            results (dict): Contains either the decoded JWT details \
                            or an error message
    """
    token = encoded_jwt.replace('Bearer ', '')
    try:
        decoded_jwt = jwt.decode(
            token,
            JWT_KEY,
            audience="https://shcs.serums.cs.st-andrews.ac.uk/",
            algorithms='HS256'
        )
        if decoded_jwt:
            return {
                'serums_id': decoded_jwt['userID'],
                'hospital_id': decoded_jwt['orgID'],
                'groupIDs': decoded_jwt['groupIDs'],
                'status_code': 200
            }
    except jwt.exceptions.InvalidSignatureError as e:
        return {'status_code': 404, 'message': str(e)}
    except jwt.exceptions.DecodeError as d:
        return {'status_code': 422, 'message': str(d)}
