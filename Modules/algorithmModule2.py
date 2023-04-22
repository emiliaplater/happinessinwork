import cv2
from calculateAlgorithmModule import secondAlgorithmCoords



def algorithmModule2(threshold, frame):
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    left_eye_coords2 = None
    right_eye_coords2 = None

    for cnt in contours:
        if len(cnt) < 3:
            continue

        (x, y), r = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(r)

        if x < frame.shape[1] / 2:
            cv2.circle(frame, center, radius, (255, 0, 0), 2)
            left_eye_coords2 = (x, y)
            # print(f'Left Eye coordinates: ({x}, {y}), radius: {radius}')
        else:
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
            right_eye_coords2 = (x, y)
            # print(f'Right Eye coordinates: {x}, {y}, radius: {radius}')

        cv2.imshow('Frame', frame)

    secondAlgorithmCoords(left_eye_coords2, right_eye_coords2)