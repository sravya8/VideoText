import time
import datetime
import os
import glob
from video_utils import download_video, video_to_frames
from common import DATA_PATH

TEST_VIDEOS = DATA_PATH + 'testvideos/'
YOUTUBE_URL='https://www.youtube.com/watch?v=0jnojoBWOdo'


def test_download_video():
    start = time.time()
    VIDEO_PATH = download_video(YOUTUBE_URL, TEST_VIDEOS)
    end = time.time()
    assert os.path.exists(VIDEO_PATH) == 1
    print(VIDEO_PATH + ' exists')
    print('Youtube video download time: ' + str(datetime.timedelta(seconds=end - start)))

def test_video_to_frames():

    videos = glob.glob(TEST_VIDEOS+'*')
    assert videos[0] is not None
    start = time.time()
    png_folder = video_to_frames(videos[0])
    end = time.time()
    assert os.path.exists(png_folder) == 1
    print(png_folder + ' exists')
    num_pngs = len(glob.glob(png_folder+'/*'))
    print(str(num_pngs) + ' frames created at ' + png_folder)
    assert num_pngs > 1   
    print('Time taken to break into frames: ' + str(datetime.timedelta(seconds=end - start)))

test_download_video()
test_video_to_frames()
