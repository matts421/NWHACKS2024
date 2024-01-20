import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
BIN_SPEED = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class AbstractTrashBin:
    # img: pygame.image
    # name: str
    # pos: list # (x, y) position tuple
    # BIN_HEIGHT = 50

    # def __init__(self, img_path: str, name: str, game):
    #     try:
    #         self.img = pygame.image.load(img_path)
    #     except IOError:
    #         raise InvalidPathError("This image file does not exist!")
        
    #     self.name = name
    #     self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    #     self.game = game

    name: str
    rect: pygame.Rect
    color = (0, 255, 0)
    # pos: list # (x, y) position tuple
    # BIN_HEIGHT = 50
    size = (100, 120)

    def __init__(self, name: str, game):
        
        self.name = name
        # self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.game = game
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, *self.size)

    def move_left(self):
        self.rect.x -= BIN_SPEED
    
    def move_right(self):
        self.rect.x += BIN_SPEED

    def cycle_bin(self):
        ...

    def render(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)