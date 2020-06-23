import os, sys
import constants as con
import utils

# ------------------------------------------------
#                  class Item
# ------------------------------------------------

class Item:
    def __init__(self, id:int, kind, name, appearance,
                 function, class_requirement, base_cost:int,
                 hit_points_restored, mana_points_restored):
        self.id = int(id)
        self.kind = kind.lower().strip()
        self.name = name.lower().strip()
        self.appearance = appearance.lower().strip()
        self.function = function.lower().strip()
        self.class_requirement = class_requirement.lower().strip()
        self.base_cost = int(base_cost)
        self.hit_points_restored = int(hit_points_restored)
        self.mana_points_restored = int(mana_points_restored)

# ------------------------------------------------
#                  class Items
# ------------------------------------------------

class Items:
    def __init__(self, char_name, char_kind):
        the_directory = ""
        self.inner = []
        if char_name == "" or char_name == "none" or char_kind == "" or char_kind == "none":
            self.item_filepath = os.path.join("data", "master_files", "items.txt")
        else:
            the_directory = "{}_{}".format(char_name, char_kind)
            self.item_filepath = os.path.join("data", "saved_player_data", the_directory, "items.txt")
            self.char_name = char_name
            self.char_kind = char_kind
        self.load_all()

    def __len__(self):
        return len(self.inner)

    def load_all(self):
        print("Loading file:")
        print(self.item_filepath)
        mylist = utils.open_text_file(self.item_filepath)
        if len(mylist) == 0:
            raise ValueError("No data was read in!")
        self.inner = []
        for line in mylist:
            if line[0][0] == "#":
                continue
            myline = line.split(";")
            myline = [i.strip() for i in myline if len(i.strip()) > 0]
            if len(myline) != 9:
                s = "The data index is the wrong length! It should be 9 but it is {}\n".format(len(myline))
                s += "Here is the line:\n"
                s += ", ".join(myline)
                raise ValueError(s)
            id = int(myline[0])
            kind = myline[1]
            name = myline[2]
            appearance = myline[3]
            function = myline[4]
            class_requirement = myline[5]
            base_cost = int(myline[6])
            hit_points_restored = int(myline[7])
            mana_points_restored = int(myline[8])
            myitem = Item(id, kind, name, appearance, function, class_requirement, base_cost, hit_points_restored, mana_points_restored)
            self.inner.append(myitem)

    def get_item(self, index):
        if type(index) == type("s"):
            raise ValueError("Error! Index is of type str: {}".format(index))
        if len(self.inner) == 0:
            raise ValueError("Error! len(self.inner) == 0")
        myids = []
        for elem in self.inner:
            myids.append(elem.id)
            if elem.id == index:
                return elem
        s = "Error! This index wasn't found: {}\n".format(index)
        s += "{}".format(myids)
        raise ValueError(s)

    def get_item_by_name(self, name):
        for elem in self.inner:
            if elem.name == name:
                return elem
        raise ValueError("{} was not found!!!!".format(name.upper()))

# ------------------------------------------------
#                  class Tile
# ------------------------------------------------

class Tile:
    def __init__(self, mydict):
        # print("mydict in Tile: {}".format(mydict))
        self.index = mydict["index"]
        self.kind_of_tile = mydict["kind"]
        self.description = mydict["description"]
        self.examination = mydict["examine"]
        self.up = mydict["up"].lower()
        self.down = mydict["down"].lower()
        self.right = mydict["right"].lower()
        self.left = mydict["left"].lower()

    def display_print(self):
        s = "index: {} | ".format(self.index)
        s += "kind_of_tile: {} | ".format(self.kind_of_tile)
        s += "description: {} | ".format(self.description)
        s += "examine: {} | ".format(self.examination)
        s += "up: {} | ".format(self.up)
        s += "down: {} | ".format(self.down)
        s += "right: {} | ".format(self.right)
        s += "left: {}".format(self.left)
        return s

    def get_fileline(self):
        s = "index: {}\n".format(self.index)
        s += "kind: {}\n".format(self.kind_of_tile)
        s += "description: {}\n".format(self.description)
        s += "examine: {}\n".format(self.examination)
        s += "up: {}\n".format(self.up)
        s += "down: {}\n".format(self.down)
        s += "right: {}\n".format(self.right)
        s += "left: {}".format(self.left)
        return s

