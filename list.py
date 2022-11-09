from flask import Flask, render_template, session, g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import user_result
import requests
import json
import operator,string

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
        filtering=request.form['selectbox']
        data=request.form['search_box']
        data=data.upper()
        print(filtering)
        print(data)
        id=session['username']
        #필터링 내용으로 db에서 데이터 가져오기
        list = user_result(g.db,id)
        list = sorted(list, key= lambda x: x['date'], reverse=True)#최신순으로 반환
        dic=[]
        c=0
        if filtering=='date':
            for i in list:#예시로 불량품만 뽑기
                filterup=str(i[filtering])
                if data in filterup:
                    dic.append(i)
                    c=c+1
        else:
            for i in list:#예시로 불량품만 뽑기
                filterup=i[filtering].upper()
                if data in filterup:
                    dic.append(i)
                    c=c+1
        if c==0:
            dic=['no']
        return render_template("list.html", list = dic)

@bp.route('/detail')#세부내역조회
def detail():
    #데이터 가져오기(아마 검사번호)
    inspection_number=1
    #검사번호로 모든 정보 가져오기(일련번호, 부량여부, 부품 종류, 불량 종류, 담당자, 시간, 라인, 검사번호,이미지 등등)
    dic_list="db_find_parts_img"
    #리스트로 받은 것을 전부 보내주기
    return render_template("detail.html",data=dic_list)

