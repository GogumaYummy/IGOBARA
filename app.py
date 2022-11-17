from flask import Flask, render_template
from api import post

app = Flask(__name__)

app.register_blueprint(post.post_api)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write')
def write():
    return render_template('write.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
