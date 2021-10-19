import constants
import utils
import sys, os
from NEW_inventory import Inventory
from inventory_classes import Weapon, Consumable
from shutil import copyfile
from conversation_input import ConversationPlaceholders
# ---- ---- ---- ----

def print_out_player_inventory():
    myobject = Inventory(player_name="henry", npc_name="lilly", character_type="player")
    myobject.read_data()
    myobject.debug_print()

def conversations_make_placeholders():
    myobject = ConversationPlaceholders()

def find_an_image_file():
    print("What term would you like to search for?")
    search_term = input("> ").lower().strip()
    basepath = os.path.join("data")
    mylist = utils.find_an_image_file(basepath, search_term)
    print("{} matches were found for {}:".format(len(mylist), search_term))
    [print(i) for i in mylist]

def _create_npc_name_helper01():
    def number_valid(mynum):
        if utils.is_int(mynum) == False: return False
        mynum = int(mynum)
        if mynum < 1: return False
        if mynum > 100: return False
        return True
    # ----
    races = ["human", "hobbit", "elf"]
    sexes = ["male", "female", "other"]
    # ----
    race = ""
    while not race in races:
        print("Creating an NPC name. Please enter the race. {}".format(races))
        race = input("> ").lower().strip()
        if race in ["q", "quit"]: goodbye()
    # ----
    sex = ""
    while not sex in sexes:
        print("Creating an NPC name. Please enter a sex. {}".format(sexes))
        sex = input("> ").lower().strip()
        if sex in ["q", "quit"]: goodbye()
    # ----
    number_of_names = -1
    while number_valid(number_of_names) == False:
        s = "Creating an NPC name. Please enter the number "
        s += "of names you would like me to generate (1 to 100)."
        print(s)
        number_of_names = input("> ").lower().strip()
        if number_of_names in ["q", "quit"]: goodbye()
        try:
            number_of_names = int(number_of_names)
        except:
            number_of_names = -1
    # ----
    print("Would you like to specify a first letter? (y/n)")
    yes_no = ""
    while not yes_no in ["y", "n", "yes", "no"]:
        yes_no = input("> ").lower().strip()
        if yes_no in ["q", "quit", "exit"]: goodbye()
    if yes_no in ["y", "yes"]:
        first_letter = ""
        print("Please choose a letter:")
        while not first_letter in constants.ALPHABET:
            first_letter = input("> ").lower().strip()
            if first_letter in ["q", "quit", "exit"]: goodbye()
        names = utils.get_random_NPC_name(race, sex, number_of_names, first_letter)
        return names
    # ----
    names = utils.get_random_NPC_name(race, sex, number_of_names)
    return names

def _create_npc_name_helper02():
    raise NotImplemented
    # filepath = os.path.join("data", "master_files", "names", "first_names_medieval.txt")
    # with open(filepath, "r") as f:
    #     lines = f.readlines()
    #     lines = [i.strip() for i in lines if len(i.strip()) > 0]
    # for name in lines:
    #     if utils.has_two_vowels(name):
    #         first_vowel, location01 = utils.get_first_vowel(name)
    #         second_vowel, location02 = utils.get_second_vowel(name)
    #         name[location:location01 + 1] = second_vowel
    #         name[location:location02 + 1] = first_vowel
    #     for mychar in name:
    #         if mychar in constants.VOWELS:


def create_the_name_of_an_NPC():
    print("Which method of name creation would you like to use?")
    print("1) Method01")
    print("2) Method02")
    user_choice = ""
    while not user_choice in ["1", "2"]:
        user_choice = input("> ").lower().strip()
        if user_choice in ["q", "quit"]: goodbye()
    user_choice = int(user_choice)
    # ----
    names = []
    if user_choice == 1:
        names = _create_npc_name_helper01()
    elif user_choice == 2:
        names = _create_npc_name_helper02()
    return names

def reset_player():
    print("Which playing character would you like to reset?")
    player_names = utils.get_all_player_names()
    print(player_names)
    player_name = ""
    while not player_name in player_names:
        player_name = input("> ").lower().strip()
        if player_name in ["q", "quit"]: goodbye()
    # ----
    print("Which profession does {} have?".format(player_name.upper()))
    print(constants.PROFESSION_NAMES)
    profession = ""
    while not profession in constants.PROFESSION_NAMES:
        profession = input("> ").lower().strip()
        if profession in ["q", "quit"]: goodbye()
    # ----
    source_path = os.path.join("data", "master_files", "player_types", profession, "player_data_file.txt")
    if os.path.isfile(source_path) == False: raise ValueError("Error")
    destination_path = os.path.join("data", "playing_characters", player_name, "player_data_file.txt")
    if os.path.isfile(destination_path) == False: raise ValueError("Error")
    copyfile(source_path, destination_path)
    # ----
    utils.reset_player_inventory(player_name, profession)

def reset_everything():
    reset_player()
    reset_all_conversations()
    print("-------------------------------------------------")
    print("The player and all conversations have been RESET.")
    print("-------------------------------------------------")

def reset_all_conversations():
    for zone in constants.ZONE_NAMES:
        map_names = utils.get_map_names(zone)
        for map in map_names:
            npc_names = utils.get_all_npc_names_by_zone(zone_name=zone, map_name=map)
            if npc_names is None:
                continue
            if len(npc_names) == 0: raise ValueError("Error")
            for npc_name in npc_names:
                utils.reset_conversation(npc_name=npc_name, zone_name=zone, map_name=map)

def reset_player_gold():
    # s = "You need to stop reading the gold value from the player.\n"
    # s += "Read the value from the item in the inventory."
    # raise ValueError(s)
    def gold_okay(mygold):
        if utils.is_int(mygold) == False: return False
        myint = int(mygold)
        if myint < 0: return False
        return True
    # ----
    all_player_names = utils.get_all_player_names()
    player_name = ""
    player_gold = -1
    # ----
    while not player_name in all_player_names:
        print("resetting gold: Which player?")
        print(all_player_names)
        player_name = input("> ").lower().strip()
        if player_name in ["q", "quit"]: goodbye()
    while gold_okay(player_gold) == False:
        print("resetting gold: How much gold?")
        player_gold = input("> ").lower().strip()
        if player_gold in ["q", "quit"]: goodbye()
    player_gold = int(player_gold)
    # ----
    filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "weapon_items.txt")
    # filepath = os.path.join("data", "playing_characters", player_name, "player_data_file.txt")
    mydict = utils.read_file(filepath)[0]
    mylist = utils.read_data_file(filepath, 11)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name" and value == "gold coin":
                mydict["units"] = player_gold
    # ----
    # filepath = os.path.join("data", "testing.txt")
    with open(filepath, "w") as f:
        for mydict in mylist:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
        # for key, value in mydict.items():
        #     s = "{}: {}\n".format(key, value)
        #     f.write(s)

