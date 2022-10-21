from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import find_id_user,admin_login
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
    
        redirect("/admin_main")
        

<<<<<<< HEAD
        find_adminid=find_id_admin(g.db,admin_id)    #db에서 관리자 아이디 가져오기
=======
        #db에서 아이디와 비밀번호로 정보 가져오기
        print(admin_id,admin_password)
        find_id_pw=admin_login(g.db, admin_id,admin_password)
        print(find_id_pw)
>>>>>>> a1838936a5be258a679e086c8febdc392ae02378
    
        if (find_adminid) : #정보가 존재하면
            if(admin_login(g.db, admin_id, admin_password)) : #맞으면 true 반환
                return render_template('admin_main.html')   #관리자 메인 페이지 이동


        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디나 비밀번호가 틀립니다.');document.location.href='/admin_login';</script>"