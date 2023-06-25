
from ultralytics import YOLO

MODEL_TYPES = (
    'detection', 
    'segmentation', 
    'classification', 
    'tracking', 
    'pose'
)

MODEL_COMPLEXITY = (
    'nano',
    'small',
    'medium',
    'large',
    'xl'
)

models = {
    'detection': {
        'nano': YOLO('../models/yolov8n.pt'),
        'small': YOLO('../models/yolov8s.pt'),
        'medium': YOLO('../models/yolov8m.pt'),
        'large': YOLO('../models/yolov8l.pt'),
        'xl': YOLO('../models/yolov8x.pt')
    }
}

def is_task_supported(type: str):
    return type in MODEL_TYPES

def is_model_complexity_supported(complexity: int):
    return complexity < len(models) or complexity >= 0

async def get_yolo_instance(type: str = 'detection', complexity: int = 0):
    if not is_task_supported(type):
        raise 'YOU FUCKING DONKEY'
    
    if not is_model_complexity_supported(complexity):
        raise 'unsupported complexity'
    
    print(type, complexity)
    
    # returns the type and the complicity with  
    # respect to the mappings above
    return models[type][MODEL_COMPLEXITY[complexity]]
