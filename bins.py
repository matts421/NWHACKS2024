import pygame
from exceptions import InvalidPathError

BIN_SPEED = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GARBAGE_NAME = "GARBAGE"
PAPER_NAME = "PAPER"
COMPOST_NAME = "COMPOST"
GLASS_NAME = "GLASS"

BIN_NAMES = [GARBAGE_NAME, PAPER_NAME, COMPOST_NAME, GLASS_NAME]

BIN_IMAGES = {GARBAGE_NAME: "./assets/bins/black.png",
              PAPER_NAME: "./assets/bins/blue.png",
              GLASS_NAME: "./assets/bins/red.png",
              COMPOST_NAME: "./assets/bins/green.png"}

class TrashBin:
    rect: pygame.Rect
    size = (130, 100)
    imgs: pygame.image
    img_index: int

    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, *self.size)
        self.img_index = 0 ## default bin is GARBAGE
        try:
            self.imgs = []
            for bin_name in BIN_NAMES:
                img = pygame.image.load(BIN_IMAGES[bin_name])
                img_w, img_h = img.get_size()
                img = pygame.transform.scale(img, (img_w // 3, img_h // 3))
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
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.rect)
        self.game.screen.blit(self.imgs[self.img_index], (self.rect.x - self.size[0] // 5, self.rect.y - self.size[1] // 7))