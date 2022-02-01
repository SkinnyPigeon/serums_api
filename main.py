from fastapi import FastAPI, Depends, Header
from auth.auth_handler import JWTBearer
from models.request_fields import HelloResponse, \
                                  StaffMemberDepartmentResponse
from components.staff.departments import get_departments
from components.staff.verify_staff_member import get_department_of_staff_member
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


@app.get("/staff_tables/departments", tags=['STAFF'])
def request_get_departments():
    # jwt = request
    pass


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
