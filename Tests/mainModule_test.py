import cv2
import unittest
import numpy as np
# outside files
from Modules.mainModule import *



class TestCapture(unittest.TestCase):
    def test_camera_capture(self):
        while True:
            ret, frame = capture.read()
            if ret is False:
                break

            self.assertGreater(len(frame), 0, msg="Captured frame should not be empty")

            key = cv2.waitKey(keyFrame) & 0xFF
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    unittest.main()