from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import BaseModel
from typing import List

from services import yolo

class ClassificationResults(BaseModel):
    class_name: str
    confidence: float

router = APIRouter(
    prefix='/classify',
)

@router.post('/')
async def classify_image(file: UploadFile) -> List[ClassificationResults]:

    if not file:
        raise HTTPException(status_code=400, detail='missing parameters')

    # check if the file type is image
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=415, detail='unsupported file type')

    image = Image.open(file.file)
    model = await yolo.get_yolo_instance('classification')

    # the model can take multiple images at the same time, so the 
    # output is a list of predictions, to get the single out put, getting the first of array
    result = model(image)[0]

    image.close()
    file.file.close()

    # mappings of the class names to inter values
    names = result.names
    all_probabilities, top_5_probs = result.probs.data.tolist(), result.probs.top5

    cleaned_data = list(map(lambda elm: clean_data(elm, all_probabilities, names), top_5_probs))

    return JSONResponse(content=cleaned_data)

def clean_data(result, all_results, class_names) -> ClassificationResults:
    return {
        'class_name': class_names[result],
        'confidence': all_results[result]
    }