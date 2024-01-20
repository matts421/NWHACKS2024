import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
BIN_SPEED = 5
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class AbstractTrashBin:
    img: pygame.image
    name: str
    pos: list # (x, y) position tuple
    BIN_HEIGHT = 50

    def __init__(self, img_path: str, name: str, game):
        try:
            self.img = pygame.image.load(img_path)
        except IOError:
            raise InvalidPathError("This image file does not exist!")
        
        self.name = name
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.game = game

    def move_left(self):
        self.pos[0] -= BIN_SPEED
    
    def move_right(self):
        self.pos[0] += BIN_SPEED

    def cycle_bin(self):
        ...

    def render(self):
        self.game.screen.blit(self.img, self.pos)