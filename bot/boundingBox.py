import cv2
import json
import numpy as np


# Load the image
image = cv2.imread("frames/frame_30.png")

with open("processedFrames/frame_30.json") as f:
    data = json.load(f)

# Draw the bounding boxes on the image
for prediction in data['predictions']:
    x = prediction['x']
    y = prediction['y']
    width = prediction['width']
    height = prediction['height']
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 3)


# Define the rectangle parameters: center, size, and angle
x = 1200
y = 750
width = 200
height = 100
center = (x + width // 2, y + height // 2)
size = (width, height)
angle = 40  # degrees

point = [623, 724]

# Define the polygon points
pos1 = np.array([
    [540, 725],
    [615, 810],
    [805, 710],
    [740, 640],
], dtype=np.int32)

pos2 = np.array([
    [605, 810],
    [725, 870],
    [850, 750],
    [805, 710],
], dtype=np.int32)

pos3 = np.array([
    [725, 870],
    [890, 900],
    [960, 735],
    [850, 750],
], dtype=np.int32)

pos4 = np.array([
    [890, 900],
    [1075, 900],
    [1050, 735],
    [960, 735],
], dtype=np.int32)

pos5 = np.array([
    [1075, 900],
    [1240, 865],
    [1140, 705],
    [1050, 735],
], dtype=np.int32)

pos6 = np.array([
    [1370, 815],
    [1240, 865],
    [1140, 705],
    [1210, 685],
], dtype=np.int32)

pos7 = np.array([
    [1370, 815],
    [1475, 715],
    [1260, 645],
    [1210, 685],
], dtype=np.int32)


# # Check if the point is inside the polygon
# result = cv2.pointPolygonTest(pos, point, False)
# print(result)

# Draw the polygon on the image
cv2.polylines(image, [pos1], True, (0, 255, 0), 3)
cv2.polylines(image, [pos2], True, (0, 255, 0), 3)
cv2.polylines(image, [pos3], True, (0, 255, 0), 3)
cv2.polylines(image, [pos4], True, (0, 255, 0), 3)
cv2.polylines(image, [pos5], True, (0, 255, 0), 3)
cv2.polylines(image, [pos6], True, (0, 255, 0), 3)
cv2.polylines(image, [pos7], True, (0, 255, 0), 3)


# Save the image
cv2.imwrite("output.png", image)