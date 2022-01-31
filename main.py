from fastapi import FastAPI

# app = FastAPI(
#     title="Serums Datalake API"
# )

from components.connection.create_connection import setup_connection
from components.utils.class_search import get_class_by_name

connection = setup_connection('ustan')

res = get_class_by_name('ustan.serums_ids', connection['base'])
print(res)
