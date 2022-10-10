from flask import Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

bp= Blueprint('cameraUpload',__name__)