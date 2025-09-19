import random, pygame
from enum import Enum
from collections import deque

class GameState(Enum):
    mainMenu = "mainMenu"
    pathfinding = "pathfinding"
    sorting = "sorting"

class Colors:
    # -=+=- UI & Background -=+=-
    background = (15, 15, 20) # A dark gray/blue
    textPrimary = (220, 220, 220) # Soft white
    textSecondary = (150, 150, 160) # Mute gray
    buttonNormal = (50, 50, 60) # Dark gray
    buttonHover = (80, 80, 100) # Lighter gray
    buttonPressed = (100, 100, 120) # Even lighter gray
    gridBackground = (30, 30, 40) # Dark gray
    gridLine = (70, 70, 80) # Soft gray

    # -=+=- Pathfinding Grid -=+=-
    wall = (60, 40, 40) # Dark red/brown ish
    empty = (200, 200, 210) # Pale gray
    start = (100, 200, 255) # Cyan
    end = (255, 100, 120) # Coral red
    visited = (140, 160, 255) # Indigo
    path = (255, 220, 120) # Warm yellow
    current = (255, 140, 60) # Vibrant orange

    # -=+=- Array Visualization -=+=-
    arrayDefault = (120, 120, 140) # Gray
    arrayComparing = (255, 120, 120) # Red
    arraySwapping = (255, 200, 100) # Amber
    arraySorted = (100, 220, 150)

class CellType(Enum):
    empty = 0
    wall = 1
    start = 2
    end = 3
    visited = 4
    path = 5
    current = 6

class Grid:
    def __init__(self, width, height, cellSize = 20):
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.cols= width // cellSize
        self.rows = height // cellSize
        self.grid = [[CellType.empty for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.end = None
    
    def getCell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    
    def setCell(self, row, col, cellType):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if cellType == CellType.start:
                if self.start:
                    self.grid[self.start[0]][self.start[1]] = CellType.empty
                self.start = (row, col)
            
            elif cellType == CellType.end:
                if self.end:
                    self.grid[self.start[0]][self.start[1]] = CellType.empty
                self.end = (row, col)
            
            self.grid[row][col] = cellType
    
    def clearPath(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] in [CellType.visited, CellType.path, CellType.current]:
                    self.grid[row][col] = CellType.empty
    
    def generateMaze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = CellType.empty
        
        for _ in range(self.rows * self.cols // 4):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.grid[row][col] = CellType.wall
        
        self.setCell(1, 1, CellType.start)
        self.setCell(self.rows - 2, self.cols - 2, CellType.end)

        if self.start:
            self.grid[self.start[0]][self.start[1]] = CellType.start
        if self.end:
            self.grid[self.end[0]][self.end[1]] = CellType.end
    
    def getNeighbors(self, row, col):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            newRow = row + dr
            newCol = col + dc

            if (0 <= newRow < self.rows and 0 <= newCol < self.cols and self.grid[newRow][newCol] != CellType.wall):
                neighbors.append((newRow, newCol))
        
        return neighbors

def getCellColor(cellType):
    colorMap = {
        CellType.empty: Colors.empty,
        CellType.wall: Colors.wall,
        CellType.start: Colors.start,
        CellType.end: Colors.end,
        CellType.visited: Colors.visited,
        CellType.path: Colors.path,
        CellType.current: Colors.current
    }
    return colorMap.get(cellType, Colors.empty)

def createFont(size):
    fonts = ["Arial", "Helvetica", "Sans-serif"]
    for fontName in fonts:
        try:
            return pygame.font.SysFont(fontName, size)
        except:
            continue
    return pygame.font.Font(None, size)