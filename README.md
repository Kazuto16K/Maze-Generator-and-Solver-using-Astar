# Maze Generator and Solver using Python

## Maze Generation Algorithm:
I have used **Recursive backtracking** to generate the Maze.
Recursive backtracking is a depth-first search algorithm used for solving constraint satisfaction problems, such as maze generation, pathfinding, and puzzle solving. The general approach involves exploring possible solutions recursively and backtracking when a dead end is reached.

## I have attached the images explaining the algorithm

![Maze_gen1](https://github.com/Kazuto16K/Maze-Generator-and-Solver-using-Astar/assets/112095521/167a8f9b-d323-41e5-abbb-2cc20156af67)

![Maze_gen2](https://github.com/Kazuto16K/Maze-Generator-and-Solver-using-Astar/assets/112095521/4afa2b36-4410-4f74-9cbf-43c869cb8521)

## Path Search Algorithm:
For Getting the path, I have used **A star search** algorithm
The A* (A-star) search algorithm is a widely used pathfinding and graph traversal algorithm. It is particularly effective for finding the shortest path from a starting node to a goal node in a weighted graph. A* combines the advantages of Dijkstra's algorithm and Greedy Best-First-Search by using a heuristic to guide its search.
Here , i have used Manhattan Distance as the heuristic function.

## Demonstration of Working 

https://github.com/Kazuto16K/Maze-Generator-and-Solver-using-Astar/assets/112095521/ccdbe632-720b-4b52-a6ec-eefe863ee6e2

## Steps to use:
  - pip install pygame
  - download the code
  - Enter dimension of the Maze
  - **Make sure python is installed**


### Note
I have used Pygame module of python for the visual demonstration. I implemented my own stack. (There was no need to do so , but since I already a previous implemented stack using LinkedList, so why not use it)

