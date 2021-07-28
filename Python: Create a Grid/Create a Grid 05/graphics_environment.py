import sys, os
import pygame
import constants
import utils

# -----------------------------------------------------------
#                      class Event
# -----------------------------------------------------------
class Event:
    def __init__(self, mydict):
        # print("mydict: {}".format(mydict))
        self.index = mydict["index"]
        if not type(self.index) == type(123):
            raise ValueError("Error!")
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
        # ----

    def conditions_passed(self, inventory, events):
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

    # ---------------------

    def parse_data(self):
        print("data string: {}".format(self.data))
        mylist = self.data.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        print("mylist: {}".format(mylist))
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
            print(tiles)
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

    def conditions_passed(self, player, events):
        current_action = self.get_action(player.x, player.y)
        if current_action is None:
            # We should not have reached this point unless there was an action
            # on the player's tile.
            raise ValueError("Error!")
        current_action.debug_print()
        return current_action.conditions_passed(player.inventory, events)

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
            raise ValueError("Error!")
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
        was_entered = False
        for mydict in mylines:
            # print("mydict: {}".format(mydict))
            # print("self.name: -{}- == mydict[name]: -{}-".format(self.name, mydict["name"]))
            # print("-{}=={}-".format(self.name, mydict["name"]))
            if self.name == mydict["name"].replace(":", ""):
                was_entered = True
                self.command = mydict["command"]
                if not self.command in constants.MAP_COMMANDS:
                    raise ValueError("{} not in {}".format(self.command, constants.MAP_COMMANDS))
                self.data = mydict["data"]
                self.inventory_condition = mydict["inventory_condition"].lower().strip()
                if self.inventory_condition == "none": self.inventory_condition = None
                self.game_condition = mydict["game_condition"]
                if self.game_condition == "none": self.game_condition = None
                self.comment = mydict["comment"]
        if was_entered == False:
            raise ValueError("Error!")

    def parse_data(self):
        # print("data string: {}".format(self.data))
        if self.data.find("zone_name") == -1 or self.data.find("map_name") == -1:
            s = "current_trigger.data: {}".format(self.data)
            raise ValueError(s)
        mylist = self.data.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        mydict = {}
        # print(mylist)
        mydict = utils.key_value(mylist[0], mydict)
        mydict = utils.key_value(mylist[1], mydict)
        return mydict

    def conditions_passed(self, inventory, events):
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

    def conditions_passed(self, player, events):
        current_trigger = self.get_trigger(player.x, player.y)
        if current_trigger is None:
            # We should not have reached this point unless there was an action
            # on the player's tile.
            raise ValueError("Error!")
        # current_trigger.debug_print()
        return current_trigger.conditions_passed(player.inventory, events)

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
        self.species = mydict["species"]
        # self.trigger = mydict["trigger"]
        self.image_filename = ""
        self.image = None
        self.rect = None
        self.comment = ""
        # ----
        if self.kind == "npc_dead" and self.species == 0:
            self.image_filename = utils.get_filepath("dead_person_cobblestones.png")
        elif self.kind == "npc_dead" and self.species == 1:
            self.image_filename = utils.get_filepath("dead_person_light_green_tile.png")
        elif self.kind == "chair" and self.species == 1:
            self.image_filename = utils.get_filepath("chair_right_light_green_tile.png")
        elif self.kind == "chair" and self.species == 2:
            self.image_filename = utils.get_filepath("chair_left_light_green_tile.png")
        elif self.kind == "chair" and self.species == 3:
            self.image_filename = utils.get_filepath("chair_down_light_green_tile.png")
        elif self.kind == "chair" and self.species == 4:
            self.image_filename = utils.get_filepath("chair_up_light_green_tile.png")
        elif self.kind == "tile" and self.species == 0:
            self.image_filename = utils.get_filepath("floor_tile_light_green.png")
        elif self.kind == "cobblestones" and self.species == 0:
            self.image_filename = utils.get_filepath("cobblestones11.png")
        elif self.kind == "cobblestones" and self.species == 1:
            self.image_filename = utils.get_filepath("cobblestones11_light01.png")
        elif self.kind == "cobblestones" and self.species == 2:
            self.image_filename = utils.get_filepath("cobblestones11_light02.png")
        elif self.kind == "portal" and self.species == 0:
            self.image_filename = utils.get_filepath("portal_cobblestones02.png")
        elif self.kind == "grass" and self.species == 0:
            self.image_filename = utils.get_filepath("grass02.png")
        elif self.kind == "flowers" and self.species == 0:
            self.image_filename = utils.get_filepath("flowers01_grass01.png")
        elif self.kind == "strawberries" and self.species == 0:
            self.image_filename = utils.get_filepath("strawberries01.png")
        elif self.kind == "mushrooms" and self.species == 0:
            self.image_filename = utils.get_filepath("mushrooms01_grass01.png")
        elif self.kind == "forest" and self.species == 0:
            self.image_filename = utils.get_filepath("forest_02.png")
        elif self.kind == "portal" and self.species == 1:
            self.image_filename = utils.get_filepath("portal_grass.png")
        elif self.kind == "portal" and self.species == 2:
            self.image_filename = utils.get_filepath("portal_grass02.png")
        elif self.kind == "portal" and self.species == 3:
            self.image_filename = utils.get_filepath("portal_pub01.png")
        elif self.kind == "pub" and self.species == 0:
            self.image_filename = utils.get_filepath("building09.png")
        elif self.kind == "pub" and self.species == 1:
            self.image_filename = utils.get_filepath("building09_grass.png")
        elif self.kind == "provisioner" and self.species == 0:
            self.image_filename = utils.get_filepath("building07.png")
        elif self.kind == "provisioner" and self.species == 1:
            self.image_filename = utils.get_filepath("building07_grass.png")
        elif self.kind == "black" and self.species == 0:
            self.image_filename = utils.get_filepath("black.png")
        elif self.kind == "empty" and self.species == 0:
            self.image_filename = utils.get_filepath("empty.png")
        else:
            s = "Couldn't find: kind: {}, species: {}".format(self.kind, self.species)
            raise ValueError(s)
        # ----
        # self.filepath = os.path.join("data", "images", self.image_filename)
        try:
            self.image = pygame.image.load(self.image_filename).convert_alpha()
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
        raise NotImplemented
        print("filepath: {}".format(self.filepath))
        print("x,y: {},{}".format(self.x, self.y))

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
        # [print(i) for i in mytiles]
        # ------------------------------------------------------------------
        # t1 = False
        # t2 = False
        big_list = []
        for col, tiles in enumerate(mytiles):
            tile_list = tiles.split(";")
            tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
            for row, tile in enumerate(tile_list):
                # print("tile: {}".format(tile))
                if tile == "a0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "npc_dead"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                if tile == "a1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "npc_dead"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "f1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "chair"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                    # print("obstacle (wall) tile added at x,y: ({},{})".format(row, col))
                elif tile == "f2":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "chair"
                    mydict["species"] = 2
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "f3":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "chair"
                    mydict["species"] = 3
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "f4":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "chair"
                    mydict["species"] = 4
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "c0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "pub"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "c1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "pub"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "e0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "provisioner"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "e1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "provisioner"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "d0":
                    # cobblestones
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "cobblestones"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                    # if row == 5 and col == 8:
                    #     mydict["comment"] = "load_map;map01"
                    #     t1 = True
                    # elif row == 6 and col == 8:
                    #     mydict["comment"] = "load_map;map01"
                    #     t2 = True
                elif tile == "d1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "cobblestones"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "d2":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "cobblestones"
                    mydict["species"] = 2
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "h0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "tile"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "b0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "black"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "l0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "portal"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "l1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "portal"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "l2":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "portal"
                    mydict["species"] = 2
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "g0":
                    mydict = {}
                    mydict["x"], mydict["y"] = row, col
                    mydict["kind"] = "grass"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "m0":
                    mydict = {}
                    mydict["x"], mydict["y"] = row, col
                    mydict["kind"] = "mushrooms"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "f0":
                    mydict = {}
                    mydict["x"], mydict["y"] = row, col
                    mydict["kind"] = "forest"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "h0":
                    mydict = {}
                    mydict["x"], mydict["y"] = row, col
                    mydict["kind"] = "flowers"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "s0":
                    mydict = {}
                    mydict["x"], mydict["y"] = row, col
                    mydict["kind"] = "strawberries"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                elif tile == "..":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "empty"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
                else:
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "empty"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
        # if t1 == False or t2 == False:
        #     raise ValueError("Something went wrong.")
        self.walkables = big_list

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
        self.species = mydict["species"]
        self.trigger = mydict["trigger"]
        # self.image_filename = mydict["image_filename"]
        self.image_filename = ""
        self.image = None
        self.rect = None
        # ----
        if self.kind == "wall" and self.species == 0:
            self.image_filename = os.path.join("structures", "brick_wall02.png")
        elif self.kind == "stove" and self.species == 0:
            self.image_filename = os.path.join("structures", "stove01.png")
        elif self.kind == "table" and self.species == 0:
            self.image_filename = os.path.join("structures", "table_large_empty_01.png")
        elif self.kind == "table" and self.species == 1:
            self.image_filename = os.path.join("structures", "table_and_wine_02.png")
        elif self.kind == "counter" and self.species == 0:
            self.image_filename = os.path.join("structures", "tile_counter.png")
        elif self.kind == "empty" and self.species == 0:
            self.image_filename = "empty.png"
        elif self.kind == "streetlamp" and self.species == 0:
            self.image_filename = os.path.join("structures", "streetlamp02.png")
        elif self.kind == "streetlamp" and self.species == 1:
            self.image_filename = os.path.join("structures", "streetlamp03.png")
        elif self.kind == "forest" and self.species == 0:
            self.image_filename = os.path.join("nature_tiles", "medievalTile_48.png")
        elif self.kind == "rocks" and self.species == 0:
            self.image_filename = os.path.join("nature_tiles", "pile_of_rocks01_grey01.png")
        else:
            s = "I can't find kind: {}, species: {} ({})".format(self.kind, self.species, type(self.species))
            raise ValueError(s)
        # ----
        filepath = os.path.join("data", "images", self.image_filename)
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
        s = "(x,y): {},{}; kind:{}, species: {}, trigger: {}, image_filename: {}, rect: {}"
        s = s.format(self.x, self.y, self.kind, self.species, self.trigger, self.image_filename, self.rect)
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
        self.obstacles = []
        for col, tiles in enumerate(mytiles):
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            for row, tile in enumerate(list_tiles):
                if tile == "w0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "wall"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "s0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "stove"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "l0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "streetlamp"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                    # print("obstacle (wall) tile added at x,y: ({},{})".format(row, col))
                elif tile == "t0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "table"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "t1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "table"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "c0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "counter"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "l1":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "streetlamp"
                    mydict["species"] = 1
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "f0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "forest"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                elif tile == "m0":
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "rocks"
                    mydict["species"] = 0
                    mydict["trigger"] = ""
                    my_obstacle = Obstacle(mydict)
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
        for a_tile in self.obstacles:
            if a_tile.kind == "empty":
                continue
            if a_tile.x == x:
                # print("tile y: {}, player y: {}".format(a_tile.y, y))
                if a_tile.y == y:
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
        self.events = Events(self.zone_name, self.map_name)
        # self.triggers = None
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True

    # def read_data(self):
    #     filepath = os.path.join("data", "zones", self.zone_name, "zone_init.txt")
    #     mylist = utils.read_data_file(filepath, 6)
    #     mydict = mylist[0]
    #     self.zone_description = mydict["zone_description"]
    #     self.obstacles.read_data()
    #     self.walkables.read_data()

    def read_data(self):
        self.walkables.read_data()
        self.obstacles.read_data()
        if not self.triggers is None:
            self.triggers.read_data()
        if not self.actions is None:
            self.actions.read_data()
        if not self.events is None:
            self.events.read_data()

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
        all_sprites = self.obstacles.update_classes(all_sprites)
        all_sprites = self.walkables.update_classes(all_sprites)
        all_sprites = self.actions.update_classes(all_sprites)
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
    myobstacles.main()

def debug_walkables():
    myobstacles = Walkables(zone_name, map_name)
    myobstacles.read_data()
    myobstacles.main()

def debug_environment():
    myenv = Environment(zone_name, map_name)
    myenv.read_data()
    myenv.main()

def debug_triggers():
    mytriggers = Triggers(zone_name, map_name)
    mytriggers.read_data()
    mytriggers.debug_print()

def debug_actions(zone_name, map_name):
    from graphics_fauna import Player
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    myplayer.x = 3
    myplayer.y = 2
    myevents = Events(zone_name, map_name)
    myevents.read_data()
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

player_name = "henry"
# zone_name = "swindon_pub_stub"
# zone_name = "swindon"
zone_name = "easthaven"
map_name = "map00"

if __name__ == "__main__":
    # debug_obstacles()
    # debug_walkables()
    debug_environment()
    # debug_triggers()
    # debug_actions(zone_name, map_name)
    # test_action(zone_name, map_name)
    # debug_events()