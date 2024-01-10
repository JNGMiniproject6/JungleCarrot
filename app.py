from flask import Flask, jsonify, render_template, request
from bs4 import BeautifulSoup
from bson import ObjectId


SECRET_KEY = 'jungle'

from pymongo import MongoClient
from flask.json.provider import JSONProvider


import requests
import jwt
import datetime
import hashlib
import smtplib
import json
import sys

from email.mime.text import MIMEText
smtp = smtplib.SMTP('smtp.gmail.com',587)
smtp.ehlo()
smtp.starttls()
smtp.login('dohyeon0518@gmail.com','gqkk rfgy ymuz kmuk')

db = MongoClient('localhost', 27017).jcarrot

app = Flask(__name__)

def scrape_coupang(url):
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  og_title = soup.find("meta", property="og:title")['content']
  prod_image_detail = soup.find("div", class_="prod-image__detail")
  total_price = soup.find("span", class_="total-price")
  return og_title, prod_image_detail, total_price

def scrape_naver_smartstore(url):
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  info_1 = soup.find("div", class_="_22kNQuEXmb _copyable")
  info_2 = soup.find("div", class_="bd_1uFKu")
  info_3 = soup.find("div", class_="_1LY7DqCnwR")
  return info_1, info_2, info_3

##사이트 추가 해야됨
@app.route('/api/site_scraping')
def index():
  url = "https://www.coupang.com/vp/products/335833200?itemId=17982326014&vendorItemId=85139110125&pickType=COU_PICK&q=%EA%B3%A0%EC%96%91%EC%9D%B4&itemsCount=36&searchId=170c23c33ddc475a8a994d1960670660&rank=1&isAddedCart="
  site_identifier = url.split('/')[2]
  if site_identifier == "www.coupang.com":
    og_title, prod_image_detail, total_price = scrape_coupang(url)
    return render_template('coupang.html', og_title=og_title, prod_image_detail=prod_image_detail, total_price=total_price)
  elif site_identifier == "smartstore.naver.com":
    info_1, info_2, info_3 = scrape_naver_smartstore(url)
    return render_template('naver_smartstore.html', info_1=info_1, info_2=info_2, info_3=info_3)
  else:
    return "Unsupported site"

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

# 위에 정의되 custom encoder 를 사용하게끔 설정한다.
app.json = CustomJSONProvider(app)
##회원가입 api
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/group_buy')
def group_buy():
    items = list(db.item.find({'item_type':"0"}, {'_id':0}))
    print(items)
    return render_template("group_buy.html", items=items)

@app.route('/group_buy/det')
def group_buyDet():
    items = list(db.item.find({'item_type':"0",'category':'세제'},{'_id':0}))
    return render_template("group_buy.html",items=items)

@app.route('/group_buy/tol')
def group_buyTol():
    items = list(db.item.find({'item_type':"0",'category':'세면도구'},{'_id':0}))
    return render_template("group_buy.html",items=items)

@app.route('/group_buy/snack')
def group_buySnack():
    items = list(db.item.find({'item_type':"0",'category':'간식'},{'_id':0}))
    return render_template("group_buy.html",items=items)

@app.route('/group_buy/tissue')
def group_buyTissue():
    items = list(db.item.find({'item_type':"0",'category':'휴지류'},{'_id':0}))
    return render_template("group_buy.html",items=items)

@app.route('/share')
def share():
    items = list(db.item.find({'item_type':"1"},{'_id':0}))
    return render_template("share.html",items=items)

@app.route('/share/det')
def shareDet():
    items = list(db.item.find({'item_type':"1",'category':'세제'},{'_id':0}))
    return render_template("share.html",items=items)

@app.route('/share/tol')
def shareTol():
    items = list(db.item.find({'item_type':"1",'category':'세면도구'},{'_id':0}))
    return render_template("share.html",items=items)

@app.route('/share/snack')
def shareSnack():
    items = list(db.item.find({'item_type':"1",'category':'간식'},{'_id':0}))
    return render_template("share.html",items=items)

@app.route('/share/tissue')
def shareTissue():
    items = list(db.item.find({'item_type':"1",'category':'휴지류'},{'_id':0}))
    return render_template("share.html",items=items)

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
        return render_template('share.html')
        # return jsonify({'result':'success', 'nickname':userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail', 'msg':'로그인 시간이 만료되었습니다. '})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail', 'msg':'로그인 정보가 존제하지 않습니다.'})
    
@app.route('/group_buy_join', methods=['POST'])
def buy_join():
   item_id_receive = request.form['item_id_give']
   user_id_receive = request.form['user_id_give']

   print(item_id_receive)
