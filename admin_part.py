from flask import Flask, render_template,session,g
from flask import jsonify,url_for,redirect,request,Blueprint
from db1011 import delete_result, update_result
import requests
import json

bp= Blueprint('admin_part',__name__)
@bp.route('/admin_part_delete/<num>')#부품 삭제
def admin_part_delete(num): 
    data=delete_result(g.db,num)
    return jsonify(
        result="success",
        data=data
        )

@bp.route('/admin_part_update',methods=['GET','POST'])#부품 업데이트
def admin_part_update():
    if request.method=='GET':
        return render_template("admin_part_update.html")
    else:
        num=request.form['num']
        part_category=request.form['part_category']
        part_judge=request.form['part_judge']
        user_id=request.form['user_id']
        print(num)
        data=update_result(g.db,part_category,part_judge,num,user_id)
        return jsonify(
            result="success",
            data=data
            )