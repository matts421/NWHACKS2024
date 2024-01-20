import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
TRASH_SPEED = 2
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class AbstractTrash:
    img: pygame.image
    name: str
    pos: list # (x, y) position tuple
    BIN_HEIGHT = 50

    def __init__(self, img_path: str, name: str, game, pos: list):
        try:
            self.img = pygame.image.load(img_path)
        except IOError:
            raise InvalidPathError("This image file does not exist!")
        
        self.name = name
        self.pos = pos
        self.game = game

    def fall(self):
        # Move the trash down the screen
        self.pos[1] += TRASH_SPEED

        # Delete the trash if it goes out of bounds
        if self.pos[1] > SCREEN_HEIGHT:
            self.game.trash_list.remove(self)
            del self

    def render(self):
        self.game.screen.blit(self.img, self.pos)