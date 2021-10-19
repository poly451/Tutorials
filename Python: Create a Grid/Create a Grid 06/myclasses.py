import random
import pygame
import constants
import utils
from graphics_environment import Environment, Triggers
import os, sys
import time
from graphics_fauna import Player, Npcs
from dialogs import DialogFight, DialogText, DialogPlayerInventory, \
    DialogInput, DialogPlayerInfo, DialogText, DialogGoodbye, \
    DialogUseItemInInventory, DialogShowQuests
from NEW_inventory import Conversation

# -----------------------------------------------------------
#                      class Game
# -----------------------------------------------------------
class Game:
    def __init__(self):
        user_info = utils.get_user_data()
        self.player_name = user_info["character_name"]
        self.zone_name = ""
        self.map_name = ""
        # ----
        self.environment = None
        self.npcs = None
        self.player = None
        self.screen = None
        self.init_pygame()
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True
        self.current_monster = None
        # -------------------------------------
        # self.quest_histories = None

    def read_data(self):
        user_data = utils.get_user_data()
        self.zone_name = user_data["zone_name"]
        self.map_name = user_data["map_name"]
        if self._exception01() == True: self._change01()
        pygame.display.set_caption("Enter {} | ({})".format(constants.TITLE, self.map_name))
        # print(user_data)
        # ----
        self.environment = Environment(self.zone_name, self.map_name)
        self.environment.read_data()
        self.npcs = Npcs(self.zone_name, self.map_name)
        self.npcs.read_data()
        self.player = Player(self.player_name, self.zone_name, self.map_name)
        self.player.read_data()
        # ----
        if self.player.is_dead() == True:
            myresult = self.player.resurrect_player()
            # ----
            if myresult == "y":
                utils.copy_original_player_files(self.player.profession, self.player.name)
                self.player.read_data()
                self.init_pygame()
            elif myresult == "n":
                self.keep_looping = False
            elif len(myresult) == 0:
                # esc was pressed; I'm going to take it that the player wishes to quit.
                self.keep_looping = False
            else:
                raise ValueError("Error!")

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def player_died(self):
        s = "You're dead! Game over."
        mydialog = DialogText(s)
        mydialog.main()
        self.player.image = self.player.image_dead
        self.init_pygame()
        self.keep_looping = False

    def there_is_a_monster_on_this_tile(self, x, y):
        this_monster = self.npcs.get_npc_if_monster(x, y)
        if this_monster is None: return False
        return True

    # def there_is_an_angel_on_this_tile(self, x, y):
    #     raise NotImplemented
    #     this_angel = self.npcs.get_npc_if_angel(x, y)
    #     if this_angel is None: return False
    #     return True

    # def this_npc_is_a_questgiver(self, x, y):
    #     current_npc = self.npcs.get_npc(self.player.x, self.player.y)
    #     if current_npc is None:
    #         s = "Error! There should be an NPC here, but there isn't."
    #         raise ValueError(s)
    #     if current_npc.is_a_questgiver(self.zone_name, self.map_name) == True:
    #         return True
    #     return False

    def there_is_an_npc_on_this_tile(self, x, y):
        this_npc = self.npcs.get_npc(x, y)
        if this_npc is None: return False
        return True

    def there_is_an_action_on_this_tile(self, x, y):
        print("Testing to see whether there is an action on tile x,y: ({},{})".format(x, y))
        this_action = self.environment.actions.get_action(x, y)
        if this_action is None: return False
        return True

    def there_is_a_persistent_object_on_this_tile(self, x, y):
        if len(self.environment.persistents) == 0: return False
        this_persistent = self.environment.persistents.get_persistent_object(x, y)
        if this_persistent is None: return False
        return True

    def debugging_info(self):
        # ---- Debugging (after) (top)----
        mylist = []
        mylist.append("character_name (from player): {}".format(self.player.name))
        mylist.append("x,y: ({},{})".format(self.player.x, self.player.y))
        mylist.append("zone_name: {}".format(self.zone_name))
        mylist.append("map_name: {}".format(self.map_name))
        mylist.append("------------")
        mylist.append("From file:")
        mydict = utils.get_user_data()
        mylist.append("character_name: {}".format(mydict["character_name"]))
        mylist.append("zone_name: {}".format(mydict["zone_name"]))
        mylist.append("map_name: {}".format(mydict["map_name"]))
        mylist.append("------------")
        mylist.append("From Player:")
        mylist.append("x,y: ({},{})".format(self.player.x, self.player.y))
        mylist.append("zone_name: {}".format(self.player.zone_name))
        mylist.append("map_name: {}".format(self.player.map_name))
        print("******************** Debugging (begin) ********************")
        print("-----------------------------------------------------------")
        print(mylist)
        print("---------------------------------------------------------")
        print("******************** Debugging (end) ********************")
        # ---- Debugging (after) (bottom) ----

    def npc_encounter(self):
        # The user wants an encounter with the NPC they clicked on.
        current_npc = self.npcs.get_npc(self.player.x, self.player.y)
        if current_npc is None:
            s = "Error! There should be an NPC here, but there isn't."
            raise ValueError(s)
        print("This is the amount of gold the player has before he has the INTERACTION: {}".format(self.player.gold))
        result, myinventory, player_gold = current_npc.have_interaction(self.environment.events, self.player)
        # ----
        # The following line is executed when the user exists out of an NPC encounter.
        if result is None and myinventory is None: return False
        if result is None or myinventory is None:
            raise ValueError("Error")
        print("This is the amount of gold the player has BEFORE: {}".format(self.player.gold))
        self.player.gold = player_gold
        print("This is the amount of gold the player has AFTER: {}".format(self.player.gold))
        self.player.inventory = myinventory
        # ----
        if result == "end game":
            self.player_died()
        elif result == "load next map":
            self.map_name = utils.get_next_map_name(self.map_name)
            utils.set_user_data(self.player.name, self.zone_name, self.map_name, self.player.profession)
            self.read_data()
        elif result in ["end conversation", "continue", "completed"]:
            # player goes on about their day
            pass
        else:
            s = "I don't understand this: {}".format(result)
            raise ValueError(s)

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                self.save_data()
                return True
            if event.type == pygame.KEYDOWN:
                print("self.player coords: x,y: {},{}: ".format(self.player.x, self.player.y))
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    self.save_data()
                    return True
                if self.player.is_dead() == True: return False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.player.move(dx=-1, dy=0, obstacles=self.environment.obstacles) == True:
                        # self.player.image = self.player.image_left
                        self.player.direction = constants.LEFT
                        self.player.my_update_image()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.player.move(dx=1, obstacles=self.environment.obstacles) == True:
                        self.player.direction = constants.RIGHT
                        self.player.my_update_image()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.player.move(dy=1, obstacles=self.environment.obstacles) == True:
                        self.player.direction = constants.DOWN
                        self.player.my_update_image()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.player.move(dy=-1, obstacles=self.environment.obstacles) == True:
                        self.player.direction = constants.UP
                        self.player.my_update_image()
                # ===============================================
                elif event.key == pygame.K_h:
                    if self.there_is_an_npc_on_this_tile(self.player.x, self.player.y) == True:
                        message, self.player.inventory = self.npcs.do_something(self.player)
                        if message == "load next map":
                            print("current map name: {}".format(self.map_name))
                            self.map_name = utils.get_next_map_name(self.map_name)
                            print("moving to map name: {}".format(self.map_name))
                            self.load_map(zone_name=self.zone_name,
                                          map_name=self.map_name,
                                          dialog_text="")
                    elif self.there_is_an_action_on_this_tile(self.player.x, self.player.y) == True:
                        # After an action is used, the tile is removed.
                        print("There is an action on this tile.")
                        if self.environment.actions.conditions_passed(self.player) == False:
                            return False
                        current_action = self.environment.actions.get_action(self.player.x, self.player.y)
                        self.do_action(current_action)
                        self.environment.actions.remove_tile(self.player.x, self.player.y)
                        self.init_pygame()
                        self.all_sprites = pygame.sprite.Group()
                        return ""
                    elif self.there_is_a_persistent_object_on_this_tile(self.player.x, self.player.y) == True:
                        # After a persistent object is used, it remains.
                        # (I could probably just make 'persistent' and 'temporary' values of a
                        # field for an Actions object rather than make a separate class.)
                        print("This is a persistent object on this tile.")
                        # if self.environment.persistents.conditions_passed(self.player, self.environment.events) == False:
                        #     return False
                        if self.environment.persistents.conditions_passed(self.player) == False:
                            return False
                        persistent_object = self.environment.persistents.get_persistent_object(self.player.x, self.player.y)
                        if persistent_object is None: raise ValueError("Error")
                        self.do_persistent(persistent_object)
                        self.init_pygame()
                        return ""
                # ===============================================
                elif event.key == pygame.K_i: # Inventory
                    if len(self.player.inventory) == 0:
                        raise ValueError("The player has lost their inventory!")
                    mydialog = DialogPlayerInventory(self.player)
                    mydialog.main()
                    self.init_pygame()
                elif event.key == pygame.K_p:
                    mydialog = DialogPlayerInfo(self.player)
                    mydialog.main()
                    self.init_pygame()
                # elif event.key == pygame.K_u:
                #     mydialog = DialogUseItemInInventory(self.player)
                #     mydialog.main()
                #     self.init_pygame()
                elif event.key == pygame.K_q:
                    mydialog = DialogShowQuests()
                    mydialog.read_data()
                    mydialog.main()
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))
                # ------------------------------------------------------
                self.check_for_trigger()

    def check_for_trigger(self):
        if self.environment.triggers is None:
            print("There is no TRIGGER on this tile.")
            return False
        current_trigger = self.environment.triggers.get_trigger(self.player.x, self.player.y)
        if not current_trigger is None:
            self.do_trigger(current_trigger)
        # self.npcs.debug_print()
        # raise NotImplemented

    def show_text(self, current_trigger):
        # print("debugging: in def load_map(self, current_trigger")
        filename = "{}.txt".format(current_trigger.data)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", filename)
        mydict = utils.read_file(filepath)[0]
        for key, value in mydict.items():
            # print(key, value)
            mytextdialog = DialogText(value)
            mytextdialog.main()
        self.init_pygame()

    def fire_attack(self, attack_strength):
        self.player.hit_points -= attack_strength
        if self.player.hit_points <= 0:
            self.player_died()

    def do_trigger(self, current_trigger):
        # print("There is a current trigger")
        # print("current_trigger.command = {}".format(current_trigger.command))
        # current_trigger.debug_print()
        if current_trigger.command == "load_map":
            if current_trigger.conditions_fulfilled(self.zone_name,
                                                    self.map_name,
                                                    self.player.inventory) == False:
                return False
            # ----
            self.save_data()
            # print("************* dkdkkd")
            zone_name, map_name = current_trigger.parse_data()
            self.zone_name = zone_name
            self.map_name = map_name
            utils.set_user_data(self.player.name, self.zone_name, self.map_name, self.player.profession)
            # ----
            self.read_data()
        elif current_trigger.command == "show_text":
            self.show_text(current_trigger)
        elif current_trigger.command == "fire_attack":
            if not utils.is_int(current_trigger.data):
                raise ValueError("Error")
            self.fire_attack(int(current_trigger.data))
        elif current_trigger.command == "fire_attack_big":
            if not utils.is_int(current_trigger.data):
                raise ValueError("Error")
            self.fire_attack(int(current_trigger.data))
        elif current_trigger.command == "change_npc_passive":
            # check to make sure that the name given in data is that of an npc
            # so check the npc_name_lookup.txt file in the zone directory.
            # if this goes through then turn that npc passive.
            if utils.npc_exists_in_zone(npc_name=current_trigger.data,
                                        zone_name=self.zone_name,
                                        map_name=self.map_name) == False:
                s = "Error! That npc ({}) does not exist in this zone ({})."
                s = s.format(current_trigger.data.replace(".txt", ""), self.zone_name)
                raise ValueError(s)
            raise NotImplemented
        elif current_trigger.command == "change_npc_agro":
            # check to make sure that the name given in data is that of an npc
            # so check the npc_name_lookup.txt file in the zone directory.
            # if this goes through then turn that npc agro.
            if utils.npc_exists_in_zone(npc_name=current_trigger.data,
                                        zone_name=self.zone_name,
                                        map_name=self.map_name) == False:
                s = "Error! That npc ({}) does not exist in this zone ({}).".format(current_trigger.data, self.zone_name)
                raise ValueError(s)
            the_npc = self.npcs.get_npc_by_name(current_trigger.data)
            if the_npc is None:
                s = "This name ({}) is not the name of a current npc.".format(current_trigger.data.replace(" ", "_"))
                print(s)
                return False
                # raise ValueError(s)
            the_npc.agro_level = "agro"
        else:
            current_trigger.debug_print()
            s = "I couldn't find that: {}".format(current_trigger.command)
            raise ValueError(s)
        return True

    def load_map(self, zone_name, map_name, dialog_text=""):
        """This loads both a zone and a map."""
        if not zone_name in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(zone_name)
            raise ValueError(s)
        if not map_name in constants.MAP_CHOICES: raise ValueError("Error")
        # ----
        if len(dialog_text) > 0:
            mydialog = DialogText(dialog_text)
            mydialog.main()
        # ----
        self.player.save_data()
        self.npcs.save_data()
        # ----
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        if self._exception01() == True: self._change01()
        # ----
        utils.set_user_data(self.player.name, self.zone_name,
                            self.map_name, self.player.profession)
        # ----
        self.read_data()

    def do_action(self, current_action):
        if current_action.command == "load_map":
            """This loads both a zone and a map."""
            # mydialog = TextDialog(current_action.dialog_text)
            mydialog = DialogText(current_action.dialog_text)
            mydialog.main()
            # ----
            self.player.save_data()
            self.npcs.save_data()
            # ----
            mydict = current_action.parse_data()
            self.zone_name = mydict["zone_name"]
            self.map_name = mydict["map_name"]
            utils.set_user_data(self.player.name, self.zone_name,
                                self.map_name, self.player.profession)
            # ----
            self.read_data()
        elif current_action.command == "find_item":
            mydialog = DialogText(current_action.display_text())
            mydialog.main()
            print("--------------- (begin)")
            print("debugging: in def show_text(self, current_action")
            self.player.inventory.add_item_by_name(current_action.data, 1)
            self.player.inventory.debug_print()
            print("--------------- (end)")
        else:
            s = "Error! I don't recognize this command: {}".format(current_action.command)
            raise ValueError(s)

    def do_persistent(self, current_persistent):
        if current_persistent.command == "load_map":
            """This loads both a zone and a map."""
            mydialog = DialogText(current_persistent.dialog_text)
            mydialog.main()
            # ----
            self.player.save_data()
            self.npcs.save_data()
            # ----
            self.zone_name, self.map_name = current_persistent.parse_data()
            if self._exception01() == True: self._change01()
            utils.set_user_data(self.player.name, self.zone_name,
                                self.map_name, self.player.profession)
            # ----
            self.read_data()
        elif current_persistent.command == "find_item":
            mydialog = DialogText(current_persistent.dialog_text)
            mydialog.main()
            print("--------------- (begin)")
            print("debugging: in def show_text(self, current_action")
            self.player.inventory.add_item_by_name(current_persistent.data, 1)
            self.player.inventory.debug_print()
            print("--------------- (end)")
        elif current_persistent.command == "find_item_and_change_image":
            filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", "images_to_load.txt")
            mylist = utils.read_data_file(filepath, 4)
            img_02 = ""
            for mydict in mylist:
                if mydict["kind_of_object"] == "persistent" and mydict["name_of_object"] == current_persistent.name:
                    img_02 = mydict["image02"]
            current_persistent.load_different_image(img_02)
            # ----
            mydialog = DialogText(current_persistent.dialog_text)
            mydialog.main()
            self.player.inventory.add_item_by_name(current_persistent.data, 1)
            self.player.inventory.debug_print()
        elif current_persistent.command == "display_image":
            # The image is already being displayed, so we don't need to do anything.
            pass
        else:
            s = "Error! I don't recognize this command: {}".format(current_persistent.command)
            raise ValueError(s)

    # --------------------------------------------------------

    def update_classes(self):
        self.all_sprites = self.environment.update_classes(self.all_sprites)
        self.all_sprites = self.npcs.update_classes(self.all_sprites)
        # print("in def update_classes: type: {}".format(type(self.player.image)))
        self.all_sprites.add(self.player)

    def draw(self):
        # ---- ----
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        # print("in def draw: ", type(self.player.image))
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    # -------------------------------------

    def update(self):
        if self.player.is_dead() == True: return False
        counter = 0
        for an_npc in self.npcs:
            counter += 1
            if an_npc.is_dead() == False:
                # time.sleep(0.4)
                print("this an_npc: {} ({})".format(an_npc, counter))
                command, inventory = an_npc.default_action(player=self.player, obstacles=self.environment.obstacles)
                print("command: {}, inventory: {}".format(command, inventory))
                if not inventory is None:
                    self.player.inventory = inventory
        # --------------------

    def main(self):
        mycounter = 0
        pygame.display.set_caption("Enter {} | ({})".format(constants.TITLE, self.map_name))
        while self.keep_looping:
            self.clock.tick(5)
            self.handle_events()
            self.update()
            self.draw()
            # print("zone_name: {}, map_name: {}".format(self.zone_name, self.map_name))
        self.goodbye()
        self.save_data()
        self.myquit()

    def save_data(self):
        self.player.save_data()
        self.npcs.save_data()
        # self.environment.events.save_data()

    def myquit(self):
        pygame.quit()
        # sys.exit()

    def goodbye(self):
        # mylist = []
        # mylist.append("Thank you for playing")
        # mylist.append("{}".format(constants.TITLE))
        # mydialog = DialogText(mylist)
        # mydialog.main()
        mydialog = DialogGoodbye()
        mydialog.main()
        self.keep_looping = False

    def _exception01(self):
        # print("self.zone_name: {}".format(self.zone_name))
        # print("self.map_name: {}".format(self.map_name))
        # raise NotImplemented
        if self.zone_name != "bridge": return False
        if self.map_name != "map00": return False
        if self.player is None: return False
        if self.player.inventory is None: return False
        my_coin = self.player.inventory.get_item_by_name("gold coin")
        if my_coin.units < 100: return False
        # ----
        from NEW_inventory import SearchMasterQuests
        myobject = SearchMasterQuests()
        myquest = myobject.get_quest_by_quest_name("buy a secret")
        if myquest.quest_accepted == False: return False
        return True

    def _change01(self):
        self.map_name = "map01"


