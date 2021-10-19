import pygame

from myclasses import Game
from dialogs import DialogLobby, DialogText, \
    DialogSpashScreen, DialogGoodbye
import constants
import utils
from input_utility import main as utility_main
import time

def begin_game():
    user_data = utils.get_user_data()
    player_name = user_data["character_name"]
    if utils.check_that_player_has_a_gold_coin(player_name) == False:
        raise ValueError("Error")
    # ----
    mygame = Game()
    mygame.read_data()
    mygame.main()

def goodbye():
    mydialog = DialogGoodbye()
    mydialog.main()

def main(zone_name, map_name, profession_name):
    if not zone_name in constants.ZONE_NAMES:
        s = "{} is not a valid zone.".format(zone_name)
        raise ValueError(s)
    if not map_name in constants.MAP_CHOICES:
        s = "{} is not a valid map.".format(map_name)
        raise ValueError(s)
    if not profession_name in constants.PROFESSION_NAMES:
        s = "{} is not a valid profession name.".format(profession_name)
        raise ValueError(s)
    # ----
    # save zone and map info
    user_info = utils.get_user_data()
    player_name = user_info["character_name"]
    utils.set_user_data(player_name,
                        zone_name, map_name,
                        profession_name)
    # ----
    choices = ["g", "c", "q", "p", "s", "u"]
    user_choice = ""
    while not user_choice in ["g", "q", "s", "u"]:
        mydialog = DialogLobby(choices)
        user_choice = mydialog.main()
        if user_choice == "u":
            pygame.quit()
        else:
            newdialog = DialogSpashScreen()
            newdialog.main()
    if user_choice == "q":
        goodbye()
    # elif user_choice == "b":
    #     begin_game_debugging()
    elif user_choice == "p":
        pass
    elif user_choice == "s":
        print("user_choice is: {}".format(user_choice))
    elif user_choice == "g":
        begin_game()
    elif user_choice == "u":
        utility_main(zone_name="provisioner", map_name="map00", player_name="henry")
    else:
        raise ValueError("Error!")

if __name__ == "__main__":
    # check to make sure that files are correct
    for an_item in constants.PROVISIONERS_GOODS:
        if not an_item in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            print(constants.CONSUMABLE_NAMES)
            print(constants.WEAPON_NAMES)
            s = "I don't recognize this item: {}".format(an_item)
            raise ValueError(s)

    # ----
    # zone_name = "dark_alley"
    # zone_name = "jeweler"
    # zone_name = "green_lawn"
    # zone_name = "bridge"
    # zone_name = "swindon"
    # zone_name = "swindon_pub"
    zone_name = "swindon_pub_haunted"
    # zone_name = "bridge"
    # zone_name = "provisioner"
    # zone_name = "cliffs"
    # zone_name = "village_blue"
    # zone_name = "apple_grove"
    # zone_name = "the_orchard"
    # zone_name = "testing"
    # zone_name = "green_lawn"
    # zone_name = "easthaven"
    map_name = "map00"
    profession_name = "warrior"
    main(zone_name, map_name, profession_name)

