import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
BIN_SPEED = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GARBAGE_NAME = "GARBAGE"
PAPER_NAME = "PAPER"
COMPOST_NAME = "COMPOST"
GLASS_NAME = "GLASS"

BIN_NAMES = [GARBAGE_NAME, PAPER_NAME, COMPOST_NAME, GLASS_NAME]

BIN_IMAGES = {GARBAGE_NAME: "./assets/black.png",
              PAPER_NAME: "./assets/blue.png",
              GLASS_NAME: "./assets/red.png",
              COMPOST_NAME: "./assets/green.png"}

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
    imgs: pygame.image
    img_index: int

    def __init__(self, game):
        self.name = GARBAGE_NAME
        # self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.game = game
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, *self.size)
        self.img_index = 0 ## default bin is GARBAGE
        try:
            self.imgs = []
            for bin_name in BIN_NAMES:
                img = pygame.image.load(BIN_IMAGES[bin_name])
                img = pygame.transform.scale(img, self.size)
                self.imgs.append(img)
        except IOError:
            raise InvalidPathError("This image file does not exist!")

    def move_left(self):
        self.rect.x -= BIN_SPEED
    
    def move_right(self):
        self.rect.x += BIN_SPEED

    def cycle_bin(self):
        self.img_index = (self.img_index + 1) % len(BIN_IMAGES)

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0, 0), self.rect)
        self.game.screen.blit(self.imgs[self.img_index], (self.rect.x, self.rect.y))
        #self.game.screen.draw.rect((0, 0, 0, 0), self.rect)