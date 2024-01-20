# Example file showing a basic pygame "game loop"
import pygame
from trash_bins.bins import AbstractTrashBin
from trash.trash import AbstractTrash
import random

# Trash traits
TRASH_SPEED = 5
TRASH_PATHS = {"TRASH" : "./assets/banana.png"}

# Bin traits
BIN_SPEED = 5
BIN_PATHS = {"GARBAGE" : "./assets/trash.jpg"}

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:
    screen: pygame.display
    clock: pygame.time.Clock
    running: bool
    player: AbstractTrashBin
    trash_list: list
    spawn_timer: int

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = AbstractTrashBin(BIN_PATHS["GARBAGE"], "GarbageBin", self)
        self.spawn_timer = 0
        self.trash_list = []        
        self.game_loop()
        pygame.quit()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("black")
            self.handle_key_events()
            self.player.render()

            for trash in self.trash_list.copy():
                trash.fall()
                trash.render()
            
            self.spawn_timer += 1
            if self.spawn_timer % 50 == 0 and len(self.trash_list) < 10:  # 60 ticks per second, 5 seconds * 60 ticks = 300
                x_position = random.randint(0, SCREEN_WIDTH - 50)
                new_trash = AbstractTrash(TRASH_PATHS["TRASH"], "Garbage", self, [x_position, 0])
                self.trash_list.append(new_trash)

            # self.trash.render()
            pygame.display.flip()
            self.clock.tick(60)

    
    def handle_key_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.pos[1] -= 5
        if keys[pygame.K_DOWN]:
            self.player.pos[1] += 5
        if keys[pygame.K_q]:
            self.running = False

if __name__ == "__main__":
    game : Game = Game()
    game.start()
