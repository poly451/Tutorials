ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
TITLE = "The World of Light and Darkness"
# ----
NUMBER_OF_BLOCKS_WIDE = 12 #TODO: shouldn't this be determined by the mapfile?
NUMBER_OF_BLOCKS_HIGH = 12 #TODO: shouldn't this be determined by the mapfile?
# ----
CHAR_KINDS = ["warrior", "mage"]
# ----
TILESIZE = 64
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH
FRAME_RATE = 20
# ----

# ---- COLORS ----
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

# ---- FILES ----
MAPFILE = "map.txt"
# MAPFILE = "map_grass_and_walls.txt"
TESTING_FILE = "testing01.txt"

# ---- ENVIRONMENT ----
GRASS_IMG = "grass02.gif"
WALL_IMG = "medievalTile_48.png"

# ---- PLAYER ----
PLAYER_ORIGINAL_DATA_FILE = "player_original_data_file.txt"
PLAYER_DATA_FILE = "player_data_file.txt"
PLAYER_IMG = "dog02.png"
PLAYER_IMG_DEAD = "dog02_wounded05.png"

# ---- MONSTERS ----
MONSTERS_ORIGINAL_DATA_FILE = "monsters_original_data_file.txt"
MONSTERS_DATA_FILE = "monsters_data_file.txt"
MONSTER_IMG = "Giant Bat.png"
MONSTER_IMG_DEAD = "giant_bat_dead.png"
