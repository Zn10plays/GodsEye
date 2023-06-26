from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel
from typing import List

from services import yolo

class ObjectData(BaseModel):
    name: str
    position: List[float]
    confidence: float

router = APIRouter(
    prefix='/scan',
)

@router.post('/')
async def scan_image(file: UploadFile, task: str | None = None, complexity: int | None = None) -> List[ObjectData]:

    if not task:
        task = 'detection'
    if not complexity:
        complexity = 0

    if not file:
        raise HTTPException(status_code=400, detail='missing parameters')

    # check if the file type is image
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=415, detail='unsupported file type')

    if not yolo.is_task_supported(type=task):
        raise HTTPException(status_code=400, detail=f'you fucking loser I can\'t do this: must be ${yolo.MODEL_TYPES.join(", ")}')

    image = Image.open(file.file)
    model = await yolo.get_yolo_instance(type=task)

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

def map_names(elm, names) -> ObjectData:
    organized_data = {
        'name': names[elm[5]],
        'position': elm[:4],
        'confidence': elm[4]
    }
    return organized_data