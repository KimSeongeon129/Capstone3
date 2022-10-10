from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('lgoin',__name__)

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
    find_id= id #디비에서 id 가져오기
    # db에 아이디가 존재하면
    if (find_id) :
        return render_template("user_main.html")
    else : #db에 아이디가 존재 하지 않는 경우
        #db에 저장
        return render_template("user_main.html")

#네이버 로그인


#관리자 로그인
@bp.route('/admin_login',methods=['POST'])
def admin_login():
    admin_id=request.form['admin_id']
    admin_password=request.form['admin_password']
    if not (admin_id and admin_password) : #둘중 하나라도 입력 안되면
        return "<script type='text/javascript'>alert('모두 입력해주세요.');document.location.href='/admin_login';</script>" 

    #db에서 아이디와 비밀번호로 정보 가져오기
    find_id_pw=admin_id
    
    if (find_id_pw) : #정보가 존재하면
        return render_template('admin_main.html')
    else : #정보가 존재하지 않으면 
        return "<script type='text/javascript'>alert('아이디나 비밀번호가 틀립니다.');document.location.href='/admin_login';</script>"