def create_the_name_of_a_town():
    filepath = os.path.join("data", "language_landmarks.txt")
    landmarks_dict = utils.read_file(filepath)[0]
    filepath = os.path.join("data", "language_modifiers.txt")
    modifiers_dict = utils.read_file(filepath)[0]
    # ----
    # mylist = []
    # for key, value in landmarks_dict.items():
    #     mylist.append(key)
    landmarks = [key.lower().strip() for key, value in landmarks_dict.items()]
    modifiers = [key.lower().strip() for key, value in modifiers_dict.items()]
    # ---- ----
    print("-------------------------------------------")
    s = "What is the name of the most prominent landmark near the town?\n"
    s += "For example: forest, tower, boulder, mountain, ..."
    print(landmarks)
    print(s)
    landmark = ""
    while not landmark in landmarks:
        landmark = input("> ").lower().strip()
        if landmark in ["q", "quit"]: goodbye()
    new_landmark = landmarks_dict[landmark]
    # print(new_landmark)
    # ----
    print("-------------------------------------------")
    s = "Whose landmark is this? Who uses it?\n"
    s += "For example, is it a tower that guards use,\n"
    s += "Is it an ancient forest? Etc."
    print(modifiers)
    print(s)
    modifier = ""
    while not modifier in constants.MODIFIERS:
        modifier = input("> ").lower().strip()
        if modifier in ["q", "quit"]: goodbye()
    new_modifier = modifiers_dict[modifier]
    # ----
    s = "You entered: {} {}".format(landmark, modifier)
    print(s)
    s = "Translation: {} {}".format(new_landmark, new_modifier)
    print(s)


def reset_conversation():
    print("Which zone?")
    zone_name = ""
    while not zone_name in constants.ZONE_NAMES:
        zone_name = input("> ")
        if zone_name in ["q", "quit"]: goodbye()
    # ----
    print("Which map in zone {}?".format(zone_name.upper()))
    map_name = ""
    while not map_name in constants.MAP_CHOICES:
        map_name = input("> ")
        if map_name in ["q", "quit"]: goodbye()
    # ----
    names = utils.get_all_npc_names_by_zone(zone_name=zone_name, map_name=map_name)
    print("Present on map:", ", ".join(names))
    print("Which npc in zone {}, map {}?".format(zone_name, map_name))
    npc_name = ""
    while not npc_name in constants.NPC_NAMES:
        npc_name = input("> ")
        if npc_name in ["q", "quit"]: goodbye()
    # ----
    print("zone: {}, map: {}, npc: {}".format(zone_name, map_name, npc_name))
    utils.reset_conversation(npc_name=npc_name, zone_name=zone_name, map_name=map_name)
    s = "All conversations in zone {}, map {}, with {} have been reset."
    s = s.format(zone_name, map_name, npc_name)
    print(s)

def print_put_NPC_names():
    names = []
    filedir = os.path.join("data", "master_files", "npcs")
    filenames = os.listdir(filedir)
    for filename in filenames:
        if filename == ".DS_Store":
            continue
        filepath = os.path.join(filedir, filename)
        mydict = utils.read_file(filepath)[0]
        # print(mydict)
        a, b, c, d = "", "", "", ""
        try:
            a = mydict["name"]
            b = mydict["species"]
            c = mydict["profession"]
            d = mydict["model_name"]
        except Exception as e:
            s = "{}, {}, {}, {}".format(a, b, c, d)
            t = "{}\n{}".format(e, s)
            raise ValueError(t)
        s = "{}, {}, {}, (model_name: {})".format(a, b, c, d)
        names.append(s)
    print("****************************************")
    print("             NPC Names (etc)")
    print("****************************************")
    [print(i) for i in names]

def make_a_new_conversation():
    character_names = utils.get_npc_names_from_files()
    display_list = []
    real_list = []
    for name in character_names:
        display_list.append(name.title())
        real_list.append(name.lower())
    display_list = list(set(display_list))
    real_list = list(set(real_list))
    print("Here are some NPC names:")
    print(display_list)
    npc_name = ""
    while not npc_name in real_list:
        print("What character would you like to create a conversation for?")
        npc_name = input("> ").lower().strip()
        if npc_name in ["quit", "q"]: goodbye()
    # ----
    print("In which ZONE will this conversation take place?")
    zone_name = ""
    while not zone_name in constants.ZONE_NAMES:
        zone_name = input("> ").lower().strip()
        if zone_name in ["quit", "q"]: goodbye()
    # ----
    print("In which MAP will this conversation take place?")
    map_name = ""
    while not map_name in constants.MAP_CHOICES:
        map_name = input("> ").lower().strip()
        if map_name in ["quit", "q"]: goodbye()
    # ----
    directory_origin = os.path.join("data", "master_files", "conversations")
    myfiles = os.listdir(directory_origin)
    for filename in myfiles:
        filepath_origin = os.path.join("data", "master_files", "conversations", filename)
        filename_destination = filename.replace("npcname", npc_name)
        filepath_destination = os.path.join("data", "zones", zone_name, map_name, "conversations", filename_destination)
        print("Copying files:")
        print(filepath_origin)
        print(filepath_destination)
        print(" ---- ")
        copyfile(filepath_origin, filepath_destination)

def search_for_phrase():
    print("Which phrase would you like me to search for?")
    the_phrase = ""
    while the_phrase in [""]:
        the_phrase = input("> ").lower()
    basepath = os.path.join("data")
    filepaths = utils.search_for_phrase(the_phrase, basepath)
    if filepaths is None:
        s = "This phrase was not found ({}) ".format(the_phrase)
        s += "in this directory: {}".format(basepath)
        print(s)
    else:
        print("These files were found:")
        [print(i) for i in filepaths]

