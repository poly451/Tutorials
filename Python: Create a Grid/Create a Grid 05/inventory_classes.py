import constants
import os, sys
import utils

# -----------------------------------------------------------
#                      class Consumable
# -----------------------------------------------------------
class Consumable:
    def __init__(self, mydict):
        # print("Consumable mydict: {}".format(mydict))
        self.index = mydict["index"]
        self.item_kind = mydict["item_kind"]
        if not self.item_kind in constants.CONSUMABLE_KINDS:
            raise ValueError("I couldn't find this item_kind: {}".format(self.item_kind))
        self.species = mydict["species"]
        if not self.species in constants.CONSUMABLE_SPECIES:
            raise ValueError("I couldn't find this species: {}".format(self.species))
        self.name = mydict["name"]
        if not self.name in constants.CONSUMABLE_NAMES:
            raise ValueError("I couldn't find this species: {}".format(self.name))
        self.cost = mydict["cost"]
        self.hp = mydict["hp"]
        self.filename = mydict["filename"]
        s = mydict["core_item"].lower().strip()
        self.core_item = True if s == "true" else False
        self.units = mydict["units"]
        if self.units <= 0:
            raise ValueError("Error!")
        # ----

    def get_fileline(self):
        s = "index: {}\nitem_kind: {}\nspecies: {}\nname: {}\nfilename: {}\n" \
            "cost: {}\nhp: {}\nunits: {}\ncore_item: {}\n"
        s = s.format(self.index, self.item_kind, self.species, self.name,
                     self.filename, self.cost, self.hp, self.units, self.core_item)
        # print("fileline: {}".format(s))
        return s

    def get_list(self):
        s = "kind of item: {}\nspecies: {}\nname: {}\ncost: {}\nhp: {}\nunits: {}"
        s = s.format(self.item_kind, self.species, self.name, self.cost, self.hp, self.units)
        mylist = ["CONSUMABLE: {}".format(self.name)]
        mylist.append(" ")
        mylist.append("species: {}".format(self.species))
        mylist.append("item kind: {}".format(self.item_kind))
        mylist.append("cost: {}".format(self.cost))
        mylist.append("hp: +{}".format(self.hp))
        mylist.append("unit(s) owned: {}".format(self.units))
        return mylist

    def display_string(self):
        s = "kind of item: {}\nspecies: {}\nname: {}\ncost: {}\nhp: {}\nunits: {}"
        s = s.format(self.item_kind, self.species, self.name, self.cost, self.hp, self.units)
        return s

    def debug_print(self):
        s = "index: {}; item_kind: {}; species: {}; name: {}; filename: {}; cost: {}; hp: {}; units: {}; core_item: {}"
        s = s.format(self.index, self.item_kind, self.species, self.name, self.filename, self.cost, self.hp, self.units, self.core_item)
        print(s)

