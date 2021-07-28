import constants
import os, sys
from shutil import copyfile
import math

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def key_value(mystring, mydict):
    # print("mystring: {}".format(mystring))
    myint = mystring.find(":")
    if myint == -1:
        s = "Error! A colon (:) was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error")
    if len(value) == 0:
        raise ValueError("Error: there is no value. Here is mystring: {}".format(mystring))
    try:
        mydict[tag] = int(value) if is_int(value) else value
    except Exception as e:
        print("tag: {}; value: {}".format(tag, value))
        raise ValueError(e)
    return mydict

def copy_original_player_files(profession_type, character_name):
    basepath = os.path.join("data", "master_files", "player_types", profession_type)
    destination = os.path.join("data", "playing_characters", character_name)
    copy_directory(basepath, destination)

def get_players_position_on_map():
    x, y = -1, -1
    filepath = os.path.join("data", constants.MAPFILE)
    with open(filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    for col, tiles in enumerate(mytiles):
        for row, tile in enumerate(tiles):
            if tile == 'p':
                x = row
                y = col
    return x, y

def read_data_file(filepath, num_of_fields):
    print("opening filepath in utils.py-->read_data_file: {}".format(filepath))
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    # print("Here is mylines: {}".format(mylines))
    # print("------------------")
    # [print(i) for i in mylines]
    big_list = []
    for i in range(0, len(mylines), num_of_fields):
        mydict = {}
        for j in range(num_of_fields):
            # print("i + j: {}".format(i + j))
            elem = mylines[i + j]
            mydict = key_value(elem, mydict)
        big_list.append(mydict)
    return big_list

def read_file(filepath):
    print("opening filepath in utils.py-->read_file: {}".format(filepath))
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    # print("Here is mylines: {}".format(mylines))
    if len(mylines) == 0:
        raise ValueError("Error!")
    # ----
    big_list = []
    num_of_fields = len(mylines)
    for i in range(0, len(mylines), num_of_fields):
        mydict = {}
        for j in range(num_of_fields):
            # print("i + j: {}".format(i + j))
            elem = mylines[i + j]
            mydict = key_value(elem, mydict)
        big_list.append(mydict)
    return big_list

def get_record(filepath, key_name, value_name, number_of_fields):
    mylist = read_data_file(filepath, number_of_fields)
    for elem in mylist:
        if elem[key_name] == value_name:
            return elem
    return None

def convert_direction_to_integer(the_direction):
    if not the_direction.lower() in ["down", "up", "right", "left"]:
        raise ValueError("I don't recognize this: {}".format(the_direction))
    the_direction = the_direction.lower()
    myint = ""
    if the_direction == "up":
        myint = 90
    elif the_direction == "down":
        myint = -90
    elif the_direction == "right":
        myint = 0
    elif the_direction == "left":
        myint = 180
    else:
        s = "This was not found: {}".format(the_direction)
        raise ValueError(s)
    return myint

def convert_integer_to_direction(my_int):
    if type(my_int) == type("abc"):
        raise ValueError("my_int is actually of type string: {}".format(my_int))
    if type(my_int) != type(123):
        s = "Error! myint: {} ({})".format(my_int, type(my_int))
        raise ValueError(s)
    #----
    the_dir = ""
    if my_int == 90:
        the_dir = "UP"
    elif my_int == -90:
        the_dir = "DOWN"
    elif my_int == 0:
        the_dir = "RIGHT"
    elif my_int == 180:
        the_dir = "LEFT"
    else:
        raise ValueError("Error! I don't recognize this: {}".format(my_int))
    return the_dir

def get_player_position_from_map(filepath):
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    big_list = []
    for i, line in enumerate(mylines):
        for j, element in enumerate(line):
            # print(i, j, element)
            if element == "p":
                return j, i
    raise ValueError("Player not found!")

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def _top_height(text_list, font):
    if not type(text_list) == type([]):
        raise ValueError("Error")
    tallest = -1
    for elem in text_list:
        try:
            _, text_height = font.size(elem)
        except:
            raise ValueError(elem)
        if text_height > tallest:
            tallest = text_height
    return tallest

def talk_dialog(screen, text, font, width_offset, height_offset, line_length=32, color=(0,0,0)):
    # text_list = separate_text_into_lines(text, line_length)
    text_list = []
    if type(text) == type("bla"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        for line in text:
            temp = separate_text_into_lines(line, line_length)
            text_list += temp
    else:
        s = "Doh! That type of data shouldn't be here!"
        raise ValueError(s)
    # ----------------------
    text_height = _top_height(text_list, font) + 3
    top = -1
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))
    return top