def make_a_new_zone_map():
    def get_highest_map_number(zone_name):
        subdirectories = utils.get_subdirectories(os.path.join("data", "zones", zone_name))
        mylist = [int(i[3:5]) for i in subdirectories]
        highest = max(mylist)
        return highest
    def get_mapname(new_map_number):
        s = ""
        if new_map_number <= 9:
            s = "map0{}".format(new_map_number)
        else:
            s = "map{}".format(new_map_number)
        return s
    # ----
    print("Which zone would you like the map to be in?")
    zone_name = ""
    while not zone_name in constants.ZONE_NAMES:
        zone_name = input("> ").lower().strip()
    # ----
    print("Here are the map names for zone {}".format(zone_name.upper()))
    subdirectories = utils.get_subdirectories(os.path.join("data", "zones", zone_name))
    print(subdirectories)
    # ----
    highest_map_number = get_highest_map_number(zone_name)
    new_map_number = highest_map_number + 1
    highest_map_name = get_mapname(highest_map_number)
    new_map_name = get_mapname(new_map_number)
    # ----
    print("This is the highest map name: {}".format(highest_map_name))
    print("This is the proposed new map subdirectory: {}".format(new_map_name))
    print("Accept? (y/n)")
    user_input = ""
    while not user_input in ["y", "yes", "n", "no"]:
        user_input = input("> ").lower().strip()
        if user_input in ["q", "quit"]:
            goodbye()
    if user_input in ["n", "no"]:
        goodbye()
    dir1 = os.path.join("data", "zones", zone_name, highest_map_name)
    dir2 = os.path.join("data", "zones", zone_name, new_map_name)
    os.mkdir(dir2)
    utils.copy_directory(dir1, dir2)
    # ----
    filenames = os.listdir(dir2)
    for file_name in filenames:
        if file_name.find(highest_map_name) > -1:
            p1 = os.path.join("data", "zones", zone_name, new_map_name, file_name)
            new_name = file_name.replace(highest_map_name, new_map_name)
            p2 = os.path.join("data", "zones", zone_name, new_map_name, new_name)
            # print(p1)
            # print(p2)
            os.rename(p1, p2)
    # print("Which map name would you like to add?")
    # map_name = ""
    # map_name = input("> ").lower().strip()


def get_unused_map_tile_names():
    # get_unused_tile_names
    # get_all_map_names_in_zone
    return utils.get_unused_tile_names()

def _add_map_tile_from_user_input():
    def filename_is_valid(filename):
        filepath = utils.get_filepath(filename)
        if filepath is None: return False
        return True
    # ----
    s = "What KIND of tile is this?"
    print(s)
    tile_kind = ""
    while not tile_kind in constants.TILE_KINDS:
        print(constants.TILE_KINDS)
        tile_kind = input("> ")
        if tile_kind in ["q", "quit"]: goodbye()
    # ----
    s = "Please give me the name of the "
    s += "image you would like to use for this tile."
    print(s)
    filename = ""
    while not utils.image_filepath_exists(filename):
        filename = input("> ").lower().strip()
        if filename in ["q", "quit"]: goodbye()
    # ----
    unused = utils.get_unused_tile_names()
    if len(unused) == 0:
        raise ValueError("Error")
    tile_name = unused[0]
    # ----
    original_filepath = os.path.join("data", "master_files", "tiles.txt")
    old_tiles = utils.read_data_file(filepath=original_filepath, num_of_fields=4)
    tile_index = utils.get_highest_index(old_tiles) + 1
    # ----
    print("tile_kind: {}".format(tile_kind))
    print("filename: {}".format(filename))
    print("tile name: {}".format(tile_name))
    print("tile index: {}".format(tile_index))
    mydict = {}
    mydict["kind"] = tile_kind
    mydict["image"] = filename
    mydict["index"] = tile_index
    mydict["name"] = tile_name
    return mydict

def _add_map_tile_from_file(old_tiles, new_dict):
    # ----
    # Check that the kind field is valid:
    if not new_dict["kind"] in constants.TILE_KINDS:
        s = "{} is not in {}".format(new_dict["kind"], constants.TILE_KINDS)
        raise ValueError(s)
    # ----
    unused = utils.get_unused_tile_names()
    if len(unused) == 0:
        raise ValueError("Error")
    new_dict["name"] = unused[0]
    # ----
    # Test to see that the image name is valid.
    filepath = utils.get_filepath(new_dict["image"])
    if filepath is None:
        raise ValueError("I didn't find this image: {}".format(new_dict["image"]))
    # ----
    print("Here is the new record. Accept it? (y/n)")
    [print("{}: {}".format(key, value)) for key, value in new_dict.items()]
    accept_new_record = ""
    while not accept_new_record in ["yes", "no", "y", "n"]:
        accept_new_record = input("> ").lower().strip()
        if accept_new_record in ["q", "quit"]:
            goodbye()
    if accept_new_record in ["n", "no"]:
        goodbye()

def _add_map_tile_helper():
    original_filepath = os.path.join("data", "master_files", "tiles.txt")
    old_tiles = utils.read_data_file(filepath=original_filepath, num_of_fields=4)
    # ----
    new_tile = {}
    print("Would you like to read the tile data from a file or would you like to enter it now? (y/n)")
    print("filename: data/input_templates/new_tile_data.txt")
    user_input = ""
    while not user_input in ["y", "n", "yes", "no"]:
        print("Read information from a file?")
        user_input = input("> ").lower().strip()
        if user_input in ["q", "quit"]:
            goodbye()
    # ----
    # GET DATA
    new_dict = {}
    if user_input in ["n", "no"]:
        new_dict = _add_map_tile_from_user_input()
        if new_dict is None: raise ValueError("Error")
    else:
        temp_path = os.path.join("data", "input_templates", "new_tile_data.txt")
        new_dict = utils.read_file(temp_path)[0]
        new_dict["index"] = utils.get_highest_index(old_tiles) + 1
        _add_map_tile_from_file(old_tiles, new_dict)
    # ----
    # CHECK DATA
    old_tiles.append(new_dict)
    for mydict in old_tiles:
        mylist = []
        for key, value in mydict.items():
            mylist.append("{}: {}".format(key, value))
        print(mylist)
    print("This is the entire file. Accept it? (y/n)")
    accept_new_record = ""
    while not accept_new_record in ["yes", "no", "y", "n"]:
        accept_new_record = input("> ").lower().strip()
        if accept_new_record in ["q", "quit"]:
            goodbye()
    if accept_new_record in ["n", "no"]:
        goodbye()
    # original_filepath = os.path.join("data", "testing.txt")
    with open(original_filepath, "w") as f:
        for mydict in old_tiles:
            for key, value in mydict.items():
                s = "{}: {}\n".format(key, value)
                f.write(s)
            f.write("\n")
    print("Tile written to file: {}".format(original_filepath))

def add_map_tile():
    def go_again():
        s = "Add another tile?"
        print(s)
        add_another = ""
        while not add_another in ["y", "n", "yes", "no"]:
            add_another = input("> ").lower().strip()
            if add_another in ["q", "quit", "exit"]:
                goodbye()
        if add_another in ["y", "yes"]: return True
        return False
    # ----
    keep_looping = True
    while keep_looping == True:
        _add_map_tile_helper()
        print("--------------------------------")
        keep_looping = go_again()

def print_out_inventory_items():
    myinventory = Inventory("henry", "alfred", "npc")
    myinventory.read_data()
    # myinventory.debug_print_names()
    myinventory.debug_print()

