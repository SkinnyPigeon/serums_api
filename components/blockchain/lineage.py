import os
import jwt
from datetime import datetime
import requests
from hashlib import sha256

BCPASSWORD = os.getenv('BCPASSWORD')
BC_PATH = os.getenv('BC_PATH')
URL = BC_PATH + '/v1/api/proof/'


def create_record(serums_id: int, rule_id: str, hospital_ids: list):
    """
    Creates a record on the lineage blockchain that will \
    track the creation of a Smart Patient Health Record
        Parameters:
            serums_id (int): The Serums ID of the patient whose Smart \
                             Patient Health Record is being created
            rule_id (str): The rule ID from the access blockchain \
                           that is being executed
            hospital_ids (list): The list of hospitals from which the \
                                 Smart Patient Health Record is being \
                                 created from
        Returns:
            proof_id (str): The proof ID of the newly created record \
                            on the lineage blockchain that will be \
                            used to continue to update the record
    """
    token = jwt.encode({}, BCPASSWORD, algorithm='HS256')
    hospital_ids = [id.upper() for id in hospital_ids]
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    header = {"Authorization": f"Bearer {token}"}
    body = {
        'serumsId': serums_id,
        'ruleId': rule_id,
        'hospitalIds': hospital_ids,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    response = requests.post(URL, json=body, headers=header)
    if response.status_code == 200:
        proof_id = response.json()['proofId']
        return proof_id
    else:
        return False


def hash_columns(columns):
    """
    Converts the columns that were selected into a hash that can be used \
    to verify that a rule was executed correctly
        Parameters:
            columns (list): The list of columns that was selected \
                            from the source system
        Returns:
            column_hash (str): A hash derived from the stringified ordered list
    """
    sorted_columns = sorted(columns)
    sorted_string = "".join(sorted_columns)
    column_hash = sha256(sorted_string.encode()).hexdigest()
    return column_hash
