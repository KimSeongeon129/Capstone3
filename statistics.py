from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('statistics',__name__)

@bp.route('/statistics')#이미지 결과페이지
def imgUpload_result():
    return render_template("statistics.html")