def _create_NPC_file_from_input(zone_name, map_name):
    print("Please give me some information about the new character:")
    print(" ")
    mydict = {}
    mydict["name"] = input("name > ").lower().strip()
    mydict["function"] = input("name > ").lower().strip()
    mydict["species"] = input("species > ").lower().strip()
    mydict["profession"] = input("profession > ").lower().strip()
    max_hit_points = input("max_hit_points > ").lower().strip()
    mydict["max_hit_points"] = int(max_hit_points)
    hit_points = input("hit_points > ").lower().strip()
    mydict["hit_points"] = int(hit_points)
    mydict["agro_level"] = input("agro_level > ").lower().strip()
    attack_distance = input("attack_distance > ").lower().strip()
    mydict["attack_distance"] = int(attack_distance)
    maximum_damage = input("maximum_damage > ").lower().strip()
    mydict["maximum_damage"] = int(maximum_damage)
    chance_to_hit = input("chance_to_hit > ").lower().strip()
    mydict["chance_to_hit"] = int(chance_to_hit)
    experience = input("experience > ").lower().strip()
    mydict["experience"] = int(experience)
    gold = input("gold > ").lower().strip()
    mydict["gold"] = int(gold)
    mydict["inventory_type"] = input("inventory type > ").lower().strip()
    is_monster = input("is_monster > ").lower().strip()
    mydict["is_monster"] = True if is_monster == "true" else False
    mydict["model_name"] = input("model_name > ").lower().strip()
    mydict["model_name"] = mydict["model_name"].replace(" ", "_")
    # ----
    if not mydict["model_name"] in constants.NPC_MODEL_NAMES:
        s = "This model_name ({}) is not in constants.NPC_MODEL_NAMES: {}"
        s = s.format(mydict["model_name"], constants.NPC_MODEL_NAMES)
        raise ValueError(s)
    # ----
    model_names = utils.get_all_model_names()
    if not mydict["model_name"] in model_names:
        s = "This model_name ({}) is not in data/images/\n{}"
        s = s.format(mydict["model_name"], constants.NPC_MODEL_NAMES, model_names)
        raise ValueError(s)
    # ---- ----
    print("Here is the information you entered. It will be saved in DATA/NEW_NPC.TXT")
    print(" ")
    for key, value in mydict.items():
        print("{}: {}".format(key, value))
    print(" ")
    print("Would you like to accept this now, or review the file first?")
    print("y = accept now; n = review the file first.")
    user_input = ""
    while not user_input in ["y", "n", "yes", "no"]:
        user_input = input("> ").lower().strip()
    # ----
    filepath = os.path.join("data", "new_npc.txt")
    print("Saving to: {}".format(filepath))
    with open(filepath, "w") as f:
        for key, value in mydict.items():
            s = "{}: {}\n".format(key, value)
            f.write(s)
    # ----
    if user_input in ["y", "yes"]:
        filename = "{}.txt".format(mydict["name"])
        filepath = os.path.join("data", "master_files", "npcs", filename)
        print("Saving to file: {}".format(filepath))
        with open(filepath, "w") as f:
            for key, value in mydict.items():
                s = "{}: {}\n".format(key, value)
                f.write(s)
        # ----
        playing_characters = utils.get_all_player_names()
        for a_player_name in playing_characters:
            filepath_new = os.path.join("data", "playing_characters", a_player_name, "npcs", filename)
            print("Saving dictionary object to this playing character's directory: {}.".format(a_player_name))
            # filepath_new = os.path.join("data", "testing.txt")
            # print("new-dict: {}".format(new_dict))
            with open(filepath_new, "w") as f:
                for key, value in mydict.items():
                    s = "{}: {}\n".format(key, value)
                    f.write(s)

def _create_NPC_file(zone_name, map_name):
    filepath_temp = os.path.join("data", "input_templates", "new_npc.txt")
    new_dict = utils.read_file(filepath_temp)[0]
    # ----
    # Check to make sure that the name of the new NPC hasn't
    # been used before.
    all_npc_names = utils.get_npc_names_from_files()
    if new_dict["name"] in all_npc_names:
        raise ValueError("Doh! That name has been used before: {}".format(new_dict["name"]))
    # ----
    from graphics_fauna import Npcs
    # I'm doing the following just to check the fields.
    # mynpcs = Npcs(zone_name, map_name)
    # ----
    # temp_dict = new_dict
    # temp_dict["x"] = 0
    # temp_dict["y"] = 0
    # temp_dict["on_contact"] = "talk"
    # temp_dict["npc_position"] = "up"
    # temp_dict["destination_point_x"] = "none"
    # temp_dict["destination_point_y"] = "none"
    # if temp_dict["function"] == "resource":
    #     new_object = ResourceNPC(temp_dict)
    #     # self.npcs.append(new_object)
    # elif temp_dict["function"] == "questgiver":
    #     new_object = QuestGiverNPC(temp_dict)
    #     # self.npcs.append(new_object)
    # elif temp_dict["function"] == "sell":
    #     new_object = SellNPC(temp_dict)
    #     # self.npcs.append(new_object)
    # elif temp_dict["function"] == "buy":
    #     new_object = BuyNPC(temp_dict)
    #     # self.npcs.append(new_object)
    # else:
    #     s = "I don't recognize this: {}".format(temp_dict["function"])
    #     raise ValueError(s)
    # ----
    # Create file in "master_files" area
    filename = "{}.txt".format(new_dict["name"].lower())
    filepath_new = os.path.join("data", "master_files", "npcs", filename)
    # filepath_new = os.path.join("data", "testing.txt")
    print("filepath_new: {}".format(filepath_new))
    print("new-dict: {}".format(new_dict))
    print("Saving dictionary object in the MASTER_FILES directory.")
    with open(filepath_new, "w") as f:
        for key, value in new_dict.items():
            s = "{}: {}\n".format(key, value)
            f.write(s)
    # ----
    playing_characters = utils.get_all_player_names()
    for a_player_name in playing_characters:
        filepath_new = os.path.join("data", "playing_characters", a_player_name, "npcs", filename)
        print("Saving dictionary object to this playing character's directory: {}.".format(a_player_name))
        # filepath_new = os.path.join("data", "testing.txt")
        # print("new-dict: {}".format(new_dict))
        with open(filepath_new, "w") as f:
            for key, value in new_dict.items():
                s = "{}: {}\n".format(key, value)
                f.write(s)

