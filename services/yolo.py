
from ultralytics import YOLO

MODEL_TYPES = (
    'detection', 
    'segmentation', 
    'classification', 
    'pose'
)

models = {
    'detection': YOLO('../models/yolov8x.pt'),
    'segmentation': YOLO('../models/yolov8x-seg.pt'),
    'classification': YOLO('../models/yolov8x-cls.pt'),
    'pose': YOLO('../models/yolov8x-pose-p6.pt')
}

def is_task_supported(type: str) -> bool:
    return type in MODEL_TYPES


async def get_yolo_instance(type: str = 'detection') -> YOLO:
    if not is_task_supported(type):
        raise 'YOU FUCKING DONKEY'
    
    # returns the type and the complicity with  
    # respect to the mappings above
    return models[type]


def get_available_models():
    return models.keys()