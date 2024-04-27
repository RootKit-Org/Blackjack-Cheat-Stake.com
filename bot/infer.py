import inference
model = inference.get_model("stake.com/1")

print("starting inference")
model.infer(image="Capture.PNG")
model.infer(image="Capture.PNG")
model.infer(image="Capture.PNG")
model.infer(image="Capture.PNG")
a = model.infer(image="Capture.PNG")
print("inference complete")

print(a)

exit()
from dotenv import load_dotenv
load_dotenv(".env")
from roboflow import Roboflow
import os
from main import Prediction
import cv2
import numpy as np
import json


apiKey = os.getenv("API_KEY")

rf = Roboflow(api_key=apiKey)
project = rf.workspace().project("stake.com")
model = project.version("1").model


frame_files = os.listdir('frames')


for frame_file in frame_files:
    data = model.predict(f'frames/{frame_file}', confidence=40, overlap=30).json()
    data = json.dumps(data)

    fileName = f"processedFrames/{frame_file[:-4]}.json"

    with open(f"{fileName}", "w") as f:
        f.write(str(data))




def getFramesFromVideo():
    video = cv2.VideoCapture('clippedGame.mp4')

    counter = 0
    frames = []

    # Loop through the video frame by frame
    while True:
        ret, frame = video.read()
        
        # If the frame was not successfully read, then we have reached the end of the video
        if not ret:
            break

        # If the counter is a multiple of 30, append the frame to the list
        if counter % 30 == 0:
            frames.append(frame)

        # Increment the counter
        counter += 1

    # Close the video file
    video.release()

    # Convert the list of frames to a numpy array
    frames = np.array(frames)

    # Loop through the list of frames
    for i, frame in enumerate(frames):
        # Construct a filename that includes the frame number
        filename = f'frames/frame_{i}.png'
        
        # Save the frame as a PNG file
        cv2.imwrite(filename, frame)