from flask import Flask, render_template
from api import articles, login_join, test # api 폴더의 파일을 가져옵니다.

app = Flask(__name__)

app.register_blueprint(login_join.login_api) # login.py 파일의 login_api 블루프린트를 연결해줍니다.
app.register_blueprint(test.test_api)
app.register_blueprint(articles.post_api)

@app.route('/')
def index():
    user_info = login_join.check_login()
    result = user_info['result']

    if(user_info['result'] == 'success'):
        userId = user_info['id']
        nick = user_info['nick']

        return render_template('index.html', result = result, userId = userId, nick = nick)
    else:
        msg = user_info['msg']

        return render_template('index.html', result = result, msg = msg)

@app.route('/article/<id>')
def article(id):
    user_info = login_join.check_login()
    result = user_info['result']
    articleId = id

    if(user_info['result'] == 'success'):
        userId = user_info['id']
        nick = user_info['nick']

        return render_template('post.html', result = result, userId = userId, nick = nick, articleId = articleId)
    else:
        msg = user_info['msg']

        return render_template('post.html', result = result, msg = msg, articleId = articleId)

@app.route('/login')
def login():
    user_info = login_join.check_login()
    result = user_info['result']

    if(user_info['result'] == 'success'):
        userId = user_info['id']
        nick = user_info['nick']

        return render_template('login.html', result = result, userId = userId, nick = nick)
    else:
        msg = user_info['msg']

        return render_template('login.html', result = result, msg = msg)



@app.route('/write')
def write():
    return render_template('write.html')

if __name__ == '__main__':    app.run('0.0.0.0', port=5000, debug=True)