def add_npc(zone_name, map_name):
    """
    - Add four image files to the "npc_models" directory of
    the image directory: up, down, right and left.
    - Create a txt file for the NPC in master_files.
    - Create a txt file for the NPC in the directory of any players
    (The text file should have the same name as the character)
    who need to interact with them.
    - Create an entry in npcs.txt in the zone-->map directory.
    - Create an entry in map00_npcs.txt fire in the zone-->map directory.
    :return: None
    """
    print("Would you like to read the new NPC in from a file or input the values yourself?")
    print("If from a file, I will look in <data/input_templates/new_npc.txt>")
    print("----")
    print("From file? (y/n)")
    user_choice = ""
    while user_choice not in ["y", "n", "yes", "no"]:
        user_choice = input("> ").lower().strip()
        if user_choice in ["q", "quit"]:
            goodbye()
    if user_choice in ["y", "yes"]:
        _create_NPC_file(zone_name=zone_name, map_name=map_name)
    else:
        _create_NPC_file_from_input(zone_name=zone_name, map_name=map_name)


# ========================================
#     Add Consumables
# ========================================
def add_consumable_to_npc(player_name):
    update_npc_consumables(player_name)

def update_npc_consumables(player_name):
    """
    All we need to do is update the inventories in npc_inventories
    since no npc currently has a unique inventory. Although they COULD
    have unique inventories by player character. So, for example, the
    npc's inventories in Henry's npc_inventory directory could be
    different from the inventories in another character's inventory.
    """
    # todo: Implement inventories for each npc character.
    if player_name is None or len(player_name) == 0:
        raise ValueError("Error")
    if utils.validate_player_name(player_name) == False:
        raise ValueError("Error")
    master_filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
    local_filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "consumable_items.txt")
    master_weapon_items = utils.read_data_file(master_filepath, 9)
    # ----
    with open(local_filepath, "w") as f:
        for mydict in master_weapon_items:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(local_filepath)

def add_consumable_to_player(player_name):
    print("Here are the players:")
    player_names = utils.get_all_player_names()
    [print(i) for i in player_names]
    print("----")
    print("Here are all the consumables in the game:")
    print(constants.CONSUMABLE_NAMES)
    print("----")
    print("Here are all the cpnsumables the player has:")
    player_consumables = utils.get_player_consumables_from_file(player_name)
    [print(i) for i in player_consumables]
    print("----")
    print("Which consumable would you like to give the player?")
    print("Here are your choices:")
    [print(i) for i in constants.CONSUMABLE_NAMES]
    consumable_name = ""
    if not consumable_name in constants.CONSUMABLE_NAMES:
        consumable_name = input("> ").lower().strip()
        if consumable_name in ["q", "quit"]:
            print("Goodbye!")
            sys.exit()
    print("You chose the consumable: {}".format(consumable_name))
    if consumable_name in player_consumables:
        s = "The player, {}, already has this weapon ({})!!"
        s = s.format(player_name.upper(), consumable_name.upper())
        raise ValueError(s)
    # ----------------------------------
    # ---- Getting the list of dictionaries ----
    master_filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
    consumables_list = utils.read_data_file(master_filepath, 9)
    target_dict = utils.get_dict(consumables_list, "name", consumable_name)
    if target_dict is None: raise ValueError("Error!")
    # ----
    # target_dict = {}
    # for mydict in weapons_list:
    #     for key, value in mydict.items():
    #         if key == "name" and value == weapon_name:
    #             target_dict = mydict
    #             break
    if len(target_dict) == 0:
        raise ValueError("Error")
    # ----
    # Checking to make sure that target_dict isn't in weapons_list
    # ----
    player_consumables_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    player_consumables = utils.read_data_file(player_consumables_filepath, 9)
    for mydict in player_consumables:
        for key, value in mydict.items():
            if key == "name" and "value" == consumable_name:
                s = "Error! The player ({}) already has this weapon ({})"
                s = s.format(player_name, consumable_name)
                raise ValueError(s)
    # ----
    # Giving the target dict to the player
    # ----
    # target_dict["index"] = target_dict["index"]
    # player_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    # player_consumables_list = utils.read_data_file(player_filepath, 11)
    player_consumables.append(target_dict)
    # ----
    print("--- This is what will be saved to the PLAYER'S file. Please read. carefully!!!! ----")
    [print(i) for i in player_consumables]
    user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
    if not user_input in ["y", "yes"]:
        print("Goodbye!")
        sys.exit()
    # ----
    debug_file = os.path.join("data", "testing.txt")
    player_filepath = debug_file
    with open(player_filepath, "w") as f:
        for mydict in player_consumables:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(player_filepath)

def add_consumable_to_game():
    # getting index
    filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
    mylist = utils.read_data_file(filepath, 9)
    new_index = utils.get_highest_index(mylist) + 1
    # ----
    user_input = ""
    while not user_input in ["y", "n", "yes", "no"]:
        print("Would you like to read in the information from a file?")
        print("data/input_templates/new_consumable_data.txt")
        user_input = input("(y/n) > ").lower().strip()
        if user_input == "quit":
            print("Goodbye!")
            sys.exit()
    # ----------------------------------
    new_consumable_dict = {}
    if not user_input in ["y", "yes"]:
        new_consumable_dict = _get_user_input()
    else:
        new_consumable_dict = _get_data_from_file("new_consumable_data.txt")
    # ----------------------------------
    # print(new_consumable_dict)
    # raise NotImplemented
    print("New index: {}".format(new_index))
    new_dict = {"index": new_index}
    new_consumable_dict.update(new_dict)
    # new_weapon_dict["index"] = new_index
    print("New index added ...")
    # ---- Checking to make sure everything is okay ---
    new_consumable = Consumable(new_consumable_dict)
    new_consumable.debug_print()
    # -------------------------------------------------
    print("---- New Weapon Data ----")
    new_consumable.debug_print()
    user_input2 = input("Add this NEW data to the master consumables list? (y/n) > ").lower().strip()
    if not user_input2 in ['y', 'yes']:
        print("Goodbye!")
        sys.exit()
    # ----
    master_filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
    consumables_list = utils.read_data_file(master_filepath, 9)
    consumables_list.append(new_consumable_dict)
    print("--- This is what will be saved to the MASTER file. Please read carefully!!!! ----")
    [print(i) for i in consumables_list]
    user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
    if not user_input in ["y", "yes"]:
        print("Goodbye!")
        sys.exit()
    # ----
    # debug_file = os.path.join("data", "testing.txt")
    # master_filepath = debug_file
    with open(master_filepath, "w") as f:
        for mydict in consumables_list:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(master_filepath)
    # ----
    all_player_characters = utils.get_all_player_names()
    for a_player_name in all_player_characters:
        local_filepath = os.path.join("data", "playing_characters", a_player_name, "npc_inventories", "consumable_items.txt")
        copyfile(master_filepath, local_filepath)
        print("The record was written successfully to the file:")
        print(local_filepath)
    # ----
    for profession in constants.PROFESSION_NAMES:
        player_master_path = os.path.join("data", "master_files", "player_types", profession, "npc_inventories", "consumable_items.txt")
        copyfile(master_filepath, player_master_path)

