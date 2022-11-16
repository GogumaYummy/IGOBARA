from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import certifi, jwt, datetime, hashlib
# 여기서 사용한 패키지는 app.py에서 다시 불러올 필요가 없습니다.

ca = certifi.where()

client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'IGO_BARA' #JWT토큰 생성시 필요

post_api = Blueprint("post", __name__, url_prefix="/postapi") #

@post_api.route('/post', methods=["POST"])
def post():
    print('서버실행')
    id = request.form['_id']
    print(id)
    result = db.post.find_one({"_id" : id})
    return jsonify({'result': result})

@post_api.route('/delete', methods=["POST"])
def delete():
    id = request.form['_id']
    result = db.post.delete_one({"_id" : id})
    return jsonify({'msg': '삭제완료'})