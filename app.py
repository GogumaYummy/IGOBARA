from flask import Flask, render_template, jsonify
from api import login_join # api 폴더의 login.py 파일을 가져옵니다.

app = Flask(__name__)

app.register_blueprint(login_join.login_api) # login.py 파일의 login_api 블루프린트를 연결해줍니다.

@app.route('/')
def index():
    user_info = login_join.check_login()
    print(user_info)

    if(user_info['result'] == 'success'):
        return render_template('index.html', id = user_info['id'], nick = user_info['nick'])
    else:
        return render_template('index.html', msg = user_info['msg'])


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
