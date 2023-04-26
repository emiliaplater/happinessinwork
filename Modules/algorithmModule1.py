import cv2
import numpy as np



def algorithmModule1(threshold, frame) -> int:
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    CA = cv2.medianBlur(closed, 7)

    circles = cv2.HoughCircles(CA, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=8.5, param2=8.5, minRadius=5, maxRadius=100)
    
    left_eye_coords1 = None
    right_eye_coords1 = None

    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')
        if len(circles) == 2:
            circles = sorted(circles, key=lambda x: x[0])
            x1, y1, r1 = circles[0]
            x2, y2, r2 = circles[1]

            left_eye_coords1 = (x1, y1, r1)
            right_eye_coords1 = (x2, y2, r2)

            if x1-r1*13 >= 0 and x1+r1*13 <= frame.shape[1] and y1-r1*13 >= 0 and y1+r1*13 <= frame.shape[0]:
                left_eye_roi = frame[y1-r1*13:y1+r1*13, x1-r1*13:x1+r1*13]
                cv2.imshow('left', left_eye_roi)

            if x2-r2*13 >= 0 and x2+r2*13 <= frame.shape[1] and y2-r2*13 >= 0 and y2+r2*13 <= frame.shape[0]:
                right_eye_roi = frame[y2-r2*13:y2+r2*13, x2-r2*13:x2+r2*13]
                cv2.imshow('right', right_eye_roi)

            cv2.circle(frame, (x1, y1), r1, (0, 255, 0), 2)
            cv2.circle(frame, (x2, y2), r2, (0, 255, 0), 2)

    return left_eye_coords1, right_eye_coords1