# ========================================
#     Add Weapons
# ========================================

def _get_user_input():
    u1 = "weapon_kind"
    u2 = "name"
    u3 = "quality"
    u4 = "cost"
    u5 = "top_damage"
    u6 = "minimum_damage"
    u7 = "filename"
    u8 = "core_item"
    u9 = "units"
    u10 = "range_of_effect"
    mydict = {}
    mylist = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
    for item in mylist:
        if item == "quality":
            print("Possible values:\n{}".format(constants.QUALITY))
        elif item == "weapon_kind":
            print("Possible weapon kinds:\n{}".format(constants.WEAPON_KINDS))
        elif item == "name":
            print("Possible weapon names:\n{}".format(constants.WEAPON_NAMES))
        elif item == "top_damage":
            print("Possible values:\n{}".format(constants.DAMAGE))
        elif item == "minimum_damage":
            print("Possible values:\n{}".format(constants.DAMAGE))
        # ----
        print("{}:".format(item))
        user_input = input("> ").lower().strip()
        if user_input in ["q", "quit"]:
            print("This is what you entered:")
            print(mydict)
            print("Goodbye!")
            sys.exit()
        # ----
        if item == "quality":
            if utils.is_int(user_input) == False:
                print("Sorry! That doesn't seem to be an integer. Goodbye!")
                sys.exit()
            user_input = int(user_input)
            if not user_input in constants.QUALITY:
                print("Sorry! This won't work as a QUALITY: {}".format(constants.QUALITY))
                sys.exit()
        elif item == "top_damage":
            if utils.is_int(user_input) == False:
                print("Sorry! That doesn't seem to be an integer. Goodbye!")
                sys.exit()
            user_input = int(user_input)
            if not user_input in constants.DAMAGE:
                print(constants.DAMAGE)
                print("Sorry! That doesn't seem to be a valid DAMAGE. Goodbye!")
                sys.exit()
        elif item == "filename":
            if user_input.find(".png") == -1:
                user_input = "{}.png".format(user_input)
            if utils.image_filepath_exists(user_input.lower().strip()) == False:
                print("Sorry, this ({}) doesn't seem to be a valid name for an image file.".format(user_input))
                sys.exit()
        # ----
        mydict[item] = user_input
    print(mydict)
    # raise NotImplemented
    return mydict

def _get_data_from_file(filename):
    data_filepath = os.path.join("data", "input_templates", filename)
    if utils.is_file(data_filepath) == False:
        print("Doh! That's not a valid path!!")
        print(data_filepath)
        sys.exit()
    return utils.read_file(data_filepath)[0]

def add_weapon_to_game():
    # getting index
    filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    mylist = utils.read_data_file(filepath, 11)
    new_index = utils.get_highest_index(mylist) + 1
    # ----
    user_input = ""
    while not user_input in ["y", "n", "yes", "no"]:
        print("Would you like to read in the information from a file? (y/n)")
        print("The file name: data/input_templates/new_weapon_data.txt")
        user_input = input("(y/n) > ").lower().strip()
        if user_input == "quit":
            print("Goodbye!")
            sys.exit()
    # ----------------------------------
    new_weapon_dict = {}
    if not user_input in ["y", "yes"]:
        new_weapon_dict = _get_user_input()
    else:
        filename = "new_weapon_data.txt"
        new_weapon_dict = _get_data_from_file(filename)
    # ----
    # CHECK TO MAKE SURE THE NAME IS NOT A DUPLICATE
    all_weapon_names = utils.get_all_weapon_names()
    if new_weapon_dict["name"].lower().strip() in all_weapon_names:
        s = "Error. This name has already been used: {}".format(new_weapon_dict["name"])
        raise ValueError(s)
    # ----------------------------------
    # print("new_weapon_dict: {}".format(new_weapon_dict))
    # [print(key, value) for key, value in new_weapon_dict.items()]
    print("New index: {}".format(new_index))
    new_dict = {"index": new_index}
    new_weapon_dict.update(new_dict)
    # new_weapon_dict["index"] = new_index
    print("New index added ...")
    # ---- Checking to make sure everything is okay ---
    new_weapon = Weapon(new_weapon_dict)
    new_weapon.debug_print()
    # -------------------------------------------------
    print("---- New Weapon Data ----")
    new_weapon.debug_print()
    user_input2 = input("Add this NEW data to the master weapons list? (y/n) > ").lower().strip()
    if not user_input2 in ['y', 'yes']:
        print("Goodbye!")
        sys.exit()
    # ----
    master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    weapons_list = utils.read_data_file(master_filepath, 11)
    weapons_list.append(new_weapon_dict)
    print("--- This is what will be saved to the MASTER file. Please read. carefully!!!! ----")
    [print(i) for i in weapons_list]
    user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
    if not user_input in ["y", "yes"]:
        print("Goodbye!")
        sys.exit()
    # ----
    # debug_file = os.path.join("data", "testing.txt")
    with open(master_filepath, "w") as f:
        for mydict in weapons_list:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(master_filepath)
    # ----
    print("Writing the new weapon to the inventories")
    print("of all the NPCs that are in player's character's")
    print("NPC directories.")
    all_player_characters = utils.get_all_player_names()
    for player_name in all_player_characters:
        filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "weapon_items.txt")
        copyfile(master_filepath, filepath)
        # with open(filepath, "w") as f:
        #     for mydict in weapons_list:
        #         s = ""
        #         for key, value in mydict.items():
        #             s += "{}: {}\n".format(key, value)
        #         s += "\n"
        #         f.write(s)
    for profession in constants.PROFESSION_NAMES:
        player_master_path = os.path.join("data", "master_files", "player_types", profession, "npc_inventories", "weapon_items.txt")
        copyfile(master_filepath, player_master_path)

