import copy
import os
import time

class Game:
    def __init__(self, startingBoard):
        self.board = {}
        for x in range(9):
            for y in range(9):
                self.board[(x, y)] = set(n for n in range(1,10))
        self.startingBoard = set()
        for pos in startingBoard.keys():
            self.startingBoard.add(pos)
            self.setValue(pos, startingBoard[pos])
    
    def setValue(self, pos, value):
        (x, y) = pos
        for n in range(9):
            if value in self.board[(x, n)] and (x, n) != pos:
                self.removeValue((x, n), value)
            if value in self.board[(n, y)] and (n, y) != pos:
                self.removeValue((n, y), value)

        xd3, yd3 = x//3, y//3
        for x in range(3):
            for y in range(3):
                coord = ((xd3*3)+x, (yd3*3)+y)
                if value in self.board[coord] and coord != pos:
                    self.removeValue(coord, value)

        self.board[pos] = set([value])
        self.updateSingles(pos)


    def updateSingles(self, pos):
        (x, y) = pos
        xd3, yd3 = x//3, y//3

        for n in range(3):
            self.checkRowColPossible(xd3, n)
            self.checkRowColPossible(n, yd3)
            self.checkAreaForSingles(xd3, n)
            self.checkAreaForSingles(n, yd3)

    def checkRowColPossible(self, x_i, y_i):
        for n in range(1, 10):
            nPos = []
            for x in range(3*x_i, 3*(x_i+1)):
                for y in range(3*y_i, 3*(y_i+1)):
                    if n in self.board[(x, y)]:
                        nPos.append((x, y))

            if self.listInSameCol(nPos):
                col = nPos[0][0]
                for coord in range(9):
                    if (col, coord) in nPos: continue
                    self.removeValue((col, coord), n)
            if self.listInSameRow(nPos):
                row = nPos[0][1]
                for coord in range(9):
                    if (coord, row) in nPos: continue
                    self.removeValue((coord, row), n)

    def listInSameCol(self, list):
        if len(list)==0: return False
        col = list[0][0]
        for i in range(1, len(list)):
            if list[i][0] != col:
                return False
        return True

    def listInSameRow(self, list):
        if len(list)==0: return False
        row = list[0][1]
        for i in range(1, len(list)):
            if list[i][1] != row:
                return False
        return True
            
    def checkAreaForSingles(self, x_i, y_i):
        counts = {x:0 for x in range(1,10)}
        for x in range(3*x_i, 3*(x_i+1)):
            for y in range(3*y_i, 3*(y_i+1)):
                for num in self.board[(x, y)]:
                    counts[num] += 1
        for key in counts.keys():
            if counts[key] == 1:
                for x in range(3*x_i, 3*(x_i+1)):
                    for y in range(3*y_i, 3*(y_i+1)):
                        if len(self.board[(x, y)]) > 1 and key in self.board[(x, y)]:
                            self.setValue((x, y), key)
    
    def removeValue(self, pos, value):
        if value in self.board[pos]:
            self.board[pos].remove(value)
            if len(self.board[pos]) == 1:
                for n in range(1, 10):
                    if n in self.board[pos]:
                        self.setValue(pos, n)
                        break

    def isPossible(self):
        for x in range(9):
            for y in range(9):
                if len(self.board[(x, y)]) == 0:
                    return False
        return True

    def isSolved(self):
        for x in range(9):
            for y in range(9):
                if len(self.board[(x, y)]) != 1:
                    return False
        return True

    def solve(self):
        solved = self.solveHelper()
        if solved == None: return
        self.board = solved.board
        
    def solveHelper(self):
        if self.isSolved():
            return self

        for x in range(9):
            for y in range(9):
                if len(self.board[(x, y)]) == 1: continue
                values = list(self.board[(x, y)])
                for nextValue in values:
                    test = copy.deepcopy(self)
                    test.setValue((x, y), nextValue)

                    if not test.isPossible():
                        test.removeValue((x, y), nextValue)
                    else:
                        next = test.solveHelper()
                        if next != None:
                            return next
                        else:
                            test.removeValue((x, y), nextValue)
        return None

    def debugString(self):
        outStr = ""
        for y in range(9):
            if (y%3==0): outStr += "  "+"-"*79+"\n"
            else: outStr += ' |'+' '*26+'|'+' '*26+'|'+' '*25+'|\n'
            for x in range(9):
                if (x%3==0): outStr += " | "
                else: outStr += '   '
                for n in range(1,4):
                    if (x, y) in self.startingBoard:
                        outStr += '\033[1m\033[93m'
                        for n in range(1,10):
                            if n in self.board[(x, y)]:
                                break
                    else:
                        if len(self.board[(x, y)])==1:
                            outStr += '\033[1m\033[94m'
                            for n in range(1,10):
                                if n in self.board[(x, y)]:
                                    break
                        else:
                            if n in self.board[(x, y)]:
                                outStr += '\033[96m'
                            else: outStr += '\033[91m'
                    outStr += str(n)+' \033[0m'
            outStr += '|\n'
            for x in range(9):
                if (x%3==0): outStr += " | "
                else: outStr += '   '
                for n in range(4,7):
                    if (x, y) in self.startingBoard:
                        outStr += '\033[1m\033[93m'
                        for n in range(1,10):
                            if n in self.board[(x, y)]:
                                break
                    else:
                        if len(self.board[(x, y)])==1:
                            outStr += '\033[1m\033[94m'
                            for n in range(1,10):
                                if n in self.board[(x, y)]:
                                    break
                        else:
                            if n in self.board[(x, y)]:
                                outStr += '\033[96m'
                            else: outStr += '\033[91m'
                    outStr += str(n)+' \033[0m'
            outStr += '|\n'
            for x in range(9):
                if (x%3==0): outStr += " | "
                else: outStr += '   '
                for n in range(7,10):
                    if (x, y) in self.startingBoard:
                        outStr += '\033[1m\033[93m'
                        for n in range(1,10):
                            if n in self.board[(x, y)]:
                                break
                    else:
                        if len(self.board[(x, y)])==1:
                            outStr += '\033[1m\033[94m'
                            for n in range(1,10):
                                if n in self.board[(x, y)]:
                                    break
                        else:
                            if n in self.board[(x, y)]:
                                outStr += '\033[96m'
                            else: outStr += '\033[91m'
                    outStr += str(n)+' \033[0m'
            outStr += '|\n'
        outStr += "  "+"-"*79+"\n"
        return outStr

    def __str__(self):
        outStr = ""
        for y in range(9):
            if (y%3==0): outStr += " "+"-"*29+"\n"
            for x in range(9):
                if (x%3==0): outStr += "|"

                if (len(self.board[(x, y)]) == 1):
                    for n in range(1, 10):
                        if n in self.board[(x, y)]:
                            if (x, y) in self.startingBoard:
                                outStr += '\033[1m\033[93m'
                            else:
                                outStr += '\033[94m'
                            outStr += " " + str(n) + " \033[0m"

                else:
                    outStr += "   "
            outStr += '|\n'
        outStr += " "+"-"*29+"\n"
        return outStr

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

