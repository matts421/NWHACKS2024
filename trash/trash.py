import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
TRASH_SPEED = 3
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GARBAGE_NAME = "GARBAGE"
PAPER_NAME = "PAPER"
COMPOST_NAME = "COMPOST"
GLASS_NAME = "GLASS"

TRASH_NAMES = [GARBAGE_NAME, PAPER_NAME, COMPOST_NAME, GLASS_NAME]

class AbstractTrash:
    name: str
    rect: pygame.Rect
    color = (255, 0, 0)
    size = (20, 20)
    state = int

    def __init__(self, name: str, game, pos: list, index: int):
        self.rect = pygame.Rect(pos[0], pos[1], *self.size)
        self.name = name
        self.game = game
        self.state = index
        # will be replaced
        if (self.state == 0):
            self.color = (0, 0, 0)
        elif (self.state == 1):
            self.color = (0, 0, 255)
        elif (self.state == 2):
            self.color = (0, 255, 0)
        elif (self.state == 3):
            self.color = (255, 0, 0)

    def fall(self):
        # Move the trash down the screen
        self.rect.y += TRASH_SPEED

    def render(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)