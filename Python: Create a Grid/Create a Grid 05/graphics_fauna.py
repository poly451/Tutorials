import os, sys
import pygame
import utils
import constants
import random
from inventory import Inventory
from dialogs import DialogSpeech, DialogInput

# -----------------------------------------------------------
#                      class Player
# -----------------------------------------------------------
"""
As you can see, class Player uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, or ask the folks over on 
Stack Overflow (https://stackoverflow.com/) or even on Twitter.
"""
class Player(pygame.sprite.Sprite):
    def __init__(self, player_name, zone_name, map_name):
        super().__init__()
        if utils.validate_name(player_name) == False:
            s = "{} is not a valid name."
            raise ValueError(s)
        self.player_name = player_name
        self.zone_name = zone_name
        self.map_name = map_name
        print("map_name: {}".format(self.map_name))
        # ---------------------------------------------
        self.init_pygame()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.direction = constants.DOWN
        # ---------------------------------------------
        self.maximum_damage = 2
        self.max_hit_points = -1
        self.hit_points = -1
        self.chance_to_hit = -1
        self.experience = -1
        self.profession = None
        self.gold = -1
        # ---------------------------------------------
        self.inventory = None
        # ---------------------------------------------
        self.image = None
        self.image_dead = None
        self.image_up = None
        self.image_down = None
        self.image_right = None
        self.image_left = None
        self.rect = None
        self.font = None
        # ---------------------------------------------
        self.image_down_filename = ""
        self.image_up_filename = ""
        self.image_right_filename = ""
        self.image_left_filename = ""
        self.image_dead_filename = ""
        # ---------------------------------------------
        self.image_down = None
        self.image_up = None
        self.image_right = None
        self.image_left = None
        self.image_dead = None
        # ---------------------------------------------

    def load_images(self):
        # print("image: {}".format(utils.get_filepath(self.image_down_filename)))
        # filepath = os.path.join("data", "images", "player_images", self.image_up_filename)
        filepath = utils.get_filepath(self.image_up_filename)
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        filepath = os.path.join("data", "images", "player_images", self.image_dead_filename)
        print("* filepath: {}".format(filepath))
        self.image_dead = pygame.image.load(filepath).convert_alpha()
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        # filepath = os.path.join("data", "images", "player_images", self.image_up_filename)
        filepath = utils.get_filepath(self.image_up_filename)
        self.image_up = pygame.image.load(filepath).convert_alpha()
        self.image_up = pygame.transform.scale(self.image_up, (constants.TILESIZE, constants.TILESIZE))
        # ----
        # filepath = os.path.join("data", "images", "player_images", self.image_down_filename)
        filepath = utils.get_filepath(self.image_down_filename)
        self.image_down = pygame.image.load(filepath).convert_alpha()
        self.image_down = pygame.transform.scale(self.image_down, (constants.TILESIZE, constants.TILESIZE))
        # ----
        # filepath = os.path.join("data", "images", "player_images", self.image_right_filename)
        filepath = utils.get_filepath(self.image_right_filename)
        self.image_right = pygame.image.load(filepath).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (constants.TILESIZE, constants.TILESIZE))
        # ----
        # filepath = os.path.join("data", "images", "player_images", self.image_left_filename)
        filepath = utils.get_filepath(self.image_left_filename)
        self.image_left = pygame.image.load(filepath).convert_alpha()
        self.image_left = pygame.transform.scale(self.image_left, (constants.TILESIZE, constants.TILESIZE))

    # def get_map_xy(self):
    #     filename = "{}_npcs.txt".format(self.map_name)
    #     filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
    #     with open(filepath, "r") as f:
    #         mytiles = f.readlines()
    #         mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    #     mytiles = [i[3:] for i in mytiles[2:]]
    #     # [print(i) for i in mytiles]
    #     # ------------------------------------------------------------------
    #     big_list = []
    #     for col, tiles in enumerate(mytiles):
    #         tile_list = tiles.split(";")
    #         tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
    #         for row, tile in enumerate(tile_list):
    #             # print("tile: {}".format(tile))
    #             if tile.find("p") > -1:
    #                 return row, col

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _read_player_data_from_file(self):
        user_data = utils.get_user_data()
        player_name = user_data["character_name"]
        if not (self.player_name == player_name):
            s = "Error! self.player_name != player_name. {} != {}".format(self.player_name, player_name)
            raise ValueError(s)
        # ----
        # player_profession = user_data["profession_name"]
        # ----
        path = os.path.join("data", "playing_characters", player_name, constants.PLAYER_DATA_FILE)
        # print("path: {}".format(path))
        mylist = utils.read_file(path)
        # [print(i) for i in mylist]
        mydict = mylist[0]
        # print("mydict: {}".format(mydict))
        # for key, value in mydict.items():
        #      print("{}: {}".format(key, value))
        # raise NotImplemented
        # ----
        # self.x = mydict["x"]
        # self.y = mydict["y"]
        self.x, self.y = utils.get_map_xy_for_player(self.zone_name, self.map_name)
        if self.x is None or self.y is None:
            s = "Error! Have you remembered to include the player in the npc map?"
            raise ValueError(s)
        # self.name = mydict["name"]
        self.name = self.player_name
        self.species = mydict["species"]
        if utils.is_int(mydict["direction"]) == True:
            self.direction = int(mydict["direction"])
        else:
            self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        self.profession = mydict["profession"]
        self.gold = mydict["gold"]
        # ----
        # print("here is mydict in read_data_first:")
        # print(mydict)
        self.image_down_filename = mydict["image_down"]
        self.image_up_filename = mydict["image_up"]
        self.image_right_filename = mydict["image_right"]
        self.image_left_filename = mydict["image_left"]
        self.image_dead_filename = mydict["image_dead"]
        # print("**************** KDFDKFJDKF ******************")
        # print("self.image_left: {}".format(self.image_right))
        # if self.image_down == None:
        #     raise ValueError('Error!')
        # if self.image_up == None:
        #     raise ValueError("Error!")
        # ----
        # print("x,y: ({},{})".format(self.x, self.y))
        # if self.zone_name == "green_lawn":
        #     raise NotImplemented
        self.load_images()

    def read_data(self):
        self._read_player_data_from_file()
        self.inventory = Inventory("player", self.name)
        self.inventory.read_data()

    # def read_data_restart(self):
    #     raise NotImplemented
    #     # print("mydict: {}".format(mydict))
    #     self.inventory = Inventory("player", self.name)
    #     self.inventory.read_data()
    #     user_data = utils.get_user_data()
    #     path = os.path.join("data", "playing_characters", user_data["character_name"], constants.PLAYER_DATA_FILE)
    #     mylist = utils.read_data_file(path, num_of_fields=16)
    #     mydict = mylist[0]
    #     # ----
    #     # Getting player x, y
    #     filename = "{}_npcs.txt".format(self.map_name)
    #     filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
    #     x, y = utils.get_player_map_coords(filepath)
    #     # ----
    #     self.name = mydict["name"]
    #     self.kind = mydict["kind"]
    #     if utils.is_int(mydict["direction"]) == True:
    #         self.direction = -90
    #     else:
    #         self.direction = utils.convert_direction_to_integer(mydict["direction"])
    #     self.max_hit_points = mydict["max_hit_points"]
    #     self.hit_points = mydict["hit_points"]
    #     self.chance_to_hit = mydict["chance_to_hit"]
    #     self.experience = mydict["experience"]
    #     self.profession = mydict["profession"]
    #     self.gold = mydict["gold"]
    #     # ----
    #     print("here is mydict in graphics_fauna.py-->Player.read_data_restart:")
    #     print(mydict)
    #     self.image_down_filename = mydict["image_down"]
    #     self.image_up_filename = mydict["image_up"]
    #     self.image_right_filename = mydict["image_right"]
    #     self.image_left_filename = mydict["image_left"]
    #     self.image_dead_filename = mydict["image_dead"]
    #     # ----
    #     self.load_images()
    #     self.x, self.y = self.get_map_xy()
    #     # **** Debugging (start) *****
    #     print("Player_x: {}".format(self.x))
    #     print("Player_y: {}".format(self.y))
    #     # raise NotImplemented
    #     # **** Debugging (end) ****
    #     # ----
    #     self.direction = "DOWN"

    def calculate_damage(self, an_npc):
        # This is just a thumbnail. In a future version of this program
        # the amount of damage received will depend on
        # - the strength of the attacker
        # - the amount of damage the weapon can deliver
        # - the quality of shielding the attacked has
        return self.maximum_damage

    def has_item(self, item_name):
        this_item = self.inventory.get_item_by_name(item_name)
        if this_item is None:
            return False
        return True

    def npc_in_range_of_item_effect(self, npc, item_name):
        an_item = self.inventory.get_item_by_name(item_name)
        if an_item is None:
            s = "This shouldn't happen because we should have "
            s += "already established that the player has the "
            s += "item in their inventory."
            raise ValueError(s)
        A, B = (self.x, self.y), (npc.x, npc.y)
        distance_between_player_and_npc = utils.distance_between_two_points(A, B)
        range_of_magical_effect = an_item.range_of_effect
        if distance_between_player_and_npc <= range_of_magical_effect:
            return True
        return False

    def inventory_display_string(self):
        s = self.inventory.display_string()

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def get_fileline(self):
        s = "name: {}\nspecies: {}\ndirection: {}\nmax_hit_points: {}" \
            "\nhit_points: {}\nchance_to_hit: {}\nexperience: {}\nprofession: {}\ngold: {}" \
            "\nimage_down: {}\nimage_up: {}\nimage_right: {}\nimage_left: {}\nimage_dead: {}\n"
        # import pdb; pdb.set_trace()
        s = s.format(self.name, self.species, "-90", self.max_hit_points,
                     self.hit_points, self.chance_to_hit, self.experience, self.profession, self.gold,
                     self.image_down_filename, self.image_up_filename, self.image_right_filename, self.image_left_filename, self.image_dead_filename)
        return s

    def save_data(self):
        player_string = self.get_fileline()
        filepath = os.path.join("data", "playing_characters", self.name, constants.PLAYER_DATA_FILE)
        with open(filepath, "w") as f:
            f.write(player_string)
        self.inventory.save_data()

    def resize(self, tilesize, new_x, new_y):
        raise NotImplemented
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def display_list(self):
        mylist = []
        mylist.append("x,y: ({},{})".format(self.x, self.y))
        # ----
        if type(self.direction) == type("abc"):
            mylist.append("direction: {}".format(self.direction))
        else:
            mylist.append("direction: {}".format(utils.convert_integer_to_direction(self.direction)))
        # ----
        mylist.append("max hit points: {}".format(self.max_hit_points))
        mylist.append("hit points: {}".format(self.hit_points))
        mylist.append("chance to hit: {}".format(self.chance_to_hit))
        mylist.append("experience: {}".format(self.experience))
        mylist.append("profession: {}".format(self.profession))
        mylist.append("gold: {}".format(self.gold))
        return mylist

    # def _collide(self, dx=0, dy=0, obstacles=None):
    #     for a_tile in obstacles:
    #         if a_tile.x == (self.x + dx) and a_tile.y == (self.y + dy):
    #             print("COLLISION!!!!!!!!")
    #             print("-- debug print (begin) --")
    #             a_tile.debug_print()
    #             print("-- debug print (end) --")
    #             return True
    #     return False

    def move(self, dx=0, dy=0, obstacles=None):
        new_x = self.x + dx
        new_y = self.y + dy
        if obstacles.collision(new_x, new_y) == True:
            # print("Colission happened")
            return False
        # print("NO collectioin happened.")
        self.x = new_x
        self.y = new_y
        self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        return True

    # def move_to_square(self, x, y, obstacles=None):
    #     if obstacles.collision(x, y) == True:
    #         return False
    #     self.x = x
    #     self.y = y
    #     self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def debug_print(self):
        title, length = utils.format_string("Player.debug_print()", length=50, my_divider="-")
        print(title)
        s = "x,y: ({},{}); name: {}; kind: {}; direction: {}; max_hit_points: {}; "
        s += "hit_points: {}; chance_to_hit: {}; experience: {}; profession: {}; gold: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.direction, self.max_hit_points,
                     self.hit_points, self.chance_to_hit, self.experience, self.profession, self.gold)
        print(s)
        self.inventory.debug_print()
        title, length = utils.format_string("- END - Player.debug_print()", length=50, my_divider="-")
        print(title)

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def resurrect_player(self):
        mylist = ["{} the {} is DEAD!!".format(self.name, self.profession)]
        mylist.append("Would you like to resurrect {}?".format(self.name))
        mylist.append(" ")
        mylist.append("(y = Yes; n = No; ESC = Yes)")
        choices = ["y", "n"]
        mydialog = DialogInput(mylist, choices)
        myresult = mydialog.main()
        # print("myresult: {}".format(myresult))
        # raise NotImplemented
        return myresult

