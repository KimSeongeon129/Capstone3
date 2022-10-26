from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json
import boto3
import os
from werkzeug.utils import secure_filename


bp= Blueprint('imgUpload',__name__)


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
    return render_template("imgUpload_result.html")

@bp.route('/imgUpload')#이미지 결과페이지
def imgUpload():
    return render_template("imgUpload.html")


@bp.route('/upload',methods=['POST'])#이미지 form으로 가져오기
def upload():
    print("이미지 불러오기 전")
    img=request.files['image']#파일 가져오기
    img.save('static/assets/img/' + secure_filename(img.filename))

    my_img = 'static/assets/img/' + secure_filename(img.filename)
    terminal_command = f"python model/detect.py --weights model/yolov7.pt --conf 0.25 --img-size 640 --source {my_img}"
    os.system(terminal_command)
    
    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(img.filename),img.filename)#파일 올리기
    print(ret)
    url=s3_get_image_url(s3, img.filename)#url 저장
    #db에 url 저장하는 코드


    return url

    

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

def s3_get_image_url(s3, filename):
    """
    s3 : 연결된 s3 객체(boto3 client)
    filename : s3에 저장된 파일 명
    """
    location = s3.get_bucket_location(Bucket="sejong-capstone-s3-bucket")["LocationConstraint"]
    return "https://sejong-capstone-s3-bucket.s3.{location}.amazonaws.com/{filename}.jpg"