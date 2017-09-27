This work is based on [Tensorflow's object detection models](https://github.com/tensorflow/models/tree/master/research/object_detection) and the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

In this work, we leverage detection models trained on coco dataset for detecting text in natural images.

We have modified config files for two models in this directory:
1. faster_rcnn_resnet101_pets_coco.config
2. ssd_mobilenet_v1_coco.config

Frozen model checkpoint trained on coco-text and minimally augmented with custom text images is stored as frozen_inference_graph.pb (Will add google drive link)

Script used to generate TF records for use with this model is at [coco-text/Coco-Text%20to%20TFRecords.ipynb](../coco-text/Coco-Text%20to%20TFRecords.ipynb)

For training:
Please follow instructions provided by [Tensorflow's object detection](https://github.com/tensorflow/models/tree/master/research/object_detection) along with scripts and configs provided in this folder.