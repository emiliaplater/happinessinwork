import cv2


def binaryModule(frame):
    gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

    _, threshold = cv2.threshold(gray_roi, 20, 255, cv2.THRESH_BINARY_INV)

    return threshold