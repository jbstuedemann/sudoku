import cv2
import imutils
from imutils.perspective import four_point_transform
import math
import numpy as np
from tensorflow import keras
import os

DEBUG = False

def _locateBoard(image_init):
    # Filter the Image
    image = image_init.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (7, 7), 3)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    image = cv2.bitwise_not(image)
    
    # Find the Largest Contours
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    sudoku_contour = None
    for cnt in cnts:
        aprrox_cnt = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(aprrox_cnt) == 4:
            sudoku_contour = aprrox_cnt
            break
    if sudoku_contour is None:
        return None

    if DEBUG:
        output = image_init.copy()
        cv2.drawContours(output, [sudoku_contour], -1, (0, 255, 0), 2)
        cv2.imshow("Puzzle Outline", output)
        cv2.waitKey(0)

    # Transform the image to the Contour
    transformed_image = four_point_transform(image, sudoku_contour.reshape(4, 2))
    if DEBUG:
        cv2.imshow("Transformed Puzzle", transformed_image)
        cv2.waitKey(0)
    return transformed_image

def _getDigit(digit_image, model):
    cnts = imutils.grab_contours(cv2.findContours(digit_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    if len(cnts) == 0:
        return 0
    digit_cnt = max(cnts, key=cv2.contourArea)
    mask = np.zeros(digit_image.shape, dtype="uint8")
    cv2.drawContours(mask, [digit_cnt], -1, 255, -1)
    digit = cv2.bitwise_and(digit_image, digit_image, mask=mask)
    img_tensor = cv2.resize(digit, (128, 128))
    img_tensor = img_tensor.astype("float") / 255.0
    img_tensor = keras.preprocessing.image.img_to_array(img_tensor)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    model_output = model.predict(img_tensor)
    return model_output.argmax()
        
def _getDigitLocations(board_image, model, padding_percent=0.0):
    board = {}
    for y in range(9):
        for x in range(9):
            x_padding = math.floor(board_image.shape[1]*padding_percent)
            y_padding = math.floor(board_image.shape[0]*padding_percent)
            pixel_x_start = math.floor((board_image.shape[1]/9) * x) + x_padding
            pixel_x_finish = math.floor((board_image.shape[1]/9) * (x+1)) - x_padding
            pixel_y_start= math.floor((board_image.shape[0]/9) * y) + y_padding
            pixel_y_finish = math.floor((board_image.shape[0]/9) * (y+1)) - y_padding
            digit_image = board_image[pixel_y_start:pixel_y_finish, pixel_x_start:pixel_x_finish]
            digit = _getDigit(digit_image, model)

            if digit == 0:
                continue

            if DEBUG:
                print(f"({x}, {y}): {digit}")
                cv2.imshow(f"({x}, {y}): {digit}", digit_image)
                cv2.waitKey(0)

            board[(x, y)] = digit

    return board

def getBoardFromImage(img, model_file="ocr.h5", debug=False):
    if not debug: os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    model = keras.models.load_model(model_file)
    board_image = _locateBoard(img)
    board = _getDigitLocations(board_image, model, padding_percent=0.01)
    return board

def getBoardFromFile(filename, model_file="ocr.h5", debug=False):
    test_image = cv2.imread(filename)
    return getBoardFromImage(test_image, model_file, debug)

if __name__ == "__main__":
    DEBUG = True
    print(getBoardFromImage("test_board.png"))
