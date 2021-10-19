import pygame
import constants
import sys, os
import utils


# class DisplaySprite(pygame.sprite.Sprite):
#     def __init__(self, myobject, x=0, y=0, height=64):
#         super().__init__()
#         print("class PlayerDisplay.__init__-->mydict:")
#         self.init_pygame()
#         self.x, self.y = x, y
#         self.height = height
#         # ----
#         # self.image_filename = myobject.large_image_filename
#         # self.image_dead_filepath = myobject.image_dead_filename
#         # path = utils.get_filepath(myobject.image_down_health_100)
#         # print("PATH: {}".format(path))
#         # if path is None:
#         #     s = "{}: I couldn't find a path for {}.".format(myobject.name, myobject.image_down_filename)
#         #     raise ValueError(s)
#         # if len(path) == 0:
#         #     s = "{}: I couldn't find a path for {}.".format(myobject.name, myobject.image_down_filename)
#         #     raise ValueError(s)
#         # try:
#         #     self.image = pygame.image.load(path).convert_alpha()
#         # except Exception as e:
#         #     s = "e\nCouldn't open: {}".format(path)
#         #     raise ValueError(s)
#         self.image = myobject.image_down_health_100
#         self.image = pygame.transform.scale(self.image, (height, height))
#         self.rect = self.image.get_rect()
#         self.rect = self.rect.move(self.x * height, self.y * height)
#
#     def init_pygame(self):
#         pygame.init()
#         self.BG_COLOR = constants.BG_COLOR
#         self.clock = pygame.time.Clock()
#         pygame.display.set_caption("Enter {}".format(constants.TITLE))
#         self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
#         self.font = pygame.font.Font(None, 40)
#         # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)
#
#     def move(self, dx, dy):
#         self.rect = self.rect.move(dx * self.height, dy * self.height)
#         self.x += dx
#         self.y += dy

# if __name__ == "__main__":
#     from graphics_fauna import Player, Npcs
#     zone_name = "green_lawn"
#     map_name = "map01"
#     myplayer = Player(zone_name, map_name)
#     myplayer.read_data_first()
#     mynpcs = Npcs(zone_name, map_name)
#     mynpc = mynpcs.debug_load_NPC("henry", "loriintr", 0, 0)
#     print("-------------------------------")
#     # mysprite = DisplaySprite(myplayer)
#     mysprite = DisplaySprite(mynpc)