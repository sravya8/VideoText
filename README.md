# Video Text Detection and Recognition
![Demo](static/tennis.gif "Demo")

[Work in progress]

Please see Demo notebook as a starting point. Use it to provide your youtube url to:
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
