# From:
# https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2001/settings.py
# ===========================================================
# define some colors (R, G, B)
import pygame

# ---------------------------------
ZONE_KINDS = ["world", "ancient_forest", "town", "shrine"]
ZONE_KINDS += ["hermit", "cliffs", "dungeon", "graveyard", "palace"]
CHAR_KINDS = ["warrior", "mage"]
ITEM_KINDS = ["magic ring", "weapon", "healing potion", "armor", "misc", "trap", "food", "drink"]
NPC_KINDS = ["provisioner", "alchemist", "cultist", "monster", "king", "server"]
# ---------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (200, 200, 200)
DARK_GREEN = (  0, 153, 0)
GREEN = (0, 255, 0)
DARK_RED = (204, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

AQUA = (  0, 255, 255)
BLUE = (  0,  0, 255)
FUCHIA = (255,   0, 255)
GRAY = (128, 128, 128)
LIME = (  0, 255,   0)
MAROON = (128,  0,   0)
NAVY_BLUE = (  0,  0, 128)
OLIVE = (128, 128,   0)
PURPLE = (128,  0, 128)
LIGHT_PURBLE = (255, 153, 255)
SILVER = (192, 192, 192)
TEAL = (  0, 128, 128)
BACKGROUND_COLOR = WHITE
# UP = 90
# DOWN = -90
# RIGHT = 0
# LEFT = 180

TILESIZE = 128 #64 # 32
TILES_WIDE = 4
TILES_HIGH = 4
WIDTH = TILESIZE * TILES_WIDE   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = TILESIZE * TILES_HIGH  # 16 * 48 or 32 * 24 or 64 * 12
DIALOGUE_WIDTH = 700
DIALOGUE_HEIGHT = 600
SPLASH_SCREEN_WIDTH = 500
SPLASH_SCREEN_HEIGHT = 600
WINDOW_WIDTH = WIDTH * 2
WINDOW_HEIGHT = int(HEIGHT * 1.5)
FPS = 60
TITLE = "The Land of Light and Shadow"
BGCOLOR = DARKGREY
MAP = "starting_town.txt"

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
# ------------------------------------
FIGHTING_IMG = "fighting_school.png"
GRASS_IMG = "grass02.gif"
# HILLS_ROLLING = "greenery01.png"
HILLS_ROLLING = "hill02.png"
HILLS_GARDEN = "greenery03.png"
HARBOR_IMG = "harbor03.png"
# ANCIENT_FOREST = "ancient_forest.png"
ANCIENT_FOREST = "ancient_forest.png"
CLIFFS = "cliffs05.png"
# DUNGEON = "dungeon.png"
DUNGEON = "dungeon03.png"
GRAVEYARD = "graveyard04.png"
# GREAT_FOREST = "great_forest.png"
GREAT_FOREST_ENTRANCE = "another_forest.png"
GREAT_FOREST = "forest04.png"
PALACE = "palace03.png"
SHRINE = "shrine03.png"
SWAMP01 = "swamp03.png"
SWAMP02 = "swamp03.png"
TOWN = "town05.png"
HERMIT = "hermit.png"
HOUSE = "house.png"
HOUSE_WITH_TREES = "house_with_trees.png"
TREEHOUSE = "treehouse.png"
HOUSE_3D = "house_3d.png"
LOBBY = "lobby.png"
PATH = "path.png"
WALL = "wall.png"
TREASURE = "treasure.png"
WORLD = "world.png"
TEXT_IMG = "white_tile.png"
ALCHEMIST_IMG = "alchemist.png"
CREAM_IMG = "cream_tile.png"
ORANGE_PANEL = "orange_panel.png"
BLUE_PANEL = "blue_panel.png"
GREY_PANEL = "light_grey_panel.png"
LIGHT_BLUE_BACKGROUND = 'light_blue_background.png'
BIG_WAVE = "big_wave.png"
LITTLE_WAVE = "little_wave.png"
# ----
TOWN_GRASS = "town_grass.png"
HAUNTED_HOUSE = "town_haunted_house.png"
GARDEN = "town_garden.png"
WOODWORKER = "town_woodwork.png"
KINGS_GUARD = "town_knight.png"
TOWN_GATE = "town_gates.png"
PROVISIONER = "town_store.png"
POTION = "town_potions.png"
INN = "town_pub.png"
# WALL_IMG = "medievalTile_48.png"
# WALL_IMG2 = "medievalTile_45.png"
# WALL_IMG3 = "medievalTile_46.png"
# WALL_IMG4 = "medievalTile_47.png"
# WALL_IMG5 = "medievalEnvironment_07.png"
# WALL_IMG6 = "medievalEnvironment_08.png"

STORE_IMG = "store_my.png"

# PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'dog02.png'
# PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

# MOB_IMG = "zoimbie1_hold.png"
