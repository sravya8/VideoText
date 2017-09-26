DATA_PATH='/home/sravya/data/muse/'
TEST_VIDEOS = DATA_PATH + 'testvideos/'

import youtube_dl, random
import ffmpy
import os
import matplotlib.pyplot as plt
import io
import base64
from IPython.display import HTML
import time
from PIL import Image
#import matplotlib
#matplotlib.use('Agg')
plt.switch_backend('agg')

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

def download_video(url,path):
    """ Use youtube_dl to download the video from youtube in mp4 format and return the filepath.
    Like: youtube-dl -f 22 https://www.youtube.com/watch?v=0jnojoBWOdo --output='test.mp4'

    Arguments: 
    url -- Youtube video url to be downloaded
    folder_path -- Absolute path where the video needs to be downloaded. 
                A video file with naming video_[random number] would be created at that location.
                
    """
    ydl_opts = {'outtmpl': path, 'format': '22'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print('Video downloaded to ' + path)

def split_video(input_path, output_path, from_time, duration):
    """ from_time in minutes:seconds, example 01:10 for one minute ten seconds
        duration in seconds, for example 10"""
    #'-ss 00:00:15.00 -t 00:00:10.00 -c:v copy -c:a copy'
    parameters = '-ss 00:{}.00 -t 00:00:{}.00 -c:v copy -c:a copy'.format(from_time, duration)
    ff = ffmpy.FFmpeg(
    inputs={input_path: None},
    outputs={output_path: parameters})
    ff.run()
    print('Splitted video starting from {}, duration: {} seconds'.format(from_time, duration))
  
def get_frames(input_video_path, output_frames_path, temp_dir, from_time, duration):
    """ Breakes video at the location video_path into frames and returns the directory path of pngs
    The directory would be video file name without extension. Fails if there exists such directory with content.
    Like: ffmpeg -i adobe.webm -vcodec png adobe/%04d.png
    """
    split_video_path = temp_dir + '/temp.mp4'
    
    split_video(input_video_path, split_video_path, from_time, duration)
    
    output_params = '-vcodec png'
    #output_params = '-vcodec png -r {}'.format(fps)
    
    ff = ffmpy.FFmpeg(
    inputs={split_video_path: None},
    outputs={output_frames_path + '/%04d.png': output_params})
    ff.run()
    print('Frames created at {}'.format(output_frames_path))

def build_video(input_files, output_file):
    ff = ffmpy.FFmpeg(
        inputs={input_files: None},
        outputs={output_file: '-pix_fmt yuv420p'})
    ff.run()
    return output_file

@timefunc
def visualize(image_path, boxes, texts, out_path=None):
    image = Image.open(image_path)
    #plt.clf()
    plt.imshow(image)

    if boxes is not None:
        for index in list(range(len(boxes))):
            box = boxes[index]
            xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
            x = xmin, xmax, xmax, xmin, xmin
            y = ymin, ymin, ymax, ymax, ymin
            plt.plot(x, y, 'g', alpha=0.8)
            # visualize the indiv vertices:
            #vcol = ['r','g','b','k']
            #for j in range(4):
            #    plt.scatter(x[j],y[j],color=vcol[j])  
            plt.text(xmin, ymin, texts[index].strip(), color='b', fontsize=15)#bbox={'facecolor':'white', 'alpha':0.5, 'pad':0})
    if out_path is not None:
        plt.savefig(out_path)
        #plt.close(fig)
    else:
        plt.show()    

def save(image_path, boxes, texts, out_path):
    visualize(image_path, boxes, texts, out_path)    
    
def play_video(path):
    video = io.open(path, 'r+b').read()
    encoded = base64.b64encode(video)
    return HTML(data='''<video alt="test" controls>
                <source src="data:video/mp4;base64,{0}" type="video/mp4" />
             </video>'''.format(encoded.decode('ascii')))