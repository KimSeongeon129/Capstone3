from flask import Flask, render_template,session
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('admin_main',__name__)
@bp.route('/admin_main')#계정 관리 페이지
def admin_main():
    if 'adminname' in session:
        return render_template("admin_main.html")
    else :
        return "<script type='text/javascript'>alert('로그인 하세요.');document.location.href='/';</script>" 
