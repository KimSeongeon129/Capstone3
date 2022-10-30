from flask import Flask, render_template,g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import add_image,add_result
import requests
import json
import boto3
import os
from werkzeug.utils import secure_filename
import time

from model.detect import detect
from model.models.experimental import attempt_load
from model.utils.general import set_logging
from model.utils.torch_utils import select_device, TracedModel


bp= Blueprint('imgUpload',__name__)
dict_data=dict(img_url="",inspection_number="21231232",part_id="123",date="2022-10-30",part_name="모코코",part_category="모코코",part_judge="모코코",user_id="nickname")

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


@bp.route('/imgUpload_result')#이미지 결과페이지
def imgUpload_result():
    #데이터 보내기

    return render_template("imgUpload_result.html",data=dict_data)

@bp.route('/imgUpload')#이미지 결과페이지
def imgUpload():
    return render_template("imgUpload.html")


@bp.route('/upload',methods=['POST'])#이미지 form으로 가져오기
def upload():
    global dict_data
    st1=time.time()
    img=request.files['image']#파일 가져오기
    st2=time.time()
    img.save('static/assets/img/' + secure_filename(img.filename))
    st3=time.time()
    my_img = 'static/assets/img/' + secure_filename(img.filename)

    # 검사 모델 로드
    set_logging()
    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA

    model = attempt_load('model/yolov7.pt', map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    model = TracedModel(model, device, 640)
    
    # 검사 모델 실행
    print(detect(model=model, source=my_img, stride=stride, device=device, half=half))
    print('실행')

    st4=time.time()
    
    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(img.filename),img.filename)#파일 올리기
    st5=time.time()
    print(ret,f"{st4 - st3:.5f} sec",st5-st4)
    object_name=img.filename
    dict_data['img_url'] = f'https://"sejong-capstone-s3-bucket".s3.ap-northeast-2.amazonaws.com/{object_name}'#url 저장
    #db에 url 저장하는 코드
    #add_result(g.db, 'part_id', 'date', 'part_name', 'part_category', 'part_judge', 'user_id', 'inspection_number')
    #add_image(g.db, 'inspection_number', 'img_id', 'bbox_x1', 'bbox_x2', 'bbox_y1', 'bbox_y2', 'image')

    return dict_data['img_url']

    

#이미지를 s3로 올리기
#올린 이미지 url 가져오기
#이미지 url db에 저장
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
