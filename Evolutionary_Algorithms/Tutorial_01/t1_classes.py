import sys, os
import t1_utils as utils
import t1_constants as con
import pygame
import time
import random
from t1_graphics import BackgroundTiles

# ---------------------------------------------------
#                        class Game
# ---------------------------------------------------
class Game:
    def __init__(self, zone_name):
        # -------------------------------------
        if not zone_name in con.ZONE_NAMES:
            raise ValueError("Error! Can't find zone name: {}".format(zone_name))
        self.zone = zone_name
        # -------------------------------------
        self.init_pygame()
        # -------------------------------------
        self.background_tiles = BackgroundTiles(self.zone)
        # -------------------------------------
        self.keep_looping = True
        self.text = "The Environment"
        self.BG_COLOR = con.LIGHTGREY
        # -------------------------------------

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(con.TITLE)
        self.surface = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                self.main_keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    self.main_keep_looping = False
                elif event.key == pygame.K_RETURN:
                    self.user_input = self.text.lower().strip()
                    self.text = ""
                elif event.key == pygame.K_a:
                    pass

    def draw_text(self):
        label = self.font.render(self.text, 1, (0, 0, 0))
        self.surface.blit(label, (10, 10))

    def draw(self):
        self.surface.fill(self.BG_COLOR)
        self.background_tiles.draw()
        self.draw_text()
        # print("x,y: {},{}".format(self.paths.current_path.x, self.paths.current_path.y))
        pygame.display.update()

    def update(self):
        pass

    def do_loop(self):
        self.clock.tick(50)
        while self.keep_looping:
            # time.sleep(.1)
            self.events()
            self.update()
            self.draw()

    def debug_print(self):
        s = "zone: {}"
        s = s.format(self.zone)
        print(s)
        t = "keep_looping: {}, text: {}".format(self.keep_looping, self.text)
        print(t)
        print("-" * 20)


if __name__ == "__main__":
    mygame = Game(con.ENVIRONMENT_VARIABLE)
    mygame.do_loop()