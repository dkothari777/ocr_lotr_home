from pytesseract import pytesseract, Output
from PIL import Image
import easyocr
import cv2
import numpy as np

SHOW_IMAGE = False


def set_image(setting):
    global SHOW_IMAGE
    SHOW_IMAGE = setting


def show_image(name, image):
    if SHOW_IMAGE:
        cv2.imshow(name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def custom_grayscale(image):
    (row, col) = image.shape[0:2]

    # Take the average of pixel values of the BGR Channels
    # to convert the colored image to grayscale image
    for i in range(row):
        for j in range(col):
            # Find the average of the BGR pixel values
            image[i, j] = sum(image[i, j]) / 10

    show_image("custom_gray", image)
    return image


# get grayscale image
def get_grayscale(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image("gray", img)
    return img


def get_hsv(image):
    # img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HLS_FULL)
    show_image("rgb", img)
    return img


# noise removal
def remove_noise(image):
    img = cv2.medianBlur(image, 3)
    show_image("noise", image)
    return img


# thresholding
def thresholding(image):
    result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    show_image("threshold", result)
    return result


# dilation
def dilate(image):
    kernel = np.ones((2, 2), np.uint16)
    result = cv2.dilate(image, kernel, iterations=1)
    show_image("dilate", result)
    return result


# erosion
def erode(image):
    kernel = np.ones((2, 2), np.uint16)
    result = cv2.erode(image, kernel, iterations=1)
    show_image("erode", result)
    return result


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((2, 2), np.uint16)
    result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    show_image("opening", result)
    return result


# canny edge detection
def canny(image):
    result = cv2.Canny(image, 23, 23)
    show_image("canny", result)
    return result


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def read_image(filename):
    original_image = cv2.imread(filename)
    original_image[original_image <= 130] = 0
    original_image[original_image >= 150] = 255
    # img = thresholding(get_grayscale(remove_noise(opening(erode(dilate(get_hsv(original_image)))))))
    img = erode(thresholding(get_grayscale(remove_noise(original_image))))

    # Adding custom options
    custom_config = r'-l eng --oem 3 --psm 6'
    return pytesseract.image_to_string(img, config=custom_config)
    # return pytesseract.image_to_string(Image.open(filename))


def read_easyocr_image(filename):
    reader = easyocr.Reader(['en'])
    original_image = cv2.imread(filename)
    img = remove_noise(get_hsv(original_image))
    read_text = reader.readtext(img)
    results = ""
    for ((x_min, y_min, x_max, y_max), text, confidence,) in read_text:
        results = results + text + "\n"
    return results
