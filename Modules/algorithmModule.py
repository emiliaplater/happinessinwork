import cv2
import numpy as np



def algorithmModule(threshold, frame):
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    CA = cv2.medianBlur(closed, 7)

    circles = cv2.HoughCircles(CA, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=8.5, param2=8.5, minRadius=5, maxRadius=22)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            
    cv2.imshow('Edges', CA)