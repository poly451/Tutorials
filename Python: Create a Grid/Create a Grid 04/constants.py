import os

# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 480
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# ----
NUMBER_OF_BLOCKS_WIDE = 12 #TODO: shouldn't this be determined by the mapfile?
NUMBER_OF_BLOCKS_HIGH = 12 #TODO: shouldn't this be determined by the mapfile?
# BLOCK_HEIGHT = round(SCREEN_HEIGHT / NUMBER_OF_BLOCKS_HIGH)
# BLOCK_WIDTH = round(SCREEN_WIDTH / NUMBER_OF_BLOCKS_WIDE)
# ----
CHAR_KINDS = ["warrior", "mage"]
# ----
TILESIZE = 64
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH
# ----

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
BG_COLOR = UGLY_PINK
# ----
MAPFILE = "map.txt"
TITLE = "The World of Light and Darkness..."
FOOD_ENERGY = 10

#-- ENVIRONMENT TILES --
GRASS_IMG = "grass02.gif"

# -- WALL --
WALL_IMG = "medievalTile_48.png"

# -- PLAYER --
PLAYER_IMG = "dog02.png"
PLAYER_IMG_q1 = "dog02_wounded01.png"
PLAYER_IMG_q2 = "dog02_wounded02.png"
PLAYER_IMG_q3 = "dog02_wounded03.png"
PLAYER_IMG_q4 = "dog02_wounded04.png"
PLAYER_IMG_q5 = "dog02_wounded05.png"
# -- PLAYER DATA --
PLAYER_ORIGINAL_DATA_FILE = "player_original_data.txt"
PLAYER_DATA_FILE = "player_data.txt"
PLAYER_DATA_FILE_TESTING = "player_data_test.txt"

# -- MONSTERS --
# MONSTER_IMG = "bug_monster01.png"
MONSTER_IMG = "Giant Bat.png"
MONSTER_IMG_DEAD = "giant_bat_dead.png"
MONSTERS_ORIGINAL_DATA_FILE = "monsters_data_file.txt"
MONSTERS_DATA_FILE = "monsters_temp_data_file.txt"
