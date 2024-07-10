import random
import pygame
from queue import PriorityQueue
import numpy as np

CELL_PATH_N = 0x01
CELL_PATH_E = 0x02
CELL_PATH_S = 0x04
CELL_PATH_W = 0x08
CELL_VISITED = 0x10

class Node:
    def __init__(self, value):
        self.data = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None  # empty stack
        self.n = 0

    def isempty(self):
        return self.top == None
    
    def push(self, value):  # Insert at Head
        new_node = Node(value)
        if self.top == None:
            self.top = new_node
            self.n = 1
            return
        
        new_node.next = self.top
        self.top = new_node
        self.n += 1

    def pop(self):  # Delete at head and returns the value
        if self.top == None:
            return 'Empty Linked list!'
        elif self.top.next == None:
            val = self.top.data
            self.top = None
            self.n -= 1
            return val
        else:
            val = self.top.data
            self.top = self.top.next
            self.n -= 1
            return val
        
    def peek(self):
        if self.isempty():
            return "Stack Empty"
        
        return self.top.data

    
class Maze:
    def __init__(self, mazeH, mazeW):
        self.mazeH = mazeH
        self.mazeW = mazeW
        self.visitedCells = 0
        self.pathWidth = 10
        self.stack = Stack()
        self.maze = [0x00] * (mazeW * mazeH)
        self.maze_grid =[]
        self.searchGrid = {}
        self.fwdPath = {}

    def generateMaze(self):

        self.stack.push((0, 0))
        self.maze[0] |= CELL_VISITED
        self.visitedCells = 1

        offset = lambda x, y: (self.stack.peek()[1] + y) * self.mazeW + (self.stack.peek()[0] + x)

        while self.visitedCells < self.mazeW * self.mazeH:
            # Create set of unvisited neighbours
            neighbours = []

            # North neighbour
            if self.stack.peek()[1] > 0:
                if not (self.maze[offset(0, -1)] & CELL_VISITED):
                    neighbours.append(0)

            # East neighbour
            if self.stack.peek()[0] < self.mazeW - 1:
                if not (self.maze[offset(1, 0)] & CELL_VISITED):
                    neighbours.append(1)

            # South neighbour
            if self.stack.peek()[1] < self.mazeH - 1:
                if not (self.maze[offset(0, 1)] & CELL_VISITED):
                    neighbours.append(2)

            # West neighbour
            if self.stack.peek()[0] > 0:
                if not (self.maze[offset(-1, 0)] & CELL_VISITED):
                    neighbours.append(3)

            if len(neighbours) != 0:
                nextCell_dir = neighbours[random.randint(0, len(neighbours) - 1)]

                # Creating path between cells
                if nextCell_dir == 0:  # North
                    self.maze[offset(0, 0)] |= CELL_PATH_N
                    self.maze[offset(0, -1)] |= CELL_PATH_S | CELL_VISITED
                    self.stack.push((self.stack.peek()[0], self.stack.peek()[1] - 1))

                elif nextCell_dir == 1:  # East
                    self.maze[offset(0, 0)] |= CELL_PATH_E
                    self.maze[offset(1, 0)] |= CELL_PATH_W | CELL_VISITED
                    self.stack.push((self.stack.peek()[0] + 1, self.stack.peek()[1]))

                elif nextCell_dir == 2:  # South
                    self.maze[offset(0, 0)] |= CELL_PATH_S
                    self.maze[offset(0, 1)] |= CELL_PATH_N | CELL_VISITED
                    self.stack.push((self.stack.peek()[0], self.stack.peek()[1] + 1))

                else:  # West
                    self.maze[offset(0, 0)] |= CELL_PATH_W
                    self.maze[offset(-1, 0)] |= CELL_PATH_E | CELL_VISITED
                    self.stack.push((self.stack.peek()[0] - 1, self.stack.peek()[1]))

                # Cell visited
                self.visitedCells += 1
                self.draw_maze()
                pygame.time.wait(10)

            else:  # Backtrack
                self.stack.pop()
        
        self.draw_maze()
        maze2D = np.reshape(self.maze,(self.mazeW,self.mazeH))
        for i in range(self.mazeW):
            for j in range(self.mazeH):
                pathDir = { 'N':0,'E':0,'S':0,'W':0 }
                val = maze2D[i][j]
                if val & CELL_PATH_N != 0:
                    pathDir['N'] = 1
                if val & CELL_PATH_E != 0:
                    pathDir['E'] = 1
                if val & CELL_PATH_S != 0:
                    pathDir['S'] = 1
                if val & CELL_PATH_W != 0:
                    pathDir['W'] = 1
                self.maze_grid.append({(i,j):pathDir})

        for item in self.maze_grid:
            self.searchGrid.update(item)

        
        for k,v in self.searchGrid.items():
            if k[0] == 0:
                v['N'] = 0
            if k[1] == 0:
                v['W'] = 0
            if k[0] == self.mazeH-1:
                v['S'] = 0
            if k[1] == self.mazeW-1:
                v['E'] = 0
        
        self.fwdPath = self.astar((0,0),(self.mazeW-1,self.mazeH-1))

        index = (0,0)
        br_cond = 1

        while br_cond:
            for k,v in self.fwdPath.items():
                if k == index:
                    pygame.draw.rect(screen, GREEN,((self.pathWidth + 1) * k[1] , (self.pathWidth + 1) * k[0] , self.pathWidth, self.pathWidth) )
                    index = v
                    if index == (self.mazeW-1,self.mazeH-1):
                        pygame.draw.rect(screen, GREEN,((self.pathWidth + 1) * v[1] , (self.pathWidth + 1) * v[0] , self.pathWidth, self.pathWidth))
                        pygame.display.flip()
                        br_cond = 0
                        break
                    pygame.display.flip()
                    pygame.time.wait(50)

    def draw_maze(self):
        # Draw the maze
        screen.fill(BG_COLOR)
        for x in range(self.mazeW):
            for y in range(self.mazeH):
                
                if self.maze[y * self.mazeW + x] & CELL_VISITED:
                    color = WHITE
                else:
                    color = BLUE

                # Draw the cells
                pygame.draw.rect(screen, color, ((self.pathWidth + 1) * x , (self.pathWidth + 1) * y , self.pathWidth, self.pathWidth))

                # Draw the paths (east and south)
                if self.maze[y * self.mazeW + x] & CELL_PATH_E:
                    pygame.draw.rect(screen, WHITE, ((self.pathWidth + 1) * x + self.pathWidth, (self.pathWidth + 1) * y, 1, self.pathWidth))
                if self.maze[y * self.mazeW + x] & CELL_PATH_S:
                    pygame.draw.rect(screen, WHITE, ((self.pathWidth + 1) * x, (self.pathWidth + 1) * y + self.pathWidth, self.pathWidth, 1))

        # Updating display

        for py in range(self.pathWidth):
            for px in range(self.pathWidth):
                x = self.stack.peek()[0] * (self.pathWidth + 1) + px
                y = self.stack.peek()[1] * (self.pathWidth + 1) + py
                pygame.draw.rect(screen, RED, (x, y, self.pathWidth, 1))

        pygame.display.flip()

    
    """********************  A STAR IMPLEMENTATION    ************************"""

    def h(self,node,goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    def astar(self,start,goal):
        g_val = {cell: float('inf') for cell in self.searchGrid}
        g_val[start] = 0
        f_val = {cell: float('inf') for cell in self.searchGrid}
        f_val[start] = self.h(start,goal) + 0 #g_val is 0

        pq = PriorityQueue()
        pq.put((self.h(start,goal),self.h(start,goal),start))
        aPath = {}
        while not pq.empty():
            current = pq.get()[2]

            if current == goal:
                break
            
            for d in 'NESW':
                if self.searchGrid[current][d] == 1:
                    if d == 'N':
                        childCell = (current[0]-1,current[1])
                    if d == 'E':
                        childCell = (current[0],current[1]+1)
                    if d == 'S':
                        childCell = (current[0]+1,current[1])
                    if d == 'W':
                        childCell = (current[0],current[1]-1)

                    temp_g_val = g_val[current] + 1
                    temp_f_val = temp_g_val + self.h(childCell,goal)

                    if temp_f_val < f_val[childCell]:
                        g_val[childCell] = temp_g_val
                        f_val[childCell] = temp_f_val
                        pq.put((temp_f_val,self.h(childCell,goal),childCell))

                        ## aPath[childCell] = current to prevent Key conflict
                        aPath[childCell] = current

        
        forwardPath = {}
        cell = goal
        try:
            while cell != start:
                    forwardPath[aPath[cell]] = cell  #value of aPath is made key of forward path
                    cell = aPath[cell]
        except KeyError:
                print('No Path Found')

        return forwardPath  


mazeD = int(input("Enter Square Maze Dimension: "))
pathWidth = 10


pygame.init()

# Screen Display settings
SCREEN_WIDTH = mazeD * (pathWidth + 1)  # = mazeWidth * (pathWidth + 1)
SCREEN_HEIGHT = mazeD * (pathWidth + 1) # = mazeHeight * (pathHeight + 1)
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
SOURCE_PURPLE = (156, 96, 181)
DEST_PINK = (230, 64, 216)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator")

# generating Maze
maze = Maze(mazeH = mazeD, mazeW = mazeD)
maze.generateMaze()
pygame.draw.rect(screen,SOURCE_PURPLE,(0,0,pathWidth,pathWidth))
pygame.draw.rect(screen,DEST_PINK,((mazeD-1)*11,(mazeD-1)*11,pathWidth,pathWidth))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
