from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.jcarrot        # 'jcarrot'이라는 db 생성

def inital_db():
    initial_user = {
        'user_id': 'abc123',        #유저의 아이디
        'pw': 'abc123',             #유저의 패스워드
        'gmail':'abc123@gmail.com', #유저의 gmail 주소
        'name':'홍길동'               #유저의 이름
    }
    initial_item = {
        'item_id':'휴지',           #품목의 아이디
        'user_id': ['a','b','c'],       #공동구매에 참여할 인원 리스트
        'item_info': '생필품',            #품목의 정보
        'category':'생필품',              #품목의 카테고리
        'current_people': 2,            #공동구매에 현재 참여한 인원
        'max_people': 3,                #공동구매에 참여할 인원
        'url': 'https://www.naver.com', #품목의 구매주소
        'item_type':1,                  #품목이 나눔, 공동구매인지 확인
        'link':'https://www.naver.com', #카카오톡 오픈채팅 주소
        "place":'강의실',                 #만날 장소
        'time': '13시 30분',              #만날 시간
        'item_label':"건조대 1개 나눔합니다."    #나눔상품설명
    }
    db.item.insert_one(initial_item)    #item 컬렉션에 더미 데이터 추가
    print("db item 등록 완료!")
    db.user.insert_one(initial_user)    #user 컬렉션에 더미 데이터 추가
    print("db user 등록 완료!")


if __name__ == '__main__':
    # db.item.drop()    #user 컬렉션 삭제
    # db.user.drop()

    inital_db()