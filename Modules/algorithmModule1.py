import cv2
import numpy as np



def algorithmModule1(frame_threshold, frame) -> int:
    circles = cv2.HoughCircles(frame_threshold, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=8.5, param2=8.5, minRadius=5, maxRadius=100)

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

            cv2.circle(frame, (x1, y1), r1, (0, 255, 0), 2)
            cv2.circle(frame, (x2, y2), r2, (0, 255, 0), 2)

    return left_eye_coords1, right_eye_coords1