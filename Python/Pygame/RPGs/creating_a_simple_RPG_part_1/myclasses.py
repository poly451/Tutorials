import pygame
import constants
from environment import Environment
from player import Player

class Game:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.keep_looping = True
        # ---- ----
        self.player = Player()
        self.environment = Environment(self.zone_name, self.map_name)

    def read_data(self):
        self.environment.read_data()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                # ==============================================
                elif event.key == pygame.K_h:
                    # interact with something in the environment
                    pass
                elif event.key == pygame.K_i:
                    # look at the convents of the player's backpack,
                    # their inventory
                    pass
            elif event.type == pygame.KEYUP:
                # self.player.move_player = False
                # self.player.change_behavior(self.player.default_behavior)
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0] / constants.TILESIZE
                y = pos[1] / constants.TILESIZE
                print(pos)
                print(x, y)

    def update_classes(self):
        self.environment.update_classes(self.all_sprites)

    def draw(self):
        pass

    def think(self):
        pass

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.update_classes()
            self.draw()
            self.think()

# *****************************************************
# *****************************************************

def main():
    zone_name = "docks"
    # zone_name = "green_lawn"
    map_name = "map00"
    # map_name = "map01"
    # map_name = "map02"
    mygame = Game(zone_name, map_name)
    mygame.read_data()
    mygame.main()

if __name__ == "__main__":
    main()