# ------------------------------------------------
#                  class Tiles
# ------------------------------------------------

class Tiles:
    def __init__(self, zone_name):
        char_name, char_kind = utils.get_char_info()
        self.char_dir = "{}_{}".format(char_name, char_kind)
        self.zone_name = zone_name
        self.inner = []
        self.load_tile_zone()

    def load_tile_zone(self):
        print("Loading zone: {}".format(self.zone_name))
        tile_kind_filename = "{}.txt".format(self.zone_name)
        filepath = os.path.join("data", "player_files", self.char_dir, "tiles", tile_kind_filename)
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
            # mylines = [i.replace(";", "") for i in mylines]
        if len(mylines) == 0:
            raise ValueError("Error!")
        mylist = []
        for i in range(0, len(mylines), 8):
            # print("debugging: ")
            # print(mylines[i])
            mydict = {}
            for j in range(8):
                elem = mylines[i + j]
                # print("elem: ", elem)
                mydict = utils.key_value_pair(elem, mydict)
            mylist.append(mydict)
        # ----
        big_list = []
        for mydict in mylist:
            new_elem = Tile(mydict)
            big_list.append(new_elem)
        self.inner = big_list

    def get_tile(self, tile_index):
        if not tile_index in con.TILE_NAMES:
            s = "This is not a tile_name: {}\n".format(tile_index)
            s += "Here are your choices: "
            s += ', '.join(con.TILE_NAMES)
            raise ValueError(s)
        if len(self.inner) == 0:
            s = "This tileset contains no tiles! len(self.inner) == 0"
            raise ValueError(s)
        for elem in self.inner:
            if elem.index == tile_index:
                return elem
        s = "Couldn't find tile: {}".format(tile_index)
        raise ValueError(s)

    def display_print(self):
        for elem in self.inner:
            print(elem.display_print())

    def __len__(self):
        return len(self.inner)

# ================================================
# ------------------------------------------------
#                  class Player
# ------------------------------------------------

class Player:
    def __init__(self, tiles, player_name, player_kind, zone_name):
        self.player_name = player_name
        self.player_kind = player_kind
        self.zone_name = zone_name
        # -------------------------------------
        self.max_hp = 10
        self.max_mp = 0
        # -------------------------------------
        self.gold = 20
        self.weapon = None # We'll flesh this out down the road
        self.inventory = None # We'll flesh this out down the road
        self.status_effects = None # We'll flesh this out down the road
        self.explored_locations = [] # We'll flesh this out down the road
        self.has_killed = False # We'll flesh this out down the road
        # -------------------------------------
        self.tiles = tiles
        self.current_tile = self.tiles.get_tile("a1")
        # -------------------------------------
        # -------------------------------------

    def move(self, direction):
        if self.current_tile is None:
            s = "Doh! current_tile has a value of None."
            raise ValueError(s)
        run_into_barrier = "-------------------------------------------------\n"
        run_into_barrier += "You run into a barrier. You cannot walk {}/{}.\n"
        run_into_barrier += "-------------------------------------------------"
        if direction == "north":
            if self.current_tile.up == "none":
                print(run_into_barrier.format(direction, "up"))
            else:
                self.current_tile = self.tiles.get_tile(self.current_tile.up)
        elif direction == "south":
            if self.current_tile.down == "none":
                print(run_into_barrier.format(direction, "down"))
            else:
                self.current_tile = self.tiles.get_tile(self.current_tile.down)
        elif direction == "west":
            if self.current_tile.left == "none":
                print(run_into_barrier.format(direction, "left"))
            else:
                self.current_tile = self.tiles.get_tile(self.current_tile.left)
        elif direction == "east":
            if self.current_tile.right == "none":
                print(run_into_barrier.format(direction, "right"))
            else:
                self.current_tile = self.tiles.get_tile(self.current_tile.right)
        else:
            s = "Sorry, I don't recognize that: {}".format(direction)
            raise ValueError(s)

    # ---------------------------------------------------------

    def display_print(self):
        # t = "---- Meet {} the {} ----".format(self.player_name, player_kind)
        # print(t)
        s = "player_name: {} | ".format(self.player_name)
        s += "player_kind: {} | ".format(self.player_kind)
        s += "zone_name: {} | ".format(self.zone_name)
        # -------------------------------------
        s += "max_hp: {} | ".format(self.max_hp)
        s += "max_mp: {} | ".format(self.max_mp)
        # -------------------------------------
        s += "gold: {} | ".format(self.gold)
        s += "weapon: {} | ".format(self.weapon)
        s += "inventory: {} | ".format(self.inventory)
        s += "status_effects: {} | ".format(self.status_effects)
        s += "explored_locations: {} | ".format(self.explored_locations)
        s += "has_killed: {} | ".format(self.has_killed)
        # -------------------------------------
        s += "tiles: {} | ".format(self.tiles)
        # s += "current_tile_name: {}".format(self.current_tile_name)
        return s

