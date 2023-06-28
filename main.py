from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from router import detection
from router import classification

app = FastAPI()

app.include_router(detection.router)
app.include_router(classification.router)