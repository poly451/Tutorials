ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
ALPHABET02 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
VOWELS = ["a", "e", "i", "o", "u", "y"]
TITLE = "The World of Light and Darkness"
# ----
NUMBER_OF_BLOCKS_WIDE = 12 #TODO: shouldn't this be determined by the mapfile?
NUMBER_OF_BLOCKS_HIGH = 12 #TODO: shouldn't this be determined by the mapfile?
# ----
CHAR_KINDS = ["warrior", "mage"]
# todo: Add 'rogue' to professions.
PROFESSION_NAMES = ["warrior"]
NPC_PROFESSIONS = ["barkeep", "baker", "mercenary", "antiques", "lamplighter", "healer", "unknown"]
NPC_PROFESSIONS += ["provisioner", "server", "jeweler", "merchant"]
NPC_FUNCTION = ["questgiver", "buy", "sell", "prey", "predator", "resource", "nuisance", "bystander"]
NPC_FUNCTION += ["bystander", "mercenary", "assassin"]
MOVEMENT_ACTION = ["walking", "standing", "flying"]
LANDMARKS = ["forest", "river", "hill", "valley", "farm", "castle", "village", "waterfall"]
MODIFIERS = ["guard", "west", "east", "south", "east", "after", "before"]
MODIFIERS += ["small", "speedily", "big", "great", "inside", "behind"]
MODIFIERS += ["between", "enclosed", "divine"]
# ----
TILESIZE = 64
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH
FRAME_RATE = 20
# ----
#INVENTORY_TYPES = ["fauna", "base"]
MERCHANT_NAMES = ["laura", "alvin", "old ben"]
NPC_NAMES = ["laura", "alvin", "old_ben", "tyla", "garakin", "alfred"]
NPC_NAMES += ["bartholomew", "westley", "aiza", "grumpy"]
NPC_NAMES += ["lilly", "tait", "bertron", "mystic", "ben"]
NPC_NAMES += ["alcott", "westleydead", "placeholder"]
NPC_NAMES += ["robrin", "daith"]
CHARACTER_KINDS = ["player", "merchant", "lamplighter"]
CHARACTER_TYPES = ["player", "npc"]
INVENTORY_KINDS = ["beginner", "normal", "advanced", None]
CONSUMABLE_KINDS = ["food", "drink"]
CONSUMABLE_NAMES = ["dry roast", "dry bread", "tough jerky", "stale lembas"]
CONSUMABLE_NAMES += ["soupy stew", "wild strawberries", "small poison"]
CONSUMABLE_NAMES += ["stewy soup", "bitter water", "spoiled wine"]
CONSUMABLE_NAMES += ["special health", "small health", "red apple"]
CONSUMABLE_NAMES += ["wild blueberries", "strong mint", "weak beer"]
CONSUMABLE_NAMES += ["health potion"]
FOOD_SPECIES = ["roast", "bread", "jerky", "lembas", "stew", "soup", "strawberries", "apple"]
FOOD_SPECIES += ["blueberries", "candy"]
DRINK_SPECIES = ["water", "wine", "potion", "beer"]
CONSUMABLE_SPECIES = FOOD_SPECIES + DRINK_SPECIES
# DRINK_KIND = ["water", "wine"]
WEAPON_KINDS = ["sword", "longsword", "magic_item", "potion", "gem", "necklace", "metal", "rock"]
WEAPON_KINDS += ["feather", "note", "rumor", "book", "money"]
WEAPON_NAMES = ["rusty sword", "normal sword", "rusty longsword", "red amulet", "gold ring"]
WEAPON_NAMES += ["silver cross", "special ruby", "ancient sword", "tarnished necklace"]
WEAPON_NAMES += ["good sword", "perfect emerald", "flawed emerald", "silver nugget"]
WEAPON_NAMES += ["dull rock", "blue feather", "small magnet", "crumpled note"]
WEAPON_NAMES += ["swindon_bertron rumor001", "small book", "100 gold", "gold coin"]
WEAPON_NAMES += ["westley note", "lilly iou", "mercenary note", "ring rumor"]
WEAPON_NAMES += ["charlel introduction"]
QUEST_NAMES = ["the three feathers", "buy_goods_from_alfred_01"]
QUEST_NAMES += ["sell_goods_to_bartholemew01", "a hint"]
QUEST_NAMES += ["the threat and the promise", "a quest for apples"]
QUEST_NAMES += ["welcome to swindon", "banter with lilly"]
QUEST_NAMES += ["grumpy bertron", "talk with the mystic"]
QUEST_NAMES += ["buy a secret", "a secret to sell", "westley was murdered"]
QUEST_NAMES += ["investigating the murder of westley"]
QUEST_NAMES += ["banter with robrin", "searching the corpse of daith"]
QUEST_NAMES += ["westley is very dead", "save lillys pub"]
QUEST_NAMES += ["why_does_someone_not_want_me_to_know_who_i_am"]
READABLE_INVENTORY_ITEMS = ["lilly iou", "westley note", "mercenary note", "ring rumor"]
ITEM_KINDS = ["food", "drink", "weapon"]
CONSUMABLE_ITEMS = "consumable_items.txt"
CONSUMABLE_ITEMS_ORIGINAL = "consumable_items_original.txt"
FONT_NAME = None
FONT_SIZE = 30
# ----
# NPCs in the various zones
# STARTING_ZONE_NPCS = ["laura"]
ZONE_NAMES = ["swindon", "easthaven", "harrogate", "swindon_pub"]
ZONE_NAMES += ["dark_alley", "testing", "green_lawn"]
ZONE_NAMES += ["provisioner", "apple_grove"]
ZONE_NAMES += ["the_orchard", "bridge", "cliffs", "jeweler", "village_blue"]
ZONE_NAMES += ["swindon_pub_haunted"]

