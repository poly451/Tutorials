import os, sys
import constants as con
from constants import p
import utils
from myclasses_other import Items, NpcItems, Tiles
from class_quests import Quests

# ------------------------------------------------
#                  class NPC
# ------------------------------------------------

class Npc:
    def __init__(self, mydict):
        if p: print("Npc.__init__:", mydict)
        self.name = mydict["name"].lower().strip()
        self.position = mydict["position"].lower().strip()
        self.kind = mydict["kind"].lower().strip()
        self.species = mydict["species"].lower().strip()
        # ----
        self.initial_greeting = mydict["initial_greeting"].strip()
        self.greeting = mydict["greeting"].strip()
        self.farewell = mydict["farewell"].strip()
        # ----
        self.items = Items()
        if mydict["items"] == "none":
            self.items = None
        else:
            mylist = utils.string_to_list(mydict["items"])
            self.items.load_items(mylist)
        # ----
        self.quests = Quests()
        if mydict["quests"] == "none":
            self.quests = None
        else:
            mylist = utils.string_to_list(mydict["quests"])
            self.quests.load_quests(mylist)
        # ----

    def _buy_menu_valid_input(self, user_input):
        if user_input == "quit": return True
        if len(user_input) == 0: return False
        if utils.is_int(user_input):
            return True
        else:
            return False

    # def _quest_menu_helper(self, player):
    #     def valid_input(mystring):
    #         if mystring == "quit": return True
    #         if len(user_input) == 0: return False
    #         if utils.is_int(user_input):
    #             return True
    #         else:
    #             return False
    #     print("Which quest would you like to undertake?")
    #     print("- " * 20, "Here are the quests you are current on:", "- " * 20)
    #     player.quests_current.debug_print()
    #     print("- " * 20, "end", "- " * 20)
    #     self.quests.debug_print()
    #     print("*" * 20)
    #     # validate input
    #     user_input = ""
    #     while not valid_input(user_input):
    #         user_input = input("buy > ").lower().strip()
    #         if user_input == "quit": return True
    #         print("You entered: {}".format(user_input))
    #     users_choice = int(user_input)
    #     chosen_item = self.items.get_item(users_choice)
    #     print("Here is the item:")
    #     chosen_item.debug_print()
    #     # ---- check to make sure player has enough money. ----
    #     if (player.gold - chosen_item.cost) <= 0:
    #         print("Doh! You don't have enough gold to buy that. :-(")
    #         return False
    #     # ---- add and remove item ----
    #     addition_successful = player.items.add_item(chosen_item)
    #     if not addition_successful:
    #         print("Doh! You already have that item in your inventory.")
    #     # self.items.remove_item(chosen_item)
    #     # ---- end ----
    #     print("gold: {}, chosen_item.cost: {}".format(type(player.gold), type(chosen_item.cost)))
    #     gold_before = player.gold
    #     player.gold -= chosen_item.cost
    #     print("You have bought: {}".format(chosen_item.name))
    #     print("You had {} of gold. Now you have {} of gold.".format(gold_before, player.display_gold()))
    #     return True
    #
    # def _quest_menu(self, player):
    #     print("This is the quest menu")
    #     shop = True
    #     while shop:
    #         was_successful = self._quest_menu_helper(player)
    #         if not was_successful:
    #             shop = False
    #             continue
    #         print("Would you like to buy something else? (y/n)")
    #         user_response = input("> ").lower().strip()
    #         while not user_response in ["quit", "y", "n", "no", "yes"]:
    #             user_response = input("> ").lower().strip()
    #         if user_response == "quit": shop = False
    #         if user_response == "n" or user_response == "no": shop = False
    #     # print("Thank you for shopping!")

    def _buy_menu_helper(self, player):
        # print(input("<Enter>"))
        print("What would you like to buy?")
        print("- " * 20, "Here is your inventory:", "- " * 20)
        print(player.items.display_screen_line())
        print("- " * 20, "Items for sale:", "- " * 20)
        print(self.items.display_screen_line())
        print("*" * 20)
        print("Your gold: {}".format(player.gold))
        print("*" * 20)
        print(" ")
        user_input = ""
        while not self._buy_menu_valid_input(user_input):
            user_input = input("buy > ").lower().strip()
            if user_input == "quit": return True
            # print("You entered: {}".format(user_input))
        users_choice = int(user_input)
        chosen_item = self.items.get_item(users_choice)
        # print("This is what {} as to sell:".format(self.name.upper()))
        # chosen_item.debug_print()
        # ---- check to make sure player has enough money. ----
        if (player.gold - chosen_item.cost) <= 0:
            print("Doh! You don't have enough gold to buy that. :-(")
            print("You have {} gold. This item costs {} of gold.".format(player.display_gold(), chosen_item.display_gold()))
            return False
        # ---- add and remove item ----
        addition_successful = player.items.add_item(chosen_item)
        if not addition_successful:
            print("Doh! You already have that item in your inventory.")
            return False
        # ---- end ----
        # print("gold: {}, chosen_item.cost: {}".format(type(player.gold), type(chosen_item.cost)))
        gold_before = player.gold
        player.gold -= chosen_item.cost
        print("You have bought: {}".format(chosen_item.name))
        print("You had {} of gold. Now you have {} of gold.".format(gold_before, player.display_gold()))
        return True

    def _buy_menu(self, player):
        print("This is the buy menu")
        shop = True
        while shop:
            was_successful = self._buy_menu_helper(player)
            if not was_successful:
                shop = False
                continue
            print("Would you like to buy something else? (y/n)")
            user_response = input("> ").lower().strip()
            while not user_response in ["quit", "y", "n", "no", "yes"]:
                user_response = input("> ").lower().strip()
            if user_response == "quit": shop = False
            if user_response == "n" or user_response == "no": shop = False
        # print("Thank you for shopping!")

    def _sell_menu_helper(self, player):
        print("What would you like to sell?")
        print(player.items.display_screen_line())
        # print("*" * 20)
        # validate input
        user_input = ""
        while not utils.is_int(user_input):
            user_input = input("sell > ").lower().strip()
            if user_input == "quit": return True
            print("You entered: {}".format(user_input))
        users_choice = int(user_input)
        if not player.items.item_exists(users_choice):
            print("Doh! It looks like you don't have that item in your inventory.")
            return False
        chosen_item = player.items.get_item(users_choice)
        print("Here is the item you want to sell:")
        print("- " * 20)
        print(chosen_item.display_screen_line())
        print("- " * 20)
        # ---- Remove item from self.items ----
        player.items.remove_item(chosen_item.id)
        print("You have sold the item!")
        # self.items.add_item(chosen_item.id)
        # ---- end ----
        print("You had {} of gold.".format(player.display_gold()))
        player.gold += chosen_item.cost
        print("You have {} of gold.".format(player.display_gold()))

    def _sell_menu(self, player):
        print("This is the sell menu")
        shop = True
        while shop:
            if len(player.items) == 0:
                print("Doh! You don't have anything to sell!!!")
                shop = False
                continue
            self._sell_menu_helper(player)
            print("Would you like to sell something else? (y/n)")
            user_response = input("> ").lower().strip()
            if user_response == "n" or user_response == "no":
                shop = False
        # print("Thank you for shopping!")

    # ----------------------------------------------------

    # def _main_loop_helper(self, player, choices):
    #     def is_valid(user_input):
    #         if len(user_input) == 0: return False
    #         if not utils.is_int(user_input): return False
    #         user_input = int(user_input)
    #         if not user_input in range(1, len(choices)+1): return False
    #         return True
    #     user_input = ""
    #     while not is_valid(user_input):
    #         user_input = input("{} > ".format(self.name))
    #         if user_input == "quit": return False
    #     user_choice = choices[int(user_input) - 1]
    #     if user_choice == "Buy something":
    #         self._buy_menu(player)
    #     elif user_choice == "Sell something":
    #         self._sell_menu(player)
    #     elif user_choice == "Quests":
    #         self.quests.main_loop(player)
    #     elif user_choice == "Show items":
    #         self.items.debug_print()
    #     elif user_choice == "Show {}'s quests".format(self.name):
    #         self.quests.debug_print()
    #         input("<Enter>")
    #         utils.clear_screen()
    #     elif user_choice == "Quit":
    #         return False
    #     else:
    #         s = "Doh! I don't know what to do this this: "
    #         s += "user_choice: {}".format(user_choice)
    #         raise ValueError(s)
    #     return True

    def _buy_item(self, player):
        self._buy_menu_helper(player)

    def _sell_item(self, player):
        if len(player.items) == 0:
            print("You don't have anything to sell!")
            return False
        self._sell_menu_helper(player)

    # def _accept_quest_helper(self, player):
    #     pass

    def _accept_quest(self, player):
        def is_valid(mystring):
            if len(mystring) == 0: return False
            if not utils.is_int(mystring): return False
            quest_indexes = self.quests._get_indexes()
            if not int(mystring) in quest_indexes: return False
            return True
        # ------------------------------------
        s = "{} the {}: Here are the quests you have completed."
        s = s.format(player.player_name, player.player_kind)
        print(s)
        print(player.quests_completed.display_screen_line())
        print("- " * 20)
        # ----
        print(" ")
        s = "{} the {}: Here are the quests you are on."
        s = s.format(player.player_name, player.player_kind)
        print(s)
        print(player.quests_current.display_screen_line())
        print("- " * 20)
        # ----
        print(" ")
        print("*" * 40)
        print("{}: Here are the quests I have:".format(self.name))
        print(self.quests.display_screen_line())
        print("- " * 20)
        print(" ")
        print("Which quest would you like to accept?")
        user_response = ""
        while not is_valid(user_response):
            user_response = input("> ").lower().strip()
            if user_response == "quit": return False
        user_choice = int(user_response)
        # ----
        # Check to make sure that the chosen quest is
        # is not in player.current_quests
        if player.quests_current.have_quest(user_choice):
            print("No! You can't accept that quest since you are already on it.")
            return False
        # Check to make sure that the chosen quest is
        # is not in player.completed_quests
        if player.quests_completed.have_quest(user_choice):
            print("No! You can't accept that quest since you have already completed it.")
            return False
        # ----
        chosen_quest = self.quests._get_quest(user_choice)
        print("You chose:")
        print(chosen_quest.display_screen_line())
        player.quests_current.add_quest(user_choice)
        print("")

    def _turn_in_quest(self, player):
        def is_valid(mystring):
            if len(mystring) == 0: return False
            if not utils.is_int(mystring): return False
            quest_indexes = player.quests_current._get_indexes()
            if not int(mystring) in quest_indexes: return False
            return True
        # ------------------------------------
        if len(player.quests_current) == 0:
            print("Doh! Sorry, but you do not have any quests.")
            print("Therefore you do not have any quests to turn in.")
            return False
        # ----
        s = "{} the {}: Here are the quests you are on."
        s = s.format(player.player_name, player.player_kind)
        print(s)
        # ----
        print(player.quests_current.display_screen_line())
        print("- " * 20)
        print(" ")
        print("Which quest would you like to turn in?")
        user_response = ""
        while not is_valid(user_response):
            user_response = input("> ").lower().strip()
            if user_response == "quit": return False
        user_choice = int(user_response)
        # ----
        # Check to make sure that the chosen quest is
        # one that this npc can accept.
        if not self.quests.have_quest(user_choice):
            print("No! You can't turn that quest in here.")
            print("I can only accept a quest I also offer.")
            return False
        # ----
        this_quest = player.quests_current._get_quest(user_choice)
        print("You earn {} experience points.".format(this_quest.experience_points))
        print("You receive the following reward: ", this_quest.reward)
        player.quests_completed.add_quest(user_choice)
        player.quests_current.remove_quest(user_choice)
        input("<Enter>")

    def _show_item_menu_helper(self, player):
        def is_valid(mystring):
            if len(mystring) == 0: return False
            if not utils.is_int(mystring): return False
            if not int(mystring) in range(1, len(choices) + 1):
                return False
            return True
        # ----------------------------------------------
        # utils.clear_screen()
        npc_string = "Show {}'s items".format(self.name)
        char_string = "Show {}'s items".format(player.player_name)
        choices = [npc_string, char_string, "Buy item", "Sell item", "Quit"]
        print("\nWould you like to:")
        for count, elem in enumerate(choices):
            print("{}) {}".format(count + 1, elem))
        print(" ")
        # ----
        user_response = ""
        while not is_valid(user_response):
            user_response = input("> ").lower().strip()
            if user_response == "quit": return False
        user_choice = choices[int(user_response) - 1]
        print(" ")
        print("You chose: ", user_choice)
        if user_choice == npc_string:
            print(self.items.display_screen_line())
        elif user_choice == char_string:
            print(player.items.display_screen_line())
        elif user_choice == "Buy item":
            self._buy_item(player)
        elif user_choice == "Sell item":
            self._sell_item(player)
        elif user_choice == "Quit":
            return False
        else:
            raise ValueError("Error! {} not found.".format(user_choice))
        # print(input("<Enter>"))
        return True

    def _show_quest_menu_helper(self, player):
        def is_valid(mystring):
            if len(mystring) == 0: return False
            if not utils.is_int(mystring): return False
            if not int(mystring) in range(1, len(choices) + 1):
                return False
            return True
        # ----------------------------------------------
        npc_string = "Show {}'s quests".format(self.name)
        char_string = "Show {}'s quests".format(player.player_name)
        choices = [npc_string, char_string, "Accept a quest", "Turn in quest", "Quit"]
        print(" ")
        print("Would you like to:")
        print(" ")
        for count, elem in enumerate(choices):
            print("{}) {}".format(count + 1, elem))
        print(" ")
        user_response = ""
        while not is_valid(user_response):
            user_response = input("> ").lower().strip()
            if user_response == "quit": return False
        user_choice = choices[int(user_response)-1]
        if user_choice == npc_string:
            print("{}'s quests:".format(self.name))
            print(self.quests.display_screen_line())
        elif user_choice == char_string:
            print("{} the {}'s quests:".format(player.player_name, player.player_kind))
            print(player.quests_current.display_screen_line())
        elif user_choice == "Accept a quest":
            print("Accept a quest")
            self._accept_quest(player)
        elif user_choice == "Turn in quest":
            print("Turn in quest")
            self._turn_in_quest(player)
        elif user_choice == "Quit":
            return False
        else:
            raise ValueError("Error! Not found: {}".format(user_choice))
        # print(input("<Enter>"))
        return True

    def _show_quest_menu(self, player):
        keep_looping = True
        while keep_looping:
            keep_looping = self._show_quest_menu_helper(player)

    def _show_item_menu(self, player):
        keep_looping = True
        while keep_looping:
            keep_looping = self._show_item_menu_helper(player)
            input("<Enter>")

    def main_loop_helper(self, player):
        utils.clear_screen()
        choices = ["items", "Quests", "Quit"]
        print(self.initial_greeting)
        keep_looping = True
        while keep_looping:
            print("1. Items")
            print("2. Quests")
            print("3. Quit")
            print(" ")
            user_response = ""
            while not user_response in ["1", "2", "3"]:
                user_response = input("> ").lower().strip()
                if user_response == "quit": return False
            user_choice = int(user_response)
            if user_choice == 1:  # Items
                self._show_item_menu(player)
            elif user_choice == 2:  # Quests
                self._show_quest_menu(player)
            elif user_choice == 3:  # Quit
                return False
            else:
                raise ValueError("Error! Not found: ", user_response)
        print(input("<Enter>"))

    def main_loop(self, player):
        keep_looping = True
        while keep_looping:
            keep_looping = self.main_loop_helper(player)
        print(self.farewell)

    def display_line(self):
        s = ""
        s += "name: {} | ".format(self.name)
        s += "position: {} | ".format(self.position)
        s += "kind: {} | ".format(self.kind)
        s += "species: {} | ".format(self.species)
        s += "initial_greeting: {} | ".format(self.initial_greeting)
        s += "greeting: {} |\n".format(self.greeting)
        s += "items:\n{}".format(self.items.print_string())
        s += "quests:\n{}".format(self.quests)
        s += "\n{}".format("-" * 40)
        return s

    def debug_print(self):
        s = "{} debug_print() {}\n".format("-" * 20, "-" * 20)
        s += "name: {} | ".format(self.name)
        s += "position: {} | ".format(self.position)
        s += "kind: {} | ".format(self.kind)
        s += "species: {} | ".format(self.species)
        s += "initial_greeting: {} | ".format(self.initial_greeting)
        s += "greeting: {} |\n".format(self.greeting)
        s += "items:\n{}".format(self.items.print_string())
        s += "quests:\n{}".format(self.quests)
        s += "\n{}".format("-" * 40)
        print(s)

