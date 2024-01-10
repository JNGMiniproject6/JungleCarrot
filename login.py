from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

import jwt

import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.ehlo()
smtp.starttls()
smtp.login('dohyeon0518@gmail.com','gqkk rfgy ymuz kmuk')

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jcarrot  

@app.route('/')
def home():
   return render_template('test.html')


@app.route('/group_buy_join', methods=['POST'])
def buy_join():
   item_id_receive = request.form['item_id_give']
   id_receive = request.form['id_give']
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
    app.run('0.0.0.0',port=8000,debug=True)
