import utils
import os, sys
import constants as con
from constants import p

# ------------------------------------------------
#                  class Tile
# ------------------------------------------------

class Tile:
    def __init__(self, mydict, npcs):
        # print("mydict in Tile: {}".format(mydict))
        self.index = mydict["index"]
        self.kind_of_tile = mydict["kind"]
        self.description = mydict["description"]
        self.examination = mydict["examine"]
        self.up = mydict["up"].lower()
        self.down = mydict["down"].lower()
        self.right = mydict["right"].lower()
        self.left = mydict["left"].lower()
        npc_name = mydict["npcs"].lower()
        if npc_name == "none":
            self.npc = None
        else:
            self.npc = npcs.get_npc(npc_name)

    def display_line(self):
        s = "index: {} | ".format(self.index)
        s += "kind_of_tile: {} | ".format(self.kind_of_tile)
        s += "description: {} | ".format(self.description)
        s += "examine: {} | ".format(self.examination)
        s += "up: {} | ".format(self.up)
        s += "down: {} | ".format(self.down)
        s += "right: {} | ".format(self.right)
        s += "left: {} | ".format(self.left)
        s += "npcs:\n{} | ".format("No NPCs on Tile." if self.npc == None else self.npc.display_line())
        return s

    def debug_print(self):
        s = "index: {} | ".format(self.index)
        s += "kind_of_tile: {} | ".format(self.kind_of_tile)
        s += "description: {} | ".format(self.description)
        s += "examine: {} | ".format(self.examination)
        s += "up: {} | ".format(self.up)
        s += "down: {} | ".format(self.down)
        s += "right: {} | ".format(self.right)
        s += "left: {} | ".format(self.left)
        s += "npcs: {} | ".format("None" if self.npc == None else self.npc.debug_print())
        print(s)

    def get_fileline(self):
        s = "index: {}\n".format(self.index)
        s += "kind: {}\n".format(self.kind_of_tile)
        s += "description: {}\n".format(self.description)
        s += "examine: {}\n".format(self.examination)
        s += "up: {}\n".format(self.up)
        s += "down: {}\n".format(self.down)
        s += "right: {}\n".format(self.right)
        s += "left: {}".format(self.left)
        s += "npcs: {} | ".format(self.npc.debug_print())
        return s

# ------------------------------------------------
#                  class Tiles
# ------------------------------------------------

class Tiles:
    def __init__(self, zone_name, npcs):
        char_name, char_kind = utils.get_char_info()
        self.char_dir = "{}_{}".format(char_name, char_kind)
        self.zone_name = zone_name
        self.inner = []
        self.load_tile_zone(npcs)

    def load_tile_zone(self, npcs):
        tile_kind_filename = "{}.txt".format(self.zone_name)
        filepath = os.path.join("data", "player_files", self.char_dir, "tiles", tile_kind_filename)
        if p: print("Tiles._load_tile_zone: ", filepath)
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
            # mylines = [i.replace(";", "") for i in mylines]
        if len(mylines) == 0:
            raise ValueError("Error!")
        mylist = []
        for i in range(0, len(mylines), 9):
            mydict = {}
            for j in range(9):
                elem = mylines[i + j]
                mydict = utils.key_value_pair(elem, mydict)
            mylist.append(mydict)
        # ----
        big_list = []
        for adict in mylist:
            new_elem = Tile(adict, npcs)
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

# ------------------------------------------------
#                  class Item
# ------------------------------------------------

