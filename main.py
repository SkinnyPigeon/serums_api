from fastapi import FastAPI
from components.staff.departments import get_department_of_staff_member
# app = FastAPI(
#     title="Serums Datalake API"
# )

check = get_department_of_staff_member('ustan', 455)
print(check)