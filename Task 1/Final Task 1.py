"""
@author: TDAF
"""

import numpy as np
from queue import PriorityQueue


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


def dijkstrapathsolver(grid, h, w, isMode1=True):
    # Transform the entire grid to a weighted graph
    # init to large number to represent infinity (height * width)
    # each cell must be a vertex
    verticesN = h * w  
    # Set the distances to each cell
    dist = [10000 for i in range(verticesN)]
    dist = np.array(dist)
    # set the initial cost
    dist[0] = grid[0, 0]  
    # Keep track of the last cell visited when moving from cell to cell
    prev = [0 for i in range(verticesN)]
    prev = np.array(prev)
    # Set the first cell as the source cell
    prev[0] = -1  
    graph = [[10000] * verticesN for _ in range(verticesN)]
    graph = np.array(graph)
    # Loop through all the cells excluding the ones in the first and last row
    for i in range(1, h - 1):
        # cover first cell in row
        currentVertex = i * w
        vRightNeighbor = currentVertex + 1
        vUpNeighbor = currentVertex - w
        vDownNeighbor = currentVertex + w
        graph[vRightNeighbor, currentVertex] = grid[i, 0]
        graph[currentVertex, vRightNeighbor] = grid[i, 1]
        graph[vUpNeighbor, currentVertex] = grid[i, 0]
        graph[currentVertex, vUpNeighbor] = grid[i - 1, 0]
        graph[vDownNeighbor, currentVertex] = grid[i, 0]
        graph[currentVertex, vDownNeighbor] = grid[i + 1, 0]
        for j in range(1, w - 1):
            currentVertex = i * w + j
            vLeftNeighbor = currentVertex - 1
            vRightNeighbor = currentVertex + 1
            vUpNeighbor = currentVertex - w
            vDownNeighbor = currentVertex + w
            graph[vLeftNeighbor, currentVertex] = grid[i, j]
            graph[currentVertex, vLeftNeighbor] = grid[i, j - 1]
            graph[vRightNeighbor, currentVertex] = grid[i, j]
            graph[currentVertex, vRightNeighbor] = grid[i, j + 1]
            graph[vUpNeighbor, currentVertex] = grid[i, j]
            graph[currentVertex, vUpNeighbor] = grid[i - 1, j]
            graph[vDownNeighbor, currentVertex] = grid[i, j]
            graph[currentVertex, vDownNeighbor] = grid[i + 1, j]
        # cover first cell in row
        currentVertex = i * w + w - 1
        vLeftNeighbor = currentVertex - 1
        vUpNeighbor = currentVertex - w
        vDownNeighbor = currentVertex + w
        graph[vLeftNeighbor, currentVertex] = grid[i, w - 1]
        graph[currentVertex, vLeftNeighbor] = grid[i, w - 2]
        graph[vUpNeighbor, currentVertex] = grid[i, w - 1]
        graph[currentVertex, vUpNeighbor] = grid[i - 1, w - 1]
        graph[vDownNeighbor, currentVertex] = grid[i, w - 1]
        graph[currentVertex, vDownNeighbor] = grid[i + 1, w - 1]

    # now first row
    graph[0, 0] = grid[0, 0]
    graph[w - 2, w - 1] = graph[w - 1, w - 2] = grid[0, w - 1]
    j = 1
    while j < w - 1:
        currentVertex = j
        vLeftNeighbor = j - 1
        vRightNeighbor = j + 1
        graph[vLeftNeighbor, currentVertex] = grid[0, j]
        graph[currentVertex, vLeftNeighbor] = grid[0, j - 1]
        graph[vRightNeighbor, currentVertex] = grid[0, j]
        graph[currentVertex, vRightNeighbor] = grid[0, j + 1]
        if h >= 2:
            vDownNeighbor = w + j
            graph[vDownNeighbor, currentVertex] = grid[0, j]
            graph[currentVertex, vDownNeighbor] = grid[1, j]
        j += 1
    # cover last cell too
    currentVertex = j
    vLeftNeighbor = j - 1
    graph[vLeftNeighbor, currentVertex] = grid[0, j]
    graph[currentVertex, vLeftNeighbor] = grid[0, j - 1]
    if h >= 2:
        vDownNeighbor = w + j
        graph[vDownNeighbor, currentVertex] = grid[0, j]
        graph[currentVertex, vDownNeighbor] = grid[1, j]

    # now last row
    if h > 1:
        graph[(h - 2) * w, (h - 1) * w] = grid[h - 1, 0]
        graph[(h - 1) * w, (h - 2) * w] = grid[h - 2, 0]
        graph[(h - 1) * w + w - 2, (h - 1) * w + w - 1] = grid[h - 1, w - 1]
        graph[(h - 1) * w + w - 1, (h - 1) * w + w - 2] = grid[h - 1, w - 2]
        j = 1
        while j < w - 1:
            currentVertex = (h - 1) * w + j
            vLeftNeighbor = currentVertex - 1
            vRightNeighbor = currentVertex + 1
            graph[vLeftNeighbor, currentVertex] = grid[h - 1, j]
            graph[currentVertex, vLeftNeighbor] = grid[h - 1, j - 1]
            graph[vRightNeighbor, currentVertex] = grid[h - 1, j]
            graph[currentVertex, vRightNeighbor] = grid[h - 1, j + 1]
            vUpNeighbor = currentVertex - w
            graph[vUpNeighbor, currentVertex] = grid[h - 1, j]
            graph[currentVertex, vUpNeighbor] = grid[h - 2, j]
            j += 1
        # cover last cell too
        currentVertex = (h - 1) * w + j
        vLeftNeighbor = currentVertex - 1
        graph[vLeftNeighbor, currentVertex] = grid[h - 1, j]
        graph[currentVertex, vLeftNeighbor] = grid[h - 1, j - 1]
        vUpNeighbor = currentVertex - w
        graph[vUpNeighbor, currentVertex] = grid[h - 1, j]
        graph[currentVertex, vUpNeighbor] = grid[h - 2, j]

    # for debug purposes......
    #print("Dijkstra graph: ")
    #print(graph)

    q = PriorityQueue()
    q.put([grid[0, 0], 0])

    while not q.empty():
        u = q.get()[1]
        if isMode1:
            for j in range(0, verticesN):
                if j != u and dist[j] > dist[u] + graph[u, j]:
                    dist[j] = dist[u] + graph[u, j]
                    prev[j] = u
                    q.put([dist[j], j])
        else:
            urow = u // w
            ucol = u % w
            for j in range(0, verticesN):
                if j != u and dist[j] > dist[u] + abs(grid[urow, ucol] - graph[u, j]):
                    dist[j] = dist[u] + abs(grid[urow, ucol] - graph[u, j])
                    prev[j] = u
                    q.put([dist[j], j])

    # Show distances
    #print()
    #print("Dijkstra distances: ")
    #print(dist)

    # Show previous vertices
    #print()
    #print("Dijkstra previous: ")
    #print(prev)

    # Build shortest path
    pathq = PriorityQueue()
    curr = verticesN - 1
    while prev[curr] != -1:
        pathq.put(curr)
        curr = prev[curr]
    pathq.put(0)  # top-left cell is always there

    # Rebuild full path from top-left to bottom-right in string format
    pathcellsqueue = []
    s = ""
    while not pathq.empty():
        idx = pathq.get()
        s += "({},{}) ".format(idx // w, idx % w)
        pathcellsqueue.append([idx // w, idx % w])
        if not pathq.empty():
            s += "-> "

    # Show full path on screen
    #print()
    #print("Full path:")
    #print(s)

    #print()
    #print("Grid with full path found by Dijkstra:")
    #display.gridwithpath(grid, h, w, pathcellsqueue)

    #print()
    #print("Dijkstra total cost:")
    #print(dist[verticesN - 1])

    return dist[verticesN - 1], pathcellsqueue


def heuristicpathsolver(grid, h, w, isMode1=True):
    # initialise the grid size and position
    i = 0
    j = 0
    myPos = grid[i, j]
    myPath = []
    myPosForPath = (i, j)
    myPath.append(myPosForPath)
    totalCost = myPos

    # get to the last cell (bottom-right)
    # while the position is not at the last cell in the bottom right
    while (i != h - 1) and (j != w - 1):
        downCost = -1
        rightCost = -1
        if i < h - 1:
            if isMode1:
                downCost = grid[i + 1, j]
            else:
                downCost = abs(myPos - grid[i + 1, j])
        if j < w - 1:
            if isMode1:
                rightCost = grid[i, j + 1]
            else:
                rightCost = abs(myPos - grid[i, j + 1])

        # Check if the bottom of the grid had been reached and if so then 
        # Restrict downward movement and only allow right movement
        # This is because left movement is not a factor in the task
        if downCost == -1:
            totalCost += rightCost
            j = j + 1
            myPos = grid[i, j]
            myPosForPath = (i, j)
            myPath.append(myPosForPath)
        # If downwards movement is possible then allow it
        else:
            # Check if the right of the grid has reached and if so then
            # Restrict right movement and only allow downward movement
            if rightCost == -1:
                totalCost += downCost
                i = i + 1
                myPos = grid[i, j]
                myPosForPath = (i, j)
                myPath.append(myPosForPath)
            else:
                # If downwards and right movement is possible then choose
                # Between going right or going down by deciding which cost
                # is lower
                if rightCost < downCost:
                    totalCost += rightCost
                    j = j + 1
                    myPos = grid[i, j]
                    myPosForPath = (i, j)
                    myPath.append(myPosForPath)
                else:
                    totalCost += downCost
                    i = i + 1
                    myPos = grid[i, j]
                    myPosForPath = (i, j)
                    myPath.append(myPosForPath)

    # Check to see if the current position is on the last row
    # If it is then only allow right movement, and move all the 
    # way until the last cell is reached
    if i == h - 1:
        for jj in range(j + 1, w):
            myPosForPath = (i, jj)
            myPath.append(myPosForPath)
            if isMode1:
                myPos = grid[i, jj]
                totalCost += myPos
            else:
                totalCost += abs(myPos - grid[i, jj])
                myPos = grid[i, jj]
    # Check to see if the current position is on the last row
    # If it is then only allow downward movement, and move all the 
    # way unitl the last cell is reached
    elif j == w - 1:
        for ii in range(i + 1, h):
            myPosForPath = (ii, j)
            myPath.append(myPosForPath)
            if isMode1:
                myPos = grid[ii, j]
                totalCost += myPos
            else:
                totalCost += abs(myPos - grid[ii, j])
                myPos = grid[ii, j]

    return totalCost, myPath


def gamemenu():
    print('Grid game')
    print('1. Game mode 1 (heuristic)')
    print('2. Game mode 2 (heuristic)')
    print('3. Game mode 1 (Dijkstra)')
    print('4. Game mode 2 (Dijkstra)')
    print('5. Comparison mode (heuristic) - run both modes on same grid')
    print('6. Comparison mode (Dijkstra) - run both modes on same grid')
    print('7. Comparison mode (both strategies) - run all strategies, both modes on same grid')
    print('8. Quit game')
    
    
    
def creategrid():
    # Grid setup
    global n
    global h
    global w
    global grid
    n = int(input('Enter the value of `n` (grid values random between 0 and n) = '))
    h = int(input('Grid height = '))
    w = int(input('Grid width = '))
    grid = np.random.randint(0, n, size=(h, w))

    # Display the random grid
    print("Generated grid: ")
    print(grid)
    print()


while True:
    gamemenu()
    userChoice = input('Your selection = ')

    # Game mode 1 (heuristic)
    if userChoice == '1':
        creategrid()
        costAndPath = heuristicpathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, 1)
        print("\n")
        

    # Game mode 2 (heuristic)
    elif userChoice == '2':
        creategrid()
        costAndPath = heuristicpathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, 2)
        print("\n")
        

    # Game mode 1 (Dijkstra)
    elif userChoice == '3':
        creategrid()
        costAndPath = dijkstrapathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        print("\n")

    # Game mode 2 (Dijkstra)
    elif userChoice == '4':
        creategrid()
        costAndPath = dijkstrapathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    # Heuristic comparison on same grid
    elif userChoice == '5':
        creategrid()
        # Mode 1 first
        costAndPath = heuristicpathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, 1)
        # Then mode 2
        costAndPath = heuristicpathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, 2)
        print("\n")

    # Dijkstra comparison on same grid
    elif userChoice == '6':
        creategrid()
        # Mode 1 first
        costAndPath = dijkstrapathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        # Then mode 2
        costAndPath = dijkstrapathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    elif userChoice == '7':
        creategrid()
        # Heuristic mode 1
        costAndPath = heuristicpathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, 1)
        # Heuristic mode 2
        costAndPath = heuristicpathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, 2)
        # Dijkstra mode 1
        costAndPath = dijkstrapathsolver(grid, h, w, True)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        # Dijkstra mode 2
        costAndPath = dijkstrapathsolver(grid, h, w, False)
        displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    # User quit game
    elif userChoice == '8':
        print('Quit game! Done.')
        break

