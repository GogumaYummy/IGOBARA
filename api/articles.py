from flask import Blueprint, jsonify
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

test_api = Blueprint("test_api", __name__, url_prefix="/test")

@test_api.route('/dummyarticles', methods=['POST'])
def create_dummy_articles():
    for i in range(100):
        doc = {
            'postedBy': 'ㅇ',
            'title': str(i) + '번째 게시글',
            'content': '내용',
            'image': 'https://cdn.travie.com/news/photo/first/201710/img_19975_1.jpg'
        }
        db.articles.insert_one(doc)

    return jsonify({'msg': 'success'})