YOUTUBE_URL='https://www.youtube.com/watch?v=0jnojoBWOdo'
import random
import youtube_dl
import ffmpy
import os
from common import DATA_PATH 

TEST_VIDEOS = DATA_PATH + 'testvideos/'
def download_video(url,folder_path):
    """ Use youtube_dl to download the video from youtube in mp4 format and return the filepath.
    Like: youtube-dl -f 22 https://www.youtube.com/watch?v=0jnojoBWOdo --output='test.mp4'

    Arguments: 
    url -- Youtube video url to be downloaded
    folder_path -- Absolute path where the video needs to be downloaded. 
                A video file with naming video_[random number] would be created at that location.
                
    """
    video_path = folder_path + 'video_' + str(random.randint(1, 1000000))+'.mp4'
    ydl_opts = {'outtmpl': video_path, 'format': '22'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print('Video downloaded to ' + video_path)
    return video_path

def video_to_frames(video_path):
    """ Breakes video at the location video_path into frames and returns the directory path of pngs
    The directory would be video file name without extension. Fails if there exists such directory with content.
    Like: ffmpeg -i adobe.webm -vcodec png adobe/%04d.png
    """
    png_folder = video_path[:video_path.index('.')]
    if os.path.exists(png_folder):
        os.removedirs(png_folder)
    os.mkdir(png_folder)
    
    ff = ffmpy.FFmpeg(
    inputs={video_path: None},
    outputs={png_folder + '/%04d.png': '-vcodec png'})
    ff.run()    
    return png_folder
