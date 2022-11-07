from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('cameraUpload',__name__)


@bp.route('/cameraUpload', methods=['GET','POST'])#이미지 결과페이지
def cameraUpload():
    if request.method=='GET':
        return render_template("cameraUpload.html")
    else:
        #post로  프론트의 실시간 데이터를 가져와서
        #db에 데이터 저장 후-> imgupload에 있는 내용 고치면 됨
        #다시 데이터를 보내든 프론트에서 보낼때 session에 데이터 저장시켜서 그걸 바로 쓰든 하면 될듯
        return render_template("camerUpload.html")