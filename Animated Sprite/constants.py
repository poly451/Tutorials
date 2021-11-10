import os
# https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
# SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
# TILESIZE = 64
TILESIZE = 100
# TILESIZE = 128
NUMBER_OF_BLOCKS_WIDE = 12 #TODO: shouldn't this be determined by the mapfile?
NUMBER_OF_BLOCKS_HIGH = 12 #TODO: shouldn't this be determined by the mapfile?
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH
TITLE = "Walk with me"
IMAGE_WIDTH, IMAGE_HEIGHT = 100, 100
UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
GREEN = (0, 200, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURBLE = (255, 153, 255)
ORANGE = (255, 128, 0)
PURPLE = (128,  0, 128)
# ----
BG_COLOR = UGLY_PINK # (Used for debugging)

FRAME_RATE = 10

ANIMATION_LIST = ["dead", "idle", "jump", "run", "slide", "walk"]
DIRECTION_LIST = ["right", "left", "up", "down"]
SPEED_LIST = ["stand", "walk", "run"]

DIRECTION_VALUES = ["back", "left", "front", "right"]
MOVEMENT_VALUES = ["walk", "slash", "spell", "fall", "idle"]

WALKSHEET_PATH = os.path.join("data", "images", "baldric", "baldric_walksheet.png")
SPELLSHEET_PATH = os.path.join("data", "images", "baldric", "baldric_SpellSheet02.png")
SLASHSHEET_PATH = os.path.join("data", "images", "baldric", "baldric_SlashSheet.png")
FALLSHEET_PATH = os.path.join("data", "images", "baldric", "baldric_fallsheet.png")