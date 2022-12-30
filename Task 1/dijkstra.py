import numpy as np
import display
from queue import PriorityQueue


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