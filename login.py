from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
from db1011 import find_id_user,find_id_admin, add_user
import requests
import json
from flask import g

bp= Blueprint('login',__name__)
@bp.route("/")
def login():
    return render_template("login.html")

#카카오 로그인
@bp.route("/oauth")
def oauth_api():
    #카카오 코드 가져오기
    code=str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload="grant_type=authorization_code&client_id=32e62fdd5c6f676f20e8792d524c06b9&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth&code="+str(code)
    headers= {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-control':"no-cache",
    }
    #토큰 가져오기
    response=requests.request("Post",url,data=payload,headers=headers)
    print(response.text)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    #토큰의 정보 가져오기
    url="https://kapi.kakao.com/v1/user/access_token_info"

    headers.update({'Authorization':"Bearer " + str(access_token)})
    response=requests.request("GET",url, headers= headers)
    #토큰에 해당하는 유저의 정보 가져오기
    url="https://kapi.kakao.com/v2/user/me"

    headers.update({'Authorization':"Bearer " + str(access_token)})
    response=requests.request("GET",url, headers= headers)
    id = json.loads(((response.text).encode('utf-8')))['id']
    kakao=json.loads(((response.text).encode('utf-8')))['kakao_account']
    profile=kakao['profile']
    name=profile['nickname']

    print(name)
    id ='k'+ str(id)#아이디에 k 붙여서 string타입으로 변경
    #이과정에서 id 타입 확인하고 
    find_id= find_id_user(g.db,id) #디비에서 id 가져오기
    # db에 아이디가 존재하면
    
    if (find_id) :
        return redirect("/user_main")
    else : #db에 아이디가 존재 하지 않는 경우
        #db에 저장
        add_user(g.db, id, name)
<<<<<<< HEAD
        
=======
>>>>>>> a1838936a5be258a679e086c8febdc392ae02378
        return redirect("/user_main")

#네이버 로그인
@bp.route("/naver")
def naver():
    url="https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=CZ4CAklls0R3pDVGPNhs&state=32raedfa38usf&redirect_uri=http://localhost:5000/naver_login"
    return redirect(url)
@bp.route("/naver_login")
def naver_login():
    code=str(request.args.get('code'))
    url = "https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id=CZ4CAklls0R3pDVGPNhs&client_secret=gLpXtGJwVL&code="+str(code)+"&state=32raedfa38usf"
    headers= {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-control':"no-cache",
    }
    #토큰 가져오기
    response=requests.request("Post",url,headers=headers)
    print(response.text)
    #토큰의 정보 가져오기
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    response = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization" : f"Bearer {access_token}"},)

    res = json.loads(((response.text).encode('utf-8')))['response']
    id=res['id']
    name=res['name']
    id ='n'+ str(id)#아이디에 n 붙여서 string타입으로 변경
    #이과정에서 id 타입 확인하고 
    find_id= find_id_user(g.db,id) #디비에서 id 가져오기
    # db에 아이디가 존재하면
    if (find_id) :
        return redirect("/user_main")
    else : #db에 아이디가 존재 하지 않는 경우
        #db에 저장
        add_user(g.db, id, name)
        return redirect("/user_main")