class Item:
    def __init__(self, mydict):
        self.id = int(mydict["id"])
        self.name = mydict["name"].lower().strip()
        self.kind = mydict["kind"].lower().strip()
        self.function = mydict["function"].lower().strip()
        self.appearance = mydict["appearance"].lower().strip()
        self.description = mydict["description"].lower().strip()
        self.class_requirement = mydict["class_requirement"].lower().strip()
        self.cost = int(mydict["cost"])
        self.hit_points = int(mydict["hit_points"])
        self.mana_points = int(mydict["mana_points"])
        self.condition = mydict["condition"].lower().strip()

    def debug_print(self):
        s = "id: {} | ".format(self.id)
        s += "name: {} | ".format(self.name)
        s += "kind: {} | ".format(self.kind)
        s += "function: {} | ".format(self.function)
        s += "appearance: {} | ".format(self.appearance)
        s += "description: {} | ".format(self.appearance)
        s += "class_requirement: {} | ".format(self.class_requirement)
        s += "cost: {} | ".format(self.cost)
        s += "hit_points: {} | ".format(self.hit_points)
        s += "mana_points: {} | ".format(self.mana_points)
        s += "condition: {}".format(self.condition)
        print(s)

    def display_line(self):
        s = "id: {} | ".format(self.id)
        s += "name: {} | ".format(self.name)
        s += "kind: {} | ".format(self.kind)
        s += "function: {} | ".format(self.function)
        s += "appearance: {} | ".format(self.appearance)
        s += "description: {} | ".format(self.appearance)
        s += "class_requirement: {} | ".format(self.class_requirement)
        s += "cost: {} | ".format(self.cost)
        s += "hit_points: {} | ".format(self.hit_points)
        s += "mana_points: {} | ".format(self.mana_points)
        s += "condition: {}".format(self.condition)
        return s

    def display_screen(self):
        s = "id: {} | ".format(self.id)
        s += "name: {} | ".format(self.name)
        s += "class_requirement: {}\n".format(self.class_requirement)
        s += "description: {} | ".format(self.appearance)
        s += "hit_points: {} | ".format(self.hit_points)
        s += "mana_points: {}\n".format(self.mana_points)
        s += "condition: {}\n".format(self.condition)
        s += "cost: {}".format(self.cost)
        return s

    def display_screen_line(self):
        s = "id: {} | ".format(self.id)
        s += "{} | ".format(self.name)
        s += "req: {}\n".format(self.class_requirement)
        s += "{} | ".format(self.appearance)
        s += "hit/mana: {}/{} | ".format(self.hit_points, self.mana_points)
        s += "cond: {}\n".format(self.condition)
        s += "cost: {}".format(self.cost)
        return s

    def display_gold(self):
        s = ""
        if self.cost == 0: s = "pieces"
        elif self.cost == 1: s = "piece"
        else: s = "pieces"
        return "{} {}".format(self.cost, s)
# ------------------------------------------------
#                  class Items
# ------------------------------------------------

