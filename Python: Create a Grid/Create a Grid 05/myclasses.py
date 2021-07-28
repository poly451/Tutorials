import pygame
import constants
import utils
from graphics_environment import Environment, Triggers
import os, sys
import time
from graphics_fauna import Player, Npcs
from dialogs import DialogFight, TextDialog, DialogPlayerInventory, DialogInput

# -----------------------------------------------------------
#                      class Game
# -----------------------------------------------------------
class Game:
    def __init__(self, player_name):
        self.player_name = player_name
        self.zone_name = ""
        self.map_name = ""
        # ----
        self.environment = None
        self.npcs = None
        self.player = None
        self.init_pygame()
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True
        self.current_monster = None
        # -------------------------------------

    def read_data(self):
        user_data = utils.get_user_data()
        self.zone_name = user_data["zone_name"]
        self.map_name = user_data["map_name"]
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

    def player_died(self):
        s = "You're dead! Game over."
        mydialog = TextDialog(s)
        mydialog.main()
        self.player.image = self.player.image_dead
        self.init_pygame()
        self.keep_looping = False

    # def restart_game(self):
    #     raise NotImplemented
    #     player_x = self.player.x
    #     player_y = self.player.y
    #     # ----
    #     self.all_sprites = pygame.sprite.Group()
    #     self.init_pygame()
    #     self.keep_looping = True
    #     # ----
    #     print("In Game.restart_game(self)")
    #     print("-- in beginning --")
    #     print("zone_name: {}".format(self.zone_name))
    #     print("map_zone: {}".format(self.map_name))
    #     self.environment = Environment(self.zone_name, self.map_name)
    #     self.npcs = Npcs(self.zone_name, self.map_name)
    #     self.player = Player(self.zone_name, self.map_name)
    #     self.fight = False
    #     # ----
    #     # self.player.read_data_restart(player_x, player_y)
    #     self.environment.read_data()
    #     self.npcs.read_data()
    #     # print("&&&&&&& player_x, player_y: {},{}".format(player_x, player_y))
    #     self.player.read_data_restart()
    #     print("-- at end --")
    #     print("zone_name: {}".format(self.zone_name))
    #     print("map_zone: {}".format(self.map_name))
    #     print("player coords: {},{}".format(self.player.x, self.player.y))

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def there_is_a_monster_on_this_tile(self, x, y):
        this_monster = self.npcs.get_npc_if_monster(x, y)
        if this_monster is None: return False
        return True

    def there_is_an_angel_on_this_tile(self, x, y):
        raise NotImplemented
        this_angel = self.npcs.get_npc_if_angel(x, y)
        if this_angel is None: return False
        return True

    def there_is_an_npc_on_this_tile(self, x, y):
        this_npc = self.npcs.get_npc(x, y)
        if this_npc is None: return False
        return True

    def there_is_an_action_on_this_tile(self, x, y):
        print("Testing to see whether there is an action on tile x,y: ({},{})".format(x, y))
        this_action = self.environment.actions.get_action(x, y)
        if this_action is None: return False
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
        result = current_npc.have_interaction(self.environment.events)
        if result == "end game":
            self.player_died()
        elif result == "end conversation":
            # end conversation -->
            # player goes on about their day but
            # nothing is changed as a result of the interaction
            pass
        elif result == "continue":
            # continue -->
            # player goes on about their day BUT something
            # is changed because of the interaction.
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
                        self.player.image = self.player.image_left
                        self.player.direction = constants.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.player.move(dx=1, obstacles=self.environment.obstacles) == True:
                        self.player.image = self.player.image_right
                        self.player.direction = constants.RIGHT
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.player.move(dy=1, obstacles=self.environment.obstacles) == True:
                        self.player.image = self.player.image_down
                        self.player.direction = constants.DOWN
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.player.move(dy=-1, obstacles=self.environment.obstacles) == True:
                        self.player.image = self.player.image_up
                        self.player.direction = constants.UP
                # ===============================================
                elif event.key == pygame.K_h:
                    if self.there_is_an_npc_on_this_tile(self.player.x, self.player.y) == True:
                        print("There is an npc on this tile.")
                        self.npc_encounter()
                        print("After self.npc_encounter()")
                    elif self.there_is_an_action_on_this_tile(self.player.x, self.player.y) == True:
                        # After an action is used, the tile is removed.
                        print("There is an action on this tile.")
                        if self.environment.actions.conditions_passed(self.player, self.environment.events) == False:
                            return False
                        current_action = self.environment.actions.get_action(self.player.x, self.player.y)
                        self.do_action(current_action)
                        self.environment.actions.remove_tile(self.player.x, self.player.y)
                        self.init_pygame()
                        self.all_sprites = pygame.sprite.Group()
                        return ""
                elif event.key == pygame.K_i: # Inventory
                    if len(self.player.inventory) == 0:
                        raise ValueError("The player has lost their inventory!")
                    mydialog = DialogPlayerInventory(self.player)
                    mydialog.main()
                    self.init_pygame()
                elif event.key == pygame.K_p:
                    mydialog = TextDialog("Displaying the Player's stats has been disabld for now.")
                    mydialog.main()
                    self.init_pygame()
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))
                # ------------------------------------------------------
                self.check_for_trigger()

    def check_for_trigger(self):
        if self.environment.triggers is None: return False
        current_trigger = self.environment.triggers.get_trigger(self.player.x, self.player.y)
        if not current_trigger is None:
            self.do_trigger(current_trigger)

    def show_text(self, current_trigger):
        # print("debugging: in def load_map(self, current_trigger")
        filename = "{}.txt".format(current_trigger.data)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", filename)
        mydict = utils.read_file(filepath)[0]
        for key, value in mydict.items():
            # print(key, value)
            mytextdialog = TextDialog(value)
            mytextdialog.main()
        self.init_pygame()

    def do_trigger(self, current_trigger):
        # print("There is a current trigger")
        if current_trigger.command == "load_map":
            if self.environment.triggers.conditions_passed(self.player, self.environment.events) == False:
                return False
            # ----
            self.save_data()
            mydict = current_trigger.parse_data()
            self.zone_name = mydict["zone_name"]
            self.map_name = mydict["map_name"]
            utils.set_user_data(self.player.name, self.zone_name, self.map_name, self.player.profession)
            # ----
            self.read_data()
        elif current_trigger.command == "show_text":
            self.show_text(current_trigger)
        elif current_trigger.command == "change_npc_passive":
            # check to make sure that the name given in data is that of an npc
            # so check the npc_name_lookup.txt file in the zone directory.
            # if this goes through then turn that npc passive.
            if utils.npc_exists_in_zone(current_trigger.data, self.zone_name) == False:
                s = "Error! That npc ({}) does not exist in this zone."
                raise ValueError(s)
            raise NotImplemented
        elif current_trigger.command == "change_npc_agro":
            # check to make sure that the name given in data is that of an npc
            # so check the npc_name_lookup.txt file in the zone directory.
            # if this goes through then turn that npc agro.
            if utils.npc_exists_in_zone(current_trigger.data, self.zone_name) == False:
                s = "Error! That npc ({}) does not exist in this zone ({}).".format(current_trigger.data, self.zone_name)
                raise ValueError(s)
            the_npc = self.npcs.get_npc_by_name(current_trigger.data)
            if the_npc is None:
                s = "This nane ({}) is not the name of a current npc.".format(current_trigger.data.replace(" ", "_"))
                raise ValueError(s)
            the_npc.agro_level = "agro"
        else:
            current_trigger.debug_print()
            s = "I couldn't find that: {}".format(current_trigger.command)
            raise ValueError(s)
        return True

    def do_action(self, current_action):
        if current_action.command == "load_map":
            """This loads both a zone and a map."""
            mydialog = TextDialog(current_action.dialog_text)
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
            mydialog = TextDialog(current_action.display_text())
            mydialog.main()
            print("--------------- (begin)")
            print("debugging: in def show_text(self, current_action")
            self.player.inventory.add_item_by_name(current_action.data, 1)
            self.player.inventory.debug_print()
            print("--------------- (end)")
        else:
            s = "Error! I don't recognize this command: {}".format(current_action.command)
            raise ValueError(s)

    # --------------------------------------------------------
    def update_classes(self):
        self.all_sprites = self.environment.update_classes(self.all_sprites)
        self.all_sprites = self.npcs.update_classes(self.all_sprites)
        self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def update(self):
        current_monster = self.npcs.closest_monster(self.player.x, self.player.y)
        # print("npc name: {}".format(current_monster.name))
        # ---- Debugging ----
        if not current_monster is None:
            print("Current monster:")
            print("Is dead: {}".format(current_monster.is_dead()))
            print("agro_level: {}".format(current_monster.agro_level))
            print("x,y: {},{}".format(current_monster.x, current_monster.y))
        # -------------------
        if not current_monster is None:
            if current_monster.is_dead() == False and current_monster.agro_level == "agro":
                # If the npc is a skeleton and the player has a silver necklace in their inventory then
                # check to see if the player is in the effect radius of the item. If they are, then
                # do not move the skeleton.
                # I added this at the last minute so I didn't include it in the tutorial.
                if current_monster.species == "skeleton":
                    if self.player.has_item("silver cross"):
                        if self.player.npc_in_range_of_item_effect(current_monster, "silver cross") == True:
                            return False
                current_monster.move_toward(self.player.x, self.player.y, self.environment.obstacles)
                if current_monster.is_dead() == True:
                    current_monster.image = current_monster.image_dead
                elif current_monster.has_caught(self.player.x, self.player.y) == True:
                    mydialog = DialogFight(self.player, current_monster)
                    mydialog.main()
                    if self.player.is_dead() == False and current_monster.is_dead() == False:
                        print("player hit points: {}".format(self.player.hit_points))
                        # raise NotImplemented
                    if self.player.is_dead() == True:
                        current_monster.agro_level = "passive"
                        self.player.image = self.player.image_dead
                        mylist = ["You're dead! Play again?"]
                        mylist.append(" ")
                        mylist.append("y = Yes; n = No")
                        mydialog = DialogInput(mylist, ["y", "n"])
                        myresult = mydialog.main()
                        if myresult == "y":
                            self.player.hit_points = self.player.max_hit_points
                            utils.copy_original_player_files(self.player.profession, self.player.name)
                            # self.player.save_data()
                            self.npcs.save_data()
                            # ----
                            previous_map = utils.get_previous_map_name(self.map_name)
                            utils.set_user_data(self.player.name,
                                                self.zone_name, previous_map,
                                                self.player.profession)
                            # self.load_map()
                            self.read_data()
                        elif myresult == "n":
                            self.keep_looping = False
                        elif len(myresult) == 0:
                            self.keep_looping = False
                        else:
                            raise ValueError("Error! This is myresult: -{}-".format(myresult))

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            time.sleep(0.5)
            self.handle_events()
            self.update()
            self.draw()
            print("zone_name: {}, map_name: {}".format(self.zone_name, self.map_name))
        self.goodbye()
        self.save_data()
        self.myquit()

    def save_data(self):
        self.player.save_data()
        self.npcs.save_data()
        self.environment.events.save_data()

    def myquit(self):
        pygame.quit()
        # sys.exit()

    def goodbye(self):
        mylist = []
        mylist.append("Thank you for playing")
        mylist.append("{}".format(constants.TITLE))
        mydialog = TextDialog(mylist)
        mydialog.main()



# **************************************************
# **************************************************

if __name__ == "__main__":
    pass
    # utils.set_user_data("henry", "testing", "map01")
    # # ----
    # mydriver = DebugDriver()
    # mydriver.read_data()
    # mydriver.main()