# -----------------------------------------------------------
#                      class Consumables
# -----------------------------------------------------------
class Consumables:
    def __init__(self, character_type, player_name):
        self.character_type = character_type
        self.player_name = player_name
        if not self.character_type in constants.CHARACTER_TYPES:
            raise ValueError("Error!")
        # ----
        if self.character_type == "player":
            self.filepath = os.path.join("data", "playing_characters", self.player_name, "inventory", "consumable_items.txt")
        elif self.character_type == "npc":
            self.filepath = os.path.join("data", "playing_characters", self.player_name, "npc_inventories", "consumable_items.txt")
        else:
            raise ValueError("Error!")
        # ----
        self.inner = []

    def read_data(self):
        self.inner = []
        mylist = utils.read_data_file(self.filepath, 9)
        for elem in mylist:
            new_item = Consumable(elem)
            self.inner.append(new_item)

    def display_string(self):
        mylist = []
        for elem in self.inner:
            if elem.units > 0:
                mylist.append((elem.name, elem.units, elem.cost, elem.hp))
        return mylist

    def get_item(self, the_index):
        for elem in self.inner:
            if the_index == elem.index:
                return elem
        return None

    def get_item_by_name(self, name):
        if not name in constants.CONSUMABLE_NAMES:
            s = "This name is not in constants.CONSUMABLE_NAMES: {}".format(name)
            raise ValueError(s)
        for elem in self.inner:
            # print("name: {}, elem: {}".format(elem.name, name))
            if elem.name == name:
                return elem
        s = "{} was not found in the {}'s inventory".format(name, self.character_type)
        print(s)
        return None

    def add_item(self, item_index):
        # print("***** Adding Item to Consumables *****")
        for elem in self.inner:
            print("ADDING: elem.index: {}; item_index: {}".format(elem.index, item_index))
            if elem.index == item_index:
                elem.units += 1
                return True
        raise ValueError("Error!")

    def add_item_by_name(self, value_name, number_of_units):
        if not value_name in constants.CONSUMABLE_NAMES:
            raise ValueError("Error! {} not in {}".format(value_name, constants.CONSUMABLE_NAMES))
        # ----
        for elem in self.inner:
            print("elem.name: {}, name: {}".format(elem.name, value_name))
            if elem.name == value_name:
                elem.units += number_of_units
                return True
        # ----
        s = "{} was not found in self.inner. Adding it ...".format(value_name)
        print(s)
        filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
        mydict = utils.get_record(filepath, "name", value_name, 9)
        mydict["units"] = number_of_units
        print("Adding: {}".format(mydict))
        new_item = Consumable(mydict)
        self.inner.append(new_item)

    def remove_item(self, index):
        for elem in self.inner:
            if elem.index == index:
                if elem.units == 0:
                    raise ValueError("Error!")
                elem.units -= 1
                return True
        return False

    def _remove_from_inventory(self, index):
        if not utils.is_int(index):
            raise ValueError("Error!")
        if index < 0:
            raise ValueError("Error!")
        # ----
        mylist = []
        for elem in self.inner:
            if elem.index == index:
                pass
            else:
                mylist.append(elem)
        return mylist

    def remove_item_by_name(self, name, number_of_items):
        if type(number_of_items) != type(123):
            raise ValueError("Error!")
        if not utils.is_int(number_of_items):
            raise ValueError("Error!")
        if number_of_items <= 0:
            raise ValueError("Error!")
        if not name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            raise ValueError("Error!")
        # ----
        for elem in self.inner:
            if elem.name == name:
                temp = elem.units - number_of_items
                if temp < 0:
                    return False
                elem.units -= number_of_items
                # ----
                if elem.units <= 0:
                    self.inner = self._remove_from_inventory(elem.index)
                return True

        return False

    def save_data(self):
        if not self.character_type == "player":
            s = "Only a player's inventory can be saved. This is the inventory of a {}"
            s = s.format(self.character_type)
            raise ValueError(s)
        s = ""
        print("Saving {} Consumable Items".format(len(self.inner)))
        for elem in self.inner:
            s += "{}\n".format(elem.get_fileline())
        with open(self.filepath, "w") as f:
            f.write(s)

    def debug_print(self):
        print("---- class Consumables ----")
        if len(self.inner) == 0:
            print("There are NO consumables!")
        for elem in self.inner:
            elem.debug_print()
            # if elem.units != 0:
            #     elem.debug_print()

    def __len__(self):
        return len(self.inner)

