from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from services.yolo import get_available_models, get_yolo_instance, is_task_supported
from typing import List

router = APIRouter(prefix='/models')

@router.get('/')
def get_available_models():
    available_models: List[str] = get_available_models()

    return JSONResponse(content=available_models)

@router.get('/class_names/{model_name}')
async def get_class_names(model_name: str):
    
    # check if the model is available
    if not is_task_supported(model_name):
        raise HTTPException(status_code=404, detail='model not found')

    model = await get_yolo_instance(model_name)

    return JSONResponse(content=model.names)
    