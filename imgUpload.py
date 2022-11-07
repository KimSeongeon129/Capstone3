from flask import Flask, render_template,g,session
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import add_image,add_result,find_inspection_number
from AI import check_type
import requests
import json
import boto3
import os,random
import sys
import cv2
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
dict_data=dict(img_url="",inspection_number=123,part_id="123",date="",part_name="양품",part_category="이상없음",part_judge="모코코",user_id="nickname",x1=0,x2=0,y1=0,y2=0)



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

    return render_template("imgUpload_result.html")

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
    cv2_my_img = cv2.imread(my_img)

     # 검사 모델 로드 ( 서비스 시 함수 밖으로 뺄 예정 )
    set_logging()
    device = select_device()
    half = device.type != 'cpu'  # half precision only supported on CUDA
    model = attempt_load('model/yolov7.pt', map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride

    # 검사 모델 실행
    dic_list=detect(model=model, img=cv2_my_img, stride=stride, device=device, half=half)
    print(dic_list)

    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(img.filename),'origin/'+img.filename)#원본 파일 올리기
    object_name=img.filename
    dict_data['img_url'] = f'https://sejong-capstone-s3-bucket.s3.ap-northeast-2.amazonaws.com/origin/{object_name}'#url 저장
    dict_data['part_id']=str(random.randint(0,9223372036854775807))#램덤 숫자 일련번호 
    #아이디 세션에 있는거 넣기
    dict_data['user_id']=session['username']
    if not dic_list:
        dict_data['part_judge']='양품'
    else:
        # 불량품 세부내용 저장
        dic1=dic_list[0]
        dict_data['part_category']=dic1['label']
        dict_data['part_name']=check_type(dict_data['part_category'])
        dict_data['part_judge']='불량품'
        dict_data['x1']=int(dic1['c1'][0])
        dict_data['x2']=int(dic1['c2'][0])
        dict_data['y1']=int(dic1['c1'][1])
        dict_data['y2']=int(dic1['c2'][1])
        
        # 불량품 bbox 그리기
        img_r = cv2.imread(my_img)
        tl = round(0.002 * (img_r.shape[0] + img_r.shape[1]) / 2) + 1  # line/font thickness
        color = [random.randint(0, 255) for _ in range(3)]
        
        c1 = dic1['c1']
        c2 = dic1['c2']
        
        cv2.rectangle(img_r, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)  # font thickness
        conf = dic1['conf']
        label = dic1['label'] + f'{conf:.2f}'
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img_r, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img_r, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        cv2.imwrite('static/assets/img/result/'+ secure_filename(img.filename),img_r)
        ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/result/' + secure_filename(img.filename),'result/'+img.filename)#결과 파일 올리기
        dict_data['img_url'] = f'https://sejong-capstone-s3-bucket.s3.ap-northeast-2.amazonaws.com/result/{object_name}'#url 저장
    
    dict_data['date']=str(time.strftime('%y-%m-%d %H:%M:%S'))
    #db에 url 저장하는 코드
    add_result(g.db, dict_data['part_id'], dict_data['part_name'], dict_data['part_category'], dict_data['part_judge'], dict_data['user_id'])
    dict_data['inspection_number']=find_inspection_number(g.db, dict_data['part_id'])
    add_image(g.db, int(dict_data['inspection_number']), dict_data['x1'],dict_data['x2'],dict_data['y1'], dict_data['y2'], object_name)
    #url가져올때 f'https://"sejong-capstone-s3-bucket".s3.ap-northeast-2.amazonaws.com/이거 붙여야함 origin이면 원본 result면 bbox있는 거
    end=time.time()
    print(end-start)
    return dict_data

    

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