def add_weapon_to_player(player_name):
    raise NotImplemented
    print("Here are the players:")
    player_names = utils.get_all_player_names()
    [print(i) for i in player_names]
    print("----")
    print("Here are all the weapons in the game:")
    print(constants.WEAPON_NAMES)
    print("----")
    print("Here are all the weapons the player has:")
    player_weapons = utils.get_player_weapons_from_file(player_name)
    [print(i) for i in player_weapons]
    print("----")
    print("Which weapon would you like to give the player?")
    print("Here are your choices:")
    [print(i) for i in constants.WEAPON_NAMES]
    weapon_name = ""
    if not weapon_name in constants.WEAPON_NAMES:
        weapon_name = input("> ").lower().strip()
        if weapon_name in ["q", "quit"]:
            print("Goodbye!")
            sys.exit()
    print("You chose the weapon: {}".format(weapon_name))
    if weapon_name in player_weapons:
        s = "The player, {}, already has this weapon ({})!!"
        s = s.format(player_name.upper(), weapon_name.upper())
        raise ValueError(s)
    # ----------------------------------
    # ---- Getting the list of dictionaries ----
    master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    weapons_list = utils.read_data_file(master_filepath, 11)
    target_dict = utils.get_dict(weapons_list, "name", weapon_name)
    if target_dict is None: raise ValueError("Error!")
    # ----
    # target_dict = {}
    # for mydict in weapons_list:
    #     for key, value in mydict.items():
    #         if key == "name" and value == weapon_name:
    #             target_dict = mydict
    #             break
    if len(target_dict) == 0:
        raise ValueError("Error")
    # ----
    # Checking to make sure that target_dict isn't in weapons_list
    # ----
    player_weapons_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    player_weapons = utils.read_data_file(player_weapons_filepath, 11)
    for mydict in player_weapons:
        for key, value in mydict.items():
            if key == "name" and "value" == weapon_name:
                s = "Error! The player ({}) already has this weapon ({})"
                s = s.format(player_name, weapon_name)
                raise ValueError(s)
    # ----
    # Giving the target dict to the player
    # ----
    target_dict["index"] = target_dict["index"]
    player_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    player_weapons_list = utils.read_data_file(player_filepath, 11)
    player_weapons_list.append(target_dict)
    # ----
    print("--- This is what will be saved to the PLAYER'S file. Please read. carefully!!!! ----")
    [print(i) for i in player_weapons_list]
    user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
    if not user_input in ["y", "yes"]:
        print("Goodbye!")
        sys.exit()
    # ----
    # debug_file = os.path.join("data", "testing.txt")
    with open(player_filepath, "w") as f:
        for mydict in player_weapons_list:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(player_filepath)

def add_weapon_to_npc(player_name):
    update_npc_weapons(player_name=player_name)

def update_npc_weapons(player_name):
    """
    All we need to do is update the inventories in npc_inventories
    since no npc currently has a unique inventory. Although they COULD
    have unique inventories by player character. So, for example, the
    npc's inventories in Henry's npc_inventory directory could be
    different from the inventories in another character's inventory.
    """
    # todo: Implement inventories for each npc character.
    if player_name is None or len(player_name) == 0:
        raise ValueError("Error")
    if utils.validate_player_name(player_name) == False:
        raise ValueError("Error")
    master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    local_filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "weapon_items.txt")
    master_weapon_items = utils.read_data_file(master_filepath, 11)
    # ----
    # local_filepath = os.path.join("data", "testing.txt")
    with open(local_filepath, "w") as f:
        for mydict in master_weapon_items:
            s = ""
            for key, value in mydict.items():
                s += "{}: {}\n".format(key, value)
            s += "\n"
            f.write(s)
    # ------------------------------------------------
    print("The record was written successfully to the file:")
    print(local_filepath)

    # npc_names = utils.get_all_npc_names_by_player(player_name)
    # if npc_name is None:
    #     if npc_names is None: raise ValueError("Error")
    #     if len(npc_names) == 0: raise ValueError("Error")
    #     # ----
    #     print("Here are all the names of {}")
    #     [print(i) for i in npc_names]
    #     npc_name = input("> ").lower().strip()
    # # ----
    # if not npc_name in npc_names: raise ValueError("Error")
    # # ---- ----
    # print("Here are all the weapons in the game:")
    # print(constants.WEAPON_NAMES)
    # print("----")
    # print("Here are all the weapons the npc ({}) has:".format(npc_name.upper()))
    # player_weapons = utils.get_npc_weapons_from_local_file(player_name=player_name)
    # [print(i) for i in player_weapons]
    # print("----")
    # print("Which weapon would you like to give the player?")
    # print("Here are your choices:")
    # [print(i) for i in constants.WEAPON_NAMES]
    # weapon_name = ""
    # if not weapon_name in constants.WEAPON_NAMES:
    #     weapon_name = input("> ").lower().strip()
    #     if weapon_name in ["q", "quit"]:
    #         print("Goodbye!")
    #         sys.exit()
    # print("You chose the weapon: {}".format(weapon_name))
    # if weapon_name in player_weapons:
    #     s = "The player, {}, already has this weapon ({})!!"
    #     s = s.format(player_name.upper(), weapon_name.upper())
    #     raise ValueError(s)
    # # ----------------------------------
    # # ---- Getting the list of dictionaries ----
    # master_filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    # weapons_list = utils.read_data_file(master_filepath, 11)
    # target_dict = utils.get_dict(weapons_list, "name", weapon_name)
    # if target_dict is None: raise ValueError("Error!")
    # # ----
    # # target_dict = {}
    # # for mydict in weapons_list:
    # #     for key, value in mydict.items():
    # #         if key == "name" and value == weapon_name:
    # #             target_dict = mydict
    # #             break
    # if len(target_dict) == 0:
    #     raise ValueError("Error")
    # # ----
    # # Checking to make sure that target_dict isn't in weapons_list
    # # ----
    # player_weapons_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    # player_weapons = utils.read_data_file(player_weapons_filepath, 11)
    # for mydict in player_weapons:
    #     for key, value in mydict.items():
    #         if key == "name" and "value" == weapon_name:
    #             s = "Error! The player ({}) already has this weapon ({})"
    #             s = s.format(player_name, weapon_name)
    #             raise ValueError(s)
    # # ----
    # # Giving the target dict to the player
    # # ----
    # target_dict["index"] = target_dict["index"]
    # player_filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    # player_weapons_list = utils.read_data_file(player_filepath, 11)
    # player_weapons_list.append(target_dict)
    # # ----
    # print("--- This is what will be saved to the PLAYER'S file. Please read. carefully!!!! ----")
    # [print(i) for i in player_weapons_list]
    # user_input = input("This is the ENTIRE file. Accept this? (y/n) > ")
    # if not user_input in ["y", "yes"]:
    #     print("Goodbye!")
    #     sys.exit()
    # # ----
    # # debug_file = os.path.join("data", "testing.txt")
    # with open(player_filepath, "w") as f:
    #     for mydict in player_weapons_list:
    #         s = ""
    #         for key, value in mydict.items():
    #             s += "{}: {}\n".format(key, value)
    #         s += "\n"
    #         f.write(s)
    # # ------------------------------------------------
    # print("The record was written successfully to the file:")
    # print(master_filepath)

