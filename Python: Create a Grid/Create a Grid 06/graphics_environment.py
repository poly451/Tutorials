import sys, os
import pygame
import constants
import utils
from mysprites import HandleMovingSprite
# -----------------------------------------------------------
#                      class PersistentObject
# -----------------------------------------------------------
class PersistentObject(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        print("mydict: {}".format(mydict))
        self.x, self.y = -1, -1
        self.name = ""
        self.command = ""
        # self.image_display = ""
        # self.image_kind = ""
        self.image_filename = ""
        self.image_path = ""
        self.data = ""
        self.inventory_condition = ""
        # game_condition --> Quest_Completed?
        self.game_condition = ""
        # "quest_accepted" of the form:
        # "quest_name: <quest_name>
        # The above line would be placed in the data field.
        # self.quest_accepted would simply be true or false.
        self.quest_accepted = ""
        self.dialog_text = ""
        self.comment = ""
        self.completed = False
        # ----
        self.image = None
        self.rect = None
        # ----------------------------
        self.x, self.y = mydict["x"], mydict["y"]
        self.name = mydict["name"]
        self.command = mydict["command"]
        self.image_filename = mydict["image_filename"]
        self.image_path = utils.get_filepath(self.image_filename)
        self.data = mydict["data"]
        self.quest_dict = {}
        # ----
        self.inventory_condition = mydict["inventory_condition"].strip().lower()
        if self.inventory_condition == "none": self.inventory_condition = None
        self.game_condition = mydict["game_condition"].strip().lower()
        if self.game_condition == "none": self.game_condition = None
        # ----
        self.quest_accepted = mydict["quest_accepted"].strip().lower()
        if len(self.quest_accepted) == 0: self.quest_accepted = None
        elif self.quest_accepted == "none": self.quest_accepted = None
        elif self.quest_accepted == "true": raise ValueError("Error")
        elif self.quest_accepted == "false": self.quest_accepted = False
        elif len(self.quest_accepted) > 0:
            self.quest_dict = self._parse_quest_accepted(self.quest_accepted)
            # print("kdkdkddd")
            # print(self.quest_dict)
            # raise NotImplemented
        else:
            s = "I don't understand this: {}".format(self.quest_accepted)
            raise ValueError(s)
        # print("888888888")
        # print(self.quest_accepted)
        # raise NotImplemented
        # ----
        self.dialog_text = mydict["dialog_text"]
        self.comment = mydict["comment"]
        # --
        self.completed = False
        # -------------------------------------------------
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(self.image_path)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----

    def _parse_quest_accepted(self, mystring):
        # data_string = npc_name: <name>; zone_name: <zone_name>; map_name: <map_name>
        mylist = mystring.lower().split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        mydict = {}
        for elem in mylist:
            mydict = utils.key_value(elem, mydict)
        return mydict

    def conditions_passed(self, zone_name, map_name, inventory):
        myinventory_condition = False
        mygame_condition = False
        myquest_accepted = False
        # ----
        if self.inventory_condition in ["any", None]:
            myinventory_condition = True
        if self.game_condition in ["any", None]:
            # print("There was no inventory or game condition.")
            mygame_condition = True
        if self.quest_accepted in ["any", None]:
            myquest_accepted = True
        if myinventory_condition == True and mygame_condition == True and myquest_accepted == True:
            return True
        # ---- ---- ---- ----
        if not self.inventory_condition in ["any", None]:
            print("There is an inventory condition: {}".format(self.inventory_condition))
            the_item = inventory.get_item_by_name(self.inventory_condition)
            if the_item is None:
                print("the item ({}) was not found in the inventory".format(self.inventory_condition))
                myinventory_condition = False
        else:
            myinventory_condition = True
        # ----
        if not self.game_condition in ["any", None]:
            print("There is a game condition: {}".format(self.game_condition))
            raise NotImplemented
            # this_value = events.get_a_value(self.game_condition)
            # if this_value is None:
            #     print("An event that matched this game condition was not found.")
            #     raise ValueError("Error!")
            # return this_value
        if not self.quest_accepted in ["any", None]:
            # raise NotImplemented
            if len(self.quest_dict) == 0:
                s = "This is self.quest_dict: {}".format(self.quest_dict)
                raise ValueError(s)
            # print("quest accepted: {}".format(self.quest_accepted))
            # ----
            from NEW_inventory import SearchMasterQuests
            all_histories = SearchMasterQuests()
            # print("dict: {}".format(self.quest_dict))
            # print("quest name: {}".format(self.quest_dict["quest_name"]))
            this_quest = all_histories.get_quest_by_quest_name(self.quest_dict["quest_name"])
            # print("Looking at quest: {}".format(self.quest_dict["quest_name"]))
            # print("DEBUGGING: ")
            # print("this_quest.quest_accepted: {} ({})".format(this_quest.quest_accepted, type(this_quest.quest_accepted)))
            # this_quest.debug_print()
            # raise NotImplemented
            if this_quest is None:
                s = "{}\n".format(self.quest_dict)
                s += "I could not find a quest for this quest name: --{}--".format(self.quest_dict["quest_name"])
                raise ValueError(s)
            if this_quest.quest_accepted == True:
                myquest_accepted = True
            else:
                myquest_accepted = False
        # ----
        # print("myinventory_condition: {}".format(myinventory_condition))
        # print("mygame_condition: {}".format(mygame_condition))
        # print("myquest_accepted: {}".format(myquest_accepted))
        # raise NotImplemented
        if myinventory_condition == True and mygame_condition == True and myquest_accepted == True:
            return True
        return False


    def parse_data(self):
        # print("data string: {}".format(self.data))
        mylist = self.data.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        # print("mylist: {}".format(mylist))
        mydict = {}
        mydict = utils.key_value(mylist[0], mydict)
        mydict = utils.key_value(mylist[1], mydict)
        return mydict["zone_name"], mydict["map_name"]

    def load_different_image(self, filename):
        # filename = "gold_ring.png"
        self.image_filename = filename
        self.image_path = utils.get_filepath(filename)
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))

    def debug_print(self):
        s = "x,y: ({},{});\nname: {};\ncommand: {};\nimage_filename: {};\nimage_path: {};\n"
        s += "data: {};\ninventory_condition: {};\ngame_condition: {};\ndialog_text: {};\ncomment: {};\n"
        s += "completed: {}"
        s = s.format(self.x, self.y, self.name, self.command, self.image_filename,
                     self.image_path, self.data, self.inventory_condition, self.game_condition,
                     self.dialog_text, self.comment, self.completed)
        print(s)

