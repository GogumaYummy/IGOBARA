from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from datetime import datetime
from . import login_join
from config import pymongo
import math
# 여기서 사용한 패키지는 app.py에서 다시 불러올 필요가 없습니다.

post_api = Blueprint("post", __name__, url_prefix="/api")

@post_api.route('/articles')
def get_articles():
    page = int(request.args.get('page', default = '0', type = str))
    max_page = math.ceil(pymongo.db.articles.count_documents({}) / 30)

    articles = list(pymongo.db.articles.find({}, {}).sort("createdAt", -1).skip((page - 1) * 30).limit(30))

    decoded_articles = list()
    for article in articles:
        new_article = article
        new_article['_id'] = str(new_article['_id'])
        new_article['postedByNick'] = pymongo.db.users.find_one({'id': new_article['postedBy']})['nick']
        decoded_articles.append(new_article)

    return jsonify({'articles': decoded_articles, 'max_page': max_page})

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
    article = pymongo.db.articles.find_one({ '_id' : _id }, {"_id": 0, "postepymongo.dby": 1})
    posted_by = article['postepymongo.dby']

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
        'postepymongo.dby': user_id,
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
    article = pymongo.db.articles.find_one({ '_id' : _id }, {"_id": 1, "postepymongo.dby": 1})
    posted_by = article['postepymongo.dby']

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