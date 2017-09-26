import infer
import sys
import uuid
from flask import Flask,  request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    print('In post', file=sys.stderr)
    url = request.form["url"]
    path = 'demo_videos/{}.mp4'.format(str(uuid.uuid4()))
    infer.infer_video_save(url, path)
    return render_template('index.html', video_path=path)