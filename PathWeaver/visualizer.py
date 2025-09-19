import pygame, random
from utils import Colors, createFont, Grid, CellType, getCellColor
from algorithms import getAlgorithmByName

class AlgorithmVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.getWidth()
        self.height = screen.getHeight()
        self.mode = "pathfinding"
        self.gridAreaWidth = 800
        self.gridAreaHeight = 600
        self.gridX = 50
        self.gridY = 100
        self.grid = Grid(self.gridAreaWidth, self.gridAreaHeight, 15)
        self.grid.generateMaze()
        self.currentAlgoritm = None
        self.algorithmName = "bfs"
        self.player = False
        self.stepDelay = 50
        self.lastStepTime = 0
        self.font = createFont(20)
        self.smallFont = createFont(16)
        self.createButtons()
        self.array = [random.randint(10, 200) for _ in range(50)]
        self.arrayAlgoritm = None
        self.comparingIndices = []
        self.swappingIndices = []
        self.sortedIndices = []

        def createButtons(self):
            buttonX = self.gridX + self.gridAreaWidth + 20
            buttonY = self.gridY
            buttonWidth = 150
            buttonHeight = 40
            spacing = 10
            self.buttons = {}

            if self.mode == "pathfinding":
                algorithms = [
                    ("bfs", "BFS"),
                    ("dfs", "DFS"),
                    ("astar", "A*")
                ]
            else:
                algorithms = [
                    ("bubbleSort", "Bubble Sort"),
                    ("quickSort", "Quick Sort")
                ]

            