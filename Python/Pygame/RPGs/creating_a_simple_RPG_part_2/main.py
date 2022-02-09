from environment import EnvironmentDriver
from player import PlayerDriver
from dialogs import DialogInput_New
import helper_functions
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "800, 100"

def main():
    display_list = ["What would you like to do?"]
    display_list.append(" ")
    choices = ["Create a player only"]
    choices.append("View background only")
    choices.append("Run a helper function")
    display_list += ["{}) {}".format(count+1, i) for count, i in enumerate(choices)]
    possible_choices = list(range(1, len(choices)+1))
    mydialog = DialogInput_New(display_list, possible_choices)
    user_choice = mydialog.main()
    user_index = int(user_choice)-1
    choice = choices[user_index]
    # ---- ----
    if choice == "Create a player only":
        zone_name = "docks"
        map_name = "map00"
        myclass = PlayerDriver(zone_name, map_name)
        myclass.read_data()
        myclass.main()
    if choice == "View background only":
        zone_name = "docks"
        map_name = "map00"
        mydriver = EnvironmentDriver(zone_name, map_name)
        mydriver.read_data()
        mydriver.main()
        # Environment
        # environment.main()
    elif choice == "Run a helper function":
        helper_functions.main()
    else:
        raise ValueError("Error")

if __name__ == "__main__":
    main()