# ------------------------------------------------
#                  class NPCs
# ------------------------------------------------
class Npcs:
    def __init__(self):
        self.inner = []
        # ---------------
        char_name, char_kind = utils.get_char_info()
        char_dir = "{}_{}".format(char_name, char_kind)
        filepath = os.path.join("data", "player_files", char_dir, "NPCs", "npcs.txt")
        if p: print("filepath: ", filepath)
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        for i in range(0, len(mylines), 9):
            mydict = {}
            for j in range(9):
                elem = mylines[i + j]
                # print("elem:", elem)
                mydict = utils.key_value_pair(elem, mydict)
            new_npc = Npc(mydict)
            self.inner.append(new_npc)

    def get_npc(self, npc_name, npc_kind=""):
        if len(npc_kind) == 0 and len(npc_name) > 0:
            for npc in self.inner:
                if npc.name == npc_name:
                    return npc
        else:
            raise NotImplemented
        raise ValueError("Error! Name not found:", npc_name)

    def display_print(self):
        s = ""
        if len(self.inner) == 0:
            raise ValueError("Error! self.inner is empty")
        for elem in self.inner:
            s += "{}\n".format(elem.display_line())
        print(s)
# ------------------------------------------------
#                  class Player
# ------------------------------------------------

class Player:
    def __init__(self, tiles, zone_name):
        char_name, char_kind = utils.get_char_info()
        self.player_name = char_name
        self.player_kind = char_kind
        self.zone_name = zone_name
        # -------------------------------------
        char_dir = "{}_{}".format(char_name, char_kind)
        filename = "{}.txt".format(char_kind)
        filepath = os.path.join("data", "player_files", char_dir, filename)
        if p: print("Player.__init__: reading from filepath:", filepath)
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        mydict = {}
        for elem in mylines:
            mydict = utils.key_value_pair(elem, mydict)
        # -------------------------------------
        self.max_hp = int(mydict["max_hp"])
        self.max_mp =  int(mydict["max_hp"])
        self.level = int(mydict["max_hp"])
        self.experience_points = int(mydict["experience_points"])
        # -------------------------------------
        self.gold = int(mydict["gold"])
        self.weapon = mydict["weapon"] # We'll flesh this out down the road
        self.status_effects = None # We'll flesh this out down the road
        self.explored_locations = [] # We'll flesh this out down the road
        self.has_killed = bool(mydict["has_killed"]) # We'll flesh this out down the road
        # -------------------------------------
        self.tiles = tiles
        self.current_tile = self.tiles.get_tile(mydict["current_tile_index"])
        # -------------------------------------
        self.items = Items()
        item_list = utils.string_to_list(mydict["items"])
        self.items.load_items(item_list)
        # -------------------------------------
        self.quests_current = Quests()
        quests_list = utils.string_to_list(mydict["quests_current"])
        self.quests_current.load_quests(quests_list)
        # ----
        self.quests_completed = Quests()
        quests_list = utils.string_to_list(mydict["quests_completed"])
        self.quests_completed.load_quests(quests_list)
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

    def complete_quest(self, quest_index):
        if not self.quests_current.have_quest(quest_index):
            s = "Error! You don't have a quest with this index ({})"
            s += "as a current quest."
            s = s.format(quest_index)
            raise ValueError(s)
        self.quests_current.remove_quest(quest_index)
        self.quests_completed.add_quest(quest_index)
    # ---------------------------------------------------------

    def display_gold(self):
        if self.gold == 0: return "0 pieces"
        elif self.gold == 1: return "1 piece"
        elif self.gold > 1: return "{} pieces".format(self.gold)

    def display_line(self):
        s = "player_name: {} | ".format(self.player_name)
        s += "player_kind: {} | ".format(self.player_kind)
        s += "zone_name: {} | ".format(self.zone_name)
        # -------------------------------------
        s += "max_hp: {} | ".format(self.max_hp)
        s += "max_mp: {} | ".format(self.max_mp)
        # -------------------------------------
        s += "gold: {} | ".format(self.gold)
        s += "weapon: {} | ".format(self.weapon)
        s += "items: {} | ".format(self.items.debug_print())
        s += "status_effects: {} | ".format(self.status_effects)
        s += "explored_locations: {} | ".format(self.explored_locations)
        s += "has_killed: {} | ".format(self.has_killed)
        # -------------------------------------
        s += "tiles: {} | ".format(self.tiles)
        # s += "current_tile_name: {}".format(self.current_tile_name)
        return s

    def debug_print(self):
        # t = "---- Meet {} the {} ----".format(self.player_name, player_kind)
        # print(t)
        s = "player_name: {}\n".format(self.player_name)
        s += "player_kind: {}\n".format(self.player_kind)
        s += "zone_name: {}\n".format(self.zone_name)
        # -------------------------------------
        s += "max_hp: {}\n".format(self.max_hp)
        s += "max_mp: {}\n".format(self.max_mp)
        # -------------------------------------
        s += "gold: {}\n".format(self.gold)
        s += "weapon: {}\n".format(self.weapon)
        s += "status_effects: {}\n".format(self.status_effects)
        s += "explored_locations: {}\n".format(self.explored_locations)
        s += "has_killed: {}\n".format(self.has_killed)
        # -------------------------------------
        s += "current_tile: {}".format(self.current_tile.display_line())
        print(s)
        # -------------------------------------
        s += "items:\n{}\n".format(self.items.display_line().strip())
        # -------------------------------------
        s += "quests_current:\n{}\n".format(self.quests_current.display_line())
        s += "quests_completed:\n{}\n".format(self.quests_completed.display_line())
        print(s)

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
        self.rpgs = Npcs()
        self.tiles = Tiles(self.zone_name, self.rpgs)
        # -----------------------------
        self.player = Player(self.tiles, self.zone_name)
        # self.player.tiles = self.tiles
        # self.player.current_tile = self.tiles.get_tile("a1")
        self.play_game = True
        # self.player.current_tile.display_print()

    # ---------------------------------------------------------

    def _check_syntax(self, command, myobject):
        if command == "enter":
            if myobject not in con.GAME_ZONES:
                return False
        return True

    def valid_command(self):
        command, myobject = "", ""
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
                    return action, myobject
            else:
                command = action[:mybreak]
                myobject = action[mybreak:].strip()
                if not command in con.ALL_COMMANDS:
                    print("bebugging: That is not a valid command: {}".format(command))
                    valid_command = False
                    continue
                if not myobject in con.OBJECTS:
                    print("bebugging: That is not a valid object: {}".format(myobject))
                    valid_command = False
                    continue
            valid_command = self._check_syntax(command, myobject)
        return command, myobject

    # ---------------------------------------------------------

    def _enter_zone(self, zone):
        if zone == "town":
            if self.zone_name != "world":
                print("Sorry! You can't enter a town if you're not in the 'world' zone.")
                return False
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
            self.tiles.load_tile_zone(self.rpgs)
            self.current_tile = self.tiles.get_tile(tile_name)
            self.player.current_tile = self.current_tile
            utils.clear_screen()
        elif zone == "world":
            # travelling from the town zone into the world zone
            if self.zone_name != "town":
                print("Sorry! You can't enter the world if you're not in the 'town' zone.")
                return False
            elif self.player.current_tile.index != "a1":
                s = "World? You want to go into the world? I don't see an exit around here, do you?!"
                s += "Debugging: You're standing on tile: {}".format(self.player.current_tile.tile_name)
            tile_name = "a4"
            self.zone_name = zone
            self.tiles.zone_name = self.zone_name
            self.tiles.load_tile_zone(self.rpgs)
            self.current_tile = self.tiles.get_tile(tile_name)
            print("This is the tile name: ", self.current_tile.index)
            self.player.current_tile = self.current_tile
            utils.clear_screen()
        else:
            s = "Sorry, I don't recognize this: {}".format(zone)
            raise ValueError(s)
        return True

    # ---------------------------------------------------------

    def _talk_NPC(self, npc_name):
        if npc_name == "provisioner":
            merchant_npc = self.player.current_tile.npc
            merchant_npc.main_loop(self.player)
        else:
            s = "Sorry, I don't recognize this: {}".format(npc_name)
            raise ValueError(s)

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
            command, myobject = self.valid_command()
            print("command: {}, object: {}".format(command, myobject))
            if command == "quit":
                print("You want to QUIT. Setting play_game to False.")
                self.play_game = False
                return False
            elif command == "walk":
                self.player.move(myobject)
            elif command == "enter":
                self._enter_zone(myobject)
            elif command == "talk":
                self._talk_NPC(myobject)
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

    # def move_player_between_zones(self, new_zone, npc_name = "", npc_kind = ""):
    #     """
    #     I'm not currently using this.
    #     :param new_zone: "world", "town" or "dungeon"
    #     :param npc_name: between 2 and 20 characters.
    #     :param npc_kind: "warrior" or "mage"
    #     :return:
    #     """
    #     while not new_zone in con.TILE_TYPES:
    #         print("I don't recognize this zone name: {}".format(new_zone))
    #         print("Here are the names I recognize: {}".format(con.TILE_TYPES))
    #         new_zone = input("> ").lower().strip()
    #         if new_zone == "quit" or new_zone == "exit":
    #             print("Goodbye! :-)")
    #             sys.exit()
    #     # self.player.save()
    #     self.zone_name = new_zone
    #     self.tiles.zone_name = new_zone
    #     self.tiles.load_tile_zone(self.zone_name)
    #     if len(self.tiles) == 0:
    #         raise ValueError("There are no tiles!")
    #     self.player.current_tile = self.tiles.get_tile("a1")
    #     if new_zone == "provisioner":
    #         if len(npc_name) == 0 or len(npc_kind) == 0:
    #             s = "This isn't going to work, I need to know the NPCs name and kind.\n"
    #             s += "name: {}, kind: {}".format(npc_name, npc_kind)
    #             raise ValueError(s)
    #         if not npc_name in ["anna", "cultist", "innkeeper", "king", "monster", "provisioner"]:
    #             raise ValueError("That npc_name ... I don't recognize it: {}".format(npc_name))
    #         if not npc_kind in ["server", "ruler", "server", "grass"]:
    #             raise ValueError("I don't recognize that npc_kind: {}".format(npc_kind))
    #         # items = Items(self.player.name, self.player.kind)
    #         self.NPC = NPC(self.player, npc_name, npc_kind)
    #         self.NPC.load()
    #         continue_loop = True
    #         while continue_loop:
    #             continue_loop = self.NPC.dialogue()

# ================================================
# ================================================

if __name__ == "__main__":
    mynpcs = Npcs()
    marty = mynpcs.get_npc("marty")
    # marty.debug_print()
    zone_name = "town"
    mytiles = Tiles(zone_name, mynpcs)
    # mytiles.display_print()
    myplayer = Player(mytiles, zone_name)
    marty.main_loop(myplayer)
