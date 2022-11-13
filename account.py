from flask import Flask, render_template,session
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('account',__name__)


@bp.route('/account')#계정 업데이트페이지
def account():
    if 'adminname' in session:
        return render_template("account.html")
    else :
        return redirect('/')

