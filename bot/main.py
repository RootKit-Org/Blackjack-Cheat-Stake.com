from dotenv import load_dotenv
load_dotenv(".env")
from roboflow import Roboflow
from roboflow.util.prediction import PredictionGroup

import os

import cv2
import json

class Prediction():
    def __init__(self, x, y, width, height, confidence, class_id, image_path, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence
        self._class = kwargs["class"]
        self.class_id = class_id
        self.image_path = image_path


apiKey = os.getenv("API_KEY")

rf = Roboflow(api_key=apiKey)
project = rf.workspace().project("stake.com")
model = project.version(1).model

# infer on a local image
data = model.predict("Capture.PNG", confidence=40, overlap=30).json()

for prediction in data['predictions']:
    pred = Prediction(**prediction)
    print(pred._class, pred.confidence)

# # Load the image
# image = cv2.imread("Capture.PNG")

# # Draw the bounding boxes on the image
# for prediction in data['predictions']:
#     x = prediction['x']
#     y = prediction['y']
#     width = prediction['width']
#     height = prediction['height']
#     cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 3)
