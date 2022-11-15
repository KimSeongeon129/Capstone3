from flask import Flask, Response, render_template, g, session
from flask import jsonify,url_for,redirect,request,Blueprint
import random
import cv2
import base64
import time
import boto3
import os

from db1011 import add_image,add_result,find_inspection_number
from werkzeug.utils import secure_filename
from model.detect_realtime import detect_realtime
from AI import device, model, half, stride
from parts import check_type

bp= Blueprint('cameraUpload',__name__)

outputFrame = None
cap = cv2.VideoCapture(0)

names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

dict_data=dict(img_url="",inspection_number=123,part_id="123",date="",part_name="양품",part_category="이상없음",part_judge="모코코",user_id="nickname",x1=0,x2=0,y1=0,y2=0,defective_rate=0)

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

s3 = s3_connection()

@bp.route('/cameraUpload')#이미지 결과페이지
def cameraUpload():
    if 'username' in session:
        return render_template("cameraUpload.html")
    else :
        return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 
    
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
    new_filename = str(time.time()).replace('.','_')
    img.save('static/assets/img/' + secure_filename(new_filename))
    my_img = 'static/assets/img/' + secure_filename(new_filename)
    cv2_my_img = cv2.imread(my_img)
    cv2.imwrite(f'static/assets/img/{new_filename}.jpg', cv2_my_img)
    os.remove(f'static/assets/img/{new_filename}')


    haveFault, detect_img=detect_realtime(model=model, img=cv2_my_img, stride=stride, device=device, half=half, names=names, colors=colors)
    detect_img, detect_list =detect_realtime(model=model, img=cv2_my_img, stride=stride, device=device, half=half, names=names, colors=colors)
    (flag, encodedImage) = cv2.imencode(".jpg", detect_img)
    
    if haveFault is True:
        dict_data['code'] = base64.b64encode(encodedImage).decode('utf-8')
    
    dict_data['code'] = base64.b64encode(encodedImage).decode('utf-8')
    
    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(new_filename) + '.jpg','origin/'+new_filename + '.jpg')#원본 파일 올리기
    object_name=new_filename+'.jpg'
    dict_data['img_url'] = f'https://sejong-capstone-s3-bucket.s3.ap-northeast-2.amazonaws.com/origin/{object_name}'#url 저장
    dict_data['part_id']=str(random.randint(0,9223372036854775807))#램덤 숫자 일련번호 
    #아이디 세션에 있는거 넣기
    dict_data['user_id']=session['username']
    
    if len(detect_list) == 0:
        dict_data['part_judge']='양품'
    else:
        dict_data['code'] = None
        dic1=detect_list[0]
        conf = dic1['conf']
        conf= f'{conf:.4}'
        dict_data['defective_rate']=float(conf)*100
        dict_data['part_category']=dic1['label']
        dict_data['part_name']=check_type(dict_data['part_category'])
        dict_data['part_judge']='불량품'
        dict_data['x1']=int(dic1['c1'][0])
        dict_data['x2']=int(dic1['c2'][0])
        dict_data['y1']=int(dic1['c1'][1])
        dict_data['y2']=int(dic1['c2'][1])
        
        cv2.imwrite('static/assets/img/result/'+ secure_filename(new_filename) + '.jpg', detect_img)
        ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/result/' + secure_filename(new_filename) + '.jpg','result/'+new_filename+ '.jpg')#결과 파일 올리기
        dict_data['img_url'] = f'https://sejong-capstone-s3-bucket.s3.ap-northeast-2.amazonaws.com/result/{object_name}'#url 저장
    
    dict_data['date']=str(time.strftime('%y-%m-%d %H:%M:%S'))
    #db에 url 저장하는 코드
    add_result(g.db, dict_data['part_id'], dict_data['part_name'], dict_data['part_category'], dict_data['part_judge'], dict_data['user_id'], dict_data['defective_rate'])
    dict_data['inspection_number']=find_inspection_number(g.db, dict_data['part_id'])
    add_image(g.db, int(dict_data['inspection_number']), dict_data['x1'],dict_data['x2'],dict_data['y1'], dict_data['y2'], object_name)
    
    return dict_data

def s3_put_object(s3, bucket, filepath, access_key):

    try:
        s3.upload_file(
            Filename=filepath,
            Bucket=bucket,
            Key=access_key,
            ExtraArgs={"ContentType": "image/jpg", "ACL": "public-read"},
        )
    except Exception as e:
        print(e)
        return False
    return True