import subprocess
import os
import asyncio

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

async def download_models():
    MODEL_URLS = [
        'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt',
        'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt',
        'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt',
        'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt',
        'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt'
    ]

    DOWNLOAD_LOCATION = os.path.abspath('./models')

    for i in range(len(MODEL_URLS)):
        runcmd(f'python -m wget -o {DOWNLOAD_LOCATION}/{MODEL_URLS[i].split("/")[-1]} {MODEL_URLS[i]}', verbose=True)


asyncio.run(download_models())