from typing import Annotated
from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix='/scan',
    
)

@router.post('/')
def scan_image(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    return {'filename': file.filename}