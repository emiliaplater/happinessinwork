import cv2
#modules
from algorithmModule1 import algorithmModule1
from algorithmModule2 import algorithmModule2



def binaryModule(frame):
    gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

    _, threshold = cv2.threshold(gray_roi, 20, 255, cv2.THRESH_BINARY_INV)

    algorithmModule1(threshold, frame)
    algorithmModule2(threshold, frame)