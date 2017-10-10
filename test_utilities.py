import time
import datetime
import os
import glob
from tempfile import TemporaryDirectory

import utilities

YOUTUBE_URL='https://www.youtube.com/watch?v=0jnojoBWOdo'


def test_video_utils():
    with TemporaryDirectory() as tempdir:
        path = tempdir + '/test.mp4'
        
        start = time.time()
        utilities.download_video(YOUTUBE_URL, path)
        end = time.time()
        
        assert os.path.exists(path) == 1
        print(path + ' exists')
        print('Youtube video download time: ' + str(datetime.timedelta(seconds=end - start)))

        output_frames_path = tempdir + '/frames'
        os.mkdir(output_frames_path)
        
        start = time.time()
        utilities.get_frames(path, output_frames_path, tempdir, from_time='00:00', duration=5)
        end = time.time()
        
        assert os.path.exists(output_frames_path) == 1
        print(output_frames_path + ' exists')
        num_pngs = len(glob.glob(output_frames_path+'/*'))
        print(str(num_pngs) + ' frames created at ' + output_frames_path)
        assert num_pngs > 1   
        print('Time taken to break into frames: ' + str(datetime.timedelta(seconds=end - start)))