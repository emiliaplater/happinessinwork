import unittest
from mainModule import MainModule


class TestMainModule(unittest.TestCase):
    def test_main_module(self):
        video_path = './vids/vid1.flv'
        video_player = MainModule(video_path, 1)

        video_player.play()

        self.assertTrue(video_player.ax.has_data())

if __name__ == '__main__':
    unittest.main()
