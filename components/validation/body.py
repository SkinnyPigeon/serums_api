from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend


def validate_body(body: dict, encrypted: bool = False):
    """
    Used to validate the request body. This checks for the fields \
    as well as the types to check that the body is correctly formatted.

        Parameters:
            body (dict): The request body that is to be validated
            encrypted (bool): Whether the request is for encrypted data
        Returns:
            errors (list): A list of errors that have been found
    """
    expected_fields = {
        'serums_id': int,
        'tags': list,
        'hospital_ids': list
    }

    errors = []

    for field in expected_fields:
        if field not in body:
            errors.append(f"Missing required field: {field.upper()}")
        if field in body and type(body[field]) != expected_fields[field]:
            errors.append(
                f"Incorrect data type for {field.upper()}. "
                f"Expected {str(expected_fields[field])}. "
                f"Received {str(type(body[field]))}")
    if encrypted:
        if 'public_key' not in body:
            errors.append(f"Missing required field: PUBLIC_KEY")
        if 'public_key' in body and type(body['public_key']) != str:
            errors.append(
                f"Incorrect data type for PUBLIC_KEY. "
                "Expected str. Received {str(type(body['public_key']))}")
        if 'public_key' in body:
            try:
                public_key = body['public_key'].encode()
                load_pem_public_key(
                    public_key, backend=default_backend()
                )
            except ValueError:
                errors.append(
                    f"Public key incorrectly formatted"
                )
    return errors
