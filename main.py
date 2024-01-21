# Example file showing a basic pygame "game loop"
import pygame, sys
from button.button import Button
from bins import TrashBin
from trash import Trash
from health.HealthBar import HealthBar
import random

#MENU_BG = pygame.image.load("assets/menu/Background.png")
MENU_BG = pygame.image.load("assets/menu/bluespace.png")
RETRY_BG = pygame.image.load("./assets/menu/title.png")
DEAD_EARTH = pygame.image.load("./assets/menu/deadearth.png")
WIN_CONDITION = 15

BLACK_BIN = pygame.image.load("./assets/bins/black.png")
RED_BIN = pygame.image.load("./assets/bins/red.png")
GREEN_BIN = pygame.image.load("./assets/bins/green.png")
BLUE_BIN = pygame.image.load("./assets/bins/blue.png")
# EARTH_GIF = "./assets/menu/bigearth.gif"

# Trash traits
TRASH_SPEED = 5
## BACKGROUND_IMAGE_PATH = "./assets/6.png"
BACKGROUND_IMAGE_PATH = "./assets/space.png"
FLOOR_IMAGE_PATH = "./assets/floor.png"
HEALTHY_EARTH = pygame.image.load("./assets/menu/bigearth.png")
subset_rect = pygame.Rect(0, 0, 400, 400)
HEALTHY_EARTH = HEALTHY_EARTH.subsurface(subset_rect)

FLOOR_IMAGE_WIDTH = 18
FLOOR_IMAGE_HEIGHT = 36
FLOOR_SCALE = 4

# Bin traits
BIN_SPEED = 20
BIN_PATHS = {"GARBAGE" : "./assets/trash.png"}

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GARBAGE_NAME = "GARBAGE"
PAPER_NAME = "PAPER"
COMPOST_NAME = "COMPOST"
GLASS_NAME = "GLASS"

BIN_NAMES = [GARBAGE_NAME, PAPER_NAME, COMPOST_NAME, GLASS_NAME]

EASY = "EASY"
HARD = "HARD"
DIFFICULTY = {EASY: 10, HARD: 20}

