from flask import Flask, render_template,session
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('user_main',__name__)

@bp.route('/user_main')# 유저 페이지
def user_main():
    if 'username' in session:
        return render_template("user_main.html")
    else :
        return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 
