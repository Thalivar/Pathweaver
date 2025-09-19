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
        if self.pressed:
            color = Colors.buttonPressed
        elif self.hovered:
            color = Colors.buttonHover
        else:
            color = Colors.buttonNormal
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, Colors.textPrimary, self.rect, 2)
        textSurface = self.font.render(self.text, True, Colors.textPrimary)
        textRect = textSurface.getRect(center = self.rect.center)
        screen.blit(textSurface, textRect)

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.getWidth()
        self.height = screen.getHeight()
        self.titleFont = createFont(48)
        self.subtitleFont = createFont(24)

        buttonWidth = 300
        buttonHeight = 60
        buttonSpacing = 20
        startY = self.height // 2

        self.buttons + {
            "pathfinding": Button(
                self.width // 2 - buttonWidth // 2,
                startY,
                buttonWidth,
                buttonHeight,
                "Pathweaving Arts",
                28
            ),
            "sorting": Button(
                self.width // 2 - buttonWidth // 2,
                startY + buttonHeight + buttonSpacing,
                buttonWidth,
                buttonHeight,
                "Ordering Magic",
                28
            ),
            "quit": Button(
                self.width // 2 - buttonWidth // 2,
                startY + buttonHeight + buttonSpacing,
                buttonWidth,
                buttonHeight,
                "Exit the Realm",
                28
            )
        }
    
    def handleEvent(self, event):
        for name, button in self.buttons.items():
            if button.handleEvent(event) == "clicked":
                return name
        return None
    
    def update(self):
        pass

    def draw(self):
        titleText = self.titleFont.render("PathWeaver", True, Colors.textPrimary)
        tittleRect = titleText.getRect(center = (self.width //2, self.height // 4))
        self.screen.blit(titleText, tittleRect)

        subtitleText = self.subtitleFont.render("Master of the Algorithmic Destinies", True, Colors.textSecondary)
        subtitleRect = subtitleText.getRect(center = (self.width // 2, self.height // 4 + 60))
        self.screen.blit(subtitleText, subtitleRect)

        for button in self.button.values():
            button.draw(self.screen)
