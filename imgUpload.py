from flask import Flask, render_template,g,session
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import add_image,add_result,find_inspection_number
from AI import check_type
import requests
import json
import boto3
import os,random
import sys
from werkzeug.utils import secure_filename
import time
import codecs

local_path = codecs.decode(os.getcwd().replace('\\','\\\\'), 'unicode_escape')
sys.path.append(local_path + '\\model')

from model.detect import detect
from model.models.experimental import attempt_load
from model.utils.general import set_logging
from model.utils.torch_utils import select_device, TracedModel


bp= Blueprint('imgUpload',__name__)
dict_data=dict(img_url="",inspection_number=123,part_id="123",date="",part_name="양품",part_category="이상없음",part_judge="모코코",user_id="nickname")

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
    start=time.time()

    img=request.files['image']#파일 가져오기
    img.save('static/assets/img/' + secure_filename(img.filename))
    my_img = 'static/assets/img/' + secure_filename(img.filename)

    # 검사 모델 로드 ( 서비스 시 함수 밖으로 뺄 예정 )
    set_logging()
    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA

    model = attempt_load('model/yolov7.pt', map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    model = TracedModel(model, device, 640)
    
    
    # 검사 모델 실행
    dic_list=detect(model=model, source=my_img, stride=stride, device=device, half=half)
    print(dic_list)

    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(img.filename),img.filename)#파일 올리기
    object_name=img.filename
    dict_data['img_url'] = f'https://"sejong-capstone-s3-bucket".s3.ap-northeast-2.amazonaws.com/{object_name}'#url 저장
    dict_data['part_id']=str(random.randint(0,9223372036854775807))#램덤 숫자 일련번호 
    #아이디 세션에 있는거 넣기
    dict_data['user_id']=session['username']
    if not dic_list:
        dict_data['part_judge']='양품'
    else:
        dic1=dic_list[0]
        dict_data['part_category']=dic1['label']
        dict_data['part_name']=check_type(dict_data['part_category'])
        dict_data['part_judge']='불량품'
    
    dict_data['date']=str(time.strftime('%y-%m-%d %H:%M:%S'))
    print(dict_data)
    end=time.time()
    print(end-start)
    #db에 url 저장하는 코드
    add_result(g.db, dict_data['part_id'], dict_data['part_name'], dict_data['part_category'], dict_data['part_judge'], dict_data['user_id'])
    dict_data['inspection_number']=find_inspection_number(g.db, dict_data['part_id'])
    add_image(g.db, int(dict_data['inspection_number']), '1','2', '3', '4', object_name)#url가져올때 f'https://"sejong-capstone-s3-bucket".s3.ap-northeast-2.amazonaws.com/이거 붙여야함

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