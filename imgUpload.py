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
    ret=s3_put_object(s3,"sejong-capstone-s3-bucket",'static/assets/img/' + secure_filename(img.filename),img.filename)
    print(ret)
    if ret: 
        return "<script type='text/javascript'>alert('업로드 성공.');document.location.href='/user_main';</script>"
    else:
        return render_template("user_main.html")

    

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

