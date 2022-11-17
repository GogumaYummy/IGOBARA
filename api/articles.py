from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from datetime import datetime
from . import login_join
from config import pymongo # 데이터베이스와 연결하는 부분 모듈화
import math
# 여기서 사용한 패키지는 app.py에서 다시 불러올 필요가 없습니다.

post_api = Blueprint("post", __name__, url_prefix="/api") # 새 블루프린트 생성

@post_api.route('/articles') #게시글 목록을 받아오는 api
def get_articles():
    page = int(request.args.get('page', default = '0', type = str)) # 요청에서 page의 값을 정수로 바꿔서 저장
    max_page = math.ceil(pymongo.db.articles.count_documents({}) / 30) # 전체 게시글의 개수를 30으로 나눈 최대 페이지 수 저장

    articles = list(pymongo.db.articles.find({}, {}).sort("createdAt", -1).skip((page - 1) * 30).limit(30)) # 페이지의 게시글을 최신 순으로 30개씩 잘라 리스트로 변환하고 저장

    decoded_articles = list() # 변환된 게시글들을 저장하기 위해 새로운 리스트 선언
    for article in articles:
        new_article = article 
        new_article['_id'] = str(new_article['_id']) # objectId 타입을 문자열로 변환
        new_article['postedByNick'] = pymongo.db.users.find_one({'id': new_article['postedBy']})['nick'] # 유저의 아이디로 닉네임을 찾아서 저장
        decoded_articles.append(new_article) # 새로 선언한 리스트에 변환된 게시글 추가

    return jsonify({'articles': decoded_articles, 'max_page': max_page}) # 변환된 게시글과 최대 페이지 수를 json으로 응답

@post_api.route('/article/<id>')
def post(id):
    _id = ObjectId(id)
    result = pymongo.db.articles.find_one({ '_id' : _id })
    result['_id'] = str(result['_id'])

    return jsonify({'result': result })


@post_api.route('/article/<id>', methods=["DELETE"])
def delete(id):
    user_data = login_join.check_login()
    user_id = user_data['id']

    _id = ObjectId(id)
    article = pymongo.db.articles.find_one({ '_id' : _id }, {"_id": 0, "postedBy": 1})
    posted_by = article['postedBy']

    if (user_id == posted_by):
        pymongo.db.articles.delete_one({"_id" : _id})
        return jsonify({'result': 'success', 'msg': '삭제 완료!'})
    else:
        return jsonify({'result': 'fail', 'msg': '삭제 실패! 아이디가 일치하지 않습니다.'})

@post_api.route('/write', methods=["POST"]) #게시글 등록 
def write():
    user_data = login_join.check_login()
    user_id = user_data['id']

    title = request.form['title_give']
    image = request.form['image_give']
    content = request.form['content_give']

    doc = {
        'title': title,
        'image': image,
        'content': content,
        'postedBy': user_id,
        'createdAt': datetime.now()
    }

    pymongo.db.articles.insert_one(doc)

    return jsonify({'msg': '작성 완료!', 'state': 1})

@post_api.route('/article/<id>', methods=["PUT"]) # 게시글 수정
def rewrite(id):
    user_data = login_join.check_login()
    user_id = user_data['id']

    title = request.form['title_give']
    image = request.form['image_give']
    content = request.form['content_give']

    _id = ObjectId(id)
    article = pymongo.db.articles.find_one({ '_id' : _id }, {"_id": 1, "postedBy": 1})
    posted_by = article['postedBy']

    doc = {
        'title': title,
        'image': image,
        'content': content
    }

    if (user_id == posted_by):
        pymongo.db.articles.update_one({ '_id': _id }, {'$set': doc})
        return jsonify({'result': 'success', 'msg': '수정 완료!'})
    else:
        return jsonify({'result': 'fail', 'msg': '수정 실패! 아이디가 일치하지 않습니다.'})