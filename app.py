from flask import Flask, render_template
from api import login_join # api 폴더의 login.py 파일을 가져옵니다.

app = Flask(__name__)

app.register_blueprint(login_join.login_api) # login.py 파일의 login_api 블루프린트를 연결해줍니다.

def render(template):
    user_info = login_join.check_login()
    result = user_info['result']

    if(user_info['result'] == 'success'):
        id = user_info['id']
        nick = user_info['nick']

        return render_template(template, result = result, id = id, nick = nick)
    else:
        msg = user_info['msg']

        return render_template(template, result = result, msg = msg)


@app.route('/')
def index():
    return render('index.html')


@app.route('/login')
def login():
    return render('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
