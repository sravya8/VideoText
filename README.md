# Video Text Detection and Recognition

[Work in progress]

Please see Demo notebook as a starting point. Use it to provide your youtube url to generate a new video with overlayed bounding boxes for all text and their respective transcriptions.

Directory structure:
- Demo.ipynb: Demo notebook as described above
- detection.py: Holds helper functions for detection task. Loads Tensorflow inference graph trained seperately using Tensorflow objection detection models on text data. We use ssd_mobile network as it is the fastest among available models.
- recognition.py: Holds helper functions for recognition task. Loads pytorch model and infers.
- utilities.py: Holds all other helper functions required for E2E video text detection and recognition.
- synth_utils.py: Helper script to prepare SynthText data
- SynthText Data Preparation notebook: Scripts to translate Synthetext data to TFrecord to be used with Tensorflow detection model
- crnn.pytorch: Pytorch implementation of CRNN for text recognition on cropped natural images.
- coco-text: Helper functions to work with Coco-Text data. Also contains Coco-Text Preparation notebook to translate coco-text to TFRecord to use with Tensorflow detection model.