# -----------------------------------------------------------
#                      class PersistentObjects
# -----------------------------------------------------------
class PersistentObjects:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.inner = []
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data(self):
        self._load_map()
        print("{} records in PersistentObjcts have been read in.".format(len(self.inner)))

    def _load_map(self):
        print("Loading _load_map")
        filename = "{}_persistents.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        print("opening zone filepath: {}".format(filepath))
        if utils.file_is_empty(filepath) == True:
            return False
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # print(mytiles)
        # raise NotImplemented
        # ------------------------------------------------------------------
        path = os.path.join("data", "zones", self.zone_name, self.map_name, "persistents.txt")
        if utils.file_is_empty(path) == True:
            print("File is empty.")
            return False
        tile_list = utils.read_data_file(path, num_of_fields=9)
        if tile_list is None:
            raise ValueError("Error! tile_list is None.")
        if len(tile_list) == 0:
            raise ValueError("Error! tile_list is empty.")
        # print("====================================================")
        # print(tile_list)
        # raise NotImplemented
        # ------------------------------------------------------------------
        self.inner = []
        for col, tiles in enumerate(mytiles):
            # print(tiles)
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            # [print(i) for i in list_tiles]
            # print(list_tiles)
            # raise NotImplemented
            for row, tile in enumerate(list_tiles):
                # print(tile)
                if tile == "..":
                    pass
                elif len(tile) > 0:
                    # print(tile)
                    # raise NotImplemented
                    mydict = utils.get_dictionary(tile_list, tile)
                    if mydict is None:
                        s = "mydict is None.\n"
                        s += "tile: {}\n".format(tile)
                        s += "Did you make sure that the new tiles you added to mapXX_persistents.txt have\n"
                        s += "matching tiles in the persistents.txt file? It looks like you might have\nforgotten "
                        s += "to do that."
                        raise ValueError(s)
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["name"] = tile
                    new_object = PersistentObject(mydict)
                    self.inner.append(new_object)
                else:
                    s = "Error! I don't recognize this: -{}-".format(tile)
                    raise ValueError(s)

    # def conditions_passed(self, player, events):
    #     current_object = self.get_persistent_object(player.x, player.y)
    #     if current_object is None:
    #         # We should not have reached this point unless there was an object
    #         # on the player's tile.
    #         raise ValueError("Error!")
    #     # current_object.debug_print()
    #     return current_object.conditions_passed(player.inventory, events)

    def conditions_passed(self, player):
        current_object = self.get_persistent_object(player.x, player.y)
        if current_object is None:
            # We should not have reached this point unless there was an object
            # on the player's tile.
            raise ValueError("Error!")
        # current_object.debug_print()
        return current_object.conditions_passed(self.zone_name, self.map_name, player.inventory)

    def remove_tile(self, x, y):
        print("Number of objects BEFORE: {}".format(len(self.inner)))
        mylist = []
        self.all_sprites = pygame.sprite.Group()
        for elem in self.inner:
            if elem.x == x and elem.y == y:
                pass
            else:
                mylist.append(elem)
        print("Number of objects AFTER: {}".format(len(mylist)))
        self.inner = mylist

    def get_persistent_object(self, x, y):
        # print(self.inner)
        if self.inner is None:
            raise ValueError("Error!")
        if len(self.inner) == 0:
            raise ValueError("Error!")
        # ----
        for elem in self.inner:
            if elem.x == x and elem.y == y:
                return elem
        return None

    def get_persistent_object_by_name(self, name):
        # print(self.inner)
        if self.inner is None:
            raise ValueError("Error!")
        if len(self.inner) == 0:
            raise ValueError("Error!")
        # ----
        for elem in self.inner:
            if elem.name == name:
                return elem
        return None

    # ---------------------------------------------------

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    # ------------------------------------------------------

    def update_classes(self, all_sprites):
        for elem in self.inner:
            # print("debugging: {}".format(elem.image_path))
            all_sprites.add(elem)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites = self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    # ------------------------------------------------------

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

    def debug_test(self):
        for an_object in self.inner:
            if len(an_object.game_condition) == 0:
                return False
        return True

    def __len__(self):
        return len(self.inner)

