import pygame
import sys
from ui import MainMenu, AlgorithmVisualizer
from utils import Colors, GameState

class PathWeaver:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.mainMenu
        self.mainMenu = MainMenu(self.screen)
        self.visualizer = AlgorithmVisualizer(self.screen)
        pygame.display.set_caption("Pathweaver")

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == GameState.mainMenu:
                action = self.mainMenu.handleEvent(event)
                if action:
                    if action == "pathfinding":
                        self.state = GameState.pathfinding
                        self.visualizer.setMode("pathfinding")
                    elif action == "sorting":
                        self.state = GameState.sorting
                        self.visualizer.setMMode("sorting")
                    elif action == "quit":
                        self.running = False

            elif self.state in [GameState.pathfinding, GameState.sorting]:
                action = self.visualizer.handleEvent(event)
                if action == "backToMenu":
                    self.state = GameState.mainMenu
    
    def update(self):
        if self.state == GameState.mainMenu:
            self.mainMenu.update()
        elif self.state in [GameState.pathfinding, GameState.sorting]:
            self.visualizer.update()
    
    def draw(self):
        self.screen.fill(Colors.background)

        if self.state == GameState.mainMenu:
            self.mainMenu.draw()
        elif self.state in [GameState.pathfinding, GameState.sorting]:
            self.visualizer.draw()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PathWeaver()
    game.run()