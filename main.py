# Example file showing a basic pygame "game loop"
import pygame
from trash_bins.bins import AbstractTrashBin
from trash.trash import AbstractTrash
from health.HealthBar import HealthBar
import random

# Trash traits
TRASH_SPEED = 5
TRASH_PATHS = {"TRASH" : "./assets/banana.png"}
BACKGROUND_IMAGE_PATH = "./assets/6.png"
FLOOR_IMAGE_PATH = "./assets/floor.png"

FLOOR_IMAGE_WIDTH = 18
FLOOR_IMAGE_HEIGHT = 36
FLOOR_SCALE = 4

# Bin traits
BIN_SPEED = 20
BIN_PATHS = {"GARBAGE" : "./assets/trash.png"}

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:
    screen: pygame.display
    clock: pygame.time.Clock
    running: bool
    background: pygame.image
    player: AbstractTrashBin
    trash_list: list
    spawn_timer: int
    floor: pygame.image
    health_bar: HealthBar
    score_map: {}

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.initialize_assets()
        # self.player = AbstractTrashBin(BIN_PATHS["GARBAGE"], "GarbageBin", self)
        self.player = AbstractTrashBin(self)
        self.spawn_timer = 0
        self.trash_list = []
        self.health_bar = HealthBar(SCREEN_WIDTH - 350, SCREEN_HEIGHT - 50, 300, 40, 100)
        self.game_loop()
        self.score_map = {"GARBAGE": 0,
                          "PAPER": 0,
                          "COMPOST": 0,
                          "GLASS": 0}
        pygame.quit()

    def initialize_assets(self):
        background = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background = pygame.transform.scale(background,
                                                 (SCREEN_WIDTH, SCREEN_HEIGHT))
        floor_png = pygame.image.load(FLOOR_IMAGE_PATH)
        subset_rect = pygame.Rect(91, 16, FLOOR_IMAGE_WIDTH, FLOOR_IMAGE_HEIGHT)
        floor_png = floor_png.subsurface(subset_rect)
        self.floor = pygame.transform.scale(floor_png,
                                            (FLOOR_SCALE * FLOOR_IMAGE_WIDTH, FLOOR_SCALE * FLOOR_IMAGE_HEIGHT))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_x:
                        self.player.cycle_bin()


            self.screen.blit(self.background, (0, 0))
            self.draw_floor()

            #self.screen.fill("black")
            self.handle_key_events()
            self.player.render()

            for trash in self.trash_list.copy():
                trash.fall()
                trash.render()

                if (trash.rect.colliderect(self.player.rect) and trash.rect.y + trash.size[1] > self.player.rect.y and 
                trash.rect.y + trash.size[1] < self.player.rect.y + 2 * trash.size[1] and self.player.img_index == trash.state):
                    self.trash_list.remove(trash)

                if trash.rect.y > SCREEN_HEIGHT - 60:
                    self.trash_list.remove(trash)
                    self.health_bar.hp -= self.health_bar.max_hp * 0.05

                if self.health_bar.hp == 0:
                    self.running = False
            
            self.health_bar.draw(self.screen)
            
            self.spawn_timer += 1
            if self.spawn_timer % 50 == 0 and len(self.trash_list) < 10:  # 60 ticks per second, 5 seconds * 60 ticks = 300
                x_position = random.randint(0, SCREEN_WIDTH - 50)
                # new_trash = AbstractTrash(TRASH_PATHS["TRASH"], "Garbage", self, [x_position, 0])
                state = random.randint(0, 3)
                new_trash = AbstractTrash("Garbage", self, [x_position, 0], state)
                self.trash_list.append(new_trash)

            # self.trash.render()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_floor(self):
        for i in range(SCREEN_WIDTH // (FLOOR_SCALE * FLOOR_IMAGE_WIDTH) + 1):
            self.screen.blit(self.floor, (i * FLOOR_SCALE * FLOOR_IMAGE_WIDTH, SCREEN_HEIGHT - 50))
    
    def handle_key_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_q]:
            self.running = False

if __name__ == "__main__":
    game : Game = Game()
    game.start()
