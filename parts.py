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

defect_dict = {
    'Duct damage':{
        '부품':'덕트',
        '한글명':'덕트 손상'
    },
    'Bad connection':{
        '부품':'덕트',
        '한글명':'연결 불량'
    },
    'Bad tape':{
        '부품':'덕트',
        '한글명':'테이프 불량'
    },
    'Poor bolting':{
        '부품':'선박 배관',
        '한글명':'볼트 체결 불량'
    },
    'Pipe damage':{
        '부품':'선박 배관',
        '한글명':'파이프 손상'
    },
    'Step difference':{
        '부품':'선체',
        '한글명':'단차'
    },
    'Poor installation of reinforcement':{
        '부품':'선체',
        '한글명':'보강재 설치 불량'
    },
    'Bad binding':{
        '부품':'케이블',
        '한글명':'바인딩 불량'
    },
    'Poor installation':{
        '부품':'케이블',
        '한글명':'설치 불량'
    },
    'Cable damage':{
        '부품':'케이블',
        '한글명':'케이블 손상'
    },
    'Poor Processing':{
        '부품':'보온재',
        '한글명':'가공 불량'
    },
    'Insulation damage':{
        '부품':'보온재',
        '한글명':'보온재 손상'
    },
    'Poor connection processing':{
        '부품':'보온재',
        '한글명':'연계 처리 불량'
    },
    'Poor handling of tin':{
        '부품':'보온재',
        '한글명':'함석 처리 불량'
    },
}

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