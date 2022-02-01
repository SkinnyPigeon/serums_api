from fastapi import FastAPI, Depends, Header, Response, status
from fastapi.responses import JSONResponse
from auth.auth_handler import JWTBearer
from models.request_fields import HelloResponse, \
    FullDepartmentRequest, \
    FullDepartmentResponse, SPHRResponse, \
    StaffMemberDepartmentResponse, \
    SingleHospitalTagsRequest, \
    SingleHospitalTagsResponse, \
    MultiHospitalTagsRequest, \
    MultiHospitalTagsResponse, \
    NotAuthenticated, \
    HandleError500, \
    UnauthorizedResponse, \
    AddUserRequest, \
    AddUserSuccessResponse, \
    RemoveUserRequest, \
    RemoveUserSuccessResponse, \
    MLSuccessResponse, \
    SearchRequest, \
    SearchResponse, \
    SPHRRequest, \
    SPHRRequestEncrypted, \
    SPHRResponseEncrypted, \
    DVResponse
from components.staff.departments import get_departments
from components.staff.verify_staff_member import get_department_of_staff_member
from components.tags.tags import get_tags
from components.users.add_or_remove_users import add_user, remove_user
from components.ml.data_for_ml import get_patient_data_for_ml
from components.search.search import search_for_serums_id
from components.sphr.get_source_data import get_patient_data, parse_sphr
from components.encryption.encryption import encrypt_data_with_new_key, \
                                             encrypt_key
from components.data_vaults.data_vault import create_data_vault
from components.data_vaults.satellites import process_satellites
from components.data_vaults.hub_post_processing import hub_equalizer
from components.data_vaults.link_post_processing import add_id_values
from components.jwt.validate import validate_jwt

responses = {
    401: {"model": UnauthorizedResponse},
    403: {"model": NotAuthenticated},
    500: {"model": HandleError500}
}

description = """
This is an updated version of the Serums Datalake API. \
While the functionality remains the same, every single \
function has been evaluated and rewritten where needed, \
hopefully leading to a smoother experience when using \
as well as an easier time maintaining.

A big part of the change comes from the far more robust \
testing suite which now covers everything so finding issues \
in the future should be a much simpler task.

## Usage

You will require to have a few things in place to use the API. \
First, you must be able to log into the [Flexpass system]\
(https://flexpass.serums.cs.st-andrews.ac.uk/web_app/login_username.html).\

Additionally, if you are testing staff members you will need to have \
rules stored on the blockchain for that member of staff. For instance, \
In the testing suite, you will see that there are various rules in \
place for the patient with the id of 117 and the medical professional \
with an id of 120 within USTAN.
"""

contact = {
    "name": "Euan Blackledge",
    "email": "euan.blackledge@soprasteria.com",
    "url": "https://github.com/SkinnyPigeon"
}

tags_metadata = [
    {
        "name": "HELLO",
        "description": "A place to check the server is on"
    },
    {
        "name": "STAFF",
        "description": "Access various elements of the staff databases"
    },
    {
        "name": "TAGS",
        "description": "Access various elements of the tags tables"
    },
    {
        "name": "USERS",
        "description": "Add or remove users from the Serums network"
    },
    {
        "name": "MACHINE LEARNING",
        "description": "Return the patient data for the machine learning "
        "algorithm"
    },
    {
        "name": "SEARCH",
        "description": "Search for a patient’s SERUMS ID"
    },
    {
        "name": "SMART PATIENT HEALTH RECORD",
        "description": "Retrieve the Smart Patient Health Record"
    },
    {
        "name": "DATA VAULT",
        "description": "Returns the patient data in data vault format"
    }
]

app = FastAPI(
    title="Serums Datalake API",
    description=description,
    contact=contact,
    openapi_tags=tags_metadata
)


@app.get("/hello/hello", response_model=HelloResponse, tags=['HELLO'])
def say_hello():
    return {"hello": "Welcome to the API. The server is on"}


@app.post("/staff_tables/departments",
          tags=['STAFF'],
          response_model=FullDepartmentResponse)
