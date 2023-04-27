import cv2


def binaryModule(frame): 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    _, frame_threshold = cv2.threshold(gray_frame, 20, 255, cv2.THRESH_BINARY_INV)

    return frame_threshold 