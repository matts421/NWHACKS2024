# Example file showing a basic pygame "game loop"
import pygame
from trash_bins.bins import AbstractTrashBin
from trash.trash import AbstractTrash
import sys

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
    trash: AbstractTrash

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = AbstractTrashBin(BIN_PATHS["GARBAGE"], "GarbageBin", self)
        self.trash = AbstractTrash(TRASH_PATHS["TRASH"], "Garbage", self)
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
            self.trash.render()
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

if __name__ == "__main__":
    game : Game = Game()
    game.start()

# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Set up the display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Pygame Keyboard Input")

# # Set up colors
# black = (0, 0, 0)
# white = (255, 255, 255)

# # Set up the player's initial position
# player_x, player_y = width // 2, height // 2
# player_speed = 5

# # Main game loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Get the state of all keys
#     keys = pygame.key.get_pressed()

#     # Update the player's position based on key input
#     if keys[pygame.K_LEFT]:
#         player_x -= player_speed
#     if keys[pygame.K_RIGHT]:
#         player_x += player_speed
#     if keys[pygame.K_UP]:
#         player_y -= player_speed
#     if keys[pygame.K_DOWN]:
#         player_y += player_speed

#     # Fill the screen with a black background
#     screen.fill(black)

#     # Draw the player as a white rectangle
#     pygame.draw.rect(screen, white, (player_x, player_y, 50, 50))

#     # Update the display
#     pygame.display.flip()

#     # Control the frame rate
#     pygame.time.Clock().tick(60)