class Game:
    screen: pygame.display
    clock: pygame.time.Clock
    running: bool
    background: pygame.image
    player: TrashBin
    trash_list: list
    spawn_timer: int
    floor: pygame.image
    health_bar: HealthBar
    score_map: dict
    difficulty: str
    loss: bool

    def start(self):
        pygame.init()
        pygame.display.set_caption("Waste Invaders")
        pygame.display.set_icon(HEALTHY_EARTH)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.initialize_assets()
        self.player = TrashBin(self)
        self.spawn_timer = 0
        self.trash_list = []
        self.health_bar = HealthBar(SCREEN_WIDTH - 416, 35, 385, 15, 100)
        self.score_map = {GARBAGE_NAME: 0,
                          PAPER_NAME: 0,
                          COMPOST_NAME: 0,
                          GLASS_NAME: 0}
        self.trash_speed = 3
        self.difficulty = EASY
        self.loss = False
        self.menu()        
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
        correct_file = "./assets/sounds/correct.wav"
        incorrect_file = "./assets/sounds/incorrect.wav"

        # Initialize the Pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/title_screen.wav")

        # Play the background music in an infinite loop
        pygame.mixer.music.play(-1)

        # Create Sound objects
        self.correct_sound = pygame.mixer.Sound(correct_file)
        self.incorrect_sound = pygame.mixer.Sound(incorrect_file)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            self.draw_floor()

            #self.screen.fill("black")
            self.handle_key_events()
            self.player.render()

            if (self.player.rect.x + self.player.rect.width) > SCREEN_WIDTH: self.player.rect.x = SCREEN_WIDTH - self.player.rect.width
            if self.player.rect.x < 0: self.player.rect.x = 0

            for trash in self.trash_list.copy():
                trash.fall()
                trash.render()

                if (trash.rect.colliderect(self.player.rect) and trash.rect.y + trash.size[1] > self.player.rect.y and 
                trash.rect.y + trash.size[1] < self.player.rect.y + 2 * trash.size[1] and self.player.img_index == trash.state):
                    current_score = self.score_map[BIN_NAMES[self.player.img_index]]
                    self.score_map[BIN_NAMES[self.player.img_index]] = current_score + 1
                    self.trash_list.remove(trash)
                    self.correct_sound.play()

                if trash.rect.y > SCREEN_HEIGHT - 60:
                    self.trash_list.remove(trash)
                    self.health_bar.hp -= self.health_bar.max_hp * 0.05
                    self.incorrect_sound.play()

                # WIN
                if (self.score_map[GARBAGE_NAME] >= WIN_CONDITION and self.score_map[PAPER_NAME] >= WIN_CONDITION and
                    self.score_map[COMPOST_NAME] >= WIN_CONDITION and self.score_map[GLASS_NAME] >= WIN_CONDITION):
                    self.running = False
                    self.end_screen()

                # LOSS
                if self.health_bar.hp == 0:
                    self.running = False
                    self.incorrect_sound.play()
                    self.loss = True
                    self.end_screen()
            
            self.health_bar.draw(self.screen)
            self.render_score()

            if self.spawn_timer % 1000 == 0:
                self.trash_speed += 1
            
            self.spawn_timer += 1
            if self.spawn_timer % (1000 / DIFFICULTY[self.difficulty]) == 0 and len(self.trash_list) < DIFFICULTY[self.difficulty]:  # 60 ticks per second, 5 seconds * 60 ticks = 300
                x_position = random.randint(0, SCREEN_WIDTH - 50)
                # new_trash = AbstractTrash(TRASH_PATHS["TRASH"], "Garbage", self, [x_position, 0])
                state = random.randint(0, 3)
                new_trash = Trash(self, (x_position, 0), state, self.trash_speed)
                self.trash_list.append(new_trash)

            # self.trash.render()
            pygame.display.flip()
            self.clock.tick(60)
    
    def render_score(self):
        font = self.get_font(24)
        black_text = f"{self.score_map[GARBAGE_NAME]}"
        blue_text = f"{self.score_map[PAPER_NAME]}"
        red_text = f"{self.score_map[GLASS_NAME]}"
        green_text = f"{self.score_map[COMPOST_NAME]}"

        black = pygame.transform.scale(BLACK_BIN, (BLACK_BIN.get_size()[0] // 8, BLACK_BIN.get_size()[1] // 8))
        blue = pygame.transform.scale(BLUE_BIN, (BLUE_BIN.get_size()[0] // 8, BLUE_BIN.get_size()[1] // 8))
        red = pygame.transform.scale(RED_BIN, (RED_BIN.get_size()[0] // 8, RED_BIN.get_size()[1] // 8))
        green = pygame.transform.scale(GREEN_BIN, (GREEN_BIN.get_size()[0] // 8, GREEN_BIN.get_size()[1] // 8))

        self.screen.blit(black, (10, 10))
        self.screen.blit(blue, (70, 10))
        self.screen.blit(red, (130, 10))
        self.screen.blit(green, (190, 10))

        black_score = font.render(black_text, True, (255, 255, 255))
        blue_score = font.render(blue_text, True, (255, 255, 255))
        red_score  = font.render(red_text, True, (255, 255, 255))
        green_score = font.render(green_text, True, (255, 255, 255))

        self.screen.blit(black_score, (10, 10))
        self.screen.blit(blue_score, (70, 10))
        self.screen.blit(red_score, (130, 10))
        self.screen.blit(green_score, (190, 10))

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
            self.start()

        if keys[pygame.K_1]:
            self.player.cycle_bin(0)
        if keys[pygame.K_2]:
            self.player.cycle_bin(1)
        if keys[pygame.K_3]:
            self.player.cycle_bin(2)
        if keys[pygame.K_4]:
            self.player.cycle_bin(3)

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def menu(self):
        earth_count = 0
        earth_img = pygame.image.load("./assets/menu/bigearth.png")
        counter = 0
        while True:
            if earth_count >= 60: earth_count = 0

            col_num = earth_count % 12
            row_num = earth_count // 12
            subset_rect = pygame.Rect(400 * col_num, 400 * row_num, 400, 400)
            curr_earth = earth_img.subsurface(subset_rect)
            self.screen.blit(MENU_BG, (0, 0))
            self.screen.blit(curr_earth, (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 75))
            if counter == 3:
                earth_count += 1
                counter = 0


            MENU_MOUSE_POS = pygame.mouse.get_pos()

            menu_font = self.get_font(100)
            line1_text = menu_font.render("WASTE", True, "#b68f40")
            line2_text = menu_font.render("INVADERS", True, "#b68f40")

            line1_rect = line1_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            line2_rect = line2_text.get_rect(center=(SCREEN_WIDTH // 2, 220))

            EASY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(640 - 125, 350),
                                text_input="EASY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            HARD_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(640 - 125, 500),
                                text_input="HARD", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=(640 - 125, 650),
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(line1_text, line1_rect)
            self.screen.blit(line2_text, line2_rect)

            for button in [EASY_BUTTON, HARD_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.difficulty = EASY
                        self.game_loop()
                    if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.difficulty = HARD
                        self.game_loop()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            counter += 1
            pygame.display.update()
        
    def end_screen(self):
        while True:
            self.screen.blit(RETRY_BG, (0, 0))
            
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            menu_font = self.get_font(100)
            if self.loss:
                line1_text = menu_font.render("THE EARTH", True, "#b68f40")
                line2_text = menu_font.render("IS DEAD!", True, "#b68f40")
                self.screen.blit(DEAD_EARTH, (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 75))
            else:
                line1_text = menu_font.render("YOU SAVED", True, "#b68f40")
                line2_text = menu_font.render("THE EARTH!", True, "#b68f40")
                self.screen.blit(HEALTHY_EARTH, (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 75))

            line1_rect = line1_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            line2_rect = line2_text.get_rect(center=(SCREEN_WIDTH // 2, 220))

            AGAIN_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(640 - 125, 400),
                                text_input="RETRY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=(640 - 125, 550),
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(line1_text, line1_rect)
            self.screen.blit(line2_text, line2_rect)

            for button in [AGAIN_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if AGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.running = True
                        self.start()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
        
if __name__ == "__main__":
    game : Game = Game()
    game.start()
