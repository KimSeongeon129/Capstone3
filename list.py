from flask import Flask, render_template, session, g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import user_result
import requests
import json

bp= Blueprint('list',__name__)
@bp.route('/list',methods=['GET','POST'])#내역조회페이지
def list():    
    if request.method=='GET':#그냥 내역조회 했을시 전체 보여주기
        id=session['username']
        list = user_result(g.db,id)
        print(list)
        return render_template("list.html", list = list)
    else: #필터링 한거 보여주기
        #필터링 내용 가져오기
        #필터링 내용으로 db에서 데이터 가져오기
        #데이터 가져온거 반환하기
        return id