# -----------------------------------------------------------
#                      class Event
# -----------------------------------------------------------
class Event:
    def __init__(self, mydict):
        # print("mydict: {}".format(mydict))
        self.index = mydict["index"]
        if not type(self.index) == type(123):
            s = "Error! This is the index: {} ({})".format(self.index, type(self.index))
            raise ValueError(s)
        self.condition = mydict["condition"]
        s = mydict["value"].lower().strip()
        if s == "true":
            self._is_fulfillled = True
        elif s == "false":
            self._is_fulfillled = False
        else:
            raise ValueError("Error")
        # ----

    @property
    def is_fulfilled(self):
        print("Getting value Event.has_been_done. Is: {}".format(self._is_fulfillled))
        return self._is_fulfillled

    @is_fulfilled.setter
    def is_fulfilled(self, new_value):
        print("_is_fulfilled being set to {}".format(new_value))
        if not new_value in [True, False]:
            raise ValueError("Error!")
        self._is_fulfillled = new_value

    @is_fulfilled.deleter
    def is_fulfilled(self):
        del self._is_fulfillled

    def fileline(self):
        s = "index: {}\ncondition: {}\nvalue: {}\n"
        s = s.format(self.index, self.condition, self.is_fulfilled)
        return s

    def debug_print(self):
        s = "index: {}, condition: {}, value: {} ({})"
        s = s.format(self.index, self.condition, self.is_fulfilled, type(self.is_fulfilled))
        print(s)


# -----------------------------------------------------------
#                      class Events
# -----------------------------------------------------------
class Events:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.events = []

    def read_data(self):
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "events.txt")
        print("filepath: {}".format(filepath))
        if utils.file_is_empty(filepath) == True:
            return False
        mylist = utils.read_data_file(filepath, 3)
        for a_dict in mylist:
            # print(a_dict)
            new_elem = Event(a_dict)
            self.events.append(new_elem)

    def save_data(self):
        s  = ""
        for elem in self.events:
            s += "{}\n".format(elem.fileline())
        print("debug map_name: {}".format(self.map_name))
        print("debug s: {}".format(s))
        # if self.map_name == "map01":
        #     raise NotImplemented
        # else:
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "events.txt")
        with open(filepath, "w") as f:
            f.write(s)

    def set_a_value(self, condition, value):
        if not value in [False, True]:
            raise ValueError("Error")
        # ----
        """Looks up whether a particular condition in events.txt was satisfied."""
        for elem in self.events:
            # print("key: -{}-, condition: -{}-".format(elem.condition, condition))
            if elem.condition == condition:
                elem.is_fulfilled = value
                return True
        return False

    def get_a_value(self, condition):
        if len(condition) == 0:
            raise ValueError("Error!")
        # ----
        for elem in self.events:
            if elem.condition == condition:
                return elem.is_fulfilled
        return None

    def debug_print(self):
        for elem in self.events:
            elem.debug_print()

