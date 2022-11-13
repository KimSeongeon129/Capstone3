<<<<<<< HEAD
from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import update_user, find_id_user, delete_user
import requests
import json

bp= Blueprint('accountDelete',__name__)
@bp.route('/accountDelete',methods=['GET','POST'])#계정 삭제

def accountDelete():
    if request.method =='GET' :
        return render_template("/accountDelete.html")
    else:
        user_id=request.form['user_id']
        if not (user_id) : 
            return "<script type='text/javascript'>alert('id를 입력해주세요.');document.location.href='/accountDelete';</script>" 
    
        redirect("/admin_main")
        find_userid = find_id_user(g.db, user_id)
        if (find_userid) : #정보가 존재하면
            delete_user(g.db, user_id)
            return render_template('admin_main.html')   #관리자 메인 페이지 이동
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디가 틀립니다.');document.location.href='/accountUpdate';</script>"
             


















    return render_template("accountDelete.html")

# @bp.route('/accountDelete')#계정 삭제페이지
# def accountDelete():
#     return 

=======
from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import update_user, find_id_user, delete_user
import requests
import json

bp= Blueprint('accountDelete',__name__)
@bp.route('/accountDelete',methods=['GET','POST'])#계정 삭제

def accountDelete():
    if request.method =='GET' :
        return render_template("/accountDelete.html")
    else:
        user_id=request.form['user_id']
        if not (user_id) : 
            return "<script type='text/javascript'>alert('id를 입력해주세요.');document.location.href='/accountDelete';</script>" 
    
        redirect("/admin_main")
        find_userid = find_id_user(g.db, user_id)
        if (find_userid) : #정보가 존재하면
            delete_user(g.db, user_id)
            return render_template('admin_main.html')   #관리자 메인 페이지 이동
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디가 틀립니다.');document.location.href='/accountUpdate';</script>"
             


















    return render_template("accountDelete.html")

# @bp.route('/accountDelete')#계정 삭제페이지
# def accountDelete():
#     return 

>>>>>>> 2020028e2216fe2cda7a5ed0a329544c17e379ea