class Items:
    """This class is never read in directly. It is always
    read in by a player or npc."""
    def __init__(self):
        self.inner = []

    def _load_all_items(self):
        big_list = []
        # ------------------
        char_name, char_kind = utils.get_char_info()
        char_dir = "{}_{}".format(char_name, char_kind)
        filepath = os.path.join("data", "player_files", char_dir, "all_items.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # ------------------
        for i in range(0, len(mylines), 11):
            mydict = {}
            for j in range(11):
                elem = mylines[i + j]
                mydict = utils.key_value_pair(elem, mydict)
                # print(elem)
            new_item = Item(mydict)
            big_list.append(new_item)
        return big_list

    def load_items(self, list_of_indexes):
        list_of_all_items = self._load_all_items()
        mylist = []
        for item in list_of_all_items:
            if item.id in list_of_indexes:
                mylist.append(item)
        self.inner = mylist

    # def load_player_items(self):
    #     self.inner = []
    #     # ------------------
    #     char_name, char_kind = utils.get_char_info()
    #     char_dir = "{}_{}".format(char_name, char_kind)
    #     filepath = os.path.join("data", "player_files", char_dir, "current_items.txt")
    #     with open(filepath, "r") as f:
    #         mylines = f.readlines()
    #         mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    #     # ----
    #     for i in range(0, len(mylines), 11):
    #         mydict = {}
    #         for j in range(11):
    #             elem = mylines[i + j]
    #             if elem.find(";") > -1:
    #                 print(elem)
    #                 raise ValueError("Found one!")
    #             mydict = utils.key_value_pair(elem, mydict)
    #             # print(elem)
    #         new_item = Item(mydict)
    #         self.inner.append(new_item)

    def add_item(self, new_item):
        # check to make sure that this item isn't already in self.inner
        for elem in self.inner:
            if elem.id == new_item.id:
                # s = "Duplicate element found! {} == {}".format(elem, new_item)
                # raise ValueError(s)
                return False
        self.inner.append(new_item)
        return True

    def get_item(self, index):
        if type(index) == type("s"):
            raise ValueError("Error! Index is of type str: {}".format(index))
        if len(self.inner) == 0:
            return None
        myids = []
        for elem in self.inner:
            myids.append(elem.id)
            if elem.id == index:
                return elem
        s = "Error! This index wasn't found: {}\n".format(index)
        s += "{}".format(myids)
        raise ValueError(s)

    def item_exists(self, index):
        if type(index) == type("s"):
            raise ValueError("Error! Index is of type str: {}".format(index))
        if len(self.inner) == 0:
            return False
        for elem in self.inner:
            if elem.id == index:
                return True
        return False

    def remove_item(self, index):
        if type(index) == type("s"):
            raise ValueError("Error! Index is of type str: {}".format(index))
        if len(self.inner) == 0:
            s = "Error! {} can not be removed because self.inner is empty.".format(index)
            raise ValueError(s)
        big_list = []
        myids = []
        item_removed = False
        for elem in self.inner:
            myids.append(elem.id)
            if elem.id == index:
                item_removed = True
            else:
                big_list.append(elem)
        if item_removed == False:
            s = "Error! This index wasn't found: {}\n".format(index)
            s += "{}".format(myids)
            raise ValueError(s)
        self.inner = big_list

    def get_item_by_name(self, name):
        if type(name) != type("s"):
            raise ValueError("Error! Name is NOT a string: {}".format(name))
        if len(self.inner) == 0:
            return None
        for elem in self.inner:
            if elem.name == name:
                return elem
        raise ValueError("{} was not found!!!!".format(name.upper()))

    def print_string(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.debug_print())
        return s

    def display_line(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.display_line())
        return s

    def display_screen(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.display_screen())
        return s

    def display_screen_line(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format("- " * 20)
            s += "{}\n".format(elem.display_screen_line())
        return s

    def debug_print(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.display_line())
        print(s.strip())

    def __len__(self):
        return len(self.inner)

# ------------------------------------------------
#                  class NpcItems
# ------------------------------------------------
class NpcItems:
    """This class is never read in directly. It is always
    read in by a player or npc."""
    def __init__(self, npc_name, npc_kind):
        self.inner = []
        # ------------------
        char_name, char_kind = utils.get_char_info()
        npc_filename = "{}_{}_items.txt".format(npc_name, npc_kind)
        char_dir = "{}_{}".format(char_name, char_kind)
        self.item_filename = "{}_{}_items.txt".format(npc_name, npc_kind)
        mypath = os.path.join("data", "player_files", char_dir, "NPCs", npc_filename)
        with open(mypath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # ----
        for i in range(0, len(mylines), 11):
            mydict = {}
            for j in range(11):
                elem = mylines[i + j]
                mydict = utils.key_value_pair(elem, mydict)
                # print(elem)
            new_item = Item(mydict)
            self.inner.append(new_item)
        # ------------------

    def add_item(self, new_item):
        # check to make sure that this item isn't already in self.inner
        for elem in self.inner:
            if elem.id == new_item.id:
                return False
        self.inner.append(new_item)
        return True

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

    def remove_item(self, index):
        if type(index) == type("s"):
            raise ValueError("Error! Index is of type str: {}".format(index))
        if len(self.inner) == 0:
            s = "Error! {} can not be removed because self.inner is empty.".format(index)
            raise ValueError(s)
        big_list = []
        myids = []
        item_removed = False
        for elem in self.inner:
            myids.append(elem.id)
            if elem.id == index:
                item_removed = True
            else:
                big_list.append(elem)
        if item_removed == False:
            s = "Error! This index wasn't found: {}\n".format(index)
            s += "{}".format(myids)
            raise ValueError(s)

    def print_string(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.display_line())
        return s

    def debug_print(self):
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.display_line())
        print(s)

    def __len__(self):
        return len(self.inner)



# =================================================
# =================================================

def main():
    pass
    # mydict = {}
    # mydict["name"] = "marty"
    # mydict["kind"] = "provioner"
    # mydict["initial_greeting"] = "Hi! What can I do for you?"
    # mydict["greeting"] = "Anything else?"
    # mydict["items"] = ["1", "2", "3"]
    # myitems = npc("marty", "provisioner")

if __name__ == "__main__":
    myitems = Items()
    myitems.load_items([1, 2])
    myitems.debug_print()
