from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('user_main',__name__)

@bp.route('/user_main')# 유저 페이지
def user_main():
    return render_template("user_main.html")

@bp.route('/statistics')#통계 페이지
def statistics():
    return 

@bp.route('/list')#내역 페이지
def list():
    return 

@bp.route('/cameraUpload')#실제 이미지 업로드 페이지
def cameraUpload():
    return 

@bp.route('/imgUpload')#이미지 업로드 페이지
def imgUpload():
    return 