from dotenv import load_dotenv
load_dotenv(".env")
from roboflow import Roboflow
from roboflow.util.prediction import PredictionGroup
import os
import cv2
import json
from pynput import keyboard, mouse

class KeyListener:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.last_position = None
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.key_listener.start()

    def on_press(self, key):
        try:
            if key.char == 'p':
                self.last_position = self.mouse_controller.position
            if key.char == 'o':
                self.last_position = self.mouse_controller.position
            if key.char == 'i':
                self.last_position = self.mouse_controller.position
            if key.char == 'u':
                self.last_position = self.mouse_controller.position
            if key.char == 'y':
                self.last_position = self.mouse_controller.position
            if key.char == 't':
                self.last_position = self.mouse_controller.position
            if key.char == 'r':
                self.last_position = self.mouse_controller.position
            if key.char == 'c':
                self.last_position = None
            print(self.last_position)
        except AttributeError:
            pass

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
        self._center = (self.x + self.width // 2, self.y + self.height // 2)
        self.timesRead = 0

    @property
    def center(self):
        self.timesRead += 1
        return self._center

def main():
    keyListener = KeyListener()
    playerCount = 0
    playerMax = 7

    
    frameFiles = os.listdir('processedFrames')

    pendingCards: dict[str, list[Prediction]] = {
        "A": [],
        "K": [],
        "Q": [],
        "J": [],
        "10": [],
        "9": [],
        "8": [],
        "7": [],
        "6": [],
        "5": [],
        "4": [],
        "3": [],
        "2": []
    }
    confirmedCards: dict[str, list[Prediction]] = {
        "A": [],
        "K": [],
        "Q": [],
        "J": [],
        "10": [],
        "9": [],
        "8": [],
        "7": [],
        "6": [],
        "5": [],
        "4": [],
        "3": [],
        "2": []
    }

    for idx, frameFile in enumerate(frameFiles):
        print(idx)
        if idx <= 21:
            continue
        # if idx == 21:
        #     break
        with open(f'processedFrames/{frameFile}', 'r') as f:
            data = json.load(f)
            for prediction in data['predictions']:
                pred = Prediction(**prediction)

                found = False
                for card in confirmedCards[pred._class]:
                    if abs(card.center[0] - pred.center[0]) <= 5 and abs(card.center[1] - pred.center[1]) <= 5:

                        for pCard in pendingCards[pred._class]:
                            if abs(card.center[0] - pCard.center[0]) <= 10 and abs(card.center[1] - pCard.center[1]) <= 10:
                                pendingCards[pred._class].remove(pCard)

                        found = True

                # If the card was not found in the confirmed cards, then check the pending cards
                if not found:
                    moveCards = []
                    for card in pendingCards[pred._class]:
                        print(f"{abs(card.center[0] - pred.center[0])} {abs(card.center[1] - pred.center[1])} {card.timesRead}")
                        if abs(card.center[0] - pred.center[0]) <= 5 and abs(card.center[1] - pred.center[1]) <= 5 and card.timesRead >= 12:
                            confirmedCards[pred._class].append(card)
                            pendingCards[pred._class].remove(card)
                            moveCards.append(card)

                            found = True
                            break

                    if not found:
                        pendingCards[pred._class].append(pred)

                # print(f"Label: {pred._class} Center: {pred.center}")

    for key, value in confirmedCards.items():
        print(f"{key}: \t TOTAL: {len(value)}")
        for item in value:
            print(f"\t - {item.center}")

    exit()

    while True:
        # TODO add logic for botting the game
        if keyListener.last_position is not None:
            pass










def detect():
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


if __name__ == "__main__":
    main()