from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import json


class HelloResponse(BaseModel):
    __root__: dict = {"hello": "Welcome to the API. The server is on"}
