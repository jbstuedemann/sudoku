import cv2
import math
import os
import random
import numpy as np
from vision import _locateBoard

def saveTrainingData(input_filename):
    board = cv2.imread(input_filename)
    board_image = _locateBoard(board)
    padding_percent = 0.01

    digit_database = {str(n):[] for n in range(10)}

    for y in range(9):
        for x in range(9):
            x_padding = math.floor(board_image.shape[1]*padding_percent)
            y_padding = math.floor(board_image.shape[0]*padding_percent)
            pixel_x_start = math.floor((board_image.shape[1]/9) * x) + x_padding
            pixel_x_finish = math.floor((board_image.shape[1]/9) * (x+1)) - x_padding
            pixel_y_start= math.floor((board_image.shape[0]/9) * y) + y_padding
            pixel_y_finish = math.floor((board_image.shape[0]/9) * (y+1)) - y_padding
            digit_image = board_image[pixel_y_start:pixel_y_finish, pixel_x_start:pixel_x_finish]
            
            cv2.imshow("Enter Number (anything else for no char)", digit_image)
            num = chr(cv2.waitKey(0))
            if num not in digit_database.keys():
                num = '0'
            digit_database[num].append(digit_image)
            cv2.destroyAllWindows()

    for key in digit_database:
        path = "training_data/"+str(key)+"/"
        count = len(os.listdir(path))
        for img in digit_database[key]:
            cv2.imwrite(path + str(count) + ".png", img)
            count += 1

def loadData(train_samples=500, test_samples=100):
    num_samples_per_digit = train_samples + test_samples
    train_data_label = []
    test_data_label = []
    for n in range(10):
        these_samples = []
        this_path = f"training_data/{n}/"
        imgs = os.listdir(this_path)
        n_count = 0
        for img_path in imgs:
            if n_count >= math.floor(num_samples_per_digit/2):
                break
            if img_path[-4:] != ".png":
                continue
            img = cv2.imread(this_path + img_path, 0)
            out_img = cv2.resize(img, (128, 128))
            these_samples.append((out_img, n))
            n_count += 1
        while n_count < num_samples_per_digit:
            img_path = random.choice(os.listdir(this_path))
            while img_path[-4:] != ".png":
                img_path = random.choice(os.listdir(this_path))
            img = cv2.imread(this_path + img_path, 0)
            img = np.array(img, dtype='float32')
            img /= 255.0
            rows, cols = img.shape
            gaussian = np.random.random((rows, cols)).astype(np.float32)
            gaussian_img = cv2.addWeighted(img, 0.75, 0.25 * gaussian, 0.25, 0)
            out_img = cv2.resize(gaussian_img, (128, 128))
            these_samples.append((out_img, n))
            n_count += 1

        for _ in range(test_samples):
            test_data_label.append(these_samples.pop(random.randint(0,len(these_samples)-1)))
        train_data_label += these_samples

    random.shuffle(train_data_label)
    
    train_data, train_labels, test_data, test_labels = [], [], [], []
    for img, label in train_data_label:
        train_data.append(img)
        train_labels.append(label)
    for img, label in test_data_label:
        test_data.append(img)
        test_labels.append(label)

    return (np.array(train_data), np.array(train_labels)), (np.array(test_data), np.array(test_labels))

def clearTrainingData():
    os.sysetm("rm training_data/*/*.png")
    