# -----------------------------------------------------------
#                      class NewNpc
# -----------------------------------------------------------
class Npc(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        print("class NewNPC.__init__-->mydict:")
        print(mydict)
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.species = mydict["species"]
        if not self.species in constants.SPECIES:
            s = "Error! {} is not in {}".format(self.species, constants.SPECIES)
            raise ValueError(s)
        self.profession = mydict["profession"]
        self.gold = mydict["gold"]
        self.attack_distance = mydict["attack_distance"]
        # ----
        self.inventory_type = mydict["inventory_type"]
        self.trigger = mydict["trigger"].lower().strip()
        if self.trigger == "none":
            self.trigger = None
        # ----
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.agro_level = mydict["agro_level"]
        if not self.agro_level in constants.AGRO_LEVEL:
            raise ValueError("Error!")
        self.maximum_damage = mydict["maximum_damage"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ----
        self.image_kind = -1
        self.image_filename = mydict["image_filename"]
        if self.image_filename is None:
            raise ValueError("Error!")
        # The following line is needed for DialogFight
        self.image_down_filename = self.image_filename
        self.image = None
        self.image_dead_filename = mydict["image_dead_filename"]
        self.image_dead = None
        self.rect = None
        # ----
        s = mydict["is_monster"].lower().strip()
        self.is_monster = True if s=="true" else False
        self.comment = ""
        # ----
        # filepath = ""
        # if self.species == "dragon" and self.profession == "unknown" and self.image_kind == 0:
        #     filepath = utils.get_filepath("dragon01.png")
        # elif self.species == "darkness" and self.profession == "unknown" and self.image_kind == 0:
        #     filepath = utils.get_filepath("black.png")
        # elif self.species == "empty" and self.species == "empty" and self.image_kind == 0:
        #     filepath = utils.get_filepath("empty.png")
        # else:
        #     s = "Couldn't find: species: {}, profession: {}, image_kind: {}"
        #     s = s.format(self.species, self.profession, self.image_dead)
        #     raise ValueError(s)
        # ----
        filepath = utils.get_filepath(self.image_filename)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            s = "e\nCouldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        filepath = utils.get_filepath(self.image_dead_filename)
        self.image_dead = pygame.image.load(filepath).convert_alpha()
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def get_fileline(self):
        s = "name: {}\nspecies: {}\nprofession: {}\nmax_hit_points: {}\nhit_points: {}\n"
        s += "agro_level: {}\nattack_distance:{}\nmaximum_damage: {}\nchange_to_hit: {}\nexperience: {}\n"
        s += "image_filename: {}\nimage_dead_filename: {}\ngold: {}\ninventory_type: {}\n"
        s += "trigger: {}\nis_monster: {}\n"
        s = s.format(self.name, self.species, self.profession, self.max_hit_points, self.hit_points,
                     self.agro_level, self.attack_distance, self.maximum_damage, self.chance_to_hit, self.experience,
                     self.image_filename, self.image_dead_filename, self.gold, self.inventory_type,
                     self.trigger, self.is_monster)
        return s

    def move(self, dx=0, dy=0, obstacles=None):
        new_x = self.x + dx
        new_y = self.y + dy
        if not obstacles.collision(new_x, new_y) == True:
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            self.x += dx
            self.y += dy
        # if not self._collide(dx, dy, obstacles):
        #     self.x += dx
        #     self.y += dy
        #     self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)

    def move_right(self, obstacles=None):
        dx, dy = -1, 0
        self.move(dx, dy, obstacles)

    def move_left(self, obstacles=None):
        dx, dy = 1, 0
        self.move(dx, dy, obstacles)

    def move_down(self, obstacles=None):
        dx, dy = 0, 1
        self.move(dx, dy, obstacles)

    def move_up(self, obstacles=None):
        dx, dy = 0, -1
        self.move(dx, dy, obstacles)

    def move_toward(self, x, y, obstacles):
        # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        if self.x == x and self.y == y:
            return True
        if self.x == x and self.y != y:
            if self.y - y < 0:
                self.move_down(obstacles)
            else:
                self.move_up(obstacles)
        elif self.x != x and self.y == y:
            if (self.x - x) < 0:
                self.move_left(obstacles)
            else:
                self.move_right(obstacles)
        elif self.x !=x and self.y != y:
            myrand = random.randint(0, 1)
            if myrand == 0:
                if self.y - y < 0:
                    self.move_down(obstacles)
                else:
                    self.move_up(obstacles)
            elif myrand == 1:
                if (self.x - x) < 0:
                    self.move_left(obstacles)
                else:
                    self.move_right(obstacles)
            else:
                raise ValueError("Error!")
        else:
            raise ValueError("Error!")

    def has_caught(self, x, y):
        if self.x == x and self.y == y: return True
        return False

    def calculate_damage(self, a_player):
        # This is just a thumbnail. In a future version of this program
        # the amount of damage received will depend on
        # - the strength of the attacker
        # - the amount of damage the weapon can deliver
        # - the quality of shielding the attacked has
        return self.maximum_damage

    # def debugging_info(self):
    #     # ---- Debugging (after) (top)----
    #     mylist = []
    #     mylist.append("character_name (from player): {}".format(self.player.name))
    #     mylist.append("x,y: ({},{})".format(self.player.x, self.player.y))
    #     mylist.append("zone_name: {}".format(self.zone_name))
    #     mylist.append("map_name: {}".format(self.map_name))
    #     mylist.append("------------")
    #     mylist.append("From file:")
    #     mydict = utils.get_user_data()
    #     mylist.append("character_name: {}".format(mydict["character_name"]))
    #     mylist.append("zone_name: {}".format(mydict["zone_name"]))
    #     mylist.append("map_name: {}".format(mydict["map_name"]))
    #     mylist.append("------------")
    #     mylist.append("From Player:")
    #     mylist.append("x,y: ({},{})".format(self.player.x, self.player.y))
    #     mylist.append("zone_name: {}".format(self.player.zone_name))
    #     mylist.append("map_name: {}".format(self.player.map_name))
    #     print("******************** Debugging (begin) ********************")
    #     print("-----------------------------------------------------------")
    #     print(mylist)
    #     print("---------------------------------------------------------")
    #     print("******************** Debugging (end) ********************")
    #     # ---- Debugging (after) (bottom) ----

    def have_interaction(self, events):
        # ---- Debugging (before) (top) ----
        print("BEFORE dialog")
        # self.debugging_info()
        result = None
        if self.is_monster == True and self.agro_level == "agro":
            pass
        elif self.is_monster == False:
            mydialog = DialogSpeech(self.name)
            mydialog.read_data()
            result = mydialog.main()
            # ----
            if result is None:
                raise ValueError("result is None.")
            print("debugging: this is the result: {}".format(result))
            choices = ["end game", "end conversation", "continue"]
            if not result in choices:
                s = "{} is not in {}".format(result, choices)
                raise ValueError(s)
            # ----
            if result == "end game":
                return result
            elif result == "end conversation":
                return result
            elif result == "continue":
                s = "conversation_with_{}_completed".format(self.name).replace(" ", "_")
                if events.set_a_value(s, True) == False:
                    raise ValueError("Error!")
                return result
            else:
                raise ValueError("Error! result = {}".format(result))

    def save_data(self):
        ud = utils.get_user_data()
        filepath = os.path.join("data", "playing_characters", ud["character_name"], "npcs", self.name)
        with open(filepath, "w") as f:
            f.write(self.get_fileline())

    def debug_print(self):
        s = "x,y: ({},{})\nname: {}, species: {}, profession: {}\n"
        s += "trigger: {}\n"
        s += "gold: {}, inventory_type: {}\n"
        s += "max_hit_points: {}, hit_points: {}, agro_level: {}, is_monster: {}\n"
        s += "maximum_damage: {}, chance_to_hit: {}, experience: {}\n"
        s += "image_kind: {}, image_filename: {}, image_dead_filename: {}\n"
        s += "is_monster: {}, comment: {}"
        s = s.format(self.x, self.y, self.name, self.species, self.profession,
                     self.trigger, self.gold, self.inventory_type, self.max_hit_points,
                     self.hit_points, self.agro_level, self.is_monster, self.maximum_damage, self.chance_to_hit,
                     self.experience, self.image_kind, self.image_filename, self.image_dead_filename,
                     self.is_monster, self.comment)
        print(s)

# -----------------------------------------------------------
#                      class NewNPCs
# -----------------------------------------------------------

class Npcs:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.init_pygame()  # <-- debugging
        self.all_sprites = pygame.sprite.Group()
        # ----
        self.npcs = []
        self.loop_index = 0
        self.keep_looping = True  # <-- debugging

    def read_data(self):
        self._load_map()
        # for npc in self.npcs:
        #     npc.load_images()
            # npc.load_inventory()

    def _load_map(self):
        filename = "{}_npcs.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # [print(i) for i in mytiles]
        # ------------------------------------------------------------------
        self.npcs = []
        for col, tiles in enumerate(mytiles):
            tile_list = tiles.split(";")
            tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
            for row, tile in enumerate(tile_list):
                if not tile == ".." and tile.find("p") == -1:
                    npc_name = utils.get_npc_name_from_map_code(self.zone_name, tile)
                    filename = "{}.txt".format(npc_name.replace(" ", "_"))
                    user_data = utils.get_user_data()
                    filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs", filename)
                    mylines = utils.read_file(filepath)
                    mydict = mylines[0]
                    # print("mydict: {}".format(mydict))
                    # ----
                    mydict["x"] = row
                    mydict["y"] = col
                    new_npc = Npc(mydict)
                    self.npcs.append(new_npc)
                # if tile == "p0":
                #     # This is the player. We read him/her in in class Player.
                #     pass
                elif tile == "n0":
                    raise NotImplemented
                    npc_name = utils.get_npc_name_from_map_code(self.zone_name, tile)
                    filename = "{}.txt".format(npc_name.replace(" ", "_"))
                    user_data = utils.get_user_data()
                    filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs", filename)
                    mylines = utils.read_file(filepath)
                    mydict = mylines[0]
                    # print("mydict: {}".format(mydict))
                    # ----
                    mydict["x"] = row
                    mydict["y"] = col
                    new_merchant = Npc(mydict)
                    self.npcs.append(new_merchant)
                elif tile == "m1":
                    raise NotImplemented
                    user_data = utils.get_user_data()
                    # ----
                    npc_name = utils.get_npc_name_from_map_code(self.zone_name, tile)
                    filename = "{}.txt".format(npc_name.replace(" ", "_"))
                    filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs", filename)
                    mydict = utils.read_file(filepath)[0]
                    # ----
                    mydict["x"] = row
                    mydict["y"] = col
                    # for key, value in mydict.items():
                        # print("{}: {}".format(key, value))
                    new_npc = Npc(mydict)
                    self.npcs.append(new_npc)
                elif tile == ".." or tile.find("p") > -1:
                    pass
                else:
                    s = "I don't recognize this tile: {}".format(tile)
                    raise ValueError(s)

    def debug_load_NPC(self, player_name, npc_name, x, y):
        if not (type(player_name) == type("abc")):
            raise ValueError("Error!")
        if not (type(npc_name) == type("abc")):
            raise ValueError("Error!")
        if not utils.is_int(x) or not utils.is_int(y):
            raise ValueError("Error!")
        # ----
        player_name = player_name
        npc_filename = "{}.txt".format(npc_name)
        filepath = os.path.join("data", "playing_characters", player_name, "npcs", npc_filename)
        mydict = utils.read_file(filepath)[0]
        # ----
        mydict["x"] = x
        mydict["y"] = y
        return Npc(mydict)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def debug_print(self):
        title, length = utils.format_string("Npcs.debug.print()", "-")
        print(title)
        for elem in self.npcs:
            print("-------------")
            elem.debug_print()
        print("*" * length)

    # --------------------------------------------------

    def closest_monster(self, player_x, player_y):
        player_location = (player_x, player_y)
        print("In closest_monster, player: ({},{})".format(player_x, player_y))
        closest_distance = 1000000
        monster_closest = None
        temp = -1
        # debugging
        if self.npcs is None:
            raise ValueError("Error!")
        for an_npc in self.npcs:
            print("This is an npc.")
            if an_npc.is_dead() == True:
                continue
            # an_npc.debug_print()
            if an_npc.is_monster == False:
                print("This npc, {}, is NOT a monster.".format(an_npc.name))
                continue
            temp = utils.distance_between_two_points((an_npc.x, an_npc.y), player_location)
            print("{}'s position: {}".format(an_npc.name, temp))
            if temp <= closest_distance:
                closest_distance = temp
                monster_closest = an_npc
        # ----
        if not monster_closest is None:
            if temp < monster_closest.attack_distance:
                return monster_closest
        return None

    # --------------------------------------------------

    def get_npc(self, x, y):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        for an_npc in self.npcs:
            if an_npc.x == x and an_npc.y == y:
                # print("Npc found:")
                # an_npc.debug_print()
                return an_npc
        return None

    def get_npc_if_monster(self, x, y):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        for an_npc in self.npcs:
            if an_npc.x == x:
                if an_npc.y == y:
                    if an_npc.is_monster == True:
                    # print("Npc found:")
                    # an_npc.debug_print()
                        return an_npc
        return None

    def get_npc_if_angel(self, x, y):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        for an_npc in self.npcs:
            if an_npc.x == x:
                if an_npc.y == y:
                    if an_npc.is_monster == False:
                    # print("Npc found:")
                    # an_npc.debug_print()
                        return an_npc
        return None

    def get_npc_by_name(self, npc_name):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        print("There are {} npcs.".format(len(self.npcs)))
        for an_npc in self.npcs:
            print("an_npc.name: {}, npc_name: {}".format(an_npc.name, npc_name))
            if an_npc.name.replace(" ", "_") == npc_name.replace(" ", "_"):
                return an_npc
        return None

        # def update_classes(self, all_sprites):
        #     for elem in self.npcs:
        #         all_sprites.add(elem)
        #     return all_sprites

    def __getitem__(self, item):
        return self.npcs[item]

    def __next__(self):
        if self.loop_index >= len(self.npcs):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.npcs[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.npcs)

        # --------------------------------------------

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True

    def update_classes(self, all_sprites):
        for elem in self.npcs:
            all_sprites.add(elem)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        """This is for debugging"""
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()

    def save_data(self):
        for elem in self.npcs:
            elem.save_data()
        # # --------------------------
        # # save data for each npc
        # user_data = utils.get_user_data()
        # filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs", "testing_npcs.txt")
        # with open(filepath, "w") as f:
        #     for an_npc in self.npcs:
        #         fileline = an_npc.get_fileline()
        #         f.write(fileline)
        # mark zone as visited if it isn't already marked as visited

# **************************************************
# **************************************************
zone_name = "green_lawn"
map_name = "map01"

def debugging_fauna():
    mydialog = Fauna(zone_name, map_name)
    mydialog.read_data()
    mydialog.main()

def debugging_npcs():
    mydialog = Npcs(zone_name, map_name)
    mydialog.read_data()
    mydialog.debug_print()
    # mydialog.main()

def debugging_player():
    myplayer = Player("swindon", "map00")
    myplayer.read_data()
    myplayer.debug_print()

if __name__ == "__main__":
    debugging_player()