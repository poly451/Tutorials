import pygame
import constants
import os, sys
from environment_classes import Walkables

# ------------------------------------------------------
#                 class Environment
# ------------------------------------------------------

class Environment:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.walkables = Walkables(self.zone_name, self.map_name)

    def read_data(self):
        self.walkables.read_data()

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        self.clock = pygame.time.Clock()

    def update_classes(self, all_sprites):
        self.walkables.update_class(all_sprites)

    def debug_print(self):
        self.walkables.debug_print()

# ------------------------------------------------------
#                   class Environment_Driver
# ------------------------------------------------------
class EnvironmentDriver:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        # ---- ----
        self.init_pygame()
        self.environment = Environment(self.zone_name, self.map_name)
        self.keep_looping = True

    def read_data(self):
        self.environment.read_data()

    def debug_print(self):
        self.environment.debug_print()

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Spritesheets')
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass

    def update_class(self):
        pass

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main(self):
        self.environment.update_classes(self.all_sprites)
        while self.keep_looping == True:
            self.clock.tick(10)
            self.handle_events()
            self.update_class()
            self.draw()
        pygame.quit()
        sys.exit()

# *****************************************************
# *****************************************************

def main():
    zone_name = "docks"
    map_name = "map00"
    mydriver = Environment_Driver(zone_name, map_name)
    mydriver.read_data()
    mydriver.main()

if __name__ == "__main__":
    main()






