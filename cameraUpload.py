from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('cameraUpload',__name__)


@bp.route('/cameraUpload')#이미지 결과페이지
def cameraUpload():
    return render_template("cameraUpload.html")