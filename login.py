from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

import jwt

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jcarrot  

@app.route('/')
def home():
   print("TEST!@#")
   return render_template('index2.html')

# @app.route('/login',methods=['POST'])
# def login_jwt():
#     user_id = request.form['id']
#     user_pw = request.form['pw']
#     check_id = db.user.find({'user_id':user_id})
#     check_pw = db.user.find({'user_pw':user_pw})


#     return jsonify({'result': 'success'})
@app.route('/register',methods=['POST'])
def test():
    a = request.form['id']
    b = request.form['pw']
    c = request.form['name']
    d = request.form['gmail']
    print("12")
    print(a + b+ c +d)
    return jsonify({'response':'success'})

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000,debug=True)