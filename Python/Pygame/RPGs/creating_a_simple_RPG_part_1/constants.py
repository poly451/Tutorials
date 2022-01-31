import os

TITLE = "A new world"

TILESIZE = 100
NUMBER_OF_BLOCKS_WIDE = 12
NUMBER_OF_BLOCKS_HIGH = 12
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
GREEN = (0, 200, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (210, 210, 210)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURBLE = (255, 153, 255)
ORANGE = (255, 128, 0)
PURPLE = (128,  0, 128)
UGLY_PINK = (255, 0, 255)
TRANSPARENT = (0, 0, 0, 0)
# ----
BG_COLOR = UGLY_PINK # (Used for debugging)

FRAME_RATE = 40

ZONE_NAMES = ["docks"]
MAP_NAMES = ["map00", "map01", "map02", "map03", "map04", "map05", "map06", "map07", "map08", "map09"]

MAPKINDS = ["walkables", "obstacles", "eatables", "persistentslower", "persistentsupper"]
MAPKINDS += ["travel", "grid"]

# IMAGES = "/Users/BigBlue/Documents/Programming/game_resources/images"
IMAGES = os.path.join("data", "images", )






















