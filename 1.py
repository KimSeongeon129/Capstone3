from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request
import requests
import json
app=Flask(__name__)
global access_token
#맨처음 페이지
@app.route("/")
def index():
    return render_template("index.html")
#로그인 
@app.route("/oauth")
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
    
    return render_template("logout.html")
#로그아웃
@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ =="__main__" :
    app.run(debug=True)