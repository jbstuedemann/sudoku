import argparse
from mss import mss
import numpy as np
import src.vision as vision
import src.solver as solver

# Given an input filename, find it's sudoku board, and solve
def solveGameFromImage(filename):
    scanned_board = vision.getBoardFromFile(filename, model_file="src/ocr.h5")
    print("Scanned Board:")
    print(solver.Game(scanned_board))
    print("Solved Board:")
    solver.solveGame(scanned_board, debug=True)

# Take a screenshot of the current screen, and solve it's sudoku board
def solveGameFromScreenshot():
    sct = mss()
    sc_sht = sct.grab(sct.monitors[1])
    img = np.array(sc_sht)
    scanned_board = vision.getBoardFromImage(img, model_file="src/ocr.h5")
    print("Scanned Board:")
    print(solver.Game(scanned_board))
    print("Solved Board:")
    solver.solveGame(scanned_board, debug=True)


# Add arguments for calling this python file
parser = argparse.ArgumentParser(description='Scan and solve sudoku boards. Trained to read the font on \033[4mhttps://sudoku.com/\033[0m')
parser.add_argument('-s', '--screen', help="take a screenshot and process it", action="store_true")
parser.add_argument('-i', '--image', help="use a given image and process it")
args = parser.parse_args()
if args.screen:
    solveGameFromScreenshot()
elif args.image:
    solveGameFromImage(args.image)
else:
    print("Please enter an option (or \033[1m-h/--help\033[0m for help)")