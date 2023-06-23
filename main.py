from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from router import scan

app = FastAPI()

app.include_router(scan.router)