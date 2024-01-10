from flask import Flask, render_template, request
from flask_socketio import SocketIO
from pymongo import MongoClient, ObjectId

app = Flask(__name__)
socketio = SocketIO(app)

# MongoDB 연결
db = MongoClient('localhost', 27017).jcarrot
chat_collection = db.item

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print('Message: ' + data['message'])

    # MongoDB에 데이터 추가
    inserted_data = {'message': data['message']}
    inserted_document = chat_collection.insert_one(inserted_data)

    # 새로 추가된 데이터의 _id 값을 클라이언트에게 전송
    new_data_id = str(inserted_document.inserted_id)
    socketio.emit('new_message_id', {'_id': new_data_id})

    # MongoDB에서 특정 _id 값의 문서를 찾고 message 필드를 업데이트
    chat_id = data.get('_id')
    if chat_id:
        chat_collection.update_one({'_id': ObjectId(chat_id)},
                                   {'$set': {'message': data['message']}})

if __name__ == '__main__':
    socketio.run(app)