def test_consumables():
    myclass = Consumables("player", "henry")
    myclass.read_data()
    myclass.debug_print()

def test_weapons(player_name, npc_name, character_type):
    myclass = Weapons(player_name=player_name, npc_name=npc_name, character_type=character_type)
    myclass.read_data()
    print("=====================")
    myitem = myclass.get_item_by_name("gold ring")
    myitem.debug_print()
    # myclass.add_item_by_name("gold ring", 2)
    # myclass.save_data()
    # myclass.remove_item_by_name("gold ring", 1)
    # myclass.remove_item(5)
    # myclass.debug_print()
    # myclass.remove_item(5)
    # myclass.remove_item(index=2)
    # myclass.debug_print()

# def test_inventory(player_name, npc_name, character_type):
#     myinventory =

def goodbye():
    print("Goodbye!")
    sys.exit()

# ***************************************************
# ***************************************************

def main(zone_name, map_name, player_name):
    if not zone_name in constants.ZONE_NAMES:
        raise ValueError("Error")
    if not map_name in constants.MAP_CHOICES:
        raise ValueError("Error")
    # ====================
    print("What would you like to do?")
    """
    Note: If you want to add a NEW item to the game
    you will need to add it to the constants.py module, 
    specifically to WEAPON_NAMES: constants.WEAPON_NAMES.
    """
    if len(player_name) == 0:
        player_names = utils.get_all_player_names()
        # print(player_names)
        # print("Player name:")
        while not player_name in player_names:
            player_name = input("> ").lower().strip()
            if player_name in ["q", "quit"]:
                print("Goodbye!")
                sys.exit()
    choices = ["Add a weapon to the GAME", "Add a weapon to a PLAYER"]
    choices += ["Update the weapons a player's NPCs have"]
    choices += ["Add a consumable to the GAME", "Add a consumable to a PLAYER"]
    choices += ["Update the consumables a player's NPCs have"]
    choices += ["Add an NPC", "Add a map tile to the game"]
    choices += ["Print out all items, both weapons and consumables"]
    choices += ["Print out all NPCs (master NPCs)"]
    choices += ["Print out all quests"]
    choices += ["Print out all accepted quests"]
    choices += ["Print out all completed quests"]
    choices += ["Print out contents of player inventory"]
    choices += ["Get a list of all unused tile names"]
    choices += ["Make a new conversation (in zone_name/map_name/conversations)"]
    choices += ["Make a new zone map"]
    choices += ["Search all text files in the data directory for a certain phrase"]
    choices += ["Reset conversation"]
    choices += ["Reset all conversations in map (unfinished)"]
    choices += ["Reset all conversations in zone (unfinished)"]
    choices += ["Reset all conversations"]
    choices += ["Reset player"]
    choices += ["Reset everything"]
    choices += ["Reset player gold"]
    choices += ["Create the name of a town"]
    choices += ["Create the name of an NPC"]
    choices += ["Get least used letter"]
    choices += ["Find an image file"]
    choices += ["Conversations: Make placeholders"]
    # ----
    print("Would you like to...")
    [print("{}) {}".format(count+1, i)) for count, i in enumerate(choices)]
    myinput = -10
    choice_numbers = list(range(1, len(choices)+1))
    while not myinput in choice_numbers:
        myinput = input("> ").lower().strip()
        if myinput in ["q", "quit"]: sys.exit()
        if utils.is_int(myinput) == True:
            myinput = int(myinput)
    myinput = myinput - 1
    user_text = choices[myinput]
    print("user_text: {}".format(user_text))
    # ---- ---- ---- ----
    if user_text == "Add a weapon to the GAME":
        add_weapon_to_game()
    elif user_text == "Add a weapon to a PLAYER":
        add_weapon_to_player(player_name=player_name)
    elif user_text == "Update the weapons a player's NPCs have":
        add_weapon_to_npc(player_name)
    # ----
    elif user_text == "Add a consumable to the GAME":
        add_consumable_to_game()
    elif user_text == "Add a consumable to a PLAYER":
        add_consumable_to_player(player_name=player_name)
    elif user_text == "Update the consumables a player's NPCs have":
        add_consumable_to_npc(player_name=player_name)
    elif user_text == "Add an NPC":
        add_npc(zone_name, map_name)
    elif user_text == "Add a map tile to the game":
        add_map_tile()
    elif user_text == "Print out all items, both weapons and consumables":
        print_out_inventory_items()
    elif user_text == "Print out all NPCs (master NPCs)":
        print_put_NPC_names()
    elif user_text == "Print out all quests":
        mylist = utils.get_all_quests()
        [print(i) for i in mylist]
    elif user_text == "Print out all accepted quests":
        utils.get_accepted_quests()
    elif user_text == "Print out all completed quests":
        utils.get_completed_quests()
    elif user_text == "Print out contents of player inventory":
        print_out_player_inventory()
    elif user_text == "Get a list of all unused tile names":
        print(get_unused_map_tile_names())
    elif user_text == "Make a new zone map":
        make_a_new_zone_map()
    elif user_text == "Make a new conversation (in zone_name/map_name/conversations)":
        make_a_new_conversation()
    elif user_text == "Search all text files in the data directory for a certain phrase":
        search_for_phrase()
    elif user_text == "Reset conversation":
        reset_conversation()
    elif user_text == "Reset all conversations in map (unfinished)":
        raise NotImplemented
    elif user_text == "Reset all conversations in zone (unfinished)":
        raise NotImplemented
    elif user_text == "Reset all conversations":
        reset_all_conversations()
    elif user_text == "Reset player":
        reset_player()
    elif user_text == "Reset everything":
        reset_everything()
    elif user_text == "Reset player gold":
        reset_player_gold()
    elif user_text == "Create the name of a town":
        create_the_name_of_a_town()
    elif user_text == "Create the name of an NPC":
        names = create_the_name_of_an_NPC()
        [print(i) for i in names]
    elif user_text == "Get least used letter":
        letter = utils.get_least_used_letter()
        print("Least used letter: {}".format(letter))
    elif user_text == "Find an image file":
        find_an_image_file()
    elif user_text == "Conversations: Make placeholders":
        conversations_make_placeholders()
    else:
        s = "I don't understand this: {}".format(user_text)
        raise ValueError(s)

if __name__ == "__main__":
    # create_the_name_of_a_town()
    main(zone_name="provisioner", map_name="map00", player_name="henry")
    # create_the_name_of_an_NPC()
    # reset_player_gold()
    # # print_put_NPC_names()
    # _add_map_tile_from_user_input()
    # add_map_tile()
    # reset_all_conversations()