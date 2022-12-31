import numpy as np
import heuristic
import display
import dijkstra


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
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, 1)
        print("\n")
        

    # Game mode 2 (heuristic)
    elif userChoice == '2':
        creategrid()
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, 2)
        print("\n")
        

    # Game mode 1 (Dijkstra)
    elif userChoice == '3':
        creategrid()
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        print("\n")

    # Game mode 2 (Dijkstra)
    elif userChoice == '4':
        creategrid()
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    # Heuristic comparison on same grid
    elif userChoice == '5':
        creategrid()
        # Mode 1 first
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, 1)
        # Then mode 2
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, 2)
        print("\n")

    # Dijkstra comparison on same grid
    elif userChoice == '6':
        creategrid()
        # Mode 1 first
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        # Then mode 2
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    elif userChoice == '7':
        creategrid()
        # Heuristic mode 1
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, 1)
        # Heuristic mode 2
        costAndPath = heuristic.heuristicpathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, 2)
        # Dijkstra mode 1
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, True)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 1")
        # Dijkstra mode 2
        costAndPath = dijkstra.dijkstrapathsolver(grid, h, w, False)
        display.displaycostandpath(grid, h, w, costAndPath, "Dijkstra 2")
        print("\n")

    # User quit game
    elif userChoice == '8':
        print('Quit game! Done.')
        break
