import argparse
from mss import mss
import numpy as np
import vision
import solver
import cv2

def solveGameFromImage(filename):
    scanned_board = vision.getBoardFromFile(filename)
    solver.solveGame(scanned_board, debug=True)

def solveGameFromScreenshot():
    sct = mss()
    sc_sht = sct.grab(sct.monitors[1])
    img = np.array(sc_sht)
    scanned_board = vision.getBoardFromImage(img)
    print(solver.Game(scanned_board))
    solver.solveGame(scanned_board, debug=True)

solveGameFromScreenshot()