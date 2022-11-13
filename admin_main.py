from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('admin_main',__name__)
@bp.route('/admin_main')#계정 관리 페이지
def admin_main():
    return render_template("admin_main.html")
# @bp.route('/account')#계정 관리 페이지
# def account():
#     return render_template("account.html")

# @bp.route('/admin_list')#품질내역 관리 페이지
# def admin_list():
#     return 

# @bp.route('/admin_statistics')#통계 페이지
# def admin_statistics():
#     return 
