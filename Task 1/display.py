import numpy as np


# snippet for bcolors from https://www.codegrepper.com/code-examples/python/python+change+print+color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def showpath(path):
    # display all cells as x,y pairs and -> between them
    for row in path[:-1]:
        print(row, end=" -> ")
    print(path[-1])


def gridwithpath(grid, h, w, path):
    path = np.array(path)
    str = ""
    for i in range(0, h):
        for j in range(0, w):
            inPath = False
            for k in range(0, len(path)):
                if i == path[k, 0] and j == path[k, 1]:
                    inPath = True
                    break
            if inPath:
                str += "{} {}{}".format(bcolors.WARNING, grid[i, j], bcolors.ENDC)
            else:
                str += " {}".format(grid[i, j])
        print(str)
        str = ""


def displaycostandpath(grid, h, w, costAndPath, mode):
    print('Mode ', mode, ' cost = ', costAndPath[0])
    print('Mode ', mode, ' path:')
    showpath(costAndPath[1])
    print('Mode ', mode, ' grid with path:')
    gridwithpath(grid, h, w, costAndPath[1])
