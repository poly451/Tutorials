"""
(a) Let's get the player up and moving around.
"""

import constants as con
import utils
from myclasses import Game

def _main_menu(first_time):
    utils.clear_screen()
    mygame = None
    if first_time:
        print("Welcome to {}".format(con.GAME_NAME))
    choices = ', '.join(con.MAIN_MENU_CHOICES)
    print("Here are your choices: {}".format(choices))
    user_input = input("main loop > ").lower().strip()
    while not user_input in con.MAIN_MENU_CHOICES:
        print("Sorry, I didn’t recognize that: {}".format(user_input))
        user_input = input("> ").lower().strip()
    # ---------------------------------------------
    print("user input: {}".format(user_input))
    if user_input == "new":
        char_name, char_kind = utils.get_player_info()
        utils.save_char_info(char_name, char_kind)
        s = "{} the {}".format(char_name.upper(), char_kind.upper())
        print("You have created a character: {}".format(s))
        print("Now let's set up a world for you ...")
        utils.copy_directory(char_name, char_kind)
        mygame = Game(char_name, char_kind, zone_name="world")
    elif user_input == "load":
        print("LOAD needs to be implemented.")
        raise NotImplemented
    elif user_input == "quit":
        return False
    else:
        s = "Sorry, I don't recognize that: {}".format(user_input)
        raise ValueError(s)
    input("Press <Enter> to continue.")
    utils.clear_screen()
    mygame.game_loop()
    return True

def main():
    keep_looping = True
    mycounter = 0
    while keep_looping:
        if mycounter == 0:
            keep_looping = _main_menu(True)
        else:
            keep_looping = _main_menu(False)
        mycounter += 1
    print("Goodbye! Thanks for playing {}.".format(con.GAME_NAME))

if __name__ == "__main__":
    main()
