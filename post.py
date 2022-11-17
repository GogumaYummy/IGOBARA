from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import certifi
# 여기서 사용한 패키지는 app.py에서 다시 불러올 필요가 없습니다.

ca = certifi.where()

client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

post_api = Blueprint("post", __name__, url_prefix="/api") # Blueprint("블루프린트 이름", __name__, url_prefix="/경로")로 새 블루프린트를 만듭니다.

@post_api.route('/api/write', methods=["POST"]) #게시글 등록 
def write():
    
    title = request.form['title_give']

    content = request.form['content_give']
    print(title, content)

    return jsonify({'msg': '가입을 환영합니다!', 'state': 1})