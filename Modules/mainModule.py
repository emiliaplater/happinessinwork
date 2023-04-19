import cv2



capture = cv2.VideoCapture('../vids/#')
timeFrame = 10

while True:
    ret, frame = capture.read()
    if ret is False:
        break

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(timeFrame) & 0xFF
    if key == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

