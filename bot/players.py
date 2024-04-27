import numpy as np

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