#    id_receive = request.form['id_give']
   print(db.item.find({'user_id':item_id_receive}))
   item = db.item.find_one({'item_id':item_id_receive})
   print(item)
   print("추가 전 ", item['current_people'])
   db.item.update_one({}, {'$set': {'current_people': 0}}) # current_people 값 초기화
   if item['current_people'] == item['max_people'] - 1:
      db.item.update_one({'item_id': item_id_receive}, {'$push': {'user_id':user_id_receive}})
      people_up = item['current_people'] + 1
      print("!@#")
      print(people_up)
      result = db.item.update_one({'item_id':item_id_receive}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기
      print("추가 후 ",people_up)
      print("GMAIL 전송하기")
      msg = MIMEText(item['link'])   # 메일의 내용
      msg['Subject'] = '공동구매를 위한 카카오톡 오픈 채팅 링크입니다.' # 메일의 제목
      receiver = ['arevolvera@gmail.com','gold6219@naver.com','moorow0729@hufs.ac.kr'] # 전송할 메일 주소의 리스트
   
    #   smtp.sendmail('dohyeon0518@gmail.com',receiver,msg.as_string())
      smtp.quit()

      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   elif item['current_people'] < item['max_people']:
      db.item.update_one({'item_id': item_id_receive}, {'$push': {'user_id':user_id_receive}})
      people_up = item['current_people'] + 1
      result = db.item.update_one({'item_id':item_id_receive}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기
      print("추가 후 ",people_up)
      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   else:
      return jsonify({'result':'failure'})

@app.route('/share_join', methods=['POST'])
def share_join():
   item_id_receive = request.form['item_id_give']
   user_id_receive = request.form['user_id_give']

   print(item_id_receive)
#    id_receive = request.form['id_give']
   item = db.item.find_one({'item_id':item_id_receive})
   db.item.update_one({}, {'$set': {'current_people': 0}}) # current_people 값 초기화
   user_list = db.item.find_one({'user_id':user_id_receive,'item_id':item_id_receive},{'_id':0})
   
   kakao_link = db.item.find_one({'user_id':user_id_receive},{'_id':0})['link']
   print(kakao_link)
   mail_list = [db.user.find_one({'user_id':user_id_receive})['gmail']]
   for i in user_list['user_id']:
       mail = db.user.find_one({'user_id':i})
       mail_list.append(mail['gmail'])
   print(mail_list)
   if item['current_people'] == item['max_people'] - 1:
      db.item.update_one({'item_id': item_id_receive}, {'$push': {'user_id':user_id_receive}})
      people_up = item['current_people'] + 1

      result = db.item.update_one({'item_id': item_id_receive}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기

      msg = MIMEText(kakao_link)   # 메일의 내용
      msg['Subject'] = '공동구매를 위한 카카오톡 오픈 채팅 링크입니다.' # 메일의 제목
    #   receiver = ['arevolvera@gmail.com','gold6219@naver.com','moorow0729@hufs.ac.kr'] # 전송할 메일 주소의 리스트
      receiver = mail_list
      print(receiver)
      smtp.sendmail('dohyeon0518@gmail.com',receiver,msg.as_string())
      smtp.quit()

      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   elif item['current_people'] < item['max_people']:
      db.item.update_one({'item_id': item_id_receive}, {'$push': {'user_id':user_id_receive}})
      people_up = item['current_people'] + 1
      result = db.item.update_one({'item_id':item_id_receive}, {'$set': {'current_people': people_up}})
      # people_list.append() # 사용자의 아이디 받아와서 리스트에 추가하기
      print("추가 후 ",people_up)
      if result.modified_count == 1:
         return jsonify({'result':'success'})
      else:
         return jsonify({'result':'failure'})
   else:
      return jsonify({'result':'failure'})

@app.route('/api/itemregist', methods=['POST'])
def api_item():
    ## 물건 db 컨테이너
    # item_id_receive = request.form['item_id_give']
    item_place_receive = request.form['place_give']
    item_time_receive = request.form['time_give']
    item_user_id_receive = request.form['user_id_give']
    item_info_receive = request.form['item_info_give']
    item_category_receive = request.form['category_give']
    item_id_receive = request.form['item_id_give']
    # item_current_people_receive = request.form['item_current_people_give']
    item_max_people_receive = request.form['people_give']
    item_url_receive = request.form['item_url_give']
    item_type_receive = request.form['item_type_give']
    chat_link_receive = request.form['chatLink_give']
    
    db.item.insert_one({
        'user_id':[item_user_id_receive],
        'info':item_info_receive,
        'place':item_place_receive,
        'time':item_time_receive,
        'category':item_category_receive,
        'current_people': 1,
        'max_people':int(item_max_people_receive),
        'url':item_url_receive,
        'item_type':item_type_receive,
        'item_id':item_id_receive,
        'link':chat_link_receive
        })#아이템 데이터
    
    return jsonify({'result': 'success', 'msg': '물품이 정상적으로 등록되었습니다.'})
    
if __name__ == '__main__':
	app.run(host = '0.0.0.0',
					port = 8000, 
					debug = True)