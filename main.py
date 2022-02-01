from fastapi import FastAPI, Depends, Header, Response, status
from auth.auth_handler import JWTBearer
from models.request_fields import HelloResponse, \
    FullDepartmentRequest, \
    FullDepartmentResponse, \
    StaffMemberDepartmentResponse, \
    SingleHospitalTagsRequest, \
    SingleHospitalTagsResponse, \
    MultiHospitalTagsRequest, \
    MultiHospitalTagsResponse, \
    NotAuthenticated, \
    HandleError500, \
    AddUserRequest, \
    AddUserUnauthorizedResponse, \
    AddUserSuccessResponse, \
    RemoveUserRequest, \
    RemoveUserResponse
from components.staff.departments import get_departments
from components.staff.verify_staff_member import get_department_of_staff_member
from components.tags.tags import get_tags
from components.users.add_or_remove_users import add_user, remove_user
from components.jwt.validate import validate_jwt


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
          responses={
              401: {
                  "model": AddUserUnauthorizedResponse
              },
              403: {
                  "model": NotAuthenticated
              },
              500: {
                  "model": HandleError500
              }
          },
          dependencies=[Depends(JWTBearer())])
def request_add_user(body: AddUserRequest,
                     response: Response,
                     Authorization: str = Header(None)):
    jwt_response = validate_jwt(Authorization)
    if jwt_response['status_code'] != 200:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Not authenticated"}
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
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Only admins can add users"}
