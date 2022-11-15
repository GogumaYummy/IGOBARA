from flask import Flask, render_template
from api import login

app = Flask(__name__)

app.register_blueprint(login.login_api) # login.py 파일의 login_api 블루프린트를 연결해줍니다.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
