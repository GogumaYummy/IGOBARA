from flask import Flask, render_template, redirect
from api import articles, login_join # api 폴더의 파일을 가져옵니다.

app = Flask(__name__)

app.register_blueprint(login_join.login_api) # login.py 파일의 login_api 블루프린트를 연결해줍니다.
app.register_blueprint(articles.post_api)

# GET / 요청에 대한 메인 페이지 응답
@app.route('/')
def index():
    user_info = login_join.check_login() # check_login() 함수로 요청에 담긴 쿠키 복호화 후 내용을 저장
    result = user_info['result'] # 쿠키 복호화 결과를 따로 저장

    if(result == 'success'): # 결과가 성공일 때 유저 id와 닉네임을 담아 index.html 렌더
        userId = user_info['id']
        nick = user_info['nick']
        return render_template('index.html', result = result, userId = userId, nick = nick)
    else: # 실패일 때는 실패 메세지를 담아 index.html 렌더
        msg = user_info['msg']
        return render_template('index.html', result = result, msg = msg)


# GET /article/{id} 요청에 대한 게시글 상세 페이지 응답
@app.route('/article/<article_id>') # 보려는 게시글의 id를 uri 마지막에 파라미터로 전달
def article(article_id): # 전달받은 파라미터를 article_id 매개변수에 담아 호출
    user_info = login_join.check_login()
    result = user_info['result']

    if(result == 'success'):
        userId = user_info['id']
        nick = user_info['nick']
        return render_template('post.html', result = result, userId = userId, nick = nick, articleId = article_id)
    else:
        msg = user_info['msg']
        return render_template('post.html', result = result, msg = msg, articleId = article_id)


# GET /login 요청에 대한 로그인/회원가입 페이지 응답
@app.route('/login')
def login():
    user_info = login_join.check_login()
    result = user_info['result']

    if(result == 'success'):
        userId = user_info['id']
        nick = user_info['nick']
        return render_template('login.html', result = result, userId = userId, nick = nick)
    else:
        msg = user_info['msg']
        return render_template('login.html', result = result, msg = msg)


# GET /write 요청에 대한 게시글 작성 페이지 응답 또는 메인 페이지로 리디렉트
@app.route('/write')
def write():
    user_info = login_join.check_login()
    result = user_info['result']

    if(result == 'success'):
        userId = user_info['id']
        nick = user_info['nick']
        return render_template('write.html', result = result, userId = userId, nick = nick)
    else:
        return redirect('/') # 로그인이 되어있지 않으면 메인 페이지로 리디렉트


# GET /rewrite 요청에 대한 게시글 수정 페이지 응답 또는 메인 페이지로 리디렉트
@app.route('/rewrite/<article_id>')
def rewrite(article_id):
    user_info = login_join.check_login()
    result = user_info['result']

    if(result == 'success'):
        userId = user_info['id']
        nick = user_info['nick']
        return render_template('rewrite.html', result = result, userId = userId, nick = nick, articleId = article_id)
    else:
        return redirect('/')


# 로컬호스트의 5000 포트에서 서버 실행
if __name__ == '__main__':    app.run('0.0.0.0', port=5000, debug=True)