MAP_TILE_NAMES_WALKABLE = ["a0", "c0", "d0", "d1", "d2", "b0", "l0", "l1", "l2", "g0", "m0", "f0", "h0", "s0", ".."]
TILE_KINDS = ["wall", "stove", "streetlamp", "table", "counter", "forest", "rocks", "chair", "pub", "provisioner"]
TILE_KINDS += ["cobblestones", "tile", "black", "portal", "grass", "mushrooms", "strawberries", "npc_dead"]
TILE_KINDS += ["flowers", "lava", "box", "wall_counter", "desk", "rug", "tree", "water", "cave", "mountain"]
TILE_KINDS += ["dirt", "tent", "path", "tile", "cliff", "shape", "bush", "fireplace", "cabinet"]
TILE_KINDS += ["torch", "gems", "couch", "bench", "bookcase", "plant", "gazebo", "stump"]
TILE_KINDS += ["building", "statue", "sign", "invisible_obstacle"]
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
BG_COLOR = UGLY_PINK # (Used for debugging)
# BG_COLOR = BLACK # (Used for playing the program)

# ---- FILES ----
# MAPFILE = "map02.txt"
# MAPFILE = "map_grass_and_walls.txt"
MAPFILE = "map.txt"
TESTING_FILE = "testing01.txt"
TESTING_WEAPONS_FILE = "testing_weapons_file.txt"
TESTING_CONSUMABLES_FILE = "testing_consumables_file.txt"

NPCS = "npcs.txt"

# ---- ENVIRONMENT ----
GRASS_IMG = "grass02.gif"
FOREST_IMG = "medievalTile_48.png"
WALL_IMG = "brick_wall.png"
DIRT_IMG = "dirt01.png"
# MERCHANT = "merchant03b.png"
BYSTANDER_IMG = "bystander01.png"
PORTAL_IMG = "portal_dirt.png"
BEGINNER_MERCHANT = "merchant03b.png"
ADVANCED_MERCHANT = "merchant04b.png"
# ---- PLAYER ----
PLAYER_ORIGINAL_DATA_FILE = "player_original_data_file.txt"
PLAYER_DATA_FILE = "player_data_file.txt"
PLAYER_IMG = "warrior03_down.png"
# PLAYER_IMG_UP = "dog_up.png"
# PLAYER_IMG_DOWN = "dog_down.png"
# PLAYER_IMG_RIGHT = "dog_right.png"
# PLAYER_IMG_LEFT = "dog_left.png"
# PLAYER_IMG_DEAD = "dog02_wounded05.png"
PLAYER_IMG_UP = "warrior03_up.png"
PLAYER_IMG_DOWN = "warrior03_down.png"
PLAYER_IMG_RIGHT = "warrior03_right.png"
PLAYER_IMG_LEFT = "warrior03_left.png"
PLAYER_IMG_DEAD = "skull_and_bones.png"
PLAYER_INVENTORY = "player_inventory.txt"
PLAYER_FOOD = "player_food.txt"
PLAYER_DRINK = "player_food.txt"
PLAYER_WEAPONS = "player_weapons.txt"
WEAPONS_FILE = "weapon_items.txt"
WEAPONS_FILE_ORIGINAL = "weapon_items_original.txt"
#---- INVENTORY ITEMS ----
# FOOD_ITEMS = "food.txt"
# DRINK_ITEMS = "drink.txt"
# WEAPON_ITEMS = "weapon.txt"
DIALOG_PLAYER_COMMANDS_CHOICES = ["g", "c"]
COMMANDS = ["rpi", "rp"]
MAP_COMMANDS = ["load_map", "show_text", "find_item"]
MAP_COMMANDS += ["change_npc_passive", "change_npc_agro", "fire_attack", "fire_attack_big"]
PLAYER_COMMANDS = "player_commands.txt"

