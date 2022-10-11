from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import find_id_user,find_id_admin
import requests
import json

bp= Blueprint('admin_login',__name__)

#관리자 로그인
@bp.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method =='GET' :
        return render_template("/admin_login.html")
    else:
        admin_id=request.form['login_id']
        admin_password=request.form['login_pw']
        if not (admin_id and admin_password) : #둘중 하나라도 입력 안되면
            return "<script type='text/javascript'>alert('모두 입력해주세요.');document.location.href='/admin_login';</script>" 
    

        #db에서 아이디와 비밀번호로 정보 가져오기
        find_id_pw=admin_id
    
        if (find_id_pw) : #정보가 존재하면
            return render_template('admin_main.html')
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디나 비밀번호가 틀립니다.');document.location.href='/admin_login';</script>"