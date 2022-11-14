from flask import Flask, render_template, session
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import update_user, find_id_user
import requests
import json

bp= Blueprint('accountUpdate',__name__)


@bp.route('/accountUpdate_id',methods=['GET','POST'])#계정 업데이트페이지

def accountUpdate_id():
    if request.method =='GET' :
        return render_template("/accountUpdate_id.html")
    else:
        user_id=request.form['user_id']
        if not (user_id) : 
            return "<script type='text/javascript'>alert('id를 입력해주세요.');document.location.href='/accountUpdate_id';</script>" 
    
        redirect("/admin_main")
        find_userid = find_id_user(g.db, user_id)
  
        if (find_userid) : #정보가 존재하면
            find=find_userid[0]
            find = find['user_id']
            print(type(find_userid))
            print(find)
            session['user_id'] = find
            return render_template('accountupdate.html')   
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디가 틀립니다.');document.location.href='/accountUpdate_id';</script>"
             

@bp.route('/accountUpdate',methods=['GET','POST'])#계정 업데이트페이지

def accountUpdate():
    if request.method =='GET' :
        return render_template("/accountUpdate.html")
    else:
        user_line=request.form['user_line']
        user_admin=request.form['user_admin']
        nickname=request.form['nickname']
        if not (user_line and user_admin and nickname) : 
            return "<script type='text/javascript'>alert('모두 입력해주세요.');document.location.href='/accountUpdate';</script>" 
    
        redirect("/admin_main")

        if (session['user_id']) : #정보가 존재하면
            update_user(g.db, nickname, user_admin, user_line, session['user_id'])
            return render_template('admin_main.html')   #관리자 메인 페이지 이동
        else : #정보가 존재하지 않으면 
            return "<script type='text/javascript'>alert('아이디가 틀립니다.');document.location.href='/accountUpdate';</script>"
             




