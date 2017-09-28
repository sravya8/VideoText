import videotext
#import sys
import uuid
from flask import Flask,  request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    #print('In post', file=sys.stderr)
    url = request.form["url"]
    start = request.form["start"]
    seconds = request.form["seconds"]
    path = 'static/{}.mp4'.format(str(uuid.uuid4()))
    videotext.save_video(url, path, from_time=start, duration=seconds)

    return render_template('index.html', video_path=path)