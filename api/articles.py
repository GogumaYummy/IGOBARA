from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from . import login_join
import certifi
# 여기서 사용한 패키지는 app.py에서 다시 불러올 필요가 없습니다.

ca = certifi.where()

client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

post_api = Blueprint("post", __name__, url_prefix="/api")


@post_api.route('/article/<id>')
def post(id):
    _id = ObjectId(id)
    result = db.articles.find_one({ '_id' : _id })
    result['_id'] = str(result['_id'])

    return jsonify({'result': result })


@post_api.route('/article/<id>', methods=["DELETE"])
def delete(id):
    user_data = login_join.check_login()
    user_id = user_data['id']

    _id = ObjectId(id)
    article = db.articles.find_one({ '_id' : _id }, {"_id": 0, "postedBy": 1})
    posted_by = article['postedBy']

    if (user_id == posted_by):
        db.articles.delete_one({"_id" : _id})
        return jsonify({'result': 'success', 'msg': '삭제 완료!'})
    else:
        return jsonify({'result': 'fail', 'msg': '삭제 실패! 아이디가 일치하지 않습니다.'})
