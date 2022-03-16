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
    `solveGameFromImage(filename)` - Given an input filename, find it's sudoku board, and solve.
    `solveGameFromScreenshot()` - Take a screenshot of the current screen, and solve it's sudoku board.
    There are also fucnction calls to create and process and parse arguments.
- ### [src/](https://github.com/jbstuedemann/sudoku/tree/main/src)
  - ### [solver.py](https://github.com/jbstuedemann/sudoku/blob/main/src/solver.py)
    This file is associated with solving the sudoku games.
    `class Game` - Representation of a sudoku board. It stores the given numbers, and calls functions to solve the remaining board.
    `solveGame(board, debug)` - This function creates a Game given a board, and return the solved Game.
  - ### [vision.py](https://github.com/jbstuedemann/sudoku/blob/main/src/vision.py)
    This file is associated with the Computer Vision for processing an input image. 
    `getBoardFromImage(img, model_file, debug)` - Given an image and an h5 model, return the dictionary representation of the board.
    `getBoardFromFile(filename, model_file, debug)` - Given an image filename and an h5 model, return the dictionary representation of the board.
  - ### [create_training_data.py](https://github.com/jbstuedemann/sudoku/blob/main/src/create_training_data.py)
    WIP
  - ### [ocr.ipynb](https://github.com/jbstuedemann/sudoku/blob/main/src/ocr.ipynb)
    This python notebook created the `ocr.h5` in to process images of numbers. The general structure is a CNN with an input size of (128, 128, 1). They are processed through 2 convultions, then through 2 linear layers. 
