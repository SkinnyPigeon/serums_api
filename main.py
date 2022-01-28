from fastapi import FastAPI

# app = FastAPI(
#     title="Serums Datalake API"
# )

from components.blockchain.lineage import create_record

check = create_record(117, 'TESTING', ['ustan'])
print(check)
