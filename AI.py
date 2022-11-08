from model.models.experimental import attempt_load
from model.utils.general import set_logging
from model.utils.torch_utils import select_device

set_logging()
device = select_device()
half = device.type != 'cpu'  # half precision only supported on CUDA
model = attempt_load('model/yolov7.pt', map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride