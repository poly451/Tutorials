import pygame
import utils
import constants
import os, sys
"""
Class LPCModel reads in a list/dir of .png files
NOT a spritesheet
"""
# ------------------------------------------------------
#                 class LPCModel
# ------------------------------------------------------
class LPCModel(pygame.sprite.Sprite):
    def __init__(self, model_name, sheet_name, player_name, facing_direction):
        super().__init__()
        # self.init_pygame()
        # ----
        if len(model_name) == 0: raise ValueError("Error")
        if len(sheet_name) == 0: raise ValueError("Error")
        self.init_pygame()
        # ----
        self.model_name = model_name
        self.sheet_name = sheet_name
        self.player_name = player_name
        self.facing_direction = facing_direction
        if self.model_name not in constants.MODEL_NAMES:
            s = "I don't recogninze this model name: {}".format(self.model_name)
            raise ValueError(s)
        if self.sheet_name not in constants.SHEET_KINDS: raise ValueError("Error")
        # ----
        self.keep_looping = True
        self.image_list = []
        self.image_counter = 0
        self.image = None
        self.rect = None
        # ----
        self.sheet = None
        self.back = []
        self.left = []
        self.front = []
        self.right = []
        # ----
        self.rows_in_sheet = -1
        self.columns_in_sheet = -1
        self.animation_end = False

    def read_data(self):
        self._read_data_lists()

    def _read_data_lists(self):
        for a_direction in constants.DIRECTION_VALUES:
            mylist = self._get_behavior(a_direction, self.sheet_name)
            if a_direction == "back":
                self.back = mylist
            elif a_direction == "left":
                self.left = mylist
            elif a_direction == "front":
                self.front = mylist
            elif a_direction == "right":
                self.right = mylist
            else:
                s = "I don't recognize this direction: {}".format(a_direction)
                raise ValueError(s)

    def _get_behavior(self, a_direction, sheet_name):
        # dir_name = "{}_{}".format(self.model_name, self.sheet_name)
        dirpath = os.path.join(constants.IMAGES, "animations", "lpc",
                        self.model_name, "lists", sheet_name, a_direction)
        if os.path.isdir(dirpath) == False:
            s = "This is not a directory: {}".format(dirpath)
            raise ValueError(s)
        # ----
        filenames = os.listdir(dirpath)
        filenames = [i for i in filenames if i != ".DS_Store"]
        image_list = []
        for filename in filenames:
            # print("filename: {}".format(filename))
            mypath = os.path.join(dirpath, filename)
            try:
                # an_image = SimpleSprite(mypath)
                an_image = pygame.image.load(mypath).convert_alpha()
                an_image = pygame.transform.scale(an_image, (constants.TILESIZE, constants.TILESIZE))
            except Exception as e:
                t = "mypath: {}".format(mypath)
                s = "{}\n{}\n".format(e, t)
                raise ValueError(s)
            image_list.append(an_image)
        return image_list

    def update_class(self, x, y):
        self.image = self.image_list[self.image_counter]
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)
        # ---- ----
        self.image_counter += 1
        self.animation_end = False
        if self.image_counter >= len(self.image_list):
            self.image_counter = 0
            self.animation_end = True

    def change_direction(self, new_direction):
        if new_direction == "right":
            self.image_list = self.right
        elif new_direction == "left":
            self.image_list = self.left
        elif new_direction in ["front", "down"]:
            self.image_list = self.front
        elif new_direction in ["back", "up"]:
            self.image_list = self.back
        else:
            s = "I don't recognize this direction: {}".format(new_direction)
            raise ValueError(s)

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Spritesheets')
        self.clock = pygame.time.Clock()

    def debug_print(self):
        self.rows_in_sheet = -1
        self.columns_in_sheet = -1
        self.facing_direction = ""

        s = "model_name: {}, sheet_name: {}, animation_kind: {}"
        s += "rows_in_sheet: {}, columns_in_sheet: {}, direction: {}"
        s = s.format(self.model_name, self.sheet_name, self.animation_kind,
                     self.rows_in_sheet, self.columns_in_sheet, self.facing_direction)
        print(s)


# -------
if __name__ == "__main__":
    model_name = "henry"
    sheet_name = "base"
    player_name = "henry"
    player_position = "down"
    # model_name, sheet_name, player_name, player_position
    # ---- ----
    mydriver = LPCModel(model_name, sheet_name, player_name, player_position)
    mydriver.read_data()
