# Sudoku Solver

This project uses **OpenCV** and **TensorFlow** to scan images and screenshots for sudoku boards, then solves them using sudoku rules.

## Dependencies

- [TensorFlow](https://www.tensorflow.org/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)
- [imutils](https://github.com/PyImageSearch/imutils)
- [mss](https://python-mss.readthedocs.io/)
- [argparse](https://docs.python.org/3/library/argparse.html)

## Usage

Main program can be run with `python sudoku.py`
There are two main commands: `--screen` and `--image IMAGE`

|Flags |Description
|-- |--
|`-h`/`--help` | show this help message and exit
|`-s`/`--screen` | take a screenshot and process it
|`-i IMAGE`/`--image IMAGE` | use a given image and process it

## Implementation
- ### [sudoku.py](https://github.com/jbstuedemann/sudoku/blob/main/sudoku.py)
    `solveGameFromImage(filename)` - Given an input filename, find it's sudoku board, and solve. <br>
    `solveGameFromScreenshot()` - Take a screenshot of the current screen, and solve it's sudoku board. <br>
    There are also fucnction calls to create and process and parse arguments. <br>
- ### [src/](https://github.com/jbstuedemann/sudoku/tree/main/src)
  - ### [solver.py](https://github.com/jbstuedemann/sudoku/blob/main/src/solver.py)
    This file is associated with solving the sudoku games. <br>
    `class Game` - Representation of a sudoku board. It stores the given numbers, and calls functions to solve the remaining board. <br>
    `solveGame(board, debug)` - This function creates a Game given a board, and return the solved Game. <br>
  - ### [vision.py](https://github.com/jbstuedemann/sudoku/blob/main/src/vision.py)
    This file is associated with the Computer Vision for processing an input image. <br>
    `getBoardFromImage(img, model_file, debug)` - Given an image and an h5 model, return the dictionary representation of the board. <br>
    `getBoardFromFile(filename, model_file, debug)` - Given an image filename and an h5 model, return the dictionary representation of the board. <br>
  - ### [create_training_data.py](https://github.com/jbstuedemann/sudoku/blob/main/src/create_training_data.py)
    This was used to create the training and testing data for the OCR. The idea is to read in sudoku boards and process them, and then let the user calssify each digit. Then, the program will randomly read in the data, and fill the dataset with random variations of the numbers. This is distributed between a few functions. <br>
    `saveTrainingData(input_filename)` - This reads in a sudoku board, and prompts the user to press keys depending on what digit each image represents. <br>
    `loadData(train_samples, test_samples)` - This function takes in a number of train and test samples per class, and creates the database given the images in the respective directory. <br>

  - ### [ocr.ipynb](https://github.com/jbstuedemann/sudoku/blob/main/src/ocr.ipynb)
    This python notebook created the `ocr.h5` in to process images of numbers. The general structure is a CNN with an input size of (128, 128, 1). They are processed through 2 convultions, then through 2 linear layers. <br>
