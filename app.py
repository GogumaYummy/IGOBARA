from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://igobara:221114@cluster0.pmylkqu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'IGO_BARA' #JWT토큰 생성시 필요

import jwt, datetime, hashlib


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/idcheck', methods=["POST"])
def idcheck():
    id_receive = request.form['id_give']
    user = db.users.find_one({'id': id_receive})
    
    if(user != None): return jsonify({'msg': '이미 사용 중인 아이디입니다.', 'state': 0})
    else: return jsonify({'msg': '사용 가능한 아이디입니다.', 'state': 1})

@app.route('/api/nickcheck', methods=["POST"])
def nickcheck():
    nick_receive = request.form['nick_give']
    user = db.users.find_one({'nick': nick_receive})
    
    if(user != None): return jsonify({'msg': '이미 사용 중인 닉네임입니다.', 'state': 0})
    else: return jsonify({'msg': '사용 가능한 닉네임입니다.', 'state': 1})

@app.route('/api/join', methods=["POST"])
def join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwc_receive = request.form['pwc_give']
    nick_receive = request.form['nick_give']\

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
