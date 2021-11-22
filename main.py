import cv2
import imutils
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller
# import subprocess

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["en", "sp", "bs"]]

dspl = ""
keyboard = Controller()
# flag = True


def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (163, 173, 178), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 25, y + 45),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    #  print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Button:
    def __init__(self, pos, text, size=[70, 70]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):  # draw button
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = imutils.resize(img, width=1080)  # size image
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1['center']
        handType1 = hand1["type"]
        fingers1 = detector.fingersUp(hand1)

        if lmList1:

            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                # #  notepad
                # if lmList1[12][0] and lmList1[12][1]:
                #     l, _, _ = detector.findDistance(lmList1[12], lmList1[9], img)
                #     if l < 25:
                #         def note():
                #             global flag
                #             if flag:
                #                 print("True")
                #                 subprocess.call('C:/Windows/System32/notepad.exe')
                #                 flag = False
                #
                #         note()

                #  distance
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (227, 98, 42), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 8, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
                    l, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)

                    #  when clicked
                    if l < 54:
                        if button.text == "en":
                            keyboard.press(Key.enter)
                        elif button.text == "sp":
                            keyboard.press(Key.space)
                        elif button.text == "bs":
                            keyboard.press(Key.backspace)
                        else:
                            keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (161, 50, 50), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 8, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                        # dspl += button.text
                        sleep(0.25)

    # display
    # cv2.rectangle(img, (500, 50), (1050, 120), (175, 0, 175), cv2.FILLED)
    # cv2.putText(img, finalText, (500, 110), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    if len(hands) == 2:
        hand2 = hands[1]
        lmList2 = hand2["lmList"]
        bbox2 = hand2["bbox"]
        centerPoint2 = hand2['center']
        handType2 = hand2["type"]
        fingers2 = detector.fingersUp(hand2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
