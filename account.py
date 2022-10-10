from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('account',__name__)


@bp.route('/accountUpdate')#계정 업데이트페이지
def accountUpload():
    return 

@bp.route('/accountDelete')#계정 삭제페이지
def accountDelete():
    return 