# -----------------------------------------------------------
#                      class Action
# -----------------------------------------------------------
class Action(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.x, self.y = x, y
        self.name = name
        self.command = ""
        self.image_display = ""
        self.data = ""
        self.inventory_condition = ""
        self.game_condition = ""
        self.dialog_text = ""
        self.comment = ""
        self.completed = False
        # ----
        self.image = None
        self.rect = None

    def read_data(self, zone_name, map_name):
        filepath = os.path.join("data", "zones", zone_name, map_name, "actions.txt")
        mylines = utils.read_data_file(filepath, 8)
        if mylines is None or len(mylines) == 0:
            raise ValueError("Error!")
        # ----
        target_dict = {}
        for elem in mylines:
            if elem["name"] == self.name:
                target_dict = elem
        if len(target_dict) == 0:
            s = "The name {} was not found in {}".format(self.name, target_dict)
            raise ValueError(s)
        self.command = target_dict["command"]
        if not self.command in constants.MAP_COMMANDS:
            raise ValueError("Error! {} is not in {}".format(target_dict["command"], constants.MAP_COMMANDS))
        self.image_display = target_dict["image_display"]
        self.data = target_dict["data"]
        self.inventory_condition = target_dict["inventory_condition"]
        if self.inventory_condition == "none":
            self.inventory_condition = None
        # Need to be able to check that the player has successfully
        # completed a conversation.
        # Perhaps also check to see that the conversation is in the
        # events file.
        self.game_condition = target_dict["game_condition"].lower().strip()
        if self.game_condition == "none":
            self.game_condition = None
        self.dialog_text = target_dict["dialog_text"]
        self.comment = target_dict["comment"]
        self.completed = False
        # ----
        self.image_display = self.image_display.replace(" ", "_")
        if self.image_display.find(".png") == -1:
            self.image_display = "{}.png".format(self.image_display)
        filepath = utils.get_filepath(self.image_display)
        if filepath is None:
            s = "I wasn't able to find a path for the file: {}".format(self.image_display)
            raise ValueError(s)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def conditions_passed(self, inventory):
        inventory_condition_okay = False
        quest_completed_okay = False
        # ----
        if self.inventory_condition in ["any", None]:
            print("There was no inventory condition")
            inventory_condition_okay = True
        if self.game_condition in ["any", None]:
            print("There was no game condition")
            quest_completed_okay = True
        # ----
        if not self.inventory_condition in ["any", None]:
            print("There is an inventory condition: {}".format(self.inventory_condition))
            the_item = inventory.get_item_by_name(self.inventory_condition)
            if the_item is None:
                print("the item ({}) was not found in the inventory".format(self.inventory_condition))
                inventory_condition_okay = False
            else:
                print("the item ({}) WAS found in the inventory".format(self.inventory_condition))
                inventory_condition_okay = True
        if not self.game_condition in ["any", None]:
            print("There is a game condition: {}".format(self.game_condition))
            # If there is a game condition then it will be a condition that a certain
            # quest has been completed.
            raise NotImplemented
        if inventory_condition_okay == True and quest_completed_okay == True:
            return True
        return False
    # ---------------------

    def parse_data(self):
        # print("data string: {}".format(self.data))
        mylist = self.data.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        # print("mylist: {}".format(mylist))
        mydict = {}
        mydict = utils.key_value(mylist[0], mydict)
        mydict = utils.key_value(mylist[1], mydict)
        return mydict

    def display_text(self):
        return self.dialog_text

    def debug_print(self):
        s = "x,y: ({},{}), name: {}, command: {}, image_display: {}, data: {}, inventory_condition: {}, " \
            "game_condition: {}, dialog_text: {}, comment: {}, completed: {}"
        s = s.format(self.x, self.y, self.name, self.command, self.image_display, self.data,
                     self.inventory_condition, self.game_condition, self.dialog_text, self.comment, self.completed)
        print(s)

# -----------------------------------------------------------
#                      class Actions
# -----------------------------------------------------------
class Actions:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.actions = []
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data(self):
        self._load_map()

    #################
    # Class Actions #
    #################
    def _load_map(self):
        print("Loading _load_map")
        filename = "{}_actions.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        print("opening zone filepath: {}".format(filepath))
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        self.obstacles = []
        for col, tiles in enumerate(mytiles):
            # print(tiles)
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            for row, tile in enumerate(list_tiles):
                print(tile)
                if tile == "..":
                    pass
                elif len(tile) > 0:
                    new_action = Action(row, col, tile)
                    new_action.read_data(self.zone_name, self.map_name)
                    self.actions.append(new_action)
                else:
                    s = "Error! I don't recognize this: -{}-".format(tile)
                    raise ValueError(s)

    # def add_new_action(self, row, col, tile_name):
    #     new_action = Action(row, col, tile_name)
    #     new_action.read_data(self.zone_name, self.map_name)
    #     self.actions.append(new_action)

    def conditions_passed(self, player):
        current_action = self.get_action(player.x, player.y)
        if current_action is None:
            # We should not have reached this point unless there was an action
            # on the player's tile.
            raise ValueError("Error!")
        # current_action.debug_print()
        return current_action.conditions_passed(player.inventory)

    def remove_tile(self, x, y):
        print("Number of actions BEFORE: {}".format(len(self.actions)))
        mylist = []
        self.all_sprites = pygame.sprite.Group()
        for elem in self.actions:
            if elem.x == x and elem.y == y:
                pass
            else:
                mylist.append(elem)
        print("Number of actions AFTER: {}".format(len(mylist)))
        self.actions = mylist

    def get_action(self, x, y):
        print(self.actions)
        if self.actions is None:
            raise ValueError("Error!")
        if len(self.actions) == 0:
            # raise ValueError("Error!")
            return None
        # ----
        for action in self.actions:
            if action.x == x and action.y == y:
                return action
        return None

    # ---------------------------------------------------

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    # ------------------------------------------------------

    def update_classes(self, all_sprites):
        for elem in self.actions:
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
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    # ------------------------------------------------------

    def debug_print(self):
        for elem in self.actions:
            elem.debug_print()

    def debug_test(self):
        for an_action in self.actions:
            if len(an_action.game_condition) == 0:
                return False
        return True

# -----------------------------------------------------------
#                      class Trigger
# -----------------------------------------------------------

class Trigger:
    def __init__(self, x, y, name):
        self.x, self.y = x, y
        self.name = name
        self.command = ""
        self.data = ""
        self.inventory_condition = ""
        self.game_condition = ""
        self.comment = ""
        self.completed = False

    def read_data(self, zone_name, map_name):
        filepath = os.path.join("data", "zones", zone_name, map_name, "triggers.txt")
        print("filepath: {}".format(filepath))
        mylines = utils.read_data_file(filepath, 6)
        if mylines is None: return False
        if len(mylines) == 0: return False
        # print("mylines: {}".format(mylines))
        # ----
        mydict = utils.get_dict(mylines, "name", self.name)
        print("mydict: {}".format(mydict))
        # ----
        self.command = mydict["command"]
        if not self.command in constants.MAP_COMMANDS:
            raise ValueError("{} not in {}".format(self.command, constants.MAP_COMMANDS))
        self.data = mydict["data"]
        self.inventory_condition = mydict["inventory_condition"].lower().strip()
        if self.inventory_condition == "none": self.inventory_condition = None
        self.game_condition = mydict["game_condition"].lower().strip()
        if self.game_condition == "none": self.game_condition = None
        self.comment = mydict["comment"]

    # def parse_data(self):
    #     myint = self.data.find(":") + 1
    #     s = self.data[myint:].strip()
    #     mylist = s.split(";")
    #     mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
    #     # [print(i) for i in mylist]
    #     mydict = {}
    #     for elem in mylist:
    #         mydict = utils.key_value(elem, mydict)

    def parse_data(self):
        '''Parse data for zone and map names.'''
        text_to_parse = self.data.replace("data:", "").lower().strip()
        if text_to_parse.find("zone_name") == -1 or text_to_parse.find("map_name") == -1:
            s = "current_trigger.data: {}".format(text_to_parse)
            raise ValueError(s)
        mylist = text_to_parse.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        mydict = {}
        # print(mylist)
        mydict = utils.key_value(mylist[0], mydict)
        mydict = utils.key_value(mylist[1], mydict)
        return mydict["zone_name"], mydict["map_name"]

    def conditions_fulfilled(self, zone_name, map_name, myinventory):
        inventory_condition_passed = False
        game_condition_passed = False
        # ---- ----
        if self.inventory_condition is None:
            print("inventory_condition_passed = True")
            inventory_condition_passed = True
        else:
            my_item = myinventory.get_item_by_name(self.inventory_condition)
            if my_item is None:
                inventory_condition_passed = False
                print("inventory_condition_passed = False")
            else:
                inventory_condition_passed = True
                print("inventory_condition_passed = True")
        # ----
        if self.game_condition is None:
            print("game_condition_passed = True")
            game_condition_passed = True
        else:
            from NEW_inventory import SearchMasterQuests
            quest_histories = SearchMasterQuests()
            mydict = utils.string_to_dict(self.game_condition)
            try:
                quest_name = mydict["quest_name"]
            except Exception as e:
                raise ValueError(e)
            if quest_histories.quest_completed(quest_name) == True:
                game_condition_passed = True
        # ---- ----
        if inventory_condition_passed == True and game_condition_passed == True:
            return True
        return False

    def conditions_passed(self, inventory, events):
        raise NotImplemented
        if self.inventory_condition in ["any", None]:
            if self.game_condition in ["any", None]:
                print("There was no inventory or game condition.")
                return True
        # ----
        if not self.inventory_condition in ["any", None]:
            print("There is an inventory condition: {}".format(self.inventory_condition))
            the_item = inventory.get_item_by_name(self.inventory_condition)
            if the_item is None:
                print("the item ({}) was not found in the inventory".format(self.inventory_condition))
                return False
        if not self.game_condition in ["any", None]:
            print("There is a game condition: {}".format(self.game_condition))
            this_value = events.get_a_value(self.game_condition)
            if this_value is None:
                print("An event that matched this game condition was not found.")
                raise ValueError("Error!")
            return this_value
        else:
            return True

    def debug_print(self):
        s = "x,y: ({},{}), name: {}, command: {}, data: {}, " \
            "inventory_condition: {}, game_condition: {}, comment: {}, completed: {}"
        s = s.format(self.x, self.y, self.name, self.command,
                     self.data, self.inventory_condition, self.game_condition, self.comment, self.completed)
        print(s)

# -----------------------------------------------------------
#                      class Triggers
# -----------------------------------------------------------

class Triggers:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.triggers = []

    def read_data(self):
        self.load_map()

    def load_map(self):
        filename = "{}_triggers.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        # print("opening zone filepath: {}".format(filepath))
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        # mytiles = mytiles[3:]
        # [print(i) for i in mytiles]
        mytiles = [i[3:] for i in mytiles[2:]]
        # [print(i) for i in mytiles]
        # ------------------------------------------------------------------
        for col, tiles in enumerate(mytiles):
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            for row, tile in enumerate(list_tiles):
                # print("tile: {}".format(tiles))
                # print("row: {}, tile: {}".format(row, tile))
                if tile != "..":
                    # if tile.find("a") == -1:
                    print("reading in trigger tile: {}".format(tile))
                    new_trigger = Trigger(row, col, tile)
                    new_trigger.read_data(self.zone_name, self.map_name)
                    # new_trigger.debug_print()
                    self.triggers.append(new_trigger)
                elif tile == "..":
                    pass
                else:
                    s = "Error! I don't recognize this: {}".format(tile)
                    raise ValueError(s)

    def get_trigger(self, x, y):
        for trigger in self.triggers:
            if trigger.x == x:
                if trigger.y == y:
                    return trigger
        return None

    # def conditions_passed(self, player, events):
    #     current_trigger = self.get_trigger(player.x, player.y)
    #     if current_trigger is None:
    #         # We should not have reached this point unless there was an action
    #         # on the player's tile.
    #         raise ValueError("Error!")
    #     # current_trigger.debug_print()
    #     return current_trigger.conditions_passed(player.inventory, events)

    def debug_print(self):
        for elem in self.triggers:
            elem.debug_print()

    def debug_test(self):
        for a_trigger in self.triggers:
            if not a_trigger.game_condition is None:
                if len(a_trigger.game_condition) == 0:
                    return False
        return True

    def __len__(self):
        return len(self.triggers)

# -----------------------------------------------------------
#                      class Walkable
# -----------------------------------------------------------

"""
As you can see, class Grass uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Walkable(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        self.image_filename = mydict["image"]
        self.image_path = utils.get_filepath(self.image_filename)
        self.image = None
        self.rect = None
        self.comment = ""
        # ----
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.image_filename)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def move(self, dx=0, dy=0, obstacles=None):
        if not self._collide(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            # print("Player has moved. x,y: {},{}; dx={}, dy={}".format(self.x, self.y, dx, dy))

    def debug_print(self):
        s = "x,y: ({},{}); kind: {}, image: {}, comment: {}"
        s = s.format(self.x, self.y, self.kind, self.image_filename, self.comment)
        print(s)

# -----------------------------------------------------------
#                      class Walkables
# -----------------------------------------------------------
class Walkables:
    def __init__(self, zone_name, map_name):
        if zone_name == None:
            raise ValueError("Error!")
        if len(zone_name) == 0:
            raise ValueError("Error!")
        if map_name == None:
            raise ValueError("Error!")
        if len(map_name) == 0:
            raise ValueError("Error!")
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.init_pygame()
        self.loop_index = 0
        # self.walkables = self.read_data()
        self.walkables = []
        self.keep_looping = True
        # if self.walkables is None:
        #     raise ValueError("Doh!")

    def read_data(self):
        self._load_map()

    def _load_map(self):
        filename = "{}_walkables.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        filepath = os.path.join("data", "master_files", "tiles.txt")
        file_tiles = utils.read_data_file(filepath, num_of_fields=4)
        # ------------------------------------------------------------------
        self.walkables = []
        for col, tiles in enumerate(mytiles):
            tile_list = tiles.split(";")
            tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
            for row, tile in enumerate(tile_list):
                # print("tile: {}".format(tile))
                if not tile == "..":
                    mydict = utils.get_dictionary(file_tiles, tile)
                    if mydict is None:
                        s = "tile: {}\n".format(tile)
                        raise ValueError(s)
                    mydict["x"] = row
                    mydict["y"] = col
                    mywalk = Walkable(mydict)
                    self.walkables.append(mywalk)
                if tile == "..":
                    pass

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        for elem in self.walkables:
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
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    def __len__(self):
        return len(self.walkables)

    def __getitem__(self, item):
        return self.walkables[item]

    def __next__(self):
        if self.loop_index >= len(self.walkables):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.walkables[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        print("Number of grasses: {}".format(len(self.walkables)))
        if len(self.walkables) == 0:
            s = "Error! There are no grasses to print."
            raise ValueError(s)
        for grass in self.walkables:
            grass.debug_print()

# -----------------------------------------------------------
#                      class Obstacle
# -----------------------------------------------------------

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        # self.trigger = mydict["trigger"]
        # self.image_filename = mydict["image_filename"]
        self.image_filename = mydict["image"]
        self.image_path = utils.get_filepath(self.image_filename)
        self.image = None
        self.rect = None
        # ----
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(self.image_path)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def read_data(self, zone_name, map_name):
        filepath = os.path.join("data", "zones", zone_name, map_name, "actions.txt")
        mylines = utils.read_data_file(filepath, 8)
        if mylines is None or len(mylines) == 0:
            raise ValueError("Error!")
        # ----
        target_dict = {}
        for elem in mylines:
            if elem["name"] == self.name:
                target_dict = elem
        if len(target_dict) == 0:
            s = "The name {} was not found in {}".format(self.name, target_dict)
            raise ValueError(s)
        self.command = target_dict["command"]
        if not self.command in constants.MAP_COMMANDS:
            raise ValueError("Error! {} is not in {}".format(target_dict["command"], constants.MAP_COMMANDS))
        self.image_display = target_dict["image_display"]
        self.data = target_dict["data"]
        self.inventory_condition = target_dict["inventory_condition"]
        if self.inventory_condition == "none":
            self.inventory_condition = None
        # Need to be able to check that the player has successfully
        # completed a conversation.
        # Perhaps also check to see that the conversation is in the
        # events file.
        self.game_condition = target_dict["game_condition"].lower().strip()
        if self.game_condition == "none":
            self.game_condition = None
        self.dialog_text = target_dict["dialog_text"]
        self.comment = target_dict["comment"]
        self.completed = False
        # ----
        self.image_display = self.image_display.replace(" ", "_")
        if self.image_display.find(".png") == -1:
            self.image_display = "{}.png".format(self.image_display)
        filepath = utils.get_filepath(self.image_display)
        if filepath is None:
            s = "I wasn't able to find a path for the file: {}".format(self.image_display)
            raise ValueError(s)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def debug_print(self):
        s = "(x,y): {},{}; kind:{}, image_filename: {}, rect: {}"
        s = s.format(self.x, self.y, self.kind, self.image_filename, self.rect)
        print(s)

# -----------------------------------------------------------
#                      class Obstacles
# -----------------------------------------------------------
class Obstacles:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.init_pygame()
        self.obstacles = []
        self.loop_index = 0
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()

    def read_data(self):
        self._load_map()

    def _load_map(self):
        # Load in the map
        filename = "{}_obstacles.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        print("Reading in obstacle map ...")
        print("zone: {}, map: {}".format(self.zone_name, self.map_name))
        print("filepath for obstacle file: {}".format(filepath))
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        filepath = os.path.join("data", "master_files", "tiles.txt")
        file_tiles = utils.read_data_file(filepath, num_of_fields=4)
        # ------------------------------------------------------------------
        self.obstacles = []
        for col, tiles in enumerate(mytiles):
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            for row, tile in enumerate(list_tiles):
                if not tile == "..":
                    tile_dict = utils.get_dictionary(file_tiles, tile)
                    if tile_dict is None:
                        raise ValueError("tile: {}".format(tile))
                    tile_dict["x"] = row
                    tile_dict["y"] = col
                    my_obstacle = Obstacle(tile_dict)
                    self.obstacles.append(my_obstacle)
                elif tile == "..":
                    pass
                else:
                    s = "Error! I don't recognize this: {}".format(tile)
                    raise ValueError(s)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def collision(self, x, y):
        if self.obstacles is None:
            raise ValueError("Error")
        if len(self.obstacles) == 1:
            raise ValueError("Error")
        for a_tile in self.obstacles:
            if a_tile.kind == "empty":
                continue
            if a_tile.x == x:
                # print("tile y: {}, player y: {}".format(a_tile.y, y))
                if a_tile.y == y:
                    print("tile x,y: ({},{}), player x,y: ({},{})".format(a_tile.x, a_tile.y, x, y))
                    return True
        return False

    def collision_is_close(self, x, y):
        if self.obstacles is None:
            raise ValueError("Error")
        if len(self.obstacles) == 1:
            raise ValueError("Error")
        # ----
        for a_tile in self.obstacles:
            if a_tile.kind == "empty":
                continue
            if utils.points_are_close(a_tile.x, x) == True:
                # print("tile y: {}, player y: {}".format(a_tile.y, y))
                if utils.points_are_close(a_tile.y, y) == True:
                    print("tile x,y: ({},{}), player x,y: ({},{})".format(a_tile.x, a_tile.y, x, y))
                    return True
        return False

    # --------------------------------------------------------

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))
                # ------------------------------------------------------

    def update_classes(self, all_sprites):
        for elem in self.obstacles:
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
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    # --------------------------------------------------------

    def __len__(self):
        return len(self.obstacles)

    def __getitem__(self, item):
        return self.obstacles[item]

    def __next__(self):
        if self.loop_index >= len(self.obstacles):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.obstacles[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        for elem in self.obstacles:
            elem.debug_print()

# -----------------------------------------------------------
#                      class Environment
# -----------------------------------------------------------

class Environment:
    def __init__(self, zone_name, map_name):
        if zone_name is None or map_name is None:
            raise ValueError("Error!")
        if len(zone_name) == 0 or len(map_name) == 0:
            raise ValueError("Error!")
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.init_pygame()
        # ----
        self.zone_description = ""
        self.obstacles = Obstacles(self.zone_name, self.map_name)
        self.walkables = Walkables(self.zone_name, self.map_name)
        self.triggers = Triggers(self.zone_name, self.map_name)
        self.actions = Actions(self.zone_name, self.map_name)
        # self.events = Events(self.zone_name, self.map_name)
        self.persistents = PersistentObjects(self.zone_name, self.map_name)
        # self.triggers = None
        # ----
        # self.mysprite = HandleMovingSprite("apple.png")
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True

    def read_data(self):
        self.walkables.read_data()
        self.obstacles.read_data()
        if not self.triggers is None:
            self.triggers.read_data()
        if not self.actions is None:
            self.actions.read_data()
        # if not self.events is None:
        #     self.events.read_data()
        if not self.persistents is None:
            self.persistents.read_data()
        # ----

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def get_walkable_tile(self, x, y):
        # for a_tile in self.obstacles:
        #     if a_tile.x == x:
        #         if a_tile.y == y:
        #             return a_tile
        for a_tile in self.walkables:
            if a_tile.x == x:
                if a_tile.y == y:
                    return a_tile
        return None

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
                # else:
                #     print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        all_sprites = self.walkables.update_classes(all_sprites)
        all_sprites = self.persistents.update_classes(all_sprites)
        all_sprites = self.obstacles.update_classes(all_sprites)
        all_sprites = self.actions.update_classes(all_sprites)
        # if self.mysprite.show_image == True:
        #     all_sprites.add(self.mysprite)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites = self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping == True:
            self.handle_events()
            self.draw()
        self.goodbye()
        self.myquit()

    def goodbye(self):
        print("Goodbye!")

    def myquit(self):
        pygame.quit()

    def debug_print(self):
        s = "zone_name: {}\nzone_description: {}"
        s = s.format(self.zone_name, self.zone_description)
        print(s)
        self.obstacles.debug_print()
        self.walkables.debug_print()

# ************************************************************

def debug_obstacles():
    myobstacles = Obstacles(zone_name, map_name)
    myobstacles.read_data()
    # myobstacles.debug_print()
    myobstacles.main()

def debug_walkables():
    mywalkables = Walkables(zone_name, map_name)
    mywalkables.read_data()
    # mywalkables.debug_print()
    mywalkables.main()

def debug_persistents():
    myobject = PersistentObjects(zone_name, map_name)
    myobject.read_data()
    # myobject.debug_print()
    myobject.main()

def debug_environment():
    myenv = Environment(zone_name, map_name)
    myenv.read_data()
    myenv.main()

def debug_triggers():
    mytriggers = Triggers(zone_name, map_name)
    mytriggers.read_data()
    mytriggers.debug_print()
    mytrigger = mytriggers.triggers[0]
    # ----
    from NEW_inventory import Inventory
    npc_name = "old ben"
    myinventory = Inventory(player_name=player_name, npc_name=npc_name, character_type="player")
    myinventory.read_data()
    # ----
    # def conditions_fulfilled(self, zone_name, map_name, myinventory):
    if mytrigger.conditions_fulfilled(zone_name, map_name, myinventory) == False:
        print("False")
    else:
        print("True")

def debug_actions(zone_name, map_name):
    from graphics_fauna import Player
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    myplayer.x = 3
    myplayer.y = 2
    # myevents = Events(zone_name, map_name)
    # myevents.read_data()
    # ----
    myactions = Actions(zone_name, map_name)
    myactions.read_data()
    myactions.main()
    # myactions.conditions_passed(myplayer, myevents)

def test_action(zone_name, map_name):
    x, y = 3, 2
    x, y = 2, 2
    # ----
    myevents = Events(zone_name, map_name)
    myevents.read_data()
    # ----
    from graphics_fauna import Player
    myplayer = Player(zone_name, map_name)
    myplayer.read_data()
    # ----
    myactions = Actions(zone_name, map_name)
    myactions.read_data()
    myaction = myactions.get_action(x, y)
    if myaction is None:
        print("There is no actioin on tile: {},{}".format(x, y))
    else:
        print("Action found:")
        myaction.debug_print()
    # ----
    the_result = myaction.conditions_passed(myplayer.inventory, myevents)
    print("The result: {}".format(the_result))
    # ----
    print("####")
    myaction.debug_print()

def debug_events():
    myevents = Events(zone_name, map_name)
    myevents.read_data()
    myevents.debug_print()
    # if myevents.mark_game_condition_completed("conversation_with_random_completed") == False:
    #     raise ValueError("Error!")
    # myevents.save_data()

# def debug_mysprite():
#     myobstacles = Obstacles("swindon", "map00")
#     myobstacles.read_data()
#     mysprite = MySpriteNew()
#     mysprite.read_data(8, 1, 1, 1, "apple02.png")

player_name = "henry"
# zone_name = "dark_alley"
# zone_name = "green_lawn"
# zone_name = "bridge"
# zone_name = "swindon"
# zone_name = "jeweler"
# zone_name = "swindon_pub"
# zone_name = "provisioner"
# zone_name = "cliffs"
# ----
zone_name = "swindon_pub_haunted"
# zone_name = "testing"
# zone_name = "the_orchard"
# zone_name = "apple_grove"
# zone_name = "easthaven"
# zone_name = "village_blue"
map_name = "map00"

if __name__ == "__main__":
    # pass
    # debug_obstacles()
    # debug_walkables()
    debug_environment()
    # ----
    # debug_triggers()
    # debug_actions(zone_name, map_name)
    # debug_persistents()
    # ----
    # test_action(zone_name, map_name)
    # debug_events()