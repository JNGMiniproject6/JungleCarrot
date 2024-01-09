from flask import Flask, render_template, jsonify, request, session, redirect, url_for
SECRET_KEY = 'jungle'
app = Flask(__name__)
##from pymongo import MongoClient 데이터베이스 연결
import jwt
import datetime
import hashlib

##회원가입 api

@app.route('/api/register/', methods=['POST'])
def api_register():
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        name_receive = request.form['name_give']
        email_receive = request.form['email_give']
    
        pw_hash = hashlib.sha256(pw_receive.endoce('utf-8')).hexdigest()
        ##pw 암호화
    
        db.user.insert_one({'id':id_receive, 'pw':pw_hash})
        ##db 경로 수정
 
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.endoce('utf-8')).hexdigest()
    
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash}) 
    ##db 경로 수정
 
    if result is not None:
        payload = {
            'id' : id_receive,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=5)    
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    
    
    
    
    

if __name__ == '__main__':
	app.run(host = '0.0.0.0',
					port = 5000, 
					debug = True)