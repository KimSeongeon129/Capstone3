from flask import Flask, Response, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import random
import cv2
import base64
import time

from werkzeug.utils import secure_filename
from model.detect_realtime import detect_realtime
from AI import device, model, half, stride

bp= Blueprint('cameraUpload',__name__)

outputFrame = None
cap = cv2.VideoCapture(0)

names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

dict_data=dict(code="")

@bp.route('/cameraUpload', methods=['GET','POST'])#이미지 결과페이지
def cameraUpload():
    if request.method=='GET':
        return render_template("cameraUpload.html")
    else:
        #post로  프론트의 실시간 데이터를 가져와서
        #db에 데이터 저장 후-> imgupload에 있는 내용 고치면 됨
        #다시 데이터를 보내든 프론트에서 보낼때 session에 데이터 저장시켜서 그걸 바로 쓰든 하면 될듯
        return render_template("camerUpload.html")

def camera():
    global cap, outputFrame
    c=0
    while True:
        ret, frame = cap.read()
        outputFrame = detect_realtime(model=model, img=frame, stride=stride, device=device, half=half, names=names, colors=colors)
        if outputFrame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        if not flag:
            continue
        c=c+1
        print(c)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        
@bp.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    
@bp.route('/realtimeUpload',methods=['POST'])
def realtimeUpload():
    global dict_data
    
    img=request.files['file']
    new_filename = str(time.time())
    img.save('static/assets/img/' + secure_filename(new_filename))
    my_img = 'static/assets/img/' + secure_filename(new_filename)
    cv2_my_img = cv2.imread(my_img)


    haveFault, detect_img=detect_realtime(model=model, img=cv2_my_img, stride=stride, device=device, half=half, names=names, colors=colors)
    (flag, encodedImage) = cv2.imencode(".jpg", detect_img)
    
    if haveFault is True:
        dict_data['code'] = base64.b64encode(encodedImage).decode('utf-8')
    else:
        dict_data['code'] = None
    
    return dict_data