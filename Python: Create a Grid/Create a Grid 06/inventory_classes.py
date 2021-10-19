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
            raise ValueError("I couldn't find this consumable name: {}".format(self.name))
        self.cost = mydict["cost"]
        self.hp = mydict["hp"]
        self.filename = mydict["filename"]
        filepath = utils.get_filepath(self.filename)
        if filepath is None:
            s = "I don't recognize this filename: {}"
            s = s.format(self.filename)
            raise ValueError(s)
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
        mylist = ["{} ({})".format(self.name, self.item_kind)]
        mylist.append("units: {}".format(self.units))
        mylist.append("gold: {}".format(self.cost))
        mylist.append("hit points: {}".format(self.hp))
        mylist.append("species: {}".format(self.species))
        mylist.append("Can be sold: {}".format(True if self.core_item == False else False))
        return mylist

    def debug_print(self):
        s = "index: {}; item_kind: {}; species: {}; name: {}; filename: {}; cost: {}; hp: {}; units: {}; core_item: {}"
        s = s.format(self.index, self.item_kind, self.species, self.name.upper(),
                     self.filename, self.cost, self.hp, self.units, self.core_item)
        print(s)

# -----------------------------------------------------------
#                      class Consumables
# -----------------------------------------------------------
class Consumables:
    def __init__(self, player_name, npc_name, character_type):
        if utils.validate_player_name(player_name) == False:
            # print("DEBUGGING: This is the character type: {}".format(character_type))
            raise ValueError("That is not a valid player name: {}".format(player_name))
        if utils.is_a_valid_npc_name(player_name=player_name, npc_name=npc_name) == False:
            raise ValueError("This is not a valid NPC name: {}".format(npc_name))
        if not character_type in constants.CHARACTER_TYPES:
            raise ValueError("That is not a valid character type: {}".format(character_type))
        # ----
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

    # in class Consumables
    def read_data(self):
        self.inner = []
        print("Reading in consumables data from: {}".format(self.filepath))
        mylist = utils.read_data_file(self.filepath, 9)
        for mydict in mylist:
            new_item = Consumable(mydict)
            self.inner.append(new_item)
        print("Read in {} records from class Consumables.".format(len(self.inner)))

    def display_list(self):
        mylist = []
        for elem in self.inner:
            if elem.units > 0:
                # s = "{} base_cost: {}g hps: {} ({})"
                # s = s.format(elem.name, elem.cost, elem.hp, elem.units)
                mylist.append([elem.name, elem.units, elem.cost, elem.hp])
                # mylist.append(s)
        return mylist

    def display_string(self):
        mylist = []
        if self.character_type == "player":
            for elem in self.inner:
                if elem.units > 0:
                    s = "{} ({}) - {}".format(elem.name, elem.cost, elem.units)
                    mylist.append(s)
            return mylist
        else:
            for elem in self.inner:
                if elem.units > 0:
                    s = "{} ({}) - {}".format(elem.name, elem.cost, elem.units)
                    mylist.append(s)
            return mylist

    def get_item(self, the_index):
        for elem in self.inner:
            if the_index == elem.index:
                return elem
        return None

    def sell_item_by_name(self, item_name, number_of_items, gold_coins):
        """The inventory sells the item to noone"""
        # Does item exist?
        if self.inner is None:
            s = "Have you remembered to call read_data?"
            raise ValueError(s)
        if not item_name in constants.CONSUMABLE_NAMES:
            s = "This name is not in constants.CONSUMABLE_NAMES: {}".format(item_name)
            raise ValueError(s)
        if gold_coins is None: raise ValueError("Error")
        # ----
        the_item = self.get_item_by_name(item_name)
        if the_item is None:
            s = "The inventory does not contain this item: {}\n".format(item_name)
            s += "Therefore the inventory cannot sell it."
            return False
        if the_item.units < number_of_items: raise ValueError("Error")
        # ----
        # How much does the inventory get from this sale?
        gold_to_receive = the_item.cost * number_of_items
        gold_coins.units += gold_to_receive
        # print("gold player has: {}".format(gold_coins.units))
        # print("number of items being removed: {}".format(number_of_items))
        # raise NotImplemented
        # self.debug_print()
        print("**********************")
        self.remove_item_by_name(item_name, number_of_items)
        # self.debug_print()
        # raise NotImplemented

    def buy_item_by_name(self, item_name, number_of_items, gold_coins):
        """The inventory buys the item from noone."""
        # Does the item exist in the player's inventory?
        # If so, then just increase the number of units.
        # If it doesn't, then get the item and add it with
        # the appropriate number of units.
        # ----
        def buy_item(item_name, number_of_items):
            filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
            mydict = utils.get_record(filepath=filepath,
                                      key_name="name",
                                      value_name=item_name,
                                      number_of_fields=9)
            mydict["units"] = number_of_items
            new_object = Consumable(mydict)
            # ----
            # Check to make sure inventory has enough gold before
            # item is included
            what_the_items_cost = mydict["cost"] * number_of_items
            if gold_coins.units < what_the_items_cost:
                raise ValueError("You don't have enough money for that!")
            gold_coins.units -= what_the_items_cost
            # ----
            # Add the item to the inventory.
            self.inner.append(new_object)
        # ---- ---- ---- ----
        the_item = self.get_item_by_name(item_name)
        if the_item is None:
            buy_item(item_name, number_of_items)
            return True
        if gold_coins is None: raise ValueError("Error")
        # ----
        # Check to make sure the inventory has enough gold.
        what_the_items_cost = the_item.cost * number_of_items
        if gold_coins.units < what_the_items_cost:
            raise ValueError("You don't have enough money for that!")
        # Pay the gold.
        gold_coins.units -= what_the_items_cost
        # ----
        # Add the item.
        the_item.units += number_of_items

    def get_item_by_name(self, name):
        if self.inner is None:
            s = "Have you remembered to call read_data?"
            raise ValueError(s)
        if not name in constants.CONSUMABLE_NAMES:
            s = "This name is not in constants.CONSUMABLE_NAMES: {}".format(name)
            raise ValueError(s)
        # ----
        for elem in self.inner:
            # print("name: {}, elem: {}".format(elem.name, name))
            if elem.name == name:
                return elem
        # ----
        s = "{} was not found in the {}'s inventory\n".format(name, self.character_type)
        s += "Here is their inventory: {}".format(self.debug_print_names())
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

    # in class Consumables
    def add_item_by_name(self, value_name, number_of_units):
        if not value_name in constants.CONSUMABLE_NAMES:
            raise ValueError("Error! {} not in {}".format(value_name, constants.CONSUMABLE_NAMES))
        # ----
        for elem in self.inner:
            # print("elem.name: {}, name: {}".format(elem.name, value_name))
            if elem.name == value_name:
                elem.units += number_of_units
                return True
        # ----
        # s = "{} was not found in self.inner. Adding it ...".format(value_name)
        # print(s)
        filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
        mydict = utils.get_record(filepath, "name", value_name, 9)
        if mydict is None:
            s = "I was not able to get this item: {}".format(value_name)
            raise ValueError(s)
        mydict["units"] = number_of_units
        # print("Adding: {}".format(mydict))
        new_object = Consumable(mydict)
        self.inner.append(new_object)

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
        s = "removing item by name: {} ({})".format(name, number_of_items)
        print(s)
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
                # print("You have {} units of item {}.".format(elem.units, name))
                temp = elem.units - number_of_items
                if temp < 0:
                    return False
                elem.units -= number_of_items
                # ----
                if elem.units <= 0:
                    self.inner = self._remove_from_inventory(elem.index)
                # print("You now have {} units of item {}.".format(elem.units, name))
                # raise NotImplemented
                return True
        return False

    def save_data(self):
        s = "Saving {} items to the {}'s inventory."
        s += "Saving to this filepath: {}"
        s = s.format(len(self.inner), self.character_type.upper(), self.filepath)
        print(s)
        if not self.character_type == "player":
            s = "Only a player's inventory can be saved. This is the inventory of a {}"
            s = s.format(self.character_type)
            raise ValueError(s)
        s = ""
        print("Saving {} Consumable Items".format(len(self.inner)))
        for elem in self.inner:
            s += "{}\n".format(elem.get_fileline())
        with open(self.filepath, "w") as f:
            print("This is what is being saved: {}".format(s))
            f.write(s)

    def debug_print_names(self):
        print("Consumables:".upper())
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.name)
        print(s)

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
            s = "Error! I don't recognize this as a weapon kind: {}"
            s = s.format(self.weapon_kind)
            raise ValueError(s)
        self.name = mydict["name"]
        if not self.name in constants.WEAPON_NAMES:
            s = "Error! This isn't a weapon name: self.name: {}".format(self.name)
            raise ValueError(s)
        self.quality = mydict["quality"]
        self.cost = mydict["cost"]
        self.top_damage = mydict["top_damage"]
        self.minimum_damage = mydict["minimum_damage"]
        self.filename = mydict["filename"]
        s = mydict["core_item"].lower().strip()
        self.core_item = True if s == "true" else False
        self.units = mydict["units"]
        if utils.is_int(self.units) == False: raise ValueError("Error")
        self.units = int(self.units)
        # ----
        self.range_of_effect = mydict["range_of_effect"]
        if utils.is_int_or_real(self.range_of_effect) == False:
            s = "I don't recognize his as an integer: {}"
            s = s.format(self.range_of_effect)
            raise ValueError(s)
        if utils.is_int(self.range_of_effect) == True:
            self.range_of_effect = int(self.range_of_effect)
        elif utils.is_real(self.range_of_effect) == True:
            self.range_of_effect = float(self.range_of_effect)
        else:
            raise ValueError("Error")
        if self.range_of_effect < 0:
            raise ValueError("Error!")

    # def display_string(self):
    #     s = "{}; +hp: {}; {} gold".format(self.index, self.weapon_kind, self.name, self.quality, self.cost, self.top_damage, self.minimum_damage)
    #     return s

    def debug_print(self):
        s = "index: {}; weaponn_kind: {}; name: {}; quality: {}; "
        s += "cost: {}; top_damage: {}; minimum_damage: {}; filename: {}; " \
             "core_item: {}; units: {}; range_of_effect: {};"
        s = s.format(self.index, self.weapon_kind, self.name.upper(), self.quality,
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

    def display_string(self):
        mylist = ["{} ({})".format(self.name, self.weapon_kind)]
        mylist.append("units: {}".format(self.units))
        mylist.append("gold: {}, quality: {}".format(self.cost, self.quality))
        mylist.append("damage: {} to {}".format(self.minimum_damage, self.top_damage))
        mylist.append("range: {}".format(self.range_of_effect))
        mylist.append("Can be sold: {}".format(True if self.core_item == False else False))
        return mylist

# -----------------------------------------------------------
#                      class Weapons
# -----------------------------------------------------------
class Weapons:
    def __init__(self, player_name, npc_name, character_type):
        if utils.validate_player_name(player_name) == False:
            raise ValueError("That is not a valid player name: {}".format(player_name))
        if utils.is_a_valid_npc_name(player_name=player_name, npc_name=npc_name) == False:
            raise ValueError("That is not a valid npc name: {}".format(npc_name))
        if not character_type in constants.CHARACTER_TYPES:
            raise ValueError("That is not a valid character type: {}".format(character_type))
        # ----
        self.character_type = character_type
        self.player_name = player_name
        self.character_type = character_type
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

    # in class Weapons
    def read_data(self):
        print("Reading in data from weapons file: {}".format(self.filepath))
        self.inner = []
        mylist = utils.read_data_file(self.filepath, 11)
        for elem in mylist:
            # print("elem: {}".format(elem))
            new_item = Weapon(elem)
            self.inner.append(new_item)
        print("Read in {} records from class Weapons.".format(len(self.inner)))

    def display_list(self):
        mylist = []
        for elem in self.inner:
            if elem.units > 0:
                mylist.append([elem.name, elem.units, elem.cost, elem.top_damage])
        return mylist

    def display_string(self):
        mylist = []
        if self.character_type == "player":
            for elem in self.inner:
                if elem.units > 0:
                    s = "{} ({}) - {}"
                    s = s.format(elem.name, elem.cost, elem.units)
                    mylist.append(s)
                    # mylist.append((elem.name, elem.units, elem.cost, elem.top_damage))
            return mylist
        else:
            for elem in self.inner:
                if elem.units > 0:
                    s = "{} ({}) - {}"
                    s = s.format(elem.name, elem.cost, elem.units)
                    mylist.append(s)
                    # mylist.append((elem.name, elem.units, elem.cost, elem.top_damage))
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
        if mydict is None:
            s = "filepath: {}\n".format(filepath)
            s += "field: name, item_name: {}".format(value_name)
            raise ValueError(s)
        mydict["units"] = number_of_units
        print("Adding: {}".format(mydict))
        new_item = Weapon(mydict)
        self.inner.append(new_item)

    def sell_item_by_name(self, item_name, number_of_items):
        """The inventory sells the item to noone"""
        # ---- ----
        gold_coins = self.get_item_by_name("gold coin")
        if gold_coins is None: raise ValueError("Error")
        # ----
        # Does item exist?
        if self.inner is None:
            s = "Have you remembered to call read_data?"
            raise ValueError(s)
        if item_name in constants.CONSUMABLE_NAMES:
            s = "This is a conumable item, NOT a weapon!!!: {}".format(item_name)
            raise ValueError(s)
        if gold_coins is None: raise ValueError("Error")
        # ----
        the_item = self.get_item_by_name(item_name)
        if the_item is None:
            s = "The inventory does not contain this item: {}\n".format(item_name)
            s += "Therefore the inventory cannot sell it."
            return False
        if the_item.units < number_of_items: raise ValueError("Error")
        # ----
        # How much does the inventory get from this sale?
        gold_to_receive = the_item.cost * number_of_items
        gold_coins.units += gold_to_receive
        # print("gold player has: {}".format(gold_coins.units))
        # print("number of items being removed: {}".format(number_of_items))
        # raise NotImplemented
        # self.debug_print()
        print("**********************")
        self.remove_item_by_name(item_name, number_of_items)
        # self.debug_print()
        # raise NotImplemented

    def buy_item_by_name(self, item_name, number_of_items):
        """The inventory buys the item from noone."""
        # Does the item exist in the player's inventory?
        # If so, then just increase the number of units.
        # If it doesn't, then get the item and add it with
        # the appropriate number of units.
        # ----
        def buy_item(item_name, number_of_items):
            filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
            mydict = utils.get_record(filepath=filepath,
                                      key_name="name",
                                      value_name=item_name,
                                      number_of_fields=11)
            if mydict is None:
                s = "item_name: {}".format(item_name)
                raise ValueError(s)
            mydict["units"] = number_of_items
            new_object = Weapon(mydict)
            # ----
            # Check to make sure inventory has enough gold before
            # item is included
            what_the_items_cost = mydict["cost"] * number_of_items
            if gold_coins.units < what_the_items_cost:
                raise ValueError("You don't have enough money for that!")
            gold_coins.units -= what_the_items_cost
            # ----
            # Add the item to the inventory.
            self.inner.append(new_object)
        # ---- ---- ---- ----
        gold_coins = self.get_item_by_name("gold coin")
        if gold_coins is None: raise ValueError("Error")
        # ----
        the_item = self.get_item_by_name(item_name)
        if the_item is None:
            buy_item(item_name, number_of_items)
            return True
        # ----
        # Check to make sure the inventory has enough gold.
        what_the_items_cost = the_item.cost * number_of_items
        if gold_coins.units < what_the_items_cost:
            raise ValueError("You don't have enough money for that!")
        # Pay the gold.
        gold_coins.units -= what_the_items_cost
        # ----
        # Add the item.
        the_item.units += number_of_items

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
        s = "Saving {} items to the {}'s inventory."
        s += "Saving to this filepath: {}".format(self.filepath)
        s = s.format(len(self.inner), self.character_type.upper())
        print(s)
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

    def debug_print_names(self):
        print("Weapons:".upper())
        s = ""
        for elem in self.inner:
            s += "{}\n".format(elem.name)
        print(s)

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
# def _get_user_input():
#     u1 = "weapon_kind"
#     u2 = "name"
#     u3 = "quality"
#     u4 = "cost"
#     u5 = "top_damage"
#     u6 = "minimum_damage"
#     u7 = "filename"
#     u8 = "core_item"
#     u9 = "units"
#     u10 = "range_of_effect"
#     mydict = {}
#     mylist = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
#     for item in mylist:
#         if item == "quality":
#             print("Possible values:\n{}".format(constants.QUALITY))
#         elif item == "weapon_kind":
#             print("Possible weapon kinds:\n{}".format(constants.WEAPON_KINDS))
#         elif item == "name":
#             print("Possible weapon names:\n{}".format(constants.WEAPON_NAMES))
#         elif item == "top_damage":
#             print("Possible values:\n{}".format(constants.DAMAGE))
#         elif item == "minimum_damage":
#             print("Possible values:\n{}".format(constants.DAMAGE))
#         # ----
#         print("{}:".format(item))
#         user_input = input("> ").lower().strip()
#         if user_input in ["q", "quit"]:
#             print("This is what you entered:")
#             print(mydict)
#             print("Goodbye!")
#             sys.exit()
#         # ----
#         if item == "quality":
#             if utils.is_int(user_input) == False:
#                 print("Sorry! That doesn't seem to be an integer. Goodbye!")
#                 sys.exit()
#             user_input = int(user_input)
#             if not user_input in constants.QUALITY:
#                 print("Sorry! This won't work as a QUALITY: {}".format(constants.QUALITY))
#                 sys.exit()
#         elif item == "top_damage":
#             if utils.is_int(user_input) == False:
#                 print("Sorry! That doesn't seem to be an integer. Goodbye!")
#                 sys.exit()
#             user_input = int(user_input)
#             if not user_input in constants.DAMAGE:
#                 print(constants.DAMAGE)
#                 print("Sorry! That doesn't seem to be a valid DAMAGE. Goodbye!")
#                 sys.exit()
#         elif item == "filename":
#             if user_input.find(".png") == -1:
#                 user_input = "{}.png".format(user_input)
#             if utils.image_filepath_exists(user_input.lower().strip()) == False:
#                 print("Sorry, this ({}) doesn't seem to be a valid name for an image file.".format(user_input))
#                 sys.exit()
#         # ----
#         mydict[item] = user_input
#     print(mydict)
#     # raise NotImplemented
#     return mydict
#
# def _get_data_from_file():
#     data_filepath = os.path.join("data", "new_weapon_data.txt")
#     if utils.is_file(data_filepath) == False:
#         print("Doh! That's not a valid path!!")
#         print(data_filepath)
#         sys.exit()
#     return utils.read_file(data_filepath)[0]
#
# def add_weapon_to_game():
#     # getting index
#     filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
#     mylist = utils.read_data_file(filepath, 11)
#     new_index = utils.get_highest_index(mylist) + 1
#     # ----
#     user_input = ""
#     while not user_input in ["y", "n", "yes", "no"]:
#         user_input = input("Would you like to read in the information from a file? (y/n) > ").lower().strip()
#         if user_input == "quit":
#             print("Goodbye!")
#             sys.exit()
#     # ----------------------------------
#     new_weapon_dict = {}
#     if not user_input in ["y", "yes"]:
#         new_weapon_dict = _get_user_input()
#     else:
#         new_weapon_dict = _get_data_from_file()
#     # ----------------------------------
#     # print("new_weapon_dict: {}".format(new_weapon_dict))
#     # [print(key, value) for key, value in new_weapon_dict.items()]
#     print("New index: {}".format(new_index))
#     new_dict = {"index": new_index}
#     new_weapon_dict.update(new_dict)
#     # new_weapon_dict["index"] = new_index
#     print("New index added ...")
#     # ---- Checking to make sure everything is okay ---
#     new_weapon = Weapon(new_weapon_dict)
#     new_weapon.debug_print()
#     # -------------------------------------------------
#     print("---- New Weapon Data ----")
#     new_weapon.debug_print()
#     user_input2 = input("Add this NEW data to the master weapons list? (y/n) > ").lower().strip()
#     if not user_input2 in ['y', 'yes']:
#         print("Goodbye!")
#         sys.exit()
#     # ----
#     master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
#     weapons_list = utils.read_data_file(master_filepath, 11)
#     weapons_list.append(new_weapon_dict)
#     print("--- This is what will be saved to the MASTER file. Please read. carefully!!!! ----")
#     [print(i) for i in weapons_list]
#     user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
#     if not user_input in ["y", "yes"]:
#         print("Goodbye!")
#         sys.exit()
#     # ----
#     # debug_file = os.path.join("data", "testing.txt")
#     with open(master_filepath, "w") as f:
#         for mydict in weapons_list:
#             s = ""
#             for key, value in mydict.items():
#                 s += "{}: {}\n".format(key, value)
#             s += "\n"
#             f.write(s)
#     # ------------------------------------------------
#     print("The record was written successfully to the file:")
#     print(master_filepath)
#
# def add_weapon_to_player(player_name):
#     print("Here are the players:")
#     player_names = utils.get_all_player_names()
#     [print(i) for i in player_names]
#     print("----")
#     print("Here are all the weapons in the game:")
#     print(constants.WEAPON_NAMES)
#     print("----")
#     print("Here are all the weapons the player has:")
#     player_weapons = utils.get_player_weapons_from_file(player_name)
#     [print(i) for i in player_weapons]
#     print("----")
#     print("Which weapon would you like to give the player?")
#     print("Here are your choices:")
#     [print(i) for i in constants.WEAPON_NAMES]
#     weapon_name = ""
#     if not weapon_name in constants.WEAPON_NAMES:
#         weapon_name = input("> ").lower().strip()
#         if weapon_name in ["q", "quit"]:
#             print("Goodbye!")
#             sys.exit()
#     print("You chose the weapon: {}".format(weapon_name))
#     if weapon_name in player_weapons:
#         s = "The player, {}, already has this weapon ({})!!"
#         s = s.format(player_name.upper(), weapon_name.upper())
#         raise ValueError(s)
#     # ----------------------------------
#     # ---- Getting the list of dictionaries ----
#     master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
#     weapons_list = utils.read_data_file(master_filepath, 11)
#     target_dict = utils.get_dict(weapons_list, "name", weapon_name)
#     if target_dict is None: raise ValueError("Error!")
#     # ----
#     # target_dict = {}
#     # for mydict in weapons_list:
#     #     for key, value in mydict.items():
#     #         if key == "name" and value == weapon_name:
#     #             target_dict = mydict
#     #             break
#     if len(target_dict) == 0:
#         raise ValueError("Error")
#     # ----
#     # Checking to make sure that target_dict isn't in weapons_list
#     # ----
#     player_weapons_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
#     player_weapons = utils.read_data_file(player_weapons_filepath, 11)
#     for mydict in player_weapons:
#         for key, value in mydict.items():
#             if key == "name" and "value" == weapon_name:
#                 s = "Error! The player ({}) already has this weapon ({})"
#                 s = s.format(player_name, weapon_name)
#                 raise ValueError(s)
#     # ----
#     # Giving the target dict to the player
#     # ----
#     target_dict["index"] = target_dict["index"]
#     player_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
#     player_weapons_list = utils.read_data_file(player_filepath, 11)
#     player_weapons_list.append(target_dict)
#     # ----
#     print("--- This is what will be saved to the PLAYER'S file. Please read. carefully!!!! ----")
#     [print(i) for i in player_weapons_list]
#     user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
#     if not user_input in ["y", "yes"]:
#         print("Goodbye!")
#         sys.exit()
#     # ----
#     # debug_file = os.path.join("data", "testing.txt")
#     with open(player_filepath, "w") as f:
#         for mydict in player_weapons_list:
#             s = ""
#             for key, value in mydict.items():
#                 s += "{}: {}\n".format(key, value)
#             s += "\n"
#             f.write(s)
#     # ------------------------------------------------
#     print("The record was written successfully to the file:")
#     print(master_filepath)
#
# def add_weapon_to_npc(player_name):
#     update_npc_weapons(player_name=player_name)
#
# def update_npc_weapons(player_name):
#     """
#     All we need to do is update the inventories in npc_inventories
#     since no npc currently has a unique inventory. Although they COULD
#     have unique inventories by player character. So, for example, the
#     npc's inventories in Henry's npc_inventory directory could be
#     different from the inventories in another character's inventory.
#     """
#     # todo: Implement inventories for each npc character.
#     if player_name is None or len(player_name) == 0:
#         raise ValueError("Error")
#     if utils.validate_player_name(player_name) == False:
#         raise ValueError("Error")
#     master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
#     local_filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "weapon_items.txt")
#     master_weapon_items = utils.read_data_file(master_filepath, 11)
#     # ----
#     # local_filepath = os.path.join("data", "testing.txt")
#     with open(local_filepath, "w") as f:
#         for mydict in master_weapon_items:
#             s = ""
#             for key, value in mydict.items():
#                 s += "{}: {}\n".format(key, value)
#             s += "\n"
#             f.write(s)
#     # ------------------------------------------------
#     print("The record was written successfully to the file:")
#     print(local_filepath)
#
#     # npc_names = utils.get_all_npc_names_by_player(player_name)
#     # if npc_name is None:
#     #     if npc_names is None: raise ValueError("Error")
#     #     if len(npc_names) == 0: raise ValueError("Error")
#     #     # ----
#     #     print("Here are all the names of {}")
#     #     [print(i) for i in npc_names]
#     #     npc_name = input("> ").lower().strip()
#     # # ----
#     # if not npc_name in npc_names: raise ValueError("Error")
#     # # ---- ----
#     # print("Here are all the weapons in the game:")
#     # print(constants.WEAPON_NAMES)
#     # print("----")
#     # print("Here are all the weapons the npc ({}) has:".format(npc_name.upper()))
#     # player_weapons = utils.get_npc_weapons_from_local_file(player_name=player_name)
#     # [print(i) for i in player_weapons]
#     # print("----")
#     # print("Which weapon would you like to give the player?")
#     # print("Here are your choices:")
#     # [print(i) for i in constants.WEAPON_NAMES]
#     # weapon_name = ""
#     # if not weapon_name in constants.WEAPON_NAMES:
#     #     weapon_name = input("> ").lower().strip()
#     #     if weapon_name in ["q", "quit"]:
#     #         print("Goodbye!")
#     #         sys.exit()
#     # print("You chose the weapon: {}".format(weapon_name))
#     # if weapon_name in player_weapons:
#     #     s = "The player, {}, already has this weapon ({})!!"
#     #     s = s.format(player_name.upper(), weapon_name.upper())
#     #     raise ValueError(s)
#     # # ----------------------------------
#     # # ---- Getting the list of dictionaries ----
#     # master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
#     # weapons_list = utils.read_data_file(master_filepath, 11)
#     # target_dict = utils.get_dict(weapons_list, "name", weapon_name)
#     # if target_dict is None: raise ValueError("Error!")
#     # # ----
#     # # target_dict = {}
#     # # for mydict in weapons_list:
#     # #     for key, value in mydict.items():
#     # #         if key == "name" and value == weapon_name:
#     # #             target_dict = mydict
#     # #             break
#     # if len(target_dict) == 0:
#     #     raise ValueError("Error")
#     # # ----
#     # # Checking to make sure that target_dict isn't in weapons_list
#     # # ----
#     # player_weapons_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
#     # player_weapons = utils.read_data_file(player_weapons_filepath, 11)
#     # for mydict in player_weapons:
#     #     for key, value in mydict.items():
#     #         if key == "name" and "value" == weapon_name:
#     #             s = "Error! The player ({}) already has this weapon ({})"
#     #             s = s.format(player_name, weapon_name)
#     #             raise ValueError(s)
#     # # ----
#     # # Giving the target dict to the player
#     # # ----
#     # target_dict["index"] = target_dict["index"]
#     # player_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
#     # player_weapons_list = utils.read_data_file(player_filepath, 11)
#     # player_weapons_list.append(target_dict)
#     # # ----
#     # print("--- This is what will be saved to the PLAYER'S file. Please read. carefully!!!! ----")
#     # [print(i) for i in player_weapons_list]
#     # user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
#     # if not user_input in ["y", "yes"]:
#     #     print("Goodbye!")
#     #     sys.exit()
#     # # ----
#     # # debug_file = os.path.join("data", "testing.txt")
#     # with open(player_filepath, "w") as f:
#     #     for mydict in player_weapons_list:
#     #         s = ""
#     #         for key, value in mydict.items():
#     #             s += "{}: {}\n".format(key, value)
#     #         s += "\n"
#     #         f.write(s)
#     # # ------------------------------------------------
#     # print("The record was written successfully to the file:")
#     # print(master_filepath)
#
# def test_consumables():
#     myclass = Consumables("player", "henry")
#     myclass.read_data()
#     myclass.debug_print()
#
# def test_weapons(player_name, npc_name, character_type):
#     myclass = Weapons(player_name=player_name, npc_name=npc_name, character_type=character_type)
#     myclass.read_data()
#     print("=====================")
#     myitem = myclass.get_item_by_name("gold ring")
#     myitem.debug_print()
#     # myclass.add_item_by_name("gold ring", 2)
#     # myclass.save_data()
#     # myclass.remove_item_by_name("gold ring", 1)
#     # myclass.remove_item(5)
#     # myclass.debug_print()
#     # myclass.remove_item(5)
#     # myclass.remove_item(index=2)
#     # myclass.debug_print()
#
# # def test_inventory(player_name, npc_name, character_type):
# #     myinventory =
#
#
# if __name__ == "__main__":
#     print("What would you like to do?")
#     """
#     Note: If you want to add a NEW item to the game
#     you will need to add it to the constants.py module,
#     specifically to WEAPON_NAMES. So:
#     constants.WEAPON_NAMES
#     """
#     player_name = "henry"
#     add_weapon_to_the_game = False
#     add_weapon_to_the_player = False
#     add_weapon_to_an_npc = True
#     # ----
#     if add_weapon_to_the_game == True:
#         add_weapon_to_game()
#     if add_weapon_to_the_player == True:
#         add_weapon_to_player(player_name=player_name)
#     if add_weapon_to_an_npc == True:
#         add_weapon_to_npc(player_name)
#     # test_weapons()
#     # test_inventory()