# -----------------------------------------------------------
#                      class Weapon
# -----------------------------------------------------------
class Weapon:
    def __init__(self, mydict):
        # print("mydict: {}".format(mydict))
        self.index = mydict["index"]
        self.weapon_kind = mydict["weapon_kind"]
        if not self.weapon_kind in constants.WEAPON_KINDS:
            raise ValueError("Error!")
        self.name = mydict["name"]
        if not self.name in constants.WEAPON_NAMES:
            raise ValueError("Error!")
        self.quality = mydict["quality"]
        self.cost = mydict["cost"]
        self.top_damage = mydict["top_damage"]
        self.minimum_damage = mydict["minimum_damage"]
        self.filename = mydict["filename"]
        s = mydict["core_item"].lower().strip()
        self.core_item = True if s == "true" else False
        self.units = mydict["units"]
        # ----
        self.range_of_effect = mydict["range_of_effect"]
        if not utils.is_int(self.range_of_effect):
            s = "Error! range_of_effect: {}".format(self.range_of_effect)
            raise ValueError(s)
        if self.range_of_effect < 0:
            raise ValueError("Error!")

    # def display_string(self):
    #     s = "{}; +hp: {}; {} gold".format(self.index, self.weapon_kind, self.name, self.quality, self.cost, self.top_damage, self.minimum_damage)
    #     return s

    def debug_print(self):
        s = "index: {}; weaponn_kind: {}; name: {}; quality: {}; "
        s += "cost: {}; top_damage: {}; minimum_damage: {}; filename: {}; " \
             "core_item: {}; units: {}; range_of_effect: {};"
        s = s.format(self.index, self.weapon_kind, self.name, self.quality,
                     self.cost, self.top_damage, self.minimum_damage,
                     self.filename, self.core_item, self.units, self.range_of_effect)
        print(s)

    def get_fileline(self):
        if not utils.is_int(self.index):
            raise ValueError("This is not an integer: {}".format(self.index))
        s = "index: {}\nweapon_kind: {}\nname: {}\nquality: {}\ncost: {}\n"
        s += "top_damage: {}\nminimum_damage: {}\nfilename: {}\ncore_item: {}\n"
        s += "units: {}\nrange_of_effect: {}\n"
        s = s.format(self.index, self.weapon_kind, self.name, self.quality, self.cost,
                     self.top_damage, self.minimum_damage, self.filename, self.core_item,
                     self.units, self.range_of_effect)
        return s

    def read_data(self, master_weapons):
        raise NotImplemented
        this_weapon = master_weapons.get_item(self.index)
        if this_weapon is None:
            raise ValueError("Error!")
        self.weapon_kind = this_weapon.weapon_kind
        self.name = this_weapon.name
        self.quality = this_weapon.quality
        self.cost = this_weapon.cost
        self.top_damage = this_weapon.top_damage
        self.minimum_damage = this_weapon.minimum_damage
        # self.debug_print()
        # ====
        if not self.weapon_kind in constants.WEAPON_KINDS:
            raise ValueError("I couldn't find this item_kind: {}".format(self.weapon_kind))

    def get_list(self):
        mylist = ["WEAPON: {}".format(self.name)]
        mylist.append(" ")
        mylist.append("weapon kind: {}".format(self.weapon_kind))
        mylist.append("quality: {}".format(self.quality))
        mylist.append("cost: {}".format(self.cost))
        mylist.append("top damage: {}".format(self.top_damage))
        mylist.append("minimum damage: {}".format(self.minimum_damage))
        mylist.append("unit(s) owned: {}".format(self.units))
        return mylist

