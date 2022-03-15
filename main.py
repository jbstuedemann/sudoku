import argparse
import vision
import solver

filename = "test_board1.png"
board = vision.getBoardFromImage(filename)
solution = solver.solveGame(board, debug=True)
print(solution)