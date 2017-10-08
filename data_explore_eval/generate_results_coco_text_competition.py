#One file per image, in each file, one line per word containing
#Task 1: left_1,top_1,right_1,bottom_1,score_1
#Task 3: left_1,top_1,right_1,bottom_1,score_1,recognition_1

#Task 2: filenum, word; single file submission

import os
import shutil
import sys

from PIL import Image
from tqdm import tqdm
import glob

sys.path.append('coco-text')
import coco_text

sys.path.append('..')
from VideoText import detection, recognition

COCO_DATA='/home/sravya/data/muse/coco/coco2014/'
COCO_WORDS_TEST='/home/sravya/data/muse/coco/cocotextwords/test/'
INPUT_PATH = COCO_DATA + 'train2014/'
TASK1_PATH = COCO_DATA + 'task1/'
TASK2_PATH = COCO_DATA + 'task2/'
TASK3_PATH = COCO_DATA + 'task3/'
VAL_RESULT = 'val_results/'
TEST_RESULT = 'test_results/'

def build_result_name(filename):
    img_num = int(filename.split('_')[-1].split('.')[0])
    return 'res_{}.txt'.format(img_num)
   
def coco_competition_result(imgs, path, task1_path, task3_path, score_threshold):
    skipped_files = []
    for img in tqdm(imgs):
        img_results = []
        bboxes = None
        texts = None
        filename = img['file_name']
        task1_filename = task1_path + build_result_name(filename)
        task3_filename = task3_path + build_result_name(filename)
        task1_f = open(task1_filename, 'w')
        task3_f = open(task3_filename, 'w')
        try:
            file_path = path + filename
            bboxes, scores = detection.detect(file_path, score_threshold)

            if scores.shape[0] == 0:
                bboxes = None
                score = None
            else:
                texts = recognition.recognize(file_path, bboxes)
        except:
            print('Skipped ' + file_path)
            skipped_files.append(filename)
        if bboxes is not None:
            for index, bbox in enumerate(bboxes):
                result = '{},{},{},{},{}'.format(int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), round(scores[index], 2))            
                print(result, file=task1_f) 
                result = '{},{}'.format(result, texts[index])
                print(result, file=task3_f)                 
        task1_f.close()
        task3_f.close()

    print(skipped_files)
    
def coco_competition_result_task2(img_paths, out_path):
    
    task2_f = open(out_path, 'w')  
    
    for img_path in tqdm(img_paths):
        raw_pred, text = recognition.recognize_cropped(Image.open(img_path))
        file_num = img_path.split('/')[-1].split('.')[0]
        result = '{},{}'.format(file_num, text)
        print(result, file=task2_f)                     
    task2_f.close()

def force_mkdirs(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    
ct = coco_text.COCO_Text(COCO_DATA+ 'COCO_Text.json')
#force_mkdirs(TASK1_PATH)
#force_mkdirs(TASK3_PATH)

thresholds = [0.6, 0.0]

for threshold in thresholds:
    path = str(int(threshold*100)) + VAL_RESULT
    print('Preparing validation results for Task 1 at {}\n Task 3 at {}'.format(
        TASK1_PATH + path, TASK3_PATH+ path))
    force_mkdirs(TASK1_PATH + path)
    force_mkdirs(TASK3_PATH + path)
    valid_img_ids = ct.getImgIds(imgIds=ct.val)
    valid_imgs = ct.loadImgs(valid_img_ids)
    coco_competition_result(valid_imgs, INPUT_PATH, TASK1_PATH + path, 
                            TASK3_PATH + path, threshold)

    path = str(int(threshold*100)) + TEST_RESULT

    print('Preparing test results for Task 1 at {}\n Task 3 at {}'.format(
        TASK1_PATH + path, TASK3_PATH+ path))
    force_mkdirs(TASK1_PATH + path)
    force_mkdirs(TASK3_PATH + path)
    test_img_ids = ct.getImgIds(imgIds=ct.test)
    test_imgs = ct.loadImgs(test_img_ids)
    coco_competition_result(test_imgs, INPUT_PATH, TASK1_PATH + path,
                                  TASK3_PATH + path, threshold)
   
      
print('Preparing test results for Task 2 at ' + TEST_RESULT_PATH)
force_mkdir(TASK2_PATH)
task2_test_img_paths = glob.glob(COCO_WORDS_TEST+'*')
out_path = TASK2_PATH + 'result.txt'
coco_competition_result_task2(img_paths, out_path)
