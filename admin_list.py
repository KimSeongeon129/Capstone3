from flask import Flask, render_template, session, g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import result,detailed_result
import requests
import json
import operator,string

bp= Blueprint('admin_list',__name__)
@bp.route('/admin_list')
def admin_list():
    if 'adminname' in session:
        return render_template("admin_list.html")
    else :
        return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 
@bp.route('/admin_list_data',methods=['GET','POST'])#내역조회페이지
def admin_list_data():    
    if request.method=='GET':#그냥 내역조회 했을시 전체 보여주기
        list = result(g.db)
        print(list)
        list = sorted(list, key= lambda x: x['date'], reverse=True)#최신순으로 반환
        return jsonify(
            success="성공",
            data=list
        )
    else: #필터링 한거 보여주기
        #필터링 내용 가져오기
        filtering=request.form['selectbox']
        data=request.form['search_box']
        data=data.upper()
        print(filtering)
        print(data)
        #필터링 내용으로 db에서 데이터 가져오기
        list = result(g.db)
        list = sorted(list, key= lambda x: x['date'], reverse=True)#최신순으로 반환
        dic=[]
        c=0
        if filtering=='date':
            data=data.replace('/','-')
            temp=data[-4:]
            data=temp+'-'+data[0:5]
            print(data)
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
        return jsonify(
            success="성공",
            data=dic
        )
@bp.route('/admin_detail_num/<num>')#세부내역조회
def admin_detail_num(num):
    
    data=detailed_result(g.db,num)
    return jsonify(
        result="success",
        data=data
        )

@bp.route('/admin_detail')#세부내역조회
def admin_detail():
    if 'adminname' in session:
        return render_template("detail.html")
    else :
        return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 