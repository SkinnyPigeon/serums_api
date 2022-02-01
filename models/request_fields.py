from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import json


class HelloResponse(BaseModel):
    __root__: dict = {"hello": "Welcome to the API. The server is on"}


class StaffMemberDepartmentResponse(BaseModel):
    serums_id: int = 120
    staff_id: int = 120
    name: str = "Charlotte Watson"
    department_id: int = 4
    department_name: str = "MEDICAL_STAFF"


class FullDepartmentRequest(BaseModel):
    hospital_id: str = 'USTAN'


staff_details = json.loads('''
    [
        {
            "serums_id": 364,
            "staff_id": 6000,
            "name": "Isla MacDonald",
            "department_id": 1,
            "department_name": "Emergency"
        },
        {
            "serums_id": 391,
            "staff_id": 6001,
            "name": "Charles Stewart",
            "department_id": 1,
            "department_name": "Emergency"
        },
        {
            "serums_id": 390,
            "staff_id": 6002,
            "name": "Oliver Wilson",
            "department_id": 3,
            "department_name": "Consultant"
        }
    ]
''')


class FullDepartmentResponse(BaseModel):
    __root__: list[dict] = staff_details