# **************************************************
# **************************************************

# def _talk(player_name, npc, zone_name, map_name, player_gold):
#     # We need to figure out whether this will be (1) a quest conversation
#     # or (2) a simple conversation/buying selling conversation.
#     # ----
#     # Is this a quest?
#     # Discover whether there is a file name_quest.txt in the texts directory.
#     # If there is, then we will call Quest()
#     filename1 = "{}_quest.txt".format(npc.name)
#     filepath1 = os.path.join("data", "zones", zone_name, map_name, "texts", filename1)
#     filename2 = "{}.txt".format(npc.name)
#     filepath2 = os.path.join("data", "zones", zone_name, map_name, "texts", filename2)
#     mydialog = None
#     if utils.is_file(filepath1) == True:
#         mydialog = Quest(player_name, npc.name, zone_name, map_name, player_gold)
#         mydialog.read_data()
#     elif utils.is_file(filepath2) == True:
#         mydialog = Conversation(player_name, npc.name, zone_name, map_name, player_gold)
#         mydialog.read_data()
#     else:
#         s = "Neither\n{}\nnor\n{}\nworked".format(filepath1, filepath2)
#         raise ValueError(s)
#     # ----
#     # s
#     npc.save_data()
#     message, player_inventory, player_gold2 = mydialog.main()
#     # reload NPC
#     # ----
#     if not message in constants.CONVERSATION_ENDINGS + constants.QUEST_ENDINGS:
#             raise ValueError("Error")

# def debug_talk():
#     # mynpcs = Npcs(zone_name="bridge", map_name="map00")
#     # westley = mynpcs.debug_load_NPC(player_name="henry", npc_name="Westley", x=1, y=1)
#     _talk(player_name="henry", npc_name="westley", zone_name="bridge", map_name="map01", player_gold=20)

if __name__ == "__main__":
    pass
    # debug_talk()
    # utils.set_user_data("henry", "testing", "map01")
    # # ----
    # mydriver = DebugDriver()
    # mydriver.read_data()
    # mydriver.main()