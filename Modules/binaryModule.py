import cv2
import numpy as np



def on_trackbar(val):
    global threshold_value
    threshold_value = val

cv2.namedWindow('Processed Frame')
cv2.createTrackbar('Threshold', 'Processed Frame', 13, 255, on_trackbar)
threshold_value = 13


def binaryModule(frame): 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    brightness = np.mean(gray_frame)
    threshold = threshold_value + int((brightness - 128) / 2)

    _, threshold = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    frame_threshold = cv2.medianBlur(closed, 7)

    return frame_threshold 