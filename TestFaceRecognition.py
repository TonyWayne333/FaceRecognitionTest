import unittest
import os
import faceRecognition


class MyTestCase(unittest.TestCase):
    def test_removefiles(self):
        removefile = faceRecognition.remove_files
        removefile(r'C:\Users\Public\testingPython')
        self.assertEqual(len(os.listdir(r'C:\Users\Public\testingPython')), 0)


if __name__ == '__main__':
    unittest.main()