easyBoard = {
    (0, 0): 3,
    (0, 1): 4,
    (0, 3): 8,
    (0, 5): 1,
    (0, 6): 7,
    (0, 7): 2,
    (1, 3): 9,
    (1, 4): 2,
    (1, 5): 6,
    (1, 8): 5,
    (2, 0): 2,
    (2, 1): 5,
    (2, 4): 7,
    (2, 5): 3,
    (2, 6): 8,
    (2, 7): 9,
    (3, 1): 9,
    (3, 7): 6,
    (3, 8): 2,
    (4, 4): 8,
    (4, 5): 5,
    (4, 7): 7,
    (5, 0): 7,
    (5, 2): 4,
    (5, 3): 2,
    (5, 4): 1,
    (5, 5): 9,
    (5, 7): 3,
    (6, 0): 9,
    (6, 1): 1,
    (6, 2): 5,
    (7, 0): 4,
    (7, 4): 6,
    (7, 7): 1,
    (8, 4): 9,
    (8, 5): 7,
    (8, 6): 2,
    (8, 8): 4
}

hardBoard = {
    (0, 0): 7,
    (0, 5): 9,
    (0, 7): 8,
    (1, 4): 5,
    (2, 0): 4,
    (2, 3): 8,
    (2, 6): 1,
    (3, 5): 8,
    (3, 7): 7,
    (3, 8): 2,
    (4, 3): 2,
    (4, 8): 1,
    (5, 3): 6,
    (5, 4): 3,
    (5, 6): 5,
    (6, 0): 9,
    (6, 2): 2,
    (6, 5): 7,
    (7, 0): 1,
    (7, 2): 5,
    (7, 3): 4,
    (7, 4): 9,
    (8, 2): 4,
    (8, 7): 2,
    (8, 8): 8
}

expertBoard = {
    (0,3):6,
    (0,7):1,
    (1,2):2,
    (1,3):7,
    (1,6):8,
    (1,8):9,
    (2,0):5,
    (2,1):3,
    (2,4):1,
    (2,6):4,
    (3,0):2,
    (3,4):9,
    (3,5):7,
    (4,6):5,
    (5,1):1,
    (5,7):4,
    (6,3):4,
    (6,5):3,
    (6,6):6,
    (7,0):7,
    (7,3):8,
    (8,2):5,
    (8,8):7
}

evilBoard = {
    (0, 5): 7,
    (1, 2): 5,
    (1, 7): 2,
    (2, 0): 2,
    (2, 3): 1,
    (2, 6): 3,
    (3, 2): 4,
    (4, 0): 8,
    (4, 3): 7,
    (4, 8): 6,
    (5, 5): 8,
    (6, 0): 1,
    (6, 3): 6,
    (6, 7): 3,
    (7, 1): 3,
    (7, 6): 8,
    (7, 8): 9,
    (8, 0): 7,
    (8, 3): 2,
    (8, 4): 9,
    (8, 7): 6
}

def main():
    boards = [easyBoard, hardBoard, expertBoard, evilBoard]
    for board in boards:
        game = Game(board)
        starting_time = time.time()
        game.solve()
        finish_time = time.time()
        print("*"*31)
        print(game)
        print("\tSolved board in "+str(int((finish_time-starting_time)*1000))+"ms\n\n")
        print("*"*31)

if __name__ == '__main__':
    main()