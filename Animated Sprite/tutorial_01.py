import sys

import pygame
import os
import constants

# ------------------------------------------------------
#                       class Player
# ------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0.0
        self.y = 0.0
        # path = os.path.join("data", "images", "characters", "pumpkin_standing.png")
        path = os.path.join("data", "images", "characters", "baldric", "walk", "front", "walk_front_0.png")
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(constants.TILESIZE, constants.TILESIZE)

    def move(self, x, y):
        myinc = 3
        dx = myinc * x
        dy = myinc * y
        self.rect = self.rect.move(dx, dy)

# ------------------------------------------------------
#                       class Game
# ------------------------------------------------------

class Game():
    def __init__(self):
        self.init_graphics()
        self.player = Player()
        self.keep_looping = True
        self.direction = "idle"
        self.drawing_counter = 0

    def init_graphics(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(constants.TITLE)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        self.all_sprites = pygame.sprite.Group()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True
                # ----
                if event.key == pygame.K_RIGHT:
                    self.direction = "right"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_UP:
                    self.direction = "up"
            elif event.type == pygame.KEYUP:
                self.direction = "idle"

    def update(self):
        if self.direction == "idle":
            pass
            # self.player.move(0, 0)
        elif self.direction == "right":
            self.player.move(1, 0)
        elif self.direction == "left":
            self.player.move(-1, 0)
        elif self.direction == "down":
            self.player.move(0, 1)
        elif self.direction == "up":
            self.player.move(0, -1)
        else:
            raise ValueError("Error")

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        self.all_sprites.add(self.player)
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def goodbye(self):
        pygame.quit()
        sys.exit()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.update()
            self.draw()
        self.goodbye()

# ***********************************************
def main():
    mygame = Game()
    mygame.main()

if __name__ == "__main__":
    main()