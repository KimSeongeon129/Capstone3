from model.models.experimental import attempt_load
from model.utils.general import set_logging
from model.utils.torch_utils import select_device
import boto3

set_logging()
device = select_device()
half = device.type != 'cpu'  # half precision only supported on CUDA
model = attempt_load('model/yolov7.pt', map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2", # 자신이 설정한 bucket region
            aws_access_key_id='AKIASXRG4M6ELFHA4UOG',
            aws_secret_access_key='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',
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3
s3=s3_connection()