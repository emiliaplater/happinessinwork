import unittest
import cv2
import numpy as np
from Modules.algorithmModule import algorithmModule



class TestAlgorithmModule(unittest.TestCase):

    def test_algorithmModule(self):
        # create a sample image
        img = np.zeros((256, 256), np.uint8)
        cv2.circle(img, (128, 128), 50, 255, -1)

        # threshold the image
        _, threshold = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY_INV)

        # apply the algorithmModule function to the image
        output = algorithmModule(threshold, img)

        # check that the output is not None
        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
