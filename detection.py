import time

import numpy as np
import tensorflow as tf
from PIL import Image

# Path to frozen detection graph. This is the model retrained on text data
PATH_TO_CKPT = './weights/frozen_inference_graph.pb'

DEFAULT_SCORE_THRESHOLD=0.8

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
    

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def decode_box_coordinates(image, file_boxes):
    width, height = image.size
    new_boxes = []
    for box in file_boxes:
        #print("box" + str(box))
        ymin = box[0] * height
        xmin = box[1] * width
        ymax = box[2] * height
        xmax = box[3] * width
        new_boxes.append((xmin,ymin,xmax,ymax))
    return new_boxes

@timefunc
def detect(image_path, score_threshold = DEFAULT_SCORE_THRESHOLD):
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            image = Image.open(image_path)
            image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (file_boxes, file_scores, file_classes, file_num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
            #return boxes, scores, classes, num

            top_box_indices = file_scores[0] > score_threshold
            
            file_boxes = file_boxes[0][top_box_indices]
            new_file_boxes = decode_box_coordinates(image, file_boxes)
            
            file_scores = file_scores[0][top_box_indices]
            
            return new_file_boxes, file_scores