# ------------------------------------------------
#                  class Game
# ------------------------------------------------

class Game:
    def __init__(self, char_name, char_kind, zone_name):
        self.char_name = char_name
        self.char_kind = char_kind
        if not zone_name in con.ZONE_KINDS:
            s = "Error! {} is not in con.ZONE_KINDS. Here are the ZONE_KINDS:\n".format(zone_name)
            s += "{}".format(con.ZONE_KINDS)
            raise ValueError(s)
        self.zone_name = zone_name
        self.tiles = Tiles(self.zone_name)
        # -----------------------------
        self.player = Player(self.tiles, self.char_name, self.char_kind, self.zone_name)
        # self.player.tiles = self.tiles
        # self.player.current_tile = self.tiles.get_tile("a1")
        self.play_game = True
        # self.player.current_tile.display_print()

    # ---------------------------------------------------------

    def valid_command(self):
        command, object = "", ""
        valid_command = False
        while valid_command == False:
            # print("Enter a value for the game loop:")
            # action = input("Game Loop > ").lower().strip()
            my_prompt = "{} > ".format(self.zone_name)
            action = input(my_prompt).lower().strip()
            mybreak = action.find(" ")
            if mybreak == -1: # if there is no spaces --> If only a single word was entered.
                if not action in con.ALL_COMMANDS:
                    command = action
                    valid_command = False
                    continue
                else:
                    return action, object
            else:
                command = action[:mybreak]
                object = action[mybreak:].strip()
                if not command in con.ALL_COMMANDS:
                    print("bebugging: That is not a valid command: {}".format(command))
                    valid_command = False
                    continue
                if not object in con.OBJECTS:
                    print("bebugging: That is not a valid object: {}".format(object))
                    valid_command = False
                    continue
            valid_command = True
        return command, object

    # ---------------------------------------------------------

    def game_loop(self):
        char_dir = "{}_{}".format(self.char_name, self.char_kind)
        filepath = os.path.join("data", "player_files", char_dir, "trailer.txt")
        with open(filepath, "r") as f:
            mytext = f.read()
        print(mytext)
        while self.play_game:
            description = utils.capitalize_sentences(self.player.current_tile.description)
            s = "{} ({} - {})".format(description, self.zone_name, self.player.current_tile.index)
            print(s)
            # --------------------------------------------------
            command, object = self.valid_command()
            print("command: {}, object: {}".format(command, object))
            if command == "quit":
                print("You want to QUIT. Setting play_game to False.")
                self.play_game = False
                return False
            elif command == "walk":
                self.player.move(object)
            elif command == "enter":
                if object == "town":
                    if self.zone_name != "world":
                        print("Sorry! You can't enter a town if you're not in the 'world' zone.")
                        continue
                    elif self.player.current_tile.index != "a4":
                        s = "Town? You want to go into town? I don't see any town!"
                        s += "Debugging: You're standing on tile: {}".format(self.player.current_tile.tile_name)
                        raise ValueError(s)
                    # ------------------------------------------------------------
                    # self.move_player_between_zones("town")
                    zone_name = "town"
                    tile_name = "a1"
                    self.zone_name = zone_name
                    self.tiles.zone_name = zone_name
                    self.tiles.load_tile_zone()
                    self.current_tile = self.tiles.get_tile(tile_name)
                    self.player.current_tile = self.current_tile
                    utils.clear_screen()
                elif object == "world":
                    if self.zone_name != "town":
                        print("Sorry! You can't enter the world if you're not in the 'town' zone.")
                        continue
                    elif self.player.current_tile.index != "a1":
                        s = "World? You want to go into the world? I don't see an exit around here, do you?!"
                        s += "Debugging: You're standing on tile: {}".format(self.player.current_tile.tile_name)
                    zone_name = "world"
                    tile_name = "a4"
                    self.zone_name = zone_name
                    self.tiles.zone_name = zone_name
                    self.tiles.load_tile_zone()
                    self.current_tile = self.tiles.get_tile(tile_name)
                    print("This is the tile name: ", self.current_tile.index)
                    self.player.current_tile = self.current_tile
                    utils.clear_screen()
                else:
                    s = "Sorry, I don't recognize this: {}".format(object)
                    raise ValueError(s)
            # -------------------------------------------
            elif command == "examine":
                utils.clear_screen()
                print("-" * 40)
                print("YOU EXAMINE THE TILE YOU ARE ON:")
                s = utils.capitalize_sentences(self.player.current_tile.examination)
                print(s)
                print("-" * 40)
            else:
                S = "Sorry, I don't recognize this:\n"
                s = "command: {}, object: {}".format(command, object)
                raise ValueError(s)

    def move_player_between_zones(self, new_zone, npc_name = "", npc_kind = ""):
        """
        I'm not currently using this.
        :param new_zone: "world", "town" or "dungeon"
        :param npc_name: between 2 and 20 characters.
        :param npc_kind: "warrior" or "mage"
        :return:
        """
        while not new_zone in con.TILE_TYPES:
            print("I don't recognize this zone name: {}".format(new_zone))
            print("Here are the names I recognize: {}".format(con.TILE_TYPES))
            new_zone = input("> ").lower().strip()
            if new_zone == "quit" or new_zone == "exit":
                print("Goodbye! :-)")
                sys.exit()
        # self.player.save()
        self.zone_name = new_zone
        self.tiles.zone_name = new_zone
        self.tiles.load_tile_zone(self.zone_name)
        if len(self.tiles) == 0:
            raise ValueError("There are no tiles!")
        self.player.current_tile = self.tiles.get_tile("a1")
        if new_zone == "provisioner":
            if len(npc_name) == 0 or len(npc_kind) == 0:
                s = "This isn't going to work, I need to know the NPCs name and kind.\n"
                s += "name: {}, kind: {}".format(npc_name, npc_kind)
                raise ValueError(s)
            if not npc_name in ["anna", "cultist", "innkeeper", "king", "monster", "provisioner"]:
                raise ValueError("That npc_name ... I don't recognize it: {}".format(npc_name))
            if not npc_kind in ["server", "ruler", "server", "grass"]:
                raise ValueError("I don't recognize that npc_kind: {}".format(npc_kind))
            # items = Items(self.player.name, self.player.kind)
            self.NPC = NPC(self.player, npc_name, npc_kind)
            self.NPC.load()
            continue_loop = True
            while continue_loop:
                continue_loop = self.NPC.dialogue()

# ================================================
# ================================================

if __name__ == "__main__":
    mytiles = Tiles("world")
    mytiles.display_print()
    # player_name = "bob"
    # player_kind = "warrior"
    # zone_name = "world"
    # mygame = Game(player_name, player_kind, zone_name)
    # mygame.game_loop()
