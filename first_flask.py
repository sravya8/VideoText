import infer
import sys
from flask import Flask,  request, render_template
app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello, World!'

@app.route('/')
def index():
    return render_template('index.html', session_id='dummy_session_id')


@app.route('/', methods=['POST'])
def index_post():
    print('In post', file=sys.stderr)
    url = request.form["url"]
    path = 'static/test.mp4'
    infer.infer_video_save(url, path)
    return render_template('index.html', video_path=path)