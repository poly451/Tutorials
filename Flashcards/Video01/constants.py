RIDER_WAITE_DIR = "/Users/BigBlue/Pictures/Occult/Tarot/rider_waite_tarot"
BACKGROUND_COLORS = ["grey", "black", "yellow", "blue"]
# ------------------------
TILESIZE = 120
TILES_WIDE = 6
TILES_HEIGH = 8
WINDOW_OFFSET = 100
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 500
WINDOW_HEIGHT = TILES_WIDE * TILESIZE
WINDOW_WIDTH = TILES_HEIGH * TILESIZE
HEIGHT = WINDOW_HEIGHT + WINDOW_OFFSET
# ------------------------
major_arcana = ["the_fool", "the_magician", "the_high_priestess", "the_empress", "the_emperor", "the_hierophant"]
major_arcana += ["the_lovers", "the_chariot", "justice", "the_hermit", "wheel_of_fortune", "strength", "the_hanged_man"]
major_arcana += ["death", "temperance", "the_star", "the_moon", "the_sun", "judgement", "the_world"]
numerals = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
suits = ["wands", "cups", "swords", "pentacles"]
# ------------------------
RW_FOOL = "/Users/BigBlue/Pictures/Occult/Tarot/rider_waite_tarot/RWS_Tarot_00_Fool.jpg"
TITLE = "My Flashcard Program"
# ------------------------
KIND_OF_TILES = ["yellow_square", "white_square", "red_checker"]
KIND_OF_TILES += ["blue_checker", "blue_checker_drowned", "red_checker_crowned"]
# ------------------------
QUIZ_NAMES = ["debugging", "world capitals", "cards"]
SELECTION_METHODS = ["Mastery level", "Number"]
SUITS = ["wands", "cups", "swords", "pents", "pentacles"]
MIDDLE_CARDS = []
# ------------------------
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
# ------------------------
YELLOW_SQUARE = "yellow_square.png"
WHITE_SQUARE = "white_square.png"
RED_CHECKER = "checker_red_blank.png"
BLUE_CHECKER = "checker_blue_blank.png"
LIGHT_BLUE_CHECKER = "blue_checker_on_yellow.png"
LIGHT_BLUE_CHECKER_CROWNED = "light_blue_crowned_checker.png"
RED_CHECKER_CROWNED = "red_checker_crowned.png"
BLUE_CHECKER_CROWNED = "blue_crowned_checker.png"
GRASS = "grass02.gif"
DIRT = "dirt_small_square.png"
DOG = "dog02.png"

cards = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
for suit in SUITS:
    for card in cards:
        MIDDLE_CARDS.append("{} of {}".format(card, suit))

if __name__ == "__main__":
    print(MIDDLE_CARDS)
