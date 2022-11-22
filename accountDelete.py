from flask import Flask, render_template,session
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import update_user, find_id_user, delete_user
import requests
import json
bp= Blueprint('accountDelete',__name__)

@bp.route('/accountDelete',methods=['GET','POST'])#계정 삭제
def accountDelete():
    if request.method =='GET' :
        if 'adminname' in session:
            return render_template("accountDelete.html")
        else :
            return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 
    else:
        user_id=request.form['user_id']
        if not (user_id) : 
            return jsonify(
                data="check_id"
            )
        find_userid = find_id_user(g.db, user_id)
        if (find_userid) : #정보가 존재하면

            delete_user(g.db, user_id)
            return jsonify(data="success")   #관리자 메인 페이지 이동
        else : #정보가 존재하지 않으면 
            return jsonify(data="no_id")
             



















    return render_template("accountDelete.html")

# @bp.route('/accountDelete')#계정 삭제페이지
# def accountDelete():
#     return 

