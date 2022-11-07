from flask import Flask, render_template, session, g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import user_result
import requests
import json

bp= Blueprint('list',__name__)
@bp.route('/list')#내역조회페이지
def list():    
    id=session['username']
    list = user_result(g.db,id)
    print(list)
    return render_template("list.html", list = list)

