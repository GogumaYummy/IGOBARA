from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from bson.objectid import ObjectId
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


@post_api.route('/delete', methods=["POST"])
def delete():
    id = request.form['_id']
    result = db.post.delete_one({"_id" : id})
    return jsonify({'msg': '삭제완료'})