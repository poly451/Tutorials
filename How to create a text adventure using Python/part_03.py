import constants as con
import utils

def main_menu(first_time):
    utils.clear_screen()
    if first_time:
        print("Welcome to {}".format(con.GAME_NAME))
    print("Here are your choices: {}".format(con.MAIN_MENU_CHOICES))
    user_input = input("> ").lower().strip()
    while not user_input in con.MAIN_MENU_CHOICES:
        print("Sorry, I didn’t recognize that: {}".format(user_input))
        user_input = input("> ").lower().strip()
    # ---------------------------------------------
    print("user input: {}".format(user_input))
    if user_input == "new":
        player_name, player_kind = utils.get_player_info()
        s = "{} the {}".format(player_name.upper(), player_kind.upper())
        print("You have created a character: {}".format(s))
    elif user_input == "load":
        print("LOAD needs to be implemented.")
    elif user_input == "quit":
        return False
    else:
        s = "Sorry, I don't recognize that: {}".format(user_input)
        raise ValueError(s)
    input("Press <Enter> to continue.")
    return True

if __name__ == "__main__":
    keep_looping = True
    mycounter = 0
    while keep_looping:
        if mycounter == 0:
            keep_looping = main_menu(True)
        else:
            keep_looping = main_menu(False)
        mycounter += 1
print("Goodbye! Thanks for playing {}.".format(con.GAME_NAME))
