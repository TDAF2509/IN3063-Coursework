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
