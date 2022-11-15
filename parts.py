from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint,g
import requests
import json
from flask import g
#이미지 불량의 따른 이미지 종류 반환

duct_def = ['Duct damage', 'Bad connection', 'Bad tape']
pipe_def = ['Poor bolting', 'Pipe damage']
hull_def = ['Step difference', 'Poor installation of reinforcement']
cable_def = ['Bad binding', 'Poor installation', 'Cable damage']
lagging_def = ['Poor Processing', 'Insulation damage', 'Poor connection processing', 'Poor handling of tin']

def check_type(label):
    type=""
    if label=='Overlap'or label=='Undercut':
        type='버트조인트'
    elif label=='Bad binding'or label=='Poor installation' or label=='Cable damage':
        type='케이블'
    elif label=='Duct damage'or label=='Bad connection' or label=='Bad tape':
        type='덕트'
    elif label in ['Poor bolting', 'Pipe damage']:
        type='선박 배관'
    elif label in ['Step difference', 'Poor painting', 'Poor installation of reinforcement']:
        type='선체'
    else :
        type='다른거'       
    return type