from flask import request, jsonify, Blueprint
from pymongo import MongoClient
import certifi, jwt, datetime, hashlib

ca = certifi.where()

client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'IGO_BARA' #JWT토큰 생성시 필요

login_api = Blueprint("login", __name__, url_prefix="/api")

@login_api.route('/idcheck', methods=["POST"]) #아이디 중복 체크
def idcheck():
    id_receive = request.form['id_give']
    user = db.users.find_one({'id': id_receive})
    
    if(user != None): return jsonify({'msg': '이미 사용 중인 아이디입니다.', 'state': 0})
    else: return jsonify({'msg': '사용 가능한 아이디입니다.', 'state': 1})

@login_api.route('/nickcheck', methods=["POST"]) #닉네임 중복 체크
def nickcheck():
    nick_receive = request.form['nick_give']
    user = db.users.find_one({'nick': nick_receive})
    
    if(user != None): return jsonify({'msg': '이미 사용 중인 닉네임입니다.', 'state': 0})
    else: return jsonify({'msg': '사용 가능한 닉네임입니다.', 'state': 1})

@login_api.route('/join', methods=["POST"]) #비밀번호 체크 및 회원가입 진행
def join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwc_receive = request.form['pwc_give']
    nick_receive = request.form['nick_give']

    if(len(pw_receive) < 12):
        return jsonify({'msg': '비밀번호는 12자 이상이어야 합니다.', 'state': 0})
    if(pw_receive != pwc_receive):
        return jsonify({'msg': '비밀번호와 비밀번호 재확인이 일치하지 않습니다.', 'state': 0})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash,
        'nick': nick_receive
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '가입을 환영합니다!', 'state': 1})

@login_api.route('/login', methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'nick': result['nick'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'state': 1, 'token': token})
    else:
        return jsonify({'msg': '아이디/비밀번호가 일치하지 않습니다.', 'state': 0})