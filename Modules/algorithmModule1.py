import cv2
import numpy as np
from calculateAlgorithmModule import firstAlgorithmCoords



def algorithmModule1(threshold, frame):
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    CA = cv2.medianBlur(closed, 7)

    circles = cv2.HoughCircles(CA, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=8.5, param2=8.5, minRadius=5, maxRadius=22)
    
    left_eye_coords1 = None
    right_eye_coords1 = None

    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        if len(circles) == 2:
            x1, y1, r1 = circles[0]
            x2, y2, r2 = circles[1]

            left_eye_coords1 = (x1, y1, r1)
            right_eye_coords1 = (x2, y2, r2)

            # print(f'Letf eye: ({x1}, {y1}), radius: {r1}')
            # print(f'Right eye: ({x2}, {y2}), radius: {r2}')

            cv2.circle(frame, (x1, y1), r1, (0, 255, 0), 2)
            cv2.circle(frame, (x2, y2), r2, (0, 255, 0), 2)

    # cv2.imshow('Edges', CA)
    # tuple1 = (left_eye_coords1, right_eye_coords1)
    firstAlgorithmCoords(left_eye_coords1, right_eye_coords1)