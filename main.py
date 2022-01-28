from fastapi import FastAPI

# app = FastAPI(
#     title="Serums Datalake API"
# )
from tests.test_valid_staff_jwt import right_jwt
from components.blockchain.rules import validate_rules

res = validate_rules(right_jwt)
print(res)