# -----------------------------------------------------------
#                      class Weapons
# -----------------------------------------------------------
class Weapons:
    def __init__(self, character_type, player_name):
        self.character_type = character_type
        self.player_name = player_name
        if not self.character_type in constants.CHARACTER_TYPES:
            raise ValueError("Error!")
        # ----
        if self.character_type == "player":
            self.filepath = os.path.join("data", "playing_characters", self.player_name, "inventory", "weapon_items.txt")
        elif self.character_type == "npc":
            self.filepath = os.path.join("data", "playing_characters", self.player_name, "npc_inventories", "weapon_items.txt")
        else:
            raise ValueError("Error!")
        # ----
        self.inner = []
        self.loop_index = 0

    def read_data(self):
        self.inner = []
        mylist = utils.read_data_file(self.filepath, 11)
        for elem in mylist:
            # print("elem: {}".format(elem))
            new_item = Weapon(elem)
            self.inner.append(new_item)

    def display_string(self):
        mylist = []
        for elem in self.inner:
            if elem.units > 0:
                mylist.append((elem.name, elem.units, elem.cost, elem.top_damage))
        return mylist

    # def add_item(self, index):
    #     for elem in self.inner:
    #         print("elem.index: {}; index: {}".format(elem.index, index))
    #         if elem.index == index:
    #             elem.units += 1
    #             return True
    #     raise ValueError("Error!")

    def add_item_by_name(self, value_name, number_of_units):
        if not value_name in constants.WEAPON_NAMES:
            raise ValueError("Error! {} not in {}".format(value_name, constants.WEAPON_NAMES))
        # ----
        for elem in self.inner:
            print("elem.name: {}, name: {}".format(elem.name, value_name))
            if elem.name == value_name:
                elem.units += number_of_units
                return True
        # ----
        s = "{} was not found in self.inner. Adding it ...".format(value_name)
        print(s)
        filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
        mydict = utils.get_record(filepath, "name", value_name, 11)
        mydict["units"] = number_of_units
        print("Adding: {}".format(mydict))
        new_item = Weapon(mydict)
        self.inner.append(new_item)

    def get_item(self, index):
        if not utils.is_int(index):
            raise ValueError("the index isn't an integer: {}".format(index))
        for a_weapon in self.inner:
            if a_weapon.index == index:
                return a_weapon
        return None

    def get_item_by_name(self, name):
        if not name in constants.WEAPON_NAMES:
            s = "This name is not in constants.WEAPON_NAMES: {}".format(name)
            raise ValueError(s)
        for elem in self.inner:
            # print("name: {}, elem: {}".format(elem.name, name))
            if elem.name == name:
                return elem
        s = "{} was not found in the {}'s inventory".format(name, self.character_type)
        print(s)
        return None

    def _remove_from_inventory(self, index):
        if not utils.is_int(index):
            raise ValueError("Error!")
        if index < 0:
            raise ValueError("Error!")
        # ----
        mylist = []
        for elem in self.inner:
            if elem.index == index:
                pass
            else:
                mylist.append(elem)
        return mylist

    def remove_item(self, index):
        for a_weapon in self.inner:
            if a_weapon.index == index:
                a_weapon.units -= 1
                if a_weapon.units <= 0:
                    # remove from inventory
                    self.inner = self._remove_from_inventory(index)
                return True
        raise ValueError("Error!")

    def remove_item_by_name(self, name, number_of_items):
        if type(number_of_items) != type(123):
            raise ValueError("Error!")
        if number_of_items <= 0:
            raise ValueError("Error!")
        # ----
        for elem in self.inner:
            if elem.name == name:
                temp = elem.units - number_of_items
                if temp < 0:
                    return False
                elem.units -= number_of_items
                if elem.units <= 0:
                    self.inner = self._remove_from_inventory(elem.index)
                return True
        return False

    def debug_print(self):
        if len(self.inner) == 0:
            print("There are NO WEAPONS!")
        print("---- class Weapons ----")
        for a_weapon in self.inner:
            a_weapon.debug_print()

    def save_data(self):
        if not self.character_type == "player":
            s = "Only a player's inventory can be saved. This is the inventory of a {}"
            s = s.format(self.character_type)
            raise ValueError(s)
        s = ""
        print("Saving {} Weapon Items".format(len(self.inner)))
        for elem in self.inner:
            s += "{}\n".format(elem.get_fileline())
        # print(s)
        with open(self.filepath, "w") as f:
            f.write(s)

    def __len__(self):
        return len(self.inner)

    def __getitem__(self, item):
        return self.inner[item]

    def __next__(self):
        if self.loop_index >= len(self.inner):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.inner[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

# **********************************************

def test_consumables():
    myclass = Consumables("player", "henry")
    myclass.read_data()
    myclass.debug_print()

def test_weapons():
    myclass = Weapons("player", "henry")
    myclass.read_data()
    print("=====================")
    myitem = myclass.get_item_by_name("gold ring")
    myitem.debug_print()
    # myclass.add_item_by_name("gold ring", 2)
    # myclass.save_data()
    # myclass.remove_item_by_name("gold ring", 1)
    # myclass.remove_item(5)
    # myclass.debug_print()
    # myclass.remove_item(5)
    # myclass.remove_item(index=2)
    # myclass.debug_print()


if __name__ == "__main__":
    test_weapons()