from flask import Flask, render_template, session, g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import user_result
import requests
import json
import operator

bp= Blueprint('list',__name__)
@bp.route('/list',methods=['GET','POST'])#내역조회페이지
def list():    
    if request.method=='GET':#그냥 내역조회 했을시 전체 보여주기
        id=session['username']
        list = user_result(g.db,id)
        list = sorted(list, key= lambda x: x['date'], reverse=True)#최신순으로 반환
        return render_template("list.html", list = list)
    else: #필터링 한거 보여주기
        #필터링 내용 가져오기
        filtering='part_judge'
        data='불량'
        id=session['username']
        #필터링 내용으로 db에서 데이터 가져오기
        list = user_result(g.db,id)
        list = sorted(list, key= lambda x: x['date'], reverse=True)#최신순으로 반환
        dic=[]
        c=0
        for i in list:#예시로 불량품만 뽑기
            if i[filtering]==data:
                dic.append(i)
                c=c+1
        if c==0:
            dic=['no']
        print(dic)
        return render_template("list.html", list = dic)


