import time
import datetime
import sys
import uuid
import argparse

from flask import Flask,  request, render_template
app = Flask(__name__)

import videotext

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    #print('In post', file=sys.stderr)
    path = 'static/{}.mp4'.format(str(uuid.uuid4()))
    
    url = request.form["url"]
    start_min = int(request.form["start_min"])
    start_sec = int(request.form["start_sec"])
    seconds = int(request.form["seconds"])
            
    if(start_min<0 or start_sec<0 or start_sec>59):
        result_string="Please correct the start time"
    elif(seconds>59 or seconds<5):
        result_string="Please correct the duration seconds. It should be in between 5 and 59 seconds "       
    else:  
        
        start_time = '{0:02d}:{1:02d}'.format(start_min,start_sec)
        print('In post start:{}'.format(start_time), file=sys.stderr)

        start = time.time()
        videotext.save_video(url, path, from_time=start_time, duration=seconds)
        end = time.time()
        result_string = 'Time taken: {}'.format(str(datetime.timedelta(seconds=end - start)))
    return render_template('index.html', video_path=path, result_string = result_string)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, type=int)
    #parser.add_argument('--checkpoint-path', default=checkpoint_path)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    #checkpoint_path = args.checkpoint_path

    #if not os.path.exists(args.checkpoint_path):
    #    raise RuntimeError(
    #        'Checkpoint `{}` not found'.format(args.checkpoint_path))

    app.debug = args.debug
    app.run('0.0.0.0', args.port)

if __name__ == '__main__':
    main()
