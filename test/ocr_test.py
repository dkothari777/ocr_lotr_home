import unittest
from src.services.ocr import read_image, read_easyocr_image, set_image

def do_test(image):
    text = read_image(image)
    # print(text)
    for line in text.split("\n"):
        if "Difficulty" in line:
            print(line)
    print()

class MyTestCase(unittest.TestCase):
    def test_something(self):
        # do_test("/Users/darshankothari/workspace/ocr_lotr_home/test/test-images/lotr_1.PNG")
        # print()
        # print()
        # do_test("/Users/darshankothari/workspace/ocr_lotr_home/test/test-images/IMG_0860.PNG")
        # print()
        # print()
        # do_test("/Users/darshankothari/workspace/ocr_lotr_home/test/test-images/IMG_0861.PNG")
        set_image(True)
        do_test("/Users/darshankothari/workspace/ocr_lotr_home/chapter_2/IMG_1239.PNG")


    def test_easy_ocr(self):
        # text = read_easyocr_image("/Users/darshankothari/workspace/ocr_lotr_home/test/test-images/lotr_1.PNG")
        text = read_easyocr_image("/Users/darshankothari/workspace/ocr_lotr_home/test/test-images/IMG_0861.PNG")
        print(text)




if __name__ == '__main__':
    unittest.main()