import glob
import sys
from PIL import Image
from datetime import datetime
import time
from tqdm import tqdm
import os

import utilities
import detection
import recognition
import importlib
#importlib.reload(utilities)
#importlib.reload(detection)
#sys.path.append("crnn.pytorch")

OUT_DIR='/home/sravya/data/muse/out/'

def prep_frames(video_url=None, video_path=None, from_time='00:10', duration=10):
    if(video_path is None and video_url is None):
        print("Please provide either video_path or video_url")
    if(video_path is None):
        video_path = utilities.download_video(video_url)

    frames_path = utilities.get_frames(video_path, from_time, duration)
    return frames_path

def infer(frame_files, every_nth=1):
    num_frames = len(frame_files)
    detect_time = 0
    recognize_time = 0
    print('Detecting and recognizing text from {} frames: {}'.format(num_frames, str(datetime.now())))
    wordBB = None
    score = None
    text = None
        
    for index, filename in tqdm(enumerate(frame_files), total=num_frames):
        out_name = OUT_DIR + 'out_{0:04d}.png'.format(index)
        if(index%every_nth == 0):
            wordBB, score = detection.detect(filename)

            if score.shape[0] == 0:
                wordBB = None
                score = None
            else:
                text = recognition.recognize(filename, wordBB)
                        
        utilities.save(filename, wordBB, text, out_name)   
    return OUT_DIR

def infer_video_save(url, path):
    print('In video save', file=sys.stderr)
    frames_path = prep_frames(url,from_time="01:25", duration=5)
    frame_files = sorted(glob.glob(frames_path + '/*'))

    out_path = infer(frame_files=frame_files, every_nth=4)

    # Stitch the video and show
    input_files = out_path + 'out_%04d.png'
    video_file_path = utilities.build_video(input_files, path)