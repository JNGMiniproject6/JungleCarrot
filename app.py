from flask import Flask, jsonify, request, render_template
SECRET_KEY = 'jungle'

from pymongo import MongoClient

import jwt
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.ehlo()
smtp.starttls()
smtp.login('dohyeon0518@gmail.com','gqkk rfgy ymuz kmuk')

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
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/main', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id':payload['id']}, {'_id':0})
        return render_template('group_buy.html')
        # return jsonify({'result':'success', 'nickname':userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail', 'msg':'로그인 시간이 만료되었습니다. '})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail', 'msg':'로그인 정보가 존제하지 않습니다.'})
    
@app.route('/group_buy_join', methods=['POST'])
def buy_join():
   item_id_receive = request.form['item_id_give']
   print(item_id_receive)
#    id_receive = request.form['id_give']
   item = db.item.find_one({'item_id':item_id_receive})
   print(item)
   print("추가 전 ", item['current_people'])
   db.item.update_one({}, {'$set': {'current_people': 0}}) # current_people 값 초기화
   if item['current_people'] == item['max_people'] - 1:
      people_up = item['current_people'] + 1
      result = db.item.update_one({}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기
      print("추가 후 ",people_up)
      print("GMAIL 전송하기")
      msg = MIMEText(item['link'])   # 메일의 내용
      msg['Subject'] = '공동구매를 위한 카카오톡 오픈 채팅 링크입니다.' # 메일의 제목
      receiver = ['arevolvera@gmail.com','gold6219@naver.com','moorow0729@hufs.ac.kr'] # 전송할 메일 주소의 리스트
   
      smtp.sendmail('dohyeon0518@gmail.com',receiver,msg.as_string())

      smtp.quit()

      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   elif item['current_people'] < item['max_people']:
      people_up = item['current_people'] + 1
      result = db.item.update_one({}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기
      print("추가 후 ",people_up)
      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   else:
      return jsonify({'result':'failure'})
    
if __name__ == '__main__':
	app.run(host = '0.0.0.0',
					port = 8000, 
					debug = True)