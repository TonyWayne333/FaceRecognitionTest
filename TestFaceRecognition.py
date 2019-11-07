import unittest
import os
import faceRecognition


class MyTestCase(unittest.TestCase):
    def test_download_files(self):
        download_file = faceRecognition.download_files
        download_file(r'C:\Users\Public\testingPython1\\', r'C:\Users\Public\testingPython2\test.jpg')
        self.assertGreater(len(os.listdir(r'C:\Users\Public\testingPython2')), 0)

    def test_remove_files(self):
        remove_file = faceRecognition.remove_files
        remove_file(r'C:\Users\Public\testingPython1')
        self.assertEqual(len(os.listdir(r'C:\Users\Public\testingPython1')), 0)


if __name__ == '__main__':
    unittest.main()
