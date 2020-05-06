import constants as con

def main_menu():
    # Display a welcome message
    print("Welcome to {}".format(con.GAME_NAME))
    print("Here are your choices: {}".format(con.MAIN_MENU_CHOICES))
    user_input = input("> ").lower().strip()
    while not user_input in con.MAIN_MENU_CHOICES:
        print("Sorry, I didn’t recognize that: {}".format(user_input))
        user_input = input("> ").lower().strip()
     # ---------------------------------------------
    print("user input: {}".format(user_input))
    if user_input == "quit":
        return False
    return True

if __name__ == "__main__":
    keep_looping = True
    while keep_looping:
            keep_looping = main_menu()
