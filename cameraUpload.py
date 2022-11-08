from flask import Flask, Response, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import random
import cv2

from model.detect_realtime import detect_realtime
from ai import device, model, half, stride

bp= Blueprint('cameraUpload',__name__)

outputFrame = None
cap = cv2.VideoCapture(0)

names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

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

    while True:
        ret, frame = cap.read()
		
        outputFrame = detect_realtime(model=model, img=frame, stride=stride, device=device, half=half, names=names, colors=colors)
        if outputFrame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        if not flag:
            continue
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        
@bp.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    