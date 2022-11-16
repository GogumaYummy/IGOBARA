from flask import Blueprint, jsonify, request
import datetime, math
from config import pymongo

test_api = Blueprint("test_api", __name__, url_prefix="/test")

@test_api.route('/dummyarticles', methods=['POST'])
def create_dummy_articles():
    for i in range(100):
        doc = {
            'postedBy': 'ㅇ',
            'title': str(i) + '번째 게시글',
            'content': '내용',
            'image': 'https://cdn.travie.com/news/photo/first/201710/img_19975_1.jpg',
            'createdAt': datetime.datetime.now()
        }
        pymongo.db.articles.insert_one(doc)

    return jsonify({'msg': 'success'})

@test_api.route('/articles')
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