import os

my_img = '경로'
terminal_command = f"python3 model/detect.py --weights model/yolov7.pt --conf 0.25 --img-size 640 --source {my_img}"
os.system(terminal_command)