from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel
from typing import List

from services import yolo

class DetectionResult(BaseModel):
    name: str
    position: List[float]
    confidence: float

router = APIRouter(
    prefix='/scan',
)

@router.post('/')
async def detect_object(file: UploadFile) -> List[DetectionResult]:

    if not file:
        raise HTTPException(status_code=400, detail='missing parameters')

    # check if the file type is image
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=415, detail='unsupported file type')

    image = Image.open(file.file)
    model = await yolo.get_yolo_instance('detection')

    # the model can take multiple images at the same time, so the 
    # output is a list of predictions, to get the single out put, getting the first of array
    result = model(image)[0]

    image.close()
    file.file.close()

    # mappings of the class names to inter values
    names = result.names
    items: list = result.boxes.data.tolist()

    cleaned_data = list(map(lambda elm: map_names(elm, names), items))

    return JSONResponse(content=cleaned_data)

def map_names(elm, names) -> DetectionResult:
    organized_data = {
        'class_name': names[elm[5]],
        'position': elm[:4],
        'confidence': elm[4]
    }
    return organized_data