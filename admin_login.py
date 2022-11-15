from flask import Flask, render_template,session
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import find_id_user,get_admin_login,find_id_admin,add_admin
import requests
import json

bp= Blueprint('admin_login',__name__)
#관리자 로그인

@bp.route('/admin_login',methods=['GET','POST'])

def admin_login():
    if request.method =='GET' :
        return render_template("admin_login.html")
    else:
        admin_id=request.form['login_id']
        admin_password=request.form['login_pw']
        if not (admin_id and admin_password) : #둘중 하나라도 입력 안되면
            return "<script type='text/javascript'>alert('모두 입력해주세요.');document.location.href='/admin_login';</script>" 
        find_adminid=find_id_admin(g.db,admin_id)    #db에서 관리자 아이디 가져오기
        #db에서 아이디와 비밀번호로 정보 가져오기
        
        if (find_adminid) : #정보가 존재하면
            if(get_admin_login(g.db, admin_id, admin_password)):  #true 혹은 false
                session['adminname']=admin_id
                return render_template('admin_main.html')   #관리자 메인 페이지 이동
            else : 
                return "<script type='text/javascript'>alert('아이디나 비밀번호가 틀립니다.');document.location.href='/admin_login';</script>"
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디나 비밀번호가 틀립니다.');document.location.href='/admin_login';</script>"


@bp.route("/admin_logout")
def admin_logout():
    if 'user_id' in session:
        session.pop('user_id',None)
    session.pop('adminname',None)
    return redirect("/")