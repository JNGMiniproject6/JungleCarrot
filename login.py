from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

import jwt

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jcarrot  

@app.route('/')
def home():
   return render_template('index2.html')


if __name__ == '__main__':
    app.run('0.0.0.0',port=8000,debug=True)