def get_user_data():
    filepath = os.path.join("data", "user_data.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
    mydict = {}
    for a_line in mylines:
        mydict = key_value(a_line, mydict)
    # ----
    # error checking
    if len(mydict["character_name"].strip()) == 0:
        raise ValueError("Error!")
    elif len(mydict["zone_name"].strip()) == 0:
        raise ValueError("Error!")
    elif len(mydict["map_name"].strip()) == 0:
        raise ValueError("Error!")
    return mydict

# def character_name_valid(char_name):
#     filepath = os.path.join("data", "playing_characters")
#     myfiles = os.listdir(filepath)
#     name_list = []
#     for elem in myfiles:
#         print("elem: {}; char_name: {}".format(elem, char_name))
#         if os.path.isdir(os.path.join(filepath, elem)):
#             name_list.append(elem)
#     print("name list: {}".format(name_list))
#     if char_name in name_list:
#         return True
#     return False

def validate_name(name):
    filepath = os.path.join("data", "playing_characters")
    name_list = get_subdirectories(filepath)
    # print(name_list)
    if name.lower().strip() in name_list:
        return True
    return False

def validate_merchant_name(npc_name):
    npc_name = npc_name.replace(" ", "_")
    # ----
    filepath = os.path.join("data", "master_files", "npcs")
    directory_contents = os.listdir(filepath)
    if directory_contents is None:
        raise ValueError("Error!")
    if len(directory_contents) == 0:
        raise ValueError("Error!")
    # print("name_list: {}".format(directory_contents))
    mylist = []
    for name in directory_contents:
        if name.find("npc") == -1:
            mylist.append(name[:-4])
    if npc_name.lower().strip() in mylist:
        return True
    return False

def set_user_data(char_name, zone_name, map_name, profession_name):
    if not validate_name(char_name):
        raise ValueError('Error!')
    if not zone_name in constants.ZONE_NAMES:
        s = "This isn't a zone name: {}"
        s += "If this is coming from a Trigger or Action, "
        s += "make sure that the ZONE_NAME in the Trigger or Action is spelled properly."
        s = s.format(zone_name)
        raise ValueError(s)
    if not profession_name.lower() in constants.CHAR_KINDS:
        raise ValueError("{} is not in {}".format(profession_name, constants.CHAR_KINDS))
    if not map_name in constants.MAP_CHOICES:
        raise ValueError("That's NOT a proper map name: {}".format(map_name))
    # ----
    s = "character_name: {}\nzone_name: {}\nmap_name: {}\nprofession_name: {}\n"
    s = s.format(char_name.lower().strip(), zone_name.lower().strip(),
                 map_name.lower().strip(), profession_name.lower().strip())
    filepath = os.path.join("data", "user_data.txt")
    with open(filepath, "w") as f:
        f.write(s)

def order_valid(user_text):
    print("mystring: {}".format(user_text))
    mylist = user_text.split(" ")
    mylist = [i.lower().strip() for i in mylist if len(i.strip()) > 0]
    if len(mylist) != 4:
        s = "Looks like something went wrong. This needs to be FOUR terms, you entered {}. Here's what has been entered: {}".format(len(mylist), user_text)
        return False
    # ----
    if not mylist[0] in ["b", "s"]:
        print("Error! The first term needs to be either b or s. You entered: {}".format(mylist[0]))
        return False
    if not mylist[1] in constants.DISCRIPTION_01:
        print("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[1], constants.DISCRIPTION_01))
        return False
    if not mylist[2] in constants.DISCRIPTION_02:
        print("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[2], constants.DISCRIPTION_02))
        return False
    if not is_int(mylist[3]):
        print("Error! The number of items you desire to buy must be an integer.")
        return False
    return True

def parse_player_purchase(mystring):
    print("mystring: {}".format(mystring))
    mylist = mystring.split(" ")
    mylist = [i.lower().strip() for i in mylist if len(i.strip()) > 0]
    # if len(mylist) != 4:
    #     s = "Looks like something went wrong. This needs to be FOUR terms, you entered {}. Here's what has been entered: {}".format(len(mylist), mystring)
    #     raise ValueError(s)
    # # ----
    # if not mylist[0] in ["b", "s"]:
    #     raise ValueError("Error! The first term needs to be either b or s. You entered: {}".format(mylist[0]))
    # if not mylist[1] in constants.DISCRIPTION_01:
    #     raise ValueError("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[1], constants.DISCRIPTION_01))
    # if not mylist[2] in constants.DISCRIPTION_02:
    #     raise ValueError("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[2], constants.DISCRIPTION_02))
    # if not is_int(mylist[3]):
    #     raise ValueError("Error! The number of items you desire to buy must be an integer.")
    # ----------------------------------
    new_list = ["0", "0", "0"]
    if mylist[0] == "b":
        new_list[0] = "buy"
    else:
        new_list[0] = "sell"
    new_list[1] = "{} {}".format(mylist[1], mylist[2])
    if not new_list[1] in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
        raise ValueError("Error!")
    new_list[2] = int(mylist[3])
    return new_list

def format_string(string_title, my_divider="-", length=50):
    if length < len(string_title):
        raise ValueError("length ({}) < len(string_title) ({})".format(length, len(string_title)))
    new_length = int((length - len(string_title)) / 2)
    s = "{} {} {}".format(my_divider * new_length, string_title, my_divider * new_length)
    return s, len(s)

def get_merchant_inventory_data(merchant_name, kind):
    """
    Retrieves the inventory of a specific merchant.
    :param merchant_name: the name of the merchant
    :return: A list of dictionaries
    """
    user_data = get_user_data()
    filename = "{}.txt".format(merchant_name)
    filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs", filename)
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    my_dictionaries = []
    inventory_list = []
    for a_line in mylines:
        this_line = a_line.split(":")
        if this_line[0] == "inventory":
            # print(a_line)
            myint = a_line.find("inventory:")
            myposition = myint + len("inventory:")
            new_line = a_line[myposition:].strip()
            # print(new_line)
            inventory_list.append(new_line)
    new_list = []
    for elem in inventory_list:
        mylist = elem.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        mydict = {}
        for an_element in mylist:
            mydict = key_value(an_element, mydict)
        new_list.append(mydict)
    big_list = []
    for a_dict in new_list:
        if a_dict["kind"] == kind:
            big_list.append(a_dict)
    return big_list

def _pad_string(mystring, desired_length):
    s = mystring
    if len(s) < desired_length:
        while len(s) < desired_length:
            s += "-"
    elif len(s) > desired_length:
        s = s[0:desired_length]
    return s

def format_npc_goods(npc_goods):
    mylist = []
    for elem in npc_goods:
        s = "{}) {}".format(elem[0], elem[1])
        mylist.append(s)
    return mylist

def format_inventory_list(mylist):
    new_list = []
    for count, elem in enumerate(mylist):
        s = "{}: ({}) {} - {}".format(elem[0], elem[2], elem[3], elem[1])
        new_list.append([count+1, s])
    return new_list

def get_number_range(npc_goods):
    mylist = []
    for elem in npc_goods:
        mylist.append(elem[0])
    return mylist

def get_subdirectories(filepath):
    directory_contents = os.listdir(filepath)
    # print(directory_contents)
    # ----
    mylist = []
    for item in directory_contents:
        # print("item: {}".format(item))
        temp = os.path.join(filepath, item)
        if os.path.isdir(temp):
            mylist.append(item)
    return mylist

def distance_between_two_points(A, B):
    dA = B[0] - A[0]
    dB = B[1] - A[1]
    dA = dA * dA
    dB = dB * dB
    return math.sqrt(dA + dB)

def zone_previously_entered(player_name, zone_name):
    filepath = os.path.join("data", "playing_characters", player_name, "zones_visited.txt")
    mydict = read_file(filepath)[0]
    # ----
    if not mydict[zone_name] in constants.ZONE_INIT_VALUES:
        raise ValueError("Error! mydict[zone_name]: {}".format(mydict[zone_name]))
    if mydict[zone_name] == "visited":
        return True
    elif mydict[zone_name] == "never_visited":
        return False
    else:
        raise ValueError("Error!")

def zone_already_entered():
    user_data = get_user_data()
    character_name = user_data["character_name"]
    zone_name = user_data["zone_name"]
    # ----
    filepath = os.path.join("data", "playing_characters", character_name, "zones_visited.txt")
    mydict = read_file(filepath)[0]
    # ----
    print(mydict)
    if not mydict[zone_name] in constants.ZONE_INIT_VALUES:
        raise ValueError("Error! mydict[zone_name]: {}".format(mydict[zone_name]))
    if mydict[zone_name] == "visited":
        return True
    elif mydict[zone_name] == "never_visited":
        return False
    else:
        raise ValueError("Error!")

def mark_zone_as_visited():
    user_data = get_user_data()
    character_name = user_data["character_name"]
    zone_name = user_data["zone_name"]
    # ----
    filepath = os.path.join("data", "playing_characters", character_name, "zones_visited.txt")
    mydict = read_file(filepath)[0]
    # ----
    mydict[zone_name] = "visited"
    # ----
    s = ""
    for key, value in mydict.items():
        # print("key: {}, value: {}".format(key, value))
        s += "{}: {}\n".format(key, value)
    print(s)
    # ----
    with open(filepath, "w") as f:
        f.write(s)

def mark_zone_as_never_visited():
    user_data = get_user_data()
    character_name = user_data["character_name"]
    zone_name = user_data["zone_name"]
    # ----
    filepath = os.path.join("data", "playing_characters", character_name, "init.txt")
    mylines = read_data_file(filepath, 9)
    mydict = mylines[0]
    # ----
    mydict[zone_name] = "never_visited"
    # ----
    s = ""
    for key, value in mydict.items():
        # print("key: {}, value: {}".format(key, value))
        s += "{}: {}\n".format(key, value)
    print(s)
    # ----
    with open(filepath, "w") as f:
        f.write(s)

def get_npc_name_from_map_code(zone_name, map_code):
    filepath = os.path.join("data", "zones", zone_name, "npc_name_lookup.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    mydict = {}
    for myline in mylines:
        mydict = key_value(myline, mydict)
    return mydict[map_code]

def get_line_height(list_of_text, font):
    line_height = -1
    for elem in list_of_text:
        try:
            text_width, text_height = font.size(elem)
        except:
            try:
                text_width, text_height = font.size(elem[0])
            except:
                raise ValueError("Error!")
        if text_height > line_height:
            line_height = text_height

def get_dictionary_for_master_npc(npc_name):
    npc_name = npc_name.replace(" ", "_")
    # ----
    user_data = get_user_data()
    # filepath = os.path.join("data", "playing_characters", user_data["character_name"], "npcs")
    # filepath = os.path.join("data", "zones", "testing", "merchants", "old_ben.txt")
    filepath = os.path.join("data", "master_files", "npcs", "merchants")
    target_name = ""
    file_names = os.listdir(filepath)
    for file_name in file_names:
        if file_name.find("npc") == -1:
            if file_name == "{}.txt".format(npc_name):
                target_name = file_name
    if len(target_name) == 0:
        # it could be a monster.
        filiepath = os.path.join("data", "master_files", "npcs", "monsters")
        for file_name in file_names:
            if file_name == "{}.txt".format(npc_name):
                target_name = file_name
    if len(target_name) == 0:
        raise ValueError("Error!")
    # ----
    # print("target name: {}".format(target_name))
    mylist = read_file(os.path.join(filepath, target_name))
    # print(mylist)
    return mylist[0]

# def set_free_events(zone_name, event_name, value):
#     # conversation_with_lamplighter_completed_successfully: False
#     filepath = os.path.join("data", "zones", zone_name, "events_completed.txt")
#     mylist = read_file(filepath)
#     mydict = mylist[0]
#     mydict[event_name] = value
#     with open(filepath, "w") as f:
#         for key, value in mydict.items():
#             s = "{}: {}".format(key, value)
#             # print(s)
#             f.write(s)

def read_free_events(zone_name, map_name):
    raise NotImplemented
    # conversation_with_lamplighter_completed_successfully: False
    filepath = os.path.join("data", "zones", zone_name, map_name, "events.txt")
    mylist = read_file(filepath)
    return mylist[0]

def save_free_events(zone_name, map_name, events):
    raise NotImplemented
    filepath = os.path.join("data", "zones", zone_name, map_name, "events.txt")
    with open(filepath, "w") as f:
        for key, value in events.items():
            s = "{}: {}".format(key, value)
            # print(s)
            f.write(s)

def only_alphabetical(mytext):
    s = ""
    for mychar in mytext:
        if mychar in constants.ALPHABET02:
            s += mychar
    return s

def get_filepath(filename):
    basepath = os.path.join("data", "images")
    # dir_contents = os.listdir(basepath)
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                return os.path.join(root, file)
            # print("root: {}".format(root))
            # print("file: {}".format(file))
    return None

def get_previous_map_name(map_name):
    myint = int(map_name[3:])
    myint -= 1
    if myint < 0: myint = 0
    s = ""
    if myint < 10:
        s = "map0{}".format(myint)
    else:
        s = "map{}".format(myint)
    return s

def get_next_map_name(map_name):
    myint = int(map_name[3:])
    myint += 1
    s = ""
    if myint < 10:
        s = "map0{}".format(myint)
    else:
        s = "map{}".format(myint)
    return s

def copy_directory(basepath, destination_directory):
    if not os.path.isdir(destination_directory):
        os.mkdir(destination_directory)
    # ----
    for root, dirs, files in os.walk(basepath):
        for dir in dirs:
            # print(os.path.join(root, dir))
            new_dir = os.path.join(destination_directory, dir)
            # print("new_path: {}".format(new_path))
            if not os.path.isdir(new_dir):
                print("new_dir: {}".format(new_dir))
                os.mkdir(new_dir)
        # ----
        for file in files:
            master_path = os.path.join(root, file)
            new_path = master_path.replace(basepath, destination_directory)
            copyfile(master_path, new_path)

def map_tile_names_walkable_get_new_name():
    used_letters = []
    for elem in constants.MAP_TILE_NAMES_WALKABLE:
        if elem[:-1] in constants.ALPHABET:
            used_letters.append(elem[:-1])
    mylist = []
    for a_char in constants.ALPHABET:
        if not a_char in used_letters:
            mylist.append(a_char)
    return mylist

def reset_zones_visited(player_name):
    s = ""
    for zone_name in constants.ZONE_NAMES:
        s += "{}: never_visited\n".format(zone_name)
    filepath = os.path.join("data", "playing_characters", player_name, "zones_visited.txt")
    with open(filepath, "w") as f:
        f.write(s)

def get_player_map_coords(map_filepath):
    with open(map_filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    mytiles = [i[3:] for i in mytiles[2:]]
    # [print(i) for i in mytiles]
    # ----
    for col, tiles in enumerate(mytiles):
        list_tiles = tiles.split(";")
        list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
        # print(list_tiles)
        # print("-----------------------")
        for row, tile in enumerate(list_tiles):
            # print(tile)
            if not tile.find("p") == -1:
                return row, col
    return None, None

def get_map_xy_for_player(zone_name, map_name):
    if len(zone_name) == 0 or len(map_name) == 0:
        raise ValueError("Error!")
    if not zone_name in constants.ZONE_NAMES:
        raise ValueError("Error")
    # ----
    filename = "{}_npcs.txt".format(map_name)
    filepath = os.path.join("data", "zones", zone_name, map_name, filename)
    print("In utils.py def get_map_xy_for_player. Filepath: {}".format(filepath))
    with open(filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    mytiles = [i[3:] for i in mytiles[2:]]
    # [print(i) for i in mytiles]
    # ------------------------------------------------------------------
    big_list = []
    for col, tiles in enumerate(mytiles):
        tile_list = tiles.split(";")
        tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
        for row, tile in enumerate(tile_list):
            # print("tile: {}".format(tile))
            if tile.find("p") > -1:
                return row, col
    return None, None

def reset_events_and_inventory(player_name):
    filepath_source = os.path.join("data", "zones", "dark_alley", "map01", "events_master.txt")
    filepath_destination = os.path.join("data", "zones", "dark_alley", "map01", "events.txt")
    copyfile(filepath_source, filepath_destination)
    # ----
    filepath_source = os.path.join("data", "master_files", "player_types", "warrior", "inventory", "consumable_items.txt")
    filepath_destination = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    copyfile(filepath_source, filepath_destination)
    # ----
    filepath_source = os.path.join("data", "master_files", "player_types", "warrior", "inventory", "weapon_items.txt")
    filepath_destination = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    copyfile(filepath_source, filepath_destination)

# *******************************************************

def testing_events():
    raise NotImplemented
    zone_name = "dark_alley"
    map_name = "map01"
    condition = "conversation_with_big_ben_completed"
    # result = game_condition_satisfied(zone_name, map_name, condition)
    # print("result: {}".format(result))
    mark_game_condition_satisfied(zone_name, map_name, condition)

def test_new_walkable_map_tile(new_tile):
    if new_tile in constants.MAP_TILE_NAMES_WALKABLE:
        return False
    return True

def walkable_map_tile_suggest_new():
    new_letters = map_tile_names_walkable_get_new_name()
    if len(new_letters) == 0:
        print("Doh! There are no more new letters.")
        return None
    return new_letters

def special_npc_player_circumstances(player, npc, item_name):
    if not npc.species == "skeleton":
        return False
    my_item = player.inventory.get_item_by_name(item_name)
    if my_item is None:
        return False
    return True

def npc_exists_in_zone(npc_name, zone_name):
    filepath = os.path.join("data", "zones", zone_name, "npc_name_lookup.txt")
    mylist = read_file(filepath)
    mydict = mylist[0]
    for key, value in mydict.items():
        # print("value: {}, npc_name: {}".format(value, npc_name))
        if value.replace("_", " ") == npc_name.replace("_", " "):
            return True
    return False

if __name__ == "__main__":
    item_name = "silver cross"
    if item_name in constants.WEAPON_NAMES:
        print("{} is a weapon!".format(item_name))
    else:
        print("{} is NOT a weapon.".format(item_name))