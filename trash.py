import pygame
from exceptions import InvalidPathError
import os
import random
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
TRASH_SPEED = 3
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GARBAGE_NAME = "GARBAGE"
PAPER_NAME = "PAPER"
COMPOST_NAME = "COMPOST"
GLASS_NAME = "GLASS"

TRASH_NAMES = [GARBAGE_NAME, PAPER_NAME, COMPOST_NAME, GLASS_NAME]

class Trash:
    rect: pygame.Rect
    size = (5, 5)
    state = int
    img: pygame.image

    def __init__(self, game, pos: tuple, index: int):
        self.rect = pygame.Rect(pos[0], pos[1], *self.size)
        self.game = game
        self.state = index

        if (self.state == 0): folder_path = "./assets/trash/trash"
        elif (self.state == 1): folder_path = "./assets/trash/paper"
        elif (self.state == 2): folder_path = "./assets/trash/organic"
        elif (self.state == 3): folder_path = "./assets/trash/glass"

        file_list = [file for file in os.listdir(folder_path) if file.endswith(".png")]
        imgs = []
        for file in file_list:
            img = pygame.image.load(f"{folder_path}/{file}")
            img_w, img_h = img.get_size()
            img = pygame.transform.scale(img, (img_w * 2, img_h * 2))
            imgs.append(img)
        self.img = imgs[random.randint(0, len(imgs) - 1)]

    def fall(self):
        # Move the trash down the screen
        self.rect.y += TRASH_SPEED

    def render(self):
        pygame.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        self.game.screen.blit(self.img, (self.rect.x - 25, self.rect.y - 15))