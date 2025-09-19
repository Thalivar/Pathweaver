import pygame, random
from utils import Colors, createFont, Grid, CellType, getCellColor
from algorithms import getAlgorithmByName

class Button:
    def __init__(self, x, y, width, height, text, fontSize = 24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = createFont(fontSize)
        self.hovered = False
        self.pressed = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos):
                    return "clicked"
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        return False
    
    def draw(self, screen):