def request_get_departments(body: FullDepartmentRequest):
    departments = get_departments(body.hospital_id)
    return departments


@app.get("/staff_tables/get_department_of_staff_member",
         tags=['STAFF'],
         response_model=StaffMemberDepartmentResponse,
         dependencies=[Depends(JWTBearer())])
def request_get_dpt_of_staff_member(Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    response = get_department_of_staff_member(
        jwt_response['hospital_id'],
        jwt_response['serums_id']
    )
    return response


@app.post('/tags_tables/tags',
          tags=['TAGS'],
          response_model=SingleHospitalTagsResponse)
def request_get_single_hospital_tags(body: SingleHospitalTagsRequest):
    tags = get_tags(body.hospital_id)
    return tags


@app.post('/tags_tables/all_tags',
          tags=['TAGS'],
          response_model=MultiHospitalTagsResponse)
def request_get_multi_hospital_tags(body: MultiHospitalTagsRequest):
    tags = {}
    for hospital_id in body.hospital_ids:
        tags[hospital_id] = get_tags(hospital_id)
    return tags


@app.post('/users/add_user',
          tags=['USERS'],
          response_model=AddUserSuccessResponse,
          responses=responses,
          dependencies=[Depends(JWTBearer())])
def request_add_user(body: AddUserRequest,
                     response: Response,
                     Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'SERUMS_ADMIN' in jwt_response['user_type'] \
            or 'HOSPITAL_ADMIN' in jwt_response['user_type']:
        result = add_user(body.serums_id,
                          body.patient_id,
                          body.hospital_id)
        if result[1] == 200:
            return result[0]
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result[0]
    else:
        return JSONResponse(status_code=401, content={
            "message": "Only admins can add users"
        })


@app.post('/users/remove_user',
          tags=['USERS'],
          response_model=RemoveUserSuccessResponse,
          responses=responses,
          dependencies=[Depends(JWTBearer())])
def request_remove_user(body: RemoveUserRequest,
                        response: Response,
                        Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'SERUMS_ADMIN' in jwt_response['user_type'] \
            or 'HOSPITAL_ADMIN' in jwt_response['user_type']:
        results = remove_user(body.serums_id,
                              body.hospital_ids)
        if results[1] == 200:
            return results[0]
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return results[0]
    else:
        return JSONResponse(status_code=401, content={
            "message": "Only admins can remove users"
        })


@app.get('/machine_learning/analytics',
         tags=['MACHINE LEARNING'],
         response_model=MLSuccessResponse,
         responses=responses,
         dependencies=[Depends(JWTBearer())])
def get_ml_data(response: Response, Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'PATIENT' in jwt_response['user_type']:
        results = get_patient_data_for_ml(jwt_response['serums_id'])
        if results[1] == 200:
            return results[0]
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return results[0]
    else:
        return JSONResponse(status_code=401, content={
            "message": "Only patients can access their own ML data"
        })


@app.post('/search/serums_id',
          tags=['SEARCH'],
          response_model=SearchResponse,
          responses=responses,
          dependencies=[Depends(JWTBearer())])
def get_search_for_serums_id(body: SearchRequest,
                             response: Response,
                             Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'MEDICAL_STAFF' in jwt_response['user_type'] or \
            'HOSPITAL_ADMIN' in jwt_response['user_type'] or \
            'SERUMS_ADMIN' in jwt_response['user_type']:
        results = search_for_serums_id(dict(body))
        if results[1] == 200:
            return results[0]
        else:
            return JSONResponse(status_code=500, content={
                "message": "Unable to find a patient with those details"
            })
    else:
        return JSONResponse(status_code=401, content={
            "message": "Must be either a medical staff or "
                       "admin to search for users"
        })


@app.post('/smart_patient_health_record/get_sphr',
          response_model=SPHRResponse,
          responses=responses,
          tags=['SMART PATIENT HEALTH RECORD'],
          dependencies=[Depends(JWTBearer())])
def get_the_unencrypted_sphr(body: SPHRRequest,
                             Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'PATIENT' in jwt_response['user_type'] and \
            body.serums_id != jwt_response['serums_id']:
        return JSONResponse(status_code=401, content={
            "message": "Patients can only access their own records, "
                       "please check the serums id in request body"
        })
    patient_data, proof_id = get_patient_data(
        jwt_response['serums_id'],
        body.hospital_ids,
        body.tags,
        Authorization
    )
    if patient_data:
        parsed_data = parse_sphr(patient_data)
        return parsed_data
    return JSONResponse(status_code=500, content={
            "message": "Unable to create SPHR"
        })


@app.post('/smart_patient_health_record/encrypted',
          response_model=SPHRResponseEncrypted,
          responses=responses,
          tags=['SMART PATIENT HEALTH RECORD'],
          dependencies=[Depends(JWTBearer())])
def get_the_encrypted_sphr(body: SPHRRequestEncrypted,
                           Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'PATIENT' in jwt_response['user_type'] and \
            body.serums_id != jwt_response['serums_id']:
        return JSONResponse(status_code=401, content={
            "message": "Patients can only access their own records, "
                       "please check the serums id in request body"
        })
    patient_data, proof_id = get_patient_data(
        jwt_response['serums_id'],
        body.hospital_ids,
        body.tags,
        Authorization
    )
    if patient_data:
        parsed_data = parse_sphr(patient_data)
        encrypted_data, encryption_key, public_key = \
            encrypt_data_with_new_key(parsed_data, body.public_key)
        encrypted_key = encrypt_key(encryption_key, public_key)
        return {"data": encrypted_data, "key": encrypted_key}
    return JSONResponse(status_code=500, content={
            "message": "Unable to create SPHR"
        })


@app.post('/data_vault/data_vault',
          response_model=DVResponse,
          responses=responses,
          tags=['DATA VAULT'],
          dependencies=[Depends(JWTBearer())])
def get_the_unencrypted_data_vault(body: SPHRRequest,
                                   Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'PATIENT' in jwt_response['user_type'] and \
            body.serums_id != jwt_response['serums_id']:
        return JSONResponse(status_code=401, content={
            "message": "Patients can only access their own records, "
                       "please check the serums id in request body"
        })
    patient_data, proof_id = get_patient_data(
        jwt_response['serums_id'],
        body.hospital_ids,
        body.tags,
        Authorization
    )
    if patient_data:
        satellites = process_satellites(patient_data)
        data_vault = create_data_vault(satellites)
        add_id_values(data_vault['links'])
        hub_equalizer(data_vault['hubs'])
        return data_vault
    return JSONResponse(status_code=500, content={
            "message": "Unable to create SPHR"
        })


@app.post('/data_vault/encrypted',
          response_model=SPHRResponseEncrypted,
          responses=responses,
          tags=['DATA VAULT'],
          dependencies=[Depends(JWTBearer())])
def get_the_encrypted_data_vault(body: SPHRRequestEncrypted,
                                 Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        return JSONResponse(status_code=403, content={
            "message": "Not authenticated"
        })
    if 'PATIENT' in jwt_response['user_type'] and \
            body.serums_id != jwt_response['serums_id']:
        return JSONResponse(status_code=401, content={
            "message": "Patients can only access their own records, "
                       "please check the serums id in request body"
        })
    patient_data, proof_id = get_patient_data(
        jwt_response['serums_id'],
        body.hospital_ids,
        body.tags,
        Authorization
    )
    if patient_data:
        satellites = process_satellites(patient_data)
        data_vault = create_data_vault(satellites)
        add_id_values(data_vault['links'])
        hub_equalizer(data_vault['hubs'])
        encrypted_data, encryption_key, public_key = \
            encrypt_data_with_new_key(data_vault, body.public_key)
        encrypted_key = encrypt_key(encryption_key, public_key)
        return {"data": encrypted_data, "key": encrypted_key}
    return JSONResponse(status_code=500, content={
            "message": "Unable to create SPHR"
        })
