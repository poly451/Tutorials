import pygame
import sys, os
import constants
from environment import Environment
from player import Player

class Game:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.environment = Environment(self.zone_name, map_name)
        self.player = Player(self.zone_name, self.map_name)
        # ---- ----
        self.init_pygame()
        # ---- ----
        self.keep_looping = True

    def read_data(self):
        self.environment.read_data()
        self.player.read_data()

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        # self.player.movement_okay = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                # ----------------------------------------------
                elif event.key == pygame.K_UP:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("up")
                    self.player.move_up(self.environment.obstacles)
                elif event.key == pygame.K_DOWN:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("down")
                    self.player.move_down(self.environment.obstacles)
                elif event.key == pygame.K_RIGHT:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("right")
                    self.player.move_right(self.environment.obstacles)
                elif event.key == pygame.K_LEFT:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("left")
                    self.player.move_left(self.environment.obstacles)
                # ==============================================
                elif event.key == pygame.K_h:
                    # interact with something in the environment
                    pass
                elif event.key == pygame.K_i:
                    # look at the convents of the player's backpack,
                    # their inventory
                    pass
            elif event.type == pygame.KEYUP:
                self.player.move_player = False
                self.player.change_behavior("stand")
                self.player.change_direction(self.player.facing_direction)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     x = pos[0] / constants.TILESIZE
            #     y = pos[1] / constants.TILESIZE
            #     print(pos)
            #     print(x, y)

    def think(self):
        if len(self.player.facing_direction) == 0: return False
        if self.player.move_player == True:
            if self.player.facing_direction == "right":
                self.player.move_right(self.environment.obstacles)
            elif self.player.facing_direction == "left":
                self.player.move_left(self.environment.obstacles)
            elif self.player.facing_direction in ["front", "up"]:
                self.player.move_up(self.environment.obstacles)
            elif self.player.facing_direction in ["back", "down"]:
                self.player.move_down(self.environment.obstacles)
            else:
                s = "I don't recognize this: -{}-".format(self.player.facing_direction)
                raise ValueError(s)

    def draw(self):
        # if self.player.movement_okay == False:
        self.all_sprites = pygame.sprite.Group()
        self.screen.fill(constants.BG_COLOR)
        self.environment.update_classes(self.all_sprites)
        self.player.update_class(self.all_sprites)
        # ---- ----
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.clock.tick(12)
            self.handle_events()
            self.think()
            self.draw()

if __name__ == "__main__":
    zone_name = "docks"
    map_name = "map00"
    mygame = Game(zone_name, map_name)
    mygame.read_data()
    mygame.main()
