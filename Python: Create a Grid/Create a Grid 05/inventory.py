import sys, os
import constants
import utils
from inventory_classes import Consumables, Weapons

# -----------------------------------------------------------
#                      class Inventory
# -----------------------------------------------------------

class Inventory:
    def __init__(self, character_type, player_name):
        if not character_type in constants.CHARACTER_TYPES:
            raise ValueError("Error!")
        if utils.validate_name(player_name) == False:
            s = "Error! {} is not a valid name.".format(player_name.upper())
            raise ValueError(s)
        # ----
        self.character_type = character_type
        self.player_name = player_name
        self.consumables = Consumables(self.character_type, self.player_name)
        self.weapons = Weapons(self.character_type, self.player_name)

    def read_data(self):
        self.consumables.read_data()
        self.weapons.read_data()

    def get_item_by_name(self, item_name):
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            s = "{} is neither a weapon nor a consumable.".format(item_name)
            raise ValueError(s)
        # ----
        if item_name in constants.CONSUMABLE_NAMES:
            an_item = self.consumables.get_item_by_name(item_name)
            if not an_item is None:
                return an_item
        elif item_name in constants.WEAPON_NAMES:
            an_item = self.weapons.get_item_by_name(item_name)
            if not an_item is None:
                return an_item
        return None

    def add_item_by_name(self, item_name, number_of_items):
        if number_of_items <= 0:
            raise ValueError("Error!")
        print("Adding {} items with the item_name: {}".format(number_of_items, item_name))
        if item_name in constants.CONSUMABLE_NAMES:
            self.consumables.add_item_by_name(item_name, number_of_items)
        elif item_name in constants.WEAPON_NAMES:
            self.weapons.add_item_by_name(item_name, number_of_items)
        else:
            s = "Error! I don't recognize this item_name: {}\n".format(item_name)
            s += "Perhaps you forgot to include the 'item_name' in the list of CONSUMABLE_NAMES or WEAPON_NAMES."
            raise ValueError(s)

    def remove_item_by_name(self, item_name, number_of_items):
        if not utils.is_int(number_of_items):
            raise ValueError("Error!")
        if number_of_items <= 0:
            raise ValueError("Error!")
        if type(item_name) != type("abc"):
            raise ValueError("Error!")
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            raise ValueError("Error")
        # ----
        if self.consumables.remove_item_by_name(item_name, number_of_items) == True:
            return True
        if self.weapons.remove_item_by_name(item_name, number_of_items) == True:
            return True
        return False

    # --------------------------------------------

    def display_string(self):
        new_list = []
        consumables_list = self.consumables.display_string()
        weapons_list = self.weapons.display_string()
        inventory_list = consumables_list + weapons_list
        ret_list = utils.format_inventory_list(inventory_list)
        # print("ret_list: {}".format(ret_list))
        # print("----------------")
        # temp = [0, "index | name | (cost) | hps | #"]
        # ret_list.insert(0, temp)
        # print("ret_list: {}".format(ret_list))
        # raise NotImplemented
        # print("*" * 20)
        # [print(i) for i in inventory_list]
        # print("*" * 20)
        return ret_list

    def debug_print(self):
        print("============= Inventory.debug_print() =============")
        print("{} || {}".format(self.character_type, self.player_name))
        self.consumables.debug_print()
        self.weapons.debug_print()
        print("===================================================")

    def save_data(self):
        """
        The only place we will ever want to save is to the player's file.
        Right now we are adjusting the food, drink, weapon, etc., files
        manually. SO all we do
        :return: None
        """
        self.consumables.save_data()
        self.weapons.save_data()

    def __len__(self):
        mylen = len(self.consumables)
        mylen += len(self.weapons)
        return mylen

if __name__ == "__main__":
    myinventory = Inventory(character_type="player", player_name="henry")
    myinventory.read_data()
    # ----
    # myinventory.add_item_by_name("tough jerky", 1)
    # myinventory.remove_item_by_name("dry bread", 199)
    # myinventory.remove_item_by_name("bitter water", 1)
    # myinventory.save_data()
    an_item = myinventory.get_item_by_name("red amulet")
    if an_item is None:
        print("No such item in inventory!")
    else:
        an_item.debug_print()
    # ----
    print("===============")
    myinventory.debug_print()
    # myinventory.remove_item(2, "food")
    # myinventory.debug_print()
    # this_item = myinventory.get_item_by_name("bread")
    # this_item = myinventory.get_item_by_name("rusty sword")
    # this_item.debug_print()
    # myinventory.debug_print()
