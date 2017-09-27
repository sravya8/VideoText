from datetime import datetime
import os

from tqdm import tqdm
import json
from PIL import Image
import glob
from tempfile import TemporaryDirectory

import utilities
import detection
import recognition

import importlib
importlib.reload(utilities)
importlib.reload(detection)

def process_inputframes(frames_path, nth=1, duration=10):
    frame_files = sorted(glob.glob(frames_path + '/*'))
    num_frames = len(frame_files)
    print('Detecting and recognizing text from {} frames for every {}th frame: {}'.format(num_frames, nth, str(datetime.now())))

    entries = []
    for f_index, filename in tqdm(enumerate(frame_files), total=num_frames):            
        if(f_index%nth == 0):
            boxes, scores = detection.detect(filename)

            if scores.shape[0] != 0:
                texts = recognition.recognize(filename, boxes)
                for index, box in enumerate(boxes):  
                    entry = {}
                    entry['f_index'] = f_index
                    entry['time_stamp'] = '{:2.2f}'.format(f_index/num_frames * duration)
                    entry['text'] = texts[index]
                    entry['bbox'] = [box[0], box[1], 
                                     box[2]-box[0], box[3]-box[1]]
                    entry['score'] = scores[index].item()
                    entries.append(entry)
    return entries

def get_json(url, nth=1, from_time="00:05", duration=10):
    """ Finds text within a youtube video and returns results in the form of json. 
        Restricts the video length to 1 minute, by default processes only 10 seconds to save resources on the demo server.
        Arguments:
        url: Youtube url of the video to be processed
        nth: Run inference for every nth frame [default=1]
        from_time: Split video from minutes:seconds [default=00:05]
        duration: duration of the video in seconds [default=10]

        Returns results in json format, each entry contains:
            f_index: frame index
            time_stamp: time_stamp of the frame
            bbox: cordinates of the bounding box where text is found [xmin, ymin, width, height]
            text: text transcription        
        
        """
    with TemporaryDirectory() as temp_dir:
        #Create temp files and folders
        input_video_path = temp_dir + '/input.mp4'
        input_frames_path = temp_dir + '/in_frames'
        os.mkdir(input_frames_path)

        utilities.download_video(url, input_video_path)
        utilities.get_frames(input_video_path, input_frames_path, temp_dir, from_time, duration)

        entries= process_inputframes(input_frames_path, nth, duration)
        return json.dumps(entries)


def infer_save_frames(input_frames_path, out_frames_path, every_nth=1):
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
    
def save_video(url, path, nth=1, from_time="00:05", duration=10):
    """ Finds text from a youtube video and saves a processed video with overlayed bounding boxes and text
        Restricts the video length to 1 minute, by default processes only 10 seconds to save resources on the demo server.
        Arguments:
        url: Youtube url of the video to be processed
        nth: Run inference for every nth frame [default=1]
        path: path to store the processed video with overlayed boxes and text
        from_time: Split video from minutes:seconds [default=00:05]
        duration: duration of the video in seconds [default=10]        
        """
    with TemporaryDirectory() as temp_dir:
        #Create temp files and folders
        input_video_path = temp_dir + '/input.mp4'
        input_frames_path = temp_dir + '/in_frames'
        output_frames_path = temp_dir + '/out_frames'
        os.mkdir(input_frames_path)
        os.mkdir(output_frames_path)

        utilities.download_video(url, input_video_path)
        utilities.get_frames(input_video_path, input_frames_path, temp_dir, from_time, duration)        
        out_path = infer_save_frames(input_frames_path, output_frames_path, every_nth=4)

        # Stitch the video and show
        output_frames = output_frames_path + '/out_%04d.png'
        utilities.build_video(output_frames, path)
        
        
# TODO:from_time 00:00 does not seem to be working
