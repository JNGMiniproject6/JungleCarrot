from flask import Flask, jsonify, request, render_template
SECRET_KEY = 'jungle'

from pymongo import MongoClient
import jwt
import datetime
import hashlib
from bs4 import BeautifulSoup
import requests

db = MongoClient('localhost', 27017).jcarrot

app = Flask(__name__)



##웹 스크래핑
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
    
    
    
    
    
##회원가입 api
@app.route('/')
def home():
    return render_template("index.html")

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
    
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash}) 
 
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
    
    
    
    
@app.route('/api/itemregist', methods=['POST'])
def api_item():
    ## 물건 db 컨테이너
    item_id_receive = request.form['item_id_give']
    item_user_id_receive = request.form['item_user_id_give']
    item_info_receive = request.form['item_info_give']
    item_category_receive = request.form['item_category_give']
    item_current_people_receive = request.form['item_current_people_give']
    item_max_people_receive = request.form['item_max_people_give']
    item_url_receive = request.form['item_url_give']
    item_type_receive = request.form['item_type_give']
    item_link_receive = request.form['item_link_give']
    
    db.item.insert_one({
        'id':item_id_receive,
        'user_id':item_user_id_receive,
        'info':item_info_receive,
        'category':item_category_receive,
        'current_people':item_current_people_receive,
        'max_people':item_max_people_receive,
        'url':item_url_receive,
        'type':item_type_receive,
        'link':item_link_receive
        })#아이템 데이터
    
    return jsonify({'result': 'success', 'msg': '물품이 정상적으로 등록되었습니다.'})
    
    
    

if __name__ == '__main__':
	app.run(host = '0.0.0.0',
					port = 5000, 
					debug = True)