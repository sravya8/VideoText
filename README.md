# Video Text Detection and Recognition

This software implements an end to end pipiline to detect and recognize text from youtube videos. The text detection is based on 
[SSD: Single Shot MultiBox Detector](https://arxiv.org/pdf/1512.02325.pdf) retrained on single text class using [Coco-Text](https://vision.cornell.edu/se3/coco-text-2/) dataset and text recognition is based on CRNN network as described in [An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition](https://arxiv.org/pdf/1507.05717.pdf) 

![Demo](static/tennis.gif "Demo")

Please see Demo notebook as a starting point. Use it to provide your youtube url to either:
1. Generate a new video with overlayed bounding boxes for all text and their respective transcriptions.
2. Get text detection/recognition results in JSON format

Directory structure:
- Demo.ipynb: Demo notebook as described above
- videotext.py: Main functionality for this project
- detection.py and detection: detection.py holds helper functions for detection task. Loads Tensorflow inference graph trained seperately using Tensorflow objection detection models on text data. We use ssd_mobile network as it is the fastest among available models. See README.md in detection folder for more details.
- recognition.py and crnn.pytorch: recognition.py holds helper functions for recognition task. Loads pytorch model and infers. See crnn.pytorch folder for more details. It contains Pytorch implementation of CRNN for text recognition on cropped natural images.
- utilities.py: Holds all other helper functions required for E2E video text detection and recognition.

- coco-text: Helper functions to work with Coco-Text data. Also contains Coco-Text Preparation notebook to translate coco-text to TFRecord to use with Tensorflow detection model.
- Eval_Coco_text_val_set.ipynb: Contains code to evaluate our model on coco-text benchmark

- synth_utils.py: Helper script to prepare SynthText data
- SynthText Data Preparation notebook[In progress]: Scripts to translate Synthetext data to TFrecord to be used with Tensorflow detection model

Web server:
- flask_server.py - Contains basic flask app
- templates - Contains html for flask app
- static - Holds demo videos

Pre-trained weights:
Download from [Google drive](https://drive.google.com/drive/folders/0B2zzsNPEVylSYmUwTnYweXpkZ00?usp=sharing) and put it into a folder named weights/
