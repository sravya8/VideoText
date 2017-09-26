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
from tempfile import TemporaryDirectory
#importlib.reload(utilities)
#importlib.reload(detection)
#sys.path.append("crnn.pytorch")

def infer(input_frames_path, out_frames_path, every_nth=1):
    frame_files = sorted(glob.glob(input_frames_path + '/*'))

    num_frames = len(frame_files)
    detect_time = 0
    recognize_time = 0
    print('Detecting and recognizing text from {} frames: {}'.format(num_frames, str(datetime.now())))
    wordBB = None
    score = None
    text = None
        
    for index, filename in tqdm(enumerate(frame_files), total=num_frames):
        out_name = out_frames_path + '/out_{0:04d}.png'.format(index)
        if(index%every_nth == 0):
            wordBB, score = detection.detect(filename)

            if score.shape[0] == 0:
                wordBB = None
                score = None
            else:
                text = recognition.recognize(filename, wordBB)
                        
        utilities.save(filename, wordBB, text, out_name)   

                
#TODO: Take start time and duration as inputs
def infer_video_save(url, path, from_time="01:25", duration=5):
    with TemporaryDirectory() as temp_dir:
        #Create temp files and folders
        input_video_path = temp_dir + '/input.mp4'
        output_video_path = path
        input_frames_path = temp_dir + '/in_frames'
        output_frames_path = temp_dir + '/out_frames'
        os.mkdir(input_frames_path)
        os.mkdir(output_frames_path)

        utilities.download_video(url, input_video_path)

        utilities.get_frames(input_video_path, input_frames_path, temp_dir, from_time, duration)
        
        out_path = infer(input_frames_path, output_frames_path, every_nth=4)

        # Stitch the video and show
        output_frames = output_frames_path + '/out_%04d.png'
        utilities.build_video(output_frames, output_video_path)
        return output_video_path