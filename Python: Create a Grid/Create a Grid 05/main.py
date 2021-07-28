from myclasses import Game
from dialogs import DialogLobby, TextDialog, DialogReset, InputDialog
import constants
import utils

def begin_game(player_name):
    mygame = Game(player_name)
    mygame.read_data()
    mygame.main()

def goodbye():
    mylist = []
    mylist.append("Thank you for playing")
    mylist.append("{}".format(constants.TITLE))
    mydialog = TextDialog(mylist)
    mydialog.main()

def main(player_name, zone_name, map_name, profession_name):
    if utils.validate_name(player_name) == False:
        s = "{} is not a valid name.".format(player_name)
        raise ValueError(s)
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
    utils.set_user_data(player_name,
                        zone_name, map_name,
                        profession_name)
    utils.reset_events_and_inventory(player_name)
    # ----
    choices = ["g", "c", "q", "p", "s"]
    user_choice = ""
    while not user_choice in ["g", "q", "s"]:
        mydialog = DialogLobby(choices)
        user_choice = mydialog.main()
        newdialog = DialogReset()
        newdialog.main()
    if user_choice == "q":
        goodbye()
    elif user_choice == "p":
        pass
    elif user_choice == "s":
        print("user_choice is: {}".format(user_choice))
    elif user_choice == "g":
        begin_game(player_name)
    else:
        raise ValueError("Error!")

if __name__ == "__main__":
    player_name = "henry"
    zone_name = "dark_alley"
    # zone_name = "green_lawn"
    map_name = "map00"
    profession_name = "warrior"
    main(player_name, zone_name, map_name, profession_name)

