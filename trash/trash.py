import pygame
from exceptions import InvalidPathError
## from main import BIN_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, Game
TRASH_SPEED = 5
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class AbstractTrash:
    name: str
    rect: pygame.Rect
    color = (255, 0, 0)  # Red color for the square
    size = (20, 20)

    def __init__(self, name: str, game, pos: list):
        self.rect = pygame.Rect(pos[0], pos[1], *self.size)
        self.name = name
        self.game = game

    def fall(self):
        # Move the trash down the screen
        self.rect.y += TRASH_SPEED

        # Delete the trash if it goes out of bounds
        if self.rect.y > SCREEN_HEIGHT:
            self.game.trash_list.remove(self)

    def render(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)