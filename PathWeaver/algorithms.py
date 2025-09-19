import heapq, random
from utils import CellType
from collections import deque

class AlgorithmRunner:
    def __init__(self):
        self.steps = []
        self.currentStep = 0
        self.finished = False
        self.foundPath = False

    def nextStep(self):
        if self.currentStep < len(self.steps):
            step = self.steps[self.currentStep]
            self.currentStep += 1
            return step
        return None
    
    def reset(self):
        self.currentStep = 0
        self.finished = False
        self.foundPath = False

class PathfindingAlgorithm(AlgorithmRunner):
    def __init__(self, grid):
        super.__init__()
        self.grid = grid
        self.path = []
    
    def reconstructPath(self, cameFrom, current):
        path = []
        while current in cameFrom:
            path.append(current)
            current = cameFrom[current]
        return list(reversed(path))

class BreadthFirstSearch(PathfindingAlgorithm):
    def run(self):
        if not self.grid.start or not self.grid.end:
            return
        
        self.steps = []
        start = self.grid.start
        end = self.grid.end
        queue = deque([start])
        visited = set([start])
        cameFrom = {}
        self.steps.append(("setCurrent", start))

        while queue:
            current = queue.popleft()
            self.steps.append(("setCurrent", current))

            if current == end:
                path = self.reconstructPath(cameFrom, current)
                for pos in path:
                    if pos != start and pos != end:
                        self.steps.append(("setPath", pos))
                    self.foundPath = True
                    self.steps.append(("finished", True))
                    break
            
            for neighbor in self.grid.getNeighbors(current[0], current[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    cameFrom[neighbor] = current
                    queue.append(neighbor)
                    if neighbor != end:
                        self.steps.append(("setVisited", neighbor))
            
        if not self.foundPath:
            self.steps.append(("finished", False))

class DepthFirstSearch(PathfindingAlgorithm):
    def run(self):
        if not self.grid.start or not self.grid.end:
            return
        
        self.steps = []
        start = self.grid.start
        end = self.grid.end
        stack = [start]
        visited = set()
        cameFrom = {}

        while stack:
            current = stack.pop()
            self.steps.append(("setCurrent", current))

            if current in visited:
                continue

            visited.add(current)
            if current != start and current != end:
                self.steps.append(("setVisited", current))
            
            if current == end:
                path = self.reconstructPath(cameFrom, current)
                for pos in path:
                    if pos != start and pos != end:
                        self.steps.append(("setPath", pos))
                
                self.foundPath = True
                self.steps.append(("finished", True))
                break

            neighbors = self.grid.getNeighbors(current[0], current[1])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    cameFrom[neighbor] = current
                    stack.append(neighbor)
        
        if not self.foundPath:
            self.steps.append(("finished", False))

class AStar(PathfindingAlgorithm):
    def run(self):
        if not self.grid.start or self.grid.end:
            return
        
        self.steps = []
        start = self.grid.start
        end = self.grid.end

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        openSet = [(0, start)]
        cameFrom = {}
        gScore = {start: 0}
        fScore = {start: heuristic(start, end)}

        while openSet:
            current = heapq.heappop(openSet)[1]
            self.steps.append(("setCurrent", current))

            if current == end:
                path = self.reconstructPath(cameFrom, current)
                for pos in path:
                    if pos != start and pos != end:
                        self.steps.append(("setPath", pos))
                self.foundPath = True
                self.steps.append(("finished", True))
                break

            for neighbor in self.grid.getNeighbors(current[0], current[1]):
                tentativeGScore = gScore[current] + 1
                if neighbor not in gScore or tentativeGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentativeGScore
                    fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, end)
                    heapq.heappush(openSet, (fScore[neighbor], neighbor))

                    if neighbor != end:
                        self.steps.append(("setVisited", neighbor))
        
        if not self.foundPath:
            self.steps.append(("finished", False))

class SortingAlgorithm(AlgorithmRunner):
    def __init__(self, array):
        super().__init__()
        self.array = array[:]
        self.originalArray = array[:]

    def resetArray(self):
        self.array = self.originalArray[:]

class BubbleSort(SortingAlgorithm):
    def run(self):
        self.steps = []
        n = len(self.array)

        for i in range(n):
            for j in range(0, n - i - 1):
                self.steps.append(("compare", j, j + 1))

                if self.array[i] > self.array[j + 1]:
                    self.steps.append(("swap", j, j + 1))
                    self.array[j] = self.array[j + 1]
                    self.array[j + 1] = self.array[j]
            
            self.steps.append(("sorted", n - i - 1))
        self.steps.append(("finished", True))

class QuickSort(SortingAlgorithm):
    def run(self):
        self.steps = []
        self.quickSort(0, len(self.array) - 1)
        self.steps.append(("finished"), True)
    
    def quickSort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quickSort(low, pi -1)
            self.quickSort(pi + 1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        self.steps.append(("pivot", high))
        i = low - 1

        for j in range(low, high):
            self.steps.append(("compare", j, high))
            if self.array[j] <= pivot:
                i += 1
                if i != j:
                    self.steps.append(("swap", i, j))
                    self.array[i] = self.array[j]
                    self.array[j] = self.array[i]
        
        if i + 1 != high:
            self.steps.append(("swap", i + 1, high))
            self.array[i + 1] = self.array[high]
            self.array[high] = self.array[i + 1]
        
        return i + 1

def getAlgorithmByName(name, *args):
    algoritms = {
        "bfs": BreadthFirstSearch,
        "dfs": DepthFirstSearch,
        "aster": AStar,
        "bubbleSort": BubbleSort,
        "quickSort": QuickSort
    }

    if name in algoritms:
        return algoritms[name](*args)
    return None