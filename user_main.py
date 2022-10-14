from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('user_main',__name__)

@bp.route('/user_main')# 유저 페이지
def user_main():
    return render_template("user_main.html")
