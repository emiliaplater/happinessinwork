import cv2



capture = cv2.VideoCapture(0)
keyFrame = 1

while True:
    ret, frame = capture.read()
    if ret is False:
        break

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(keyFrame) & 0xFF
    if key == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()