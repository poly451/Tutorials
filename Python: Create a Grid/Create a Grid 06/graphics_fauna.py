import os, sys
import pygame
import utils
import constants
import random
from NEW_inventory import Inventory, Conversation
from dialogs import DialogSpeech, DialogInput, DialogText, DialogFight
from child_classes import GerekinNPC, QuestGiverNPC, SellNPC, \
    BuyNPC, NuisanceNPC, BystanderNPC, PredatorNPC, \
    MercenaryNPC, AssassinNPC

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
        if utils.validate_player_name(player_name) == False:
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
        # self.direction = constants.DOWN
        self.direction = utils.get_player_initial_direction(zone_name, map_name)
        # ---------------------------------------------
        self.maximum_damage = 2
        self.max_hit_points = -1
        self._hit_points = -1
        self.chance_to_hit = -1
        self.experience = -1
        self.profession = None
        # self._gold = -1
        # ---------------------------------------------
        self.inventory = None
        # ---------------------------------------------
        self.image = None
        self.rect = None
        # self.image_dead = None
        # self.image_up = None
        # self.image_down = None
        # self.image_right = None
        # self.image_left = None
        self.rect = None
        self.font = None
        # ---------------------------------------------
        self.model_name = utils.find_model_name()
        # self.image_model = "wanderer01"
        # self.image_down_filename = None
        # self.image_up_filename = None
        # self.image_right_filename = ""
        # self.image_left_filename = ""
        # self.image_dead_filename = ""
        # ---------------------------------------------
        d_100 = "down_health_100.png"
        self.image_down = d_100
        d_75 = "down_health_75.png"
        d_50 = "down_health_50.png"
        d_25 = "down_health_25.png"
        d_1 = "down_health_1.png"
        d_0 = "down_health_0.png"
        # ----
        u_100 = "up_health_100.png"
        self.image_up = u_100
        u_75 = "up_health_75.png"
        u_50 = "up_health_50.png"
        u_25 = "up_health_25.png"
        u_1 = "up_health_1.png"
        u_0 = "up_health_0.png"
        # ----
        r_100 = "right_health_100.png"
        self.image_right = r_100
        r_75 = "right_health_75.png"
        r_50 = "right_health_50.png"
        r_25 = "right_health_25.png"
        r_1 = "right_health_1.png"
        r_0 = "right_health_0.png"
        # ----
        l_100 = "left_health_100.png"
        self.image_left = l_100
        l_75 = "left_health_75.png"
        l_50 = "left_health_50.png"
        l_25 = "left_health_25.png"
        l_1 = "left_health_1.png"
        l_0 = "left_health_0.png"

        # ---------------------------------------------

        self.image_down_health_100 = self.load_image(d_100)
        self.image_down_health_75 = self.load_image(d_75)
        self.image_down_health_50 = self.load_image(d_50)
        self.image_down_health_25 = self.load_image(d_25)
        self.image_down_health_1 = self.load_image(d_1)
        self.image_down_health_0 = self.load_image(d_0)
        # ----
        self.image_up_health_100 = self.load_image(u_100)
        self.image_up_health_75 = self.load_image(u_75)
        self.image_up_health_50 = self.load_image(u_50)
        self.image_up_health_25 = self.load_image(u_25)
        self.image_up_health_1 = self.load_image(u_1)
        self.image_up_health_0 = self.load_image(u_0)
        # ----
        self.image_right_health_100 = self.load_image(r_100)
        self.image_right_health_75 = self.load_image(r_75)
        self.image_right_health_50 = self.load_image(r_50)
        self.image_right_health_25 = self.load_image(r_25)
        self.image_right_health_1 = self.load_image(r_1)
        self.image_right_health_0 = self.load_image(r_0)
        # ----
        self.image_left_health_100 = self.load_image(l_100)
        self.image_left_health_75 = self.load_image(l_75)
        self.image_left_health_50 = self.load_image(l_50)
        self.image_left_health_25 = self.load_image(l_25)
        self.image_left_health_1 = self.load_image(l_1)
        self.image_left_health_0 = self.load_image(l_0)
        # ---------------------------------------------
        # self.image_down = None
        # self.image_up = None
        # self.image_right = None
        # self.image_left = None
        self.image_dead = self.load_image("skull_and_bones.png")
        self.display_image = d_100
        # ---------------------------------------------
        # self.load_images()
        self.my_update_image()

    @property
    def hit_points(self):
        return self._hit_points

    # @property
    # def gold(self):
    #     return self._gold

    @hit_points.setter
    def hit_points(self, value):
        if value is None:
            raise ValueError("Error")
        elif value < 0:
            # raise ValueError("Error")
            self._hit_points = 0
        else:
            self._hit_points = value
        # ----
        self.my_update_image()

    # @gold.setter
    # def gold(self, value):
    #     if value is None: raise ValueError("Error")
    #     elif utils.is_int(value) == False: raise ValueError("Error")
    #     elif type(value) != type(123): raise ValueError("Error")
    #     else:
    #         s = "current_gold: {}; value being added: {}; ".format(self._gold, value)
    #         self._gold += value
    #         s += "gold after update: {}".format(self._gold)
    #         print(s)

    @hit_points.deleter
    def hit_points(self):
        del self._hit_points

    # @gold.deleter
    # def gold(self):
    #     del self._gold

    # ---- ---- ---- ----

    def load_image(self, filename):
        if filename is None: raise ValueError("Error")
        if len(filename) == 0: raise ValueError("Error")
        filepath = utils.get_model_filepath(filename, self.model_name)
        try:
            an_image = pygame.image.load(filepath).convert_alpha()
            an_image = pygame.transform.scale(an_image, (constants.TILESIZE, constants.TILESIZE))
            # the_rect = self.image.get_rect()
            # the_rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        except Exception as e:
            s = "{}\nfilename: {}".format(e, filepath)
            raise ValueError(s)
        return an_image

    def load_images(self):
        initial_position = utils.get_initial_player_position(self.zone_name, self.map_name)
        if not initial_position in ["up", "down", "right", "left"]:
            raise ValueError("Error")
        # ----
        if initial_position == "up":
            self.image = self.image_up_health_100
        elif initial_position == "down":
            self.image = self.image_down_health_100
        elif initial_position == "right":
            self.image = self.image_right_health_100
        elif initial_position == "left":
            self.image = self.image_left_health_100
        else:
            raise ValueError("Error")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def my_update_image(self):
        # print("In update_image.... **********************************")
        if utils.health_percent(self.max_hit_points, self._hit_points) >= 100:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_100
                if self.image is None:
                    raise ValueError("Error")
                # print("in def my_update_image: type: {}".format(type(self.image)))
            elif self.direction == constants.UP:
                self.image = self.image_up_health_100
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_100
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_100
            else:
                print("direction: {}".format(self.direction))
                print("conversation: {}".format(utils.convert_integer_to_direction(self.direction)))
                raise ValueError("Error")
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        elif utils.health_percent(self.max_hit_points, self._hit_points) >= 75:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_75
            elif self.direction == constants.UP:
                self.image = self.image_up_health_75
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_75
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_75
            else:
                raise ValueError("Error")
        elif utils.health_percent(self.max_hit_points, self._hit_points) >= 50:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_50
            elif self.direction == constants.UP:
                self.image = self.image_up_health_50
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_50
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_50
            else:
                raise ValueError("Error")
        elif utils.health_percent(self.max_hit_points, self._hit_points) >= 25:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_25
            elif self.direction == constants.UP:
                self.image = self.image_up_health_25
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_25
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_25
            else:
                raise ValueError("Error")
        elif utils.health_percent(self.max_hit_points, self._hit_points) > 5:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_1
            elif self.direction == constants.UP:
                self.image = self.image_up_health_1
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_1
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_1
            else:
                raise ValueError("Error")
        elif utils.health_percent(self.max_hit_points, self._hit_points) >= 1:
            if self.direction == constants.DOWN:
                self.image = self.image_down_health_0
            elif self.direction == constants.UP:
                self.image = self.image_up_health_0
            elif self.direction == constants.RIGHT:
                self.image = self.image_right_health_0
            elif self.direction == constants.LEFT:
                self.image = self.image_left_health_0
            else:
                raise ValueError("Error")
        elif utils.health_percent(self.max_hit_points, self._hit_points) <= 0:
            if self.direction == constants.DOWN:
                # self.image = self.image_down_health_0
                self.image = self.image_dead
            elif self.direction == constants.UP:
                # self.image = self.image_up_health_0
                self.image = self.image_dead
            elif self.direction == constants.RIGHT:
                # self.image = self.image_right_health_0
                self.image = self.image_dead
            elif self.direction == constants.LEFT:
                # self.image = self.image_left_health_0
                self.image = self.image_dead
            else:
                raise ValueError("Error")
        else:
            print("max_hit_points: {}, hit_points: {}".format(self.max_hit_points, self._hit_points))
            print("health_percent: {}".format(utils.health_percent(self.max_hit_points, self._hit_points)))
            raise ValueError("Error")
        # ----
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

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
        path = os.path.join("data", "playing_characters", player_name, constants.PLAYER_DATA_FILE)
        mylist = utils.read_file(path)
        mydict = mylist[0]
        self.x, self.y = utils.get_map_xy_for_player(self.zone_name, self.map_name)
        if self.x is None or self.y is None:
            s = "Error! Have you remembered to include the player in the npc map?"
            raise ValueError(s)
        if self.x < 0 or self.y < 0:
            s = "Error! Both x and y must be above zero. x,y = ({},{})".format(self.x, self.y)
            raise ValueError(s)
        # ----
        self.name = self.player_name
        self.species = mydict["species"]
        # if utils.is_int(mydict["direction"]) == True:
        #     self.direction = int(mydict["direction"])
        # else:
        #     self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        self.profession = mydict["profession"]
        # self.gold = mydict["gold"]
        # ----
        # print("here is mydict in read_data_first:")
        # print(mydict)
        # self.image_down_filename = mydict["image_down"]
        # self.image_up_filename = mydict["image_up"]
        # self.image_right_filename = mydict["image_right"]
        # self.image_left_filename = mydict["image_left"]
        # self.image_dead_filename = mydict["image_dead"]
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
        # self.load_images()
        self.my_update_image()

    def read_data(self):
        self._read_player_data_from_file()
        self.inventory = Inventory(player_name=self.player_name, npc_name=None, character_type="player")
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
        a = "name: {}\nspecies: {}\ndirection: {}\n".format(self.name, self.species, "-90")
        a += "max_hit_points: {}\nhit_points: {}\n".format(self.max_hit_points, self.hit_points)
        a += "chance_to_hit: {}\nexperience: {}\nprofession: {}\n".format(self.chance_to_hit, self.experience, self.profession)
        # b = "image_down: {}\nimage_up: {}\n".format(self.image_down_health_100, self.image_up_health_100)
        # b += "image_right: {}\nimage_left: {}\n".format(self.image_right_health_100, self.image_left_health_100)
        a += "image_model: {}\n".format(self.model_name)
        return a

    def save_data(self):
        player_string = self.get_fileline()
        filepath = os.path.join("data", "playing_characters", self.name, constants.PLAYER_DATA_FILE)
        with open(filepath, "w") as f:
            f.write(player_string)
        self.inventory.save_data()

    def resize(self, tilesize, new_x, new_y):
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
            return False
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
        s += "hit_points: {}; chance_to_hit: {}; experience: {}; profession: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.direction, self.max_hit_points,
                     self.hit_points, self.chance_to_hit, self.experience, self.profession)
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
#                      class NewNPCs
# -----------------------------------------------------------

class Npcs:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        user_info = utils.get_user_data()
        self.player_name = user_info["character_name"]
        # ----
        self.init_pygame()  # <-- debugging
        self.all_sprites = pygame.sprite.Group()
        # ----
        self.npcs = []
        self.loop_index = 0
        self.keep_looping = True  # <-- debugging

    def read_data(self):
        self._load_map()

    def _load_map(self):
        """
        This function loads data from both the npc files in the master files directory
        AND the NPC data contained in the npcs.txt file contained in the
        specific zone/map directory the NPC is in.
        """
        # ---- Debugging ----
        user_data = utils.get_user_data()
        if not user_data["zone_name"] == self.zone_name:
            s = "{} != {}".format(user_data["zone_name"], self.zone_name)
            raise ValueError(s)
        # ----
        # print("Getting coords from the map")
        tiles = utils.get_coords_from_map(self.zone_name, self.map_name)
        # print("tile_names: {}".format(tiles))
        # If there are no tiles in the map, there is nothing to load.
        if len(tiles) == 0:
            self.npcs = []
            return False
        # ----
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "npcs.txt")
        print("Debugging: this is the filepath for npcs.txt: {}".format(filepath))
        npc_lists = utils.read_data_file(filepath, 7)
        # print("npc_list: {}".format(npc_lists))
        # ----
        # ----
        # print("=================+++++")
        big_list = []
        for tile in tiles:
            # if tile["tile"].find("a") > -1:
            #     s = "It looks as though you may have player's coords (p0, p1, p2, etc.)\n"
            #     s += "in the <map_name>_npcs.txt data file."
            #     raise ValueError(s)
            npc_dict = utils.get_dict(npc_lists, key="tile", value=tile["tile"])
            # print("------")
            # print("local_npc_stats: {}".format(npc_lists))
            # print("tile name: {}".format(tile["tile"]))
            # print("npc_dict: {}".format(npc_dict))
            # print("---------")
            # print("npc_dict: {}".format(npc_dict))
            # print("tile: {}".format(tile))
            new_dict = utils.merge_two_dictionaries(npc_dict, tile)
            # print("new_dict: {}".format(new_dict))
            # raise NotImplemented
            # print(new_dict)
            # ----
            filepath = os.path.join("data", "playing_characters", self.player_name, "npcs", new_dict["npc_file"])
            print("filepath for npc_main_file: {}".format(filepath))
            npc_main_file = utils.read_file(filepath)[0]
            # print("npc_file_dict: {}".format(npc_main_file))
            # print(npc_file_dict)
            # ----
            # print("new_dict: {}".format(new_dict))
            # print("npc_file_dict: {}".format(npc_main_file))
            big_dict = utils.merge_two_dictionaries(npc_main_file, new_dict)
            # print("big_dict: {}".format(big_dict))
            # raise NotImplemented
            # print("big_dict: {}".format(big_dict))
            # raise NotImplemented
            # print(new_dict)
            big_list.append(big_dict)
            # raise NotImplemented
        print("++++++++++++++")
        # At this point big_list contains all the data I need to construct all the
        # NPCs in any one map area (in the zones directory).
        self.npcs = []
        for mydict in big_list:
            # print("mydict: {}".format(mydict))
            try:
                temp = mydict["function"]
            except Exception as e:
                t = "This is the record for the NPC: {}\n".format(mydict["name"])
                t += "You need to add a FUNCTION field to it."
                s = "{}\n{}\n".format(e, t)
                raise ValueError(s)
            if mydict["function"] == "resource":
                new_object = GerekinNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "questgiver":
                new_object = QuestGiverNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "sell":
                new_object = SellNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "buy":
                new_object = BuyNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "nuisance":
                new_object = NuisanceNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "bystander":
                new_object = BystanderNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "predator":
                new_object = PredatorNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "mercenary":
                new_object = MercenaryNPC(mydict)
                self.npcs.append(new_object)
            elif mydict["function"] == "assassin":
                new_object = AssassinNPC(mydict)
                self.npcs.append(new_object)
            # elif mydict["function"] == "talkandfight":
            #     new_object = TalkAndFightNPC(mydict)
            #     self.npcs.append(new_object)
            else:
                s = "I don't recognize this: {}".format(mydict["function"])
                raise ValueError(s)
        # print("********** debugging ***********")
        # self.debug_print()
        # raise NotImplemented

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
        print("FILEPATH: {}".format(filepath))
        mydict = utils.read_file(filepath)[0]
        # ----
        mydict["x"] = x
        mydict["y"] = y
        mynpc = Npc(mydict)
        return mynpc

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

    def _this_npc_is_a_questgiver(self, npc, x, y):
        raise NotImplemented
        current_npc = self.npcs.get_npc(self.player.x, self.player.y)
        if current_npc is None:
            s = "Error! There should be an NPC here, but there isn't."
            raise ValueError(s)
        if current_npc.is_a_questgiver(self.zone_name, self.map_name) == True:
            return True
        return False

    def do_something(self, player):
        message = ""
        # ----
        this_npc = self.get_npc(player.x, player.y)
        if this_npc is None: raise("Error!")
        if not this_npc.function in constants.NPC_FUNCTION:
            raise ValueError("Error")
        # ----
        if this_npc.function == "questgiver":
            myobject = Conversation(self.player_name, this_npc.name,
                                    self.zone_name, self.map_name)
            myobject.read_data()
            return myobject.main()
        elif this_npc.function == "bystander":
            myobject = Conversation(self.player_name, this_npc.name,
                                    self.zone_name, self.map_name, conversation_only=True)
            myobject.read_data()
            return myobject.main()
        elif this_npc.function == "resource":
            if this_npc.number_of_resources == 0:
                mydialog = DialogText("Doh! This critter doesn't have any resources left.")
                mydialog.main()
            elif this_npc.number_of_resources > 0:
                this_npc.number_of_resources -= 1
                player.inventory.add_item_by_name(this_npc.resource, 1)
                mydialog = DialogText("You acquire a blue feather!")
                mydialog.main()
            else:
                s = "Something is wrong! {}".format(this_npc.resource)
                raise ValueError(s)
            # ----
            if this_npc.gold > 0:
                gold_coins = player.inventory.get_item_by_name("gold coin")
                if gold_coins is None: raise ValueError("Error")
                gold_coins.units += this_npc.gold
        elif this_npc.function == "buy":
            myobject = Conversation(self.player_name, this_npc.name,
                                    self.zone_name, self.map_name, conversation_only=True)
            myobject.read_data()
            return myobject.main()
        elif this_npc.function == "sell":
            myobject = Conversation(self.player_name, this_npc.name,
                                    self.zone_name, self.map_name, conversation_only=True)
            myobject.read_data()
            return myobject.main()
        elif this_npc.function == "nuisance":
            pass
        elif this_npc.function == "predator":
            mydialog = DialogFight(player, this_npc)
            mydialog.main()
            if this_npc.is_dead() == True:
                this_npc.image = this_npc.image_dead
        elif this_npc.function == "mercenary":
            myobject = Conversation(self.player_name, this_npc.name,
                                         self.zone_name, self.map_name)
            myobject.read_data()
            message, player.player_inventory = myobject.main()
        elif this_npc.function == "assassin":
            if this_npc.is_dead() == True:
                mydialog = Conversation(self.player_name, this_npc.name,
                                        self.zone_name, self.map_name)
                mydialog.read_data()
                return mydialog.main()
            else:
                mydialog = DialogFight(player, this_npc)
                mydialog.main()
                if this_npc.is_dead() == True:
                    this_npc.image = this_npc.image_dead
        else:
            s = "Error: I don't understand this function: {}".format(this_npc.function)
            raise ValueError(s)
        return message, player.inventory

    # --------------------------------------------------

    def turn_all_agro(self):
        for elem in self.npcs:
            elem.agro_level = "agro"

    def closest_agro_npc_to_talk(self, player_x, player_y):
        player_location = (player_x, player_y)
        # ----
        print("In def closest_agro_npc. Here are coords: player: ({},{})".format(player_x, player_y))
        closest_distance = 1000000
        monster_closest = None
        temp = -1
        # debugging
        if self.npcs is None:
            raise ValueError("Error!")
        for an_npc in self.npcs:
            if an_npc.is_dead() == True:
                continue
            if an_npc.agro_level == "passive":
                continue
            if an_npc.is_monster == True:
                continue
            if an_npc.on_contact == "talk":
                temp = utils.distance_between_two_points((an_npc.x, an_npc.y), player_location)
                # print("{}'s position: {}".format(an_npc.name, temp))
                # print("temp: {}, closest_distance: {}".format(temp, closest_distance))
                if temp <= closest_distance:
                    closest_distance = temp
                    monster_closest = an_npc
        # ----
        if not monster_closest is None:
            # print("temp: {}, attack_distance: {}".format(temp, monster_closest.attack_distance))
            if temp < monster_closest.attack_distance:
                return monster_closest
        return None

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

    def remove_npc(self, target_npc):
        def is_okay(an_npc, target_npc):
            if an_npc.name != target_npc.name: return False
            if an_npc.species != target_npc.species: return False
            if an_npc.profession != target_npc.profession: return False
            return True
        # ----
        mylist = []
        for an_npc in self.npcs:
            if is_okay(an_npc, target_npc) == True:
                pass
            else:
                mylist.append(an_npc)
        if mylist is None: raise ValueError
        # print("debugging: mylist: {}".format(mylist))
        # print("self.npcs: npcs: {}".format(self.npcs))
        # print("length: {}".format(len(self.npcs)))
        # raise NotImplemented
        if not(len(mylist) + 1 == len(self.npcs)):
            raise NotImplemented("Error")
        self.npcs = mylist

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

    def get_agro_npcs(self):
        mylist = []
        for an_npc in self.npcs:
            if an_npc.agro_level == "agro":
                mylist.append(an_npc)
        return mylist

    def get_agro_fight_monsters(self):
        mylist = []
        for an_npc in self.npcs:
            if an_npc.agro_level == "agro" and an_npc.on_contact == "fight" and an_npc.is_monster == True:
                mylist.append(an_npc)
        return mylist

    def get_agro_flee_npcs(self):
        mylist = []
        for an_npc in self.npcs:
            if an_npc.agro_level == "agro" and an_npc.on_contact == "flee" and an_npc.is_monster == False:
                mylist.append(an_npc)
        return mylist

    def get_agro_talk_npcs(self):
        mylist = []
        for an_npc in self.npcs:
            if an_npc.agro_level == "agro" and an_npc.on_contact == "talk" and an_npc.is_monster == False:
                mylist.append(an_npc)
        return mylist

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
        player_info = utils.get_user_data()
        player_name = player_info["character_name"]
        # ----
        s = ""
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
# zone_name = "green_lawn"
zone_name = "bridge"
map_name = "map00"
npc_name = "westley"
player_name = "henry"

# def debugging_fauna():
#     mydialog = Fauna(zone_name, map_name)
#     mydialog.read_data()
#     mydialog.main()

def debugging_npcs():
    # user_info = utils.get_user_data()
    # zone_name = user_info["zone_name"]
    # map_name = user_info["map_name"]
    # zone_name = "swindon_pub"
    zone_name = "green_lawn"
    map_name = "map01"
    mydialog = Npcs(zone_name, map_name)
    mydialog.read_data()
    mydialog.debug_print()
    mydialog.main()

def debugging_npc_with_player(npc_name, player_name):
    mydialog = Npcs(zone_name, map_name)
    mydialog.read_data()
    mydialog.main()

def debugging_player():
    # make sure the player is on the map
    player_coords = utils.get_map_xy_for_player(zone_name, map_name)
    print("player's coords: {}".format(player_coords))
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    print("&&&&&&&&& *******" * 4)
    myplayer.debug_print()

if __name__ == "__main__":
    debugging_npcs()
    # debugging_player()
    # debugging_npc_with_player(npc_name, player_name)