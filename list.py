from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('list',__name__)


@bp.route('/list')#상세조회페이지
def detail():
    return render_template("list.html")