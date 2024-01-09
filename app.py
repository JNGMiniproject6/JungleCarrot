from flask import Flask, jsonify, request, render_template
SECRET_KEY = 'jungle'

from pymongo import MongoClient
import jwt
import datetime
import hashlib

db = MongoClient('localhost', 27017).jcarrot

app = Flask(__name__)

##회원가입 api
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/group_buy')
def group_buy():
    return render_template("group_buy.html")

@app.route('/api/register', methods=['POST', 'GET'])
def api_register():
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        name_receive = request.form['name_give']
        email_receive = request.form['email_give']
        print("id_receive", id_receive)
    
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
        db.user.insert_one({'user_id':id_receive, 'pw':pw_hash,'gmail':email_receive, 'name':name_receive})
        
        return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다.'})
 
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print("pw_hash", pw_hash)
    print("id_receive", id_receive)
    
    result = db.user.find_one({'user_id': id_receive, 'pw': pw_hash}) 
 
    if result is not None:
        payload = {
            'id' : id_receive,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.kookies.get('mytoken')
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        
        userinfo = db.user.find_one({'id':payload['id']}, {'_id':0})
        return jsonify({'result':'success', 'nickname':userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail', 'msg':'로그인 시간이 만료되었습니다. '})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail', 'msg':'로그인 정보가 존제하지 않습니다.'})
    
if __name__ == '__main__':
	app.run(host = '0.0.0.0',
					port = 5000, 
					debug = True)