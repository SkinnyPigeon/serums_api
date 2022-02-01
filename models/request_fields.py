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