# ---- MONSTERS ----
MONSTERS_ORIGINAL_DATA_FILE = "monsters_original_data_file.txt"
MONSTERS_DATA_FILE = "monsters_data_file.txt"
MONSTERS_TEMP_FILE = "monster_temp_file.txt"
# MONSTER_IMG = "Giant Bat.png"
# MONSTER_IMG_DEAD = "giant_bat_dead.png"
# ---- NPCS ----
NPC_BEGINNER_MERCHANT_INVENTORY = "npc_beginner_merchant_inventory.txt"
NPC_NORMAL_MERCHANT_INVENTORY = "npc_normal_merchant_inventory.txt"
NPC_ADVANCED_MERCHANT_INVENTORY = "npc_advanced_merchant_inventory.txt"
# -------------
DISCRIPTION_01 = ['rusty', 'normal', 'dry', 'tough', 'stale', 'soupy', 'stewy', 'bitter', 'spoiled']
DISCRIPTION_02 = ['sword', 'longsword', 'roast', 'bread', 'jerky', 'lembas']
DISCRIPTION_02 += ['stew', 'soup', 'water', 'wine']
AGRO_LEVEL = ["passive", "agro"]
ZONE_INIT_VALUES = ["visited", "never_visited"]
TILE_OBSTACLE_KINDS = ["empty", "streetlamp", "wall", "forest"]
TILE_WALKABLE_KINDS = ["empty", "black", "cobblestones", "portal"]
WHAT_HAPPENS_NOW_old = ["continue", "end conversation", "end game", "completed", "load next map"]
CONVERSATION_ENDINGS = ["continue", "end conversation", "end game", "completed", "load next map"]
CONVERSATION_ENDINGS += ["buy", "sell", "accepted", "sell all", "take item"]
CONVERSATION_COMMANDS = ["sell", "buy", "sell all", "end conversation", "take item"]
CONVERSATION_COMMANDS += ["continue", "accepted", "completed", "load next map"]
QUEST_ENDINGS = ["end game", "load next map", "turn npc passive", "turn npc agro"]
SPECIES = ["human", "dragon", "skeleton", "bird", "raccoon", "unknown"]
MAP_CHOICES = ["map00", "map01", "map02", "map03", "map04", "map05", "map06"]
MAP_CHOICES += ["map07", "map08", "map09"]
NPC_MODEL_NAMES = ["matilda", 'orange_cape', 'big_merchant', 'westley', 'older_merchant_male', "blue_bird"]
NPC_MODEL_NAMES += ["shadowy01", "green_orange_dragon", "lamplighter", "lilly", "aiza"]
NPC_MODEL_NAMES += ["elf_ears_female", "raccoon", "older_man", "shaggy_hair"]
NPC_MODEL_NAMES += ["blond_townsperson_facial_hair", "mystic", "shadowy01dead"]
NPC_MODEL_NAMES += ["firehair", "shady_mercenary", "skeleton"]
CONTACT_KINDS = ["fight", "talk", "flee"]
PROVISIONERS_GOODS = ["stewy soup", "bitter water", "spoiled wine", "rusty sword", "rusty longsword"]
PROVISIONERS_GOODS += ["dry bread", "red amulet", "blue feather", "swindon_bertron rumor001"]
PROVISIONERS_GOODS += ["health potion", "ring rumor", "red apple"]
PROVISIONERS_GOODS += ["wild blueberries", "mercenary note"]
ITEMS_PLAYER_CAN_USE = ["health potion", "bitter water", "tough jerky"]
# QUEST_DIALOG_COMMANDS = ["buy", "sell", "continue"]
SPRITES_SUBDIRECTORY = "data/images/sprites"

QUALITY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
DAMAGE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]