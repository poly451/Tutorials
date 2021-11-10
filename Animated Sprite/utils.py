import random
import constants
import os, sys
from shutil import copyfile
import math
import time

def get_unique_number():
    tt = time.gmtime()
    return "{}{}{}{}{}{}".format(tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min, tt.tm_sec)

def reset_data(player_name, profession):
    # reset player's inventory
    filepath_master_consumables = os.path.join("data", "master_files", "player_types", profession, "inventory", "consumable_items.txt")
    filepath_master_weapons = os.path.join("data", "master_files", "player_types", profession, "inventory", "weapon_items.txt")
    filepath_player_consumables = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    filepath_player_weapons = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    copyfile(filepath_master_consumables, filepath_player_consumables)
    copyfile(filepath_master_weapons, filepath_player_weapons)
    # ---- reset dark_alley ----
    # --------------------------
    filepath = os.path.join("data", "zones", "dark_alley", "map01", "texts", "event_record.txt")
    mydict = read_file(filepath)[0]
    # filepath = os.path.join("data", "testing01.txt")
    with open(filepath, "w") as f:
        for key, value in mydict.items():
            s = "{}: {}\n".format(key, False)
            f.write(s)
    # ----
    filepath = os.path.join("data", "zones", "dark_alley", "map01", "texts", "old_ben_history.txt")
    mydict = read_file(filepath)[0]
    # filepath = os.path.join("data", "testing02.txt")
    new_dict = {}
    for key, value in mydict.items():
        if key == "quest_accepted":
            new_dict[key] = False
        elif key == "quest_completed":
            new_dict[key] = False
        else:
            new_dict[key] = value
    with open(filepath, "w") as f:
        for key, value in new_dict.items():
            s = "{}: {}\n".format(key, value)
            f.write(s)
    # ---- reset green_lawn ----
    # --------------------------
    filepath = os.path.join("data", "zones", "bridge", "map00", "texts", "westley_history.txt")
    mydict = read_file(filepath)[0]
    # filepath = os.path.join("data", "testing02.txt")
    new_dict = {}
    for key, value in mydict.items():
        if key == "quest_accepted":
            new_dict[key] = False
        elif key == "quest_completed":
            new_dict[key] = False
        else:
            new_dict[key] = value
    with open(filepath, "w") as f:
        for key, value in new_dict.items():
            s = "{}: {}\n".format(key, value)
            f.write(s)


def npc_fight_on_contact(player_name, npc_name):
    filename = "{}.txt".format(npc_name)
    filepath = os.path.join("data", "playing_characters", player_name, "npcs", filename)
    mydict = read_file(filepath)[0]
    mydict["on_contact"] = "fight"
    with open(filepath, "w") as f:
        for key, value in mydict.items():
            s = "{}: {}\n".format(key, value)
            f.write(s)

def get_player_initial_direction(zone_name, map_name):
    filepath = os.path.join("data", "zones", zone_name, map_name, "player.txt")
    mydict = read_file(filepath)[0]
    if mydict["npc_position"] == "up":
        return constants.UP
    elif mydict["npc_position"] == "down":
        return constants.DOWN
    elif mydict["npc_position"] == "right":
        return constants.RIGHT
    elif mydict["npc_position"] == "left":
        return constants.LEFT
    else:
        raise ValueError("Error")

def get_coords_from_map(zone_name, map_name):
    """This reads in coords from the tiles on a map."""
    filename = "{}_npcs.txt".format(map_name)
    filepath = os.path.join("data", "zones", zone_name, map_name, filename)
    print("opening zone filepath: {}".format(filepath))
    with open(filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    mytiles = [i[3:] for i in mytiles[2:]]
    # print("debugging: mytiles: {}".format(mytiles))
    # ------------------------------------------------------------------
    tile_names = []
    for col, tiles in enumerate(mytiles):
        # print(tiles)
        list_tiles = tiles.split(";")
        list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
        for row, tile in enumerate(list_tiles):
            if tile == "..":
                pass
            elif len(tile) > 0:
                tile_names.append([row, col, tile])
            else:
                s = "Error! I don't recognize this: -{}-".format(tile)
                raise ValueError(s)
    # ----
    new_list = []
    for i in range(len(tile_names)):
        mydict = {}
        mydict["x"] = tile_names[i][0]
        mydict["y"] = tile_names[i][1]
        mydict["tile"] = tile_names[i][2]
        new_list.append(mydict)
    # print("debugging: new_list: {}".format(new_list))
    return new_list

def health_percent(max_health, current_health):
    temp = math.floor((current_health * 100) / max_health)
    return temp

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def is_real(mystring):
    try:
        temp = float(mystring)
        return True
    except:
        return False

def is_int_or_real(mystring):
    if is_int(mystring) == True: return True
    if is_real(mystring) == True: return True
    return False

def is_alpha(mystring):
    for mychar in mystring:
        if not mychar in constants.ALPHABET:
            return False
    return True

def key_value(mystring, mydict):
    # print("mystring: {}".format(mystring))
    # print("mydict: {}".format(mydict))
    if mystring.find(":") == -1:
        s = "Error! A colon (:) was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    if len(mystring) == 0:
        s = "The length of this string is 0."
        raise ValueError(s)
    # ----
    myint = mystring.find(":")
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error: mystring = {}".format(mystring))
    if len(value) == 0:
        s = "mystring: {}\n".format(mystring)
        s += "Error: there is no value. Here is mystring: {}".format(mystring)
        raise ValueError(s)
    try:
        mydict[tag] = int(value) if is_int(value) else value
        # mydict[tag] = True if value.lower() == "true" else value
        # mydict[tag] = False if value.lower() == "false" else value
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
    if not is_int(num_of_fields):
        s = "Error! num_of_fields is NOT an integer: {} != {}".format(type(num_of_fields), type(123))
        raise ValueError(s)
    # ----
    print("opening filepath in utils.py-->read_data_file: {}".format(filepath))
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    # ----
    big_list = []
    for i in range(0, len(mylines), num_of_fields):
        mydict = {}
        for j in range(num_of_fields):
            # print("i + j: {}".format(i + j))
            # print("debugging: {}".format(mydict))
            try:
                elem = mylines[i + j]
            except Exception as e:
                t = "the index: {}, filepath: {}".format(i+j, filepath)
                s = "{}\n{}\n".format(e, t)
                raise ValueError(s)
            # print("elem: {}".format(elem))
            mydict = key_value(elem, mydict)
        big_list.append(mydict)
    return big_list

def read_file(filepath):
    print("opening filepath in utils.py-->read_file: {}".format(filepath))
    if not os.path.isfile(filepath):
        raise ValueError("Error! This is not a file: --{}--".format(filepath))
    if file_is_empty(filepath) == True: return None
    with open(filepath, "r") as f:
        try:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        except Exception as e:
            s = "I'm having trouble reading this file: {}".format(filepath)
            t = "{}\n{}".format(e, s)
            raise ValueError(t)
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
            if len(elem) == 0: raise ValueError("len(elem) == 0")
            try:
                mydict = key_value(elem, mydict)
            except Exception as e:
                s = "Having trouble with this file: {}".format(filepath)
                t = "{}\n{}".format(e, s)
                raise ValueError(t)
        big_list.append(mydict)
    # ----
    if big_list is None: raise ValueError("Error")
    if len(big_list) == 0: raise ValueError("Error")
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

def _top_height(text_list, myfont):
    # print("this is the type of text_list: {}".format(type(text_list)))
    # print("t--- his is the type of 'font': {}".format(type(myfont)))
    if not type(text_list) == type([]):
        raise ValueError("Error")
    tallest = -1
    for elem in text_list:
        try:
            _, text_height = myfont.size(elem)
        except Exception as e:
            s = "elem: {}, type: {}\n".format(elem, type(elem))
            s += "type of myfont: {}".format(type(myfont))
            s = "{}\n{}".format(s, e)
            raise ValueError(s)
        if text_height > tallest:
            tallest = text_height
    return tallest

def convert_list_of_lists(a_list):
    return [",".join(i) for i in a_list]

def command_okay(todo_list):
    todo_string = ' '.join(todo_list)
    for a_command in constants.CONVERSATION_ENDINGS:
        if a_command in todo_string:
            return True
    return False

def talk_dialog(screen, text, font, width_offset, height_offset, line_length=32, color=(0,0,0)):
    # text_list = separate_text_into_lines(text, line_length)
    text_list = []
    if type(text) == type("abc"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        for elem in text:
            if type(elem) != type("abc"):
                s = "Error! (type: {})".format(type(elem))
                raise ValueError(s)
        for line in text:
            temp = separate_text_into_lines(line, line_length)
            text_list += temp
    else:
        s = "Doh! That type of data shouldn't be here!: {}".format(type(text))
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

def get_npc_names_from_files():
    filepath = os.path.join("data", "master_files", "npcs")
    files = os.listdir(filepath)
    name_list = []
    for file in files:
        if file.lower() == ".ds_store":
            continue
        path = os.path.join(filepath, file)
        # print("path: {}".format(path))
        mylist = read_file(path)
        mydict = mylist[0]
        # print("mydict: {}".format(mydict))
        name_list.append(mydict["name"])
    return name_list

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
    elif len(mydict["profession_name"].strip()) == 0:
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

def validate_player_name(name):
    filepath = os.path.join("data", "playing_characters")
    name_list = get_subdirectories(filepath)
    # print(name_list)
    if name.lower().strip() in name_list:
        return True
    return False

def get_all_player_names():
    filepath = os.path.join("data", "playing_characters")
    name_list = get_subdirectories(filepath)
    # print(name_list)
    new_list = []
    for name in name_list:
        new_list.append(name.lower().strip())
    return new_list

def get_all_model_names():
    filepath = os.path.join("data", "images", "npc_models")
    name_list = get_subdirectories(filepath)
    # print(name_list)
    new_list = []
    for name in name_list:
        new_list.append(name.lower().strip())
    return new_list

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
    if validate_player_name(char_name) == False:
        s = "Error! I can't find a directory with this name: {}".format(char_name)
        raise ValueError(s)
    if not zone_name in constants.ZONE_NAMES:
        s = "This isn't a zone name: {}\n"
        s += "If this is coming from a Trigger or Action,\n"
        s += "make sure that the ZONE_NAME in the Trigger or Action is spelled properly.\n"
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

# def get_npc_name_from_map_code(zone_name, map_code):
#     filepath = os.path.join("data", "zones", zone_name, "npc_name_lookup.txt")
#     with open(filepath, "r") as f:
#         mylines = f.readlines()
#         mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
#     mydict = {}
#     for myline in mylines:
#         mydict = key_value(myline, mydict)
#     return mydict[map_code]

def get_npc_file_name(mylist_of_dictionaries, tile_name, player_name, zone_name, map_name):
    print("mylist_of_dictionaries: {}".format(mylist_of_dictionaries))
    print("zone_name: {}".format(zone_name))
    print("map_name: {}".format(map_name))
    npc_file_name = ""
    for mydict in mylist_of_dictionaries:
        print("mydict: {}".format(mydict))
        print("tile name: {}".format(tile_name))
        if mydict["tile_name"] == tile_name:
            npc_file_name = mydict["npc_file"]
            if npc_file_name is None:
                raise ValueError("Error!")
    if len(npc_file_name) == 0:
        raise ValueError("Error!")
    print("npc_file_name: {}".format(npc_file_name))
    # ----
    filepath = os.path.join("data", "playing_characters", player_name, "npcs", npc_file_name)
    print("filepath: {}".format(filepath))
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    if len(mylines) == 0:
        raise ValueError("Error!")
    # ----
    mydict = {}
    for myline in mylines:
        mydict = key_value(myline, mydict)
    return mydict

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
    return s.lower().strip()

def get_filepath(filename, basepath="data"):
    if os.path.isdir(filename) == True:
        s = "This is a directory NOT a filename: {}".format(filename)
        raise ValueError(s)
    if filename is None:
        raise ValueError("Error")
    if len(filename) == 0:
        s = "Error: I can't find a file with this name: {}".format(filename)
        raise ValueError(s)
    # ----
    if basepath == "data":
        basepath = os.path.join("data")
    elif basepath == "images":
        basepath = os.path.join("data", "images")
    # dir_contents = os.listdir(basepath)
    # ----
    the_path_01 = "initial"
    the_path_02 = "initial"
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                the_path_01 = os.path.join(root, file)
                the_path_02 = file
    if os.path.isfile(the_path_01) == True:
        return the_path_01
    if os.path.isfile(the_path_02) == True:
        return the_path_02
    # ----
    if the_path_01 == "initial" and the_path_02 == "initial":
        s = "This filename is not in the data directory: -{}-".format(filename)
        raise ValueError(s)
    s1 = "This is not a valid path: {}".format(the_path_01)
    s2 = "This is not a valid path: {}".format(the_path_02)
    s3 = "This was the filename: {}".format(filename)
    s = "filename: {}\nfilepath1: {}\nfilepath2: {}".format(s3, s1, s2)
    raise ValueError(s)

def _get_image_filepath_helper(filename):
    if filename is None:
        raise ValueError("Error")
    if len(filename) == 0:
        s = "Error: I can't find a file with this name: {}".format(filename)
        raise ValueError(s)
    # ----
    basepath = os.path.join("data", "images")
    # ----
    the_path_01 = "initial"
    the_path_02 = "initial"
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                the_path_01 = os.path.join(root, file)
                the_path_02 = file
    if os.path.isfile(the_path_01) == True:
        return the_path_01
    if os.path.isfile(the_path_02) == True:
        return the_path_02
    # ----
    if the_path_01 == "initial" and the_path_02 == "initial":
        # s = "This filename is not in the data directory: {}".format(filename)
        return None
    # s1 = "This is not a valid path: {}".format(the_path_01)
    # s2 = "This is not a valid path: {}".format(the_path_02)
    # s3 = "This was the filename: {}".format(filename)
    # s = "filename: {}\nfilepath1: {}\nfilepath2: {}".format(s3, s1, s2)
    raise None

def get_image_filepath(filename, model=None):
    def get_filepath(filename):
        if filename is None:
            raise ValueError("Error")
        if len(filename) == 0:
            s = "Error: I can't find a file with this name: {}".format(filename)
            raise ValueError(s)
        # ----
        if model == None:
            filepath = _get_image_filepath_helper(filename)
            if filepath is None:
                s = "This should be an ordinary image file (not a model)."
                s += "But it couldn't be found amount the ordinary image files."
                raise ValueError(s)
            # If the filepath is not None then return it.
            return filepath
        # ----
        basepath = os.path.join("data", "images", "player_images", model)
        # ----
        the_path_01 = "initial"
        the_path_02 = "initial"
        for root, dirs, files in os.walk(basepath):
            for file in files:
                if filename.lower().strip() == file.lower().strip():
                    the_path_01 = os.path.join(root, file)
                    the_path_02 = file
        if os.path.isfile(the_path_01) == True:
            return the_path_01
        if os.path.isfile(the_path_02) == True:
            return the_path_02
        # ----
        if the_path_01 == "initial" and the_path_02 == "initial":
            # s = "This filename is not in the data directory: {}".format(filename)
            return None
        # s1 = "This is not a valid path: {}".format(the_path_01)
        # s2 = "This is not a valid path: {}".format(the_path_02)
        # s3 = "This was the filename: {}".format(filename)
        # s = "filename: {}\nfilepath1: {}\nfilepath2: {}".format(s3, s1, s2)
        return None

def get_model_filepath(filename, model):
    if filename is None or model is None:
        raise ValueError("Error")
    if len(filename) == 0 or len(model) == 0:
        s = "Error: I can't find a file with this name: {}".format(filename)
        raise ValueError(s)
    # ----
    basepath = os.path.join("data", "images", "player_images", model)
    if not os.path.isdir(basepath):
        raise ValueError("Error")
    # dir_contents = os.listdir(basepath)
    # ----
    the_path_01 = "initial"
    the_path_02 = "initial"
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                the_path_01 = os.path.join(root, file)
                the_path_02 = file
    if os.path.isfile(the_path_01) == True:
        return the_path_01
    if os.path.isfile(the_path_02) == True:
        return the_path_02
    # ----
    if the_path_01 == "initial" and the_path_02 == "initial":
        s = "This filename is not in the data directory: {}".format(filename)
        # Trying this as a last chance.
        return get_filepath(filename)
    s1 = "This is not a valid path: {}".format(the_path_01)
    s2 = "This is not a valid path: {}".format(the_path_02)
    s3 = "This was the filename: {}".format(filename)
    s = "filename: {}\nfilepath1: {}\nfilepath2: {}".format(s3, s1, s2)
    raise ValueError(s)

def image_filepath_exists(filename):
    if filename is None:
        raise ValueError("Error")
    if len(filename) == 0: return False
    # ----
    basepath = os.path.join("data", "images")
    # ----
    the_path_01 = "initial"
    the_path_02 = "initial"
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                the_path_01 = os.path.join(root, file)
                the_path_02 = file
    if os.path.isfile(the_path_01) == True:
        return True
    if os.path.isfile(the_path_02) == True:
        return True
    return False

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
    filename = "{}_player.txt".format(map_name)
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

def reset_player_inventory(player_name, profession):
    # user_info = get_user_data()
    # player_name = user_info["character_name"]
    # ----
    # filepath_source = os.path.join("data", "zones", "dark_alley", "map01", "events_master.txt")
    # filepath_destination = os.path.join("data", "zones", "dark_alley", "map01", "events.txt")
    # copyfile(filepath_source, filepath_destination)
    # ----
    filepath_source = os.path.join("data", "master_files", "player_types", profession, "inventory", "consumable_items.txt")
    filepath_destination = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    copyfile(filepath_source, filepath_destination)
    # ----
    filepath_source = os.path.join("data", "master_files", "player_types", profession, "inventory", "weapon_items.txt")
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

def npc_exists_in_zone_OLD(npc_name, zone_name):
    filepath = os.path.join("data", "zones", zone_name, "npc_name_lookup.txt")
    mylist = read_file(filepath)
    mydict = mylist[0]
    for key, value in mydict.items():
        # print("value: {}, npc_name: {}".format(value, npc_name))
        if value.replace("_", " ") == npc_name.replace("_", " "):
            return True
    return False

def npc_exists_in_zone(npc_name, zone_name, map_name):
    filepath = os.path.join("data", "zones", zone_name, map_name, "npcs.txt")
    mylist = read_data_file(filepath, 7)
    # print("mylist: {}".format(mylist))
    for mydict in mylist:
        for key, value in mydict.items():
            # print("key: {}, value: {}".format(key, value))
            if key == "npc_file":
                myvalue = npc_name.replace(".txt", "").lower().strip()
                # print("**** key: {}, value: {}".format(key, myvalue))
                if npc_name == myvalue:
                    return True
    return False

def file_is_empty(filepath):
    print("In module utils.py, in function file_is_empty")
    # print("filepath: {}".format(filepath))
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # print(mylines)
    if mylines is None:
        # print("mylines is none")
        return True
    if len(mylines) == 0:
        # print("len(mylines) == 0")
        return True
    if mylines[0].lower().strip() == "empty":
        # print("mylines[0].lower().strip() == empty")
        return True
    return False

def get_dictionary(mylist, value_to_search_for):
    for mydict in mylist:
        try:
            if mydict["name"] == value_to_search_for:
                return mydict
        except Exception as e:
            s = "{}\nvalue_to_search_for: {}\nmydict: {}".format(e, value_to_search_for, mydict)
            raise ValueError(s)
    return None

def string_to_dict(mystring):
    if len(mystring) == 0: raise ValueError("Error")
    if mystring.find(";") == -1: raise ValueError("Error")
    mylist = mystring.split(";")
    mylist = [i for i in mylist if len(i.strip()) > 0]
    mydict = {}
    for elem in mylist:
        mydict = key_value(elem, mydict)
    if len(mydict) == 0: raise ValueError("Error")
    return mydict

def get_dict(mylist, key, value):
    print("mylist: {}".format(mylist))
    print("key: {}".format(key))
    print("value: {}".format(value))
    # ----
    if type(mylist) != type([]):
        raise ValueError("Error")
    for mydict in mylist:
        if type(mydict) != type({}):
            raise ValueError("Error")
    # ----
    new_dict = {}
    for mydict in mylist:
        if mydict[key] == value:
            return mydict
    # ----
    # value was not found.
    if new_dict is None:
        raise ValueError("Error")
    if len(new_dict) == 0:
        print("This is mylist: {}".format(mylist))
        print("key: {}, value: {}".format(key, value))
        s = "Error: Have you gotten rid of p0 from the NPC map file (eg, map00_npcs.txt)?\n"
        s += "OR it could be that the name in your map file (check the KEY and the VALUE)\n"
        s += "does not match with any name in the npcs.txt file."
        raise ValueError(s)
    raise ValueError("Error")

def _fill_empty_file_helper(filepath):
    if os.path.isfile(filepath) == False:
        raise ValueError("Error! This isn't a valid path: {}".format(filepath))
    with open(filepath, "r") as f:
        try:
            mylines = f.readlines()
        except Exception as e:
            s = "e: {}\nfilepath: {}".format(e, filepath)
            raise ValueError(s)
        if mylines is None:
            raise ValueError("Error! This should have been a valid filepath!!!")
    if len(mylines) == 0:
        # print("file would be written")
        # print(filepath)
        with open(filepath, "w") as f:
            f.write("empty")

def fill_empty_files():
    """
    It is a quirk of GitHub that one isn't allowed to upload an empty file.
    But my program requires certain filenames to be present in every zone.
    SO I can run this function to make sure that IF a file is empty, THEN
    the word 'empty' will be written into the file. My program checks for
    files with this word and treads them like they are empty.
    :return: None
    """
    # dir_contents = os.listdir(basepath)
    basepath = os.path.join("data", "zones")
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file[0:1] == ".":
                continue
            # elif file.find(".png") > -1:
            #     continue
            # elif file.find(".gif") > -1:
            #     continue
            # ----
            this_path = os.path.join(root, file)
            # print("debugging: this_path: {}".format(this_path))
            if os.path.isfile(this_path) == True:
                _fill_empty_file_helper(this_path)
            elif os.path.isfile(file):
                _fill_empty_file_helper(file)
            else:
                s1 = "path1: {}".format(this_path)
                s2 = "path2: {}".format(file)
                s = "Neith of these are valid paths:\npath1: {}\npath2: {}".format(s1, s2)
                raise ValueError(s)

# ---------------------------------------------

def _create_file_in_directory_if_absent(root_path, dir_name):
    # print("root: {}".format(root_path))
    # print("dir_name: {} ({})".format(dir_name, type(dir_name)))
    if dir_name[0:3] != "map":
        s = "Error! I only look through map directories. This is NOT a map directory: {}".format(dir_name)
        raise ValueError(s)
    # ----
    this_path = os.path.join(root_path, dir_name)
    # print("this_path: {}".format(this_path))
    these_files = os.listdir(this_path)
    file_present = False
    for a_file in these_files:
        if a_file.lower() == ".ds_store":
            continue
        # print("--")
        # print("a_file: {}".format(a_file))
        # print("filename: {}".format(filename))
        if a_file.lower() == filename:
            file_present = True
        # print("file: {}".format(a_file))
    return file_present

def create_file_in_each_nested_directory(basepath, filename):
    """
    Creates a file in each nested directory.
    :param basepath: The base path for the search
    :param filename: The file being searched for (e.g., mytext.txt)
    :return: None
    """
    for root_name, dirs, files in os.walk(basepath):
        for file in files:
            if file[0:1] == ".":
                continue
        # ----
        for dir_name in dirs:
            # this_path = os.path.join(root, file)
            print("dir_name[0:3]: {}".format(dir_name[0:3]))
            if not dir_name[0:3] == "map":
                print("This directory name does NOT have 'map' in it: {}".format(dir_name))
                continue
            else:
                print("---------- top")
                print("This directory name is {} so that's okay.".format(dir_name))
                file_present = _create_file_in_directory_if_absent(root_name, dir_name)
                # print("This file is present: {}, root: {}, dir: {}".format(file_present, root_name, dir_name))
                if file_present == False:
                    print("The file is being created.")
                    new_file = os.path.join(root_name, dir_name, filename)
                    print("Creating file: {}".format(new_file))
                    with open(new_file, "w") as f:
                        f.write("empty")
                print("---------- bottom")

def is_a_valid_npc_name(player_name, npc_name):
    if npc_name is None:
        return True
    # filename = "{}.txt".format(npc_name)
    dir_path = os.path.join("data", "playing_characters", player_name, "npcs")
    # print("debugging: {}".format(dir_path))
    # ----
    directory_contents = os.listdir(dir_path)
    # print(directory_contents)
    # ----
    name_list = []
    for filename in directory_contents:
        if filename.lower() == ".ds_store":
            continue
        name_list.append(filename.replace(".txt", ""))
    name_list = list(set(name_list))
    # ----
    if npc_name in name_list:
        return True
    temp_name = npc_name.replace(" ", "_")
    if temp_name in name_list:
        return True
    # ----
    print("**********************************")
    print("This name: {}".format(npc_name))
    print("was not found among the files in this directory:")
    print(dir_path)
    print("Here are the files in that directory:")
    [print(i) for i in name_list]
    print("**********************************")
    return False

def _hook_dict_up(dict1, dict2, mykey):
    new_dict = {}
    if dict1[mykey] == dict2[mykey]:
        for key, value in dict1.items():
            new_dict[key] = value
        for key, value in dict2.items():
            new_dict[key] = value
        return new_dict
    else:
        raise ValueError("Error!")

def merge_two_lists_of_dictionaries(list01, list02, mykey):
    # tile & tile_name
    if type(list01) != type([]):
        raise ValueError("Error")
    if type(list02) != type([]):
        raise ValueError("Error")
    for mydict1 in list01:
        if type(mydict1) != type({}): raise ValueError("Error!")
    for mydict in list02:
        if type(mydict) != type({}): raise ValueError("Error!")
    # ----
    new_list = []
    for mydict1 in list01:
        for mydict2 in list02:
            if mydict1[mykey] == mydict2[mykey]:
                new_dict = _hook_dict_up(mydict1, mydict2, mykey)
                new_list.append(new_dict)
    # ----
    if new_list is None:
        raise ValueError("Error!")
    if len(new_list) == 0:
        raise ValueError("Error!")
    return new_list

def merge_two_dictionaries(dict01, dict02):
    if type(dict01) != type({}):
        # print("dict01: {}".format(dict01))
        s = "dict01 is a {} and not a dictionary.".format(type(dict01))
        raise ValueError(s)
    if type(dict02) != type({}):
        # print("dict02: {}".format(dict02))
        s = "dict02 is a {} and not a dictionary.".format(type(dict02))
        raise ValueError(s)
    # ----
    # print("In utils.py, merge_two_dictionaries")
    # print("dict01: {}".format(dict01))
    # print("dict02: {}".format(dict02))
    new_dict = {}
    for key, value in dict01.items():
        new_dict[key] = value
    for key, value in dict02.items():
        new_dict[key] = value
    # ----
    if new_dict is None:
        raise ValueError("Error")
    if len(new_dict) == 0:
        raise ValueError("Error")
    return new_dict

def get_info_from_npc_file(mylist):
    if type(mylist) != type([]):
        s = "Error: type: {}, mylist: {}".format(type(mylist), mylist)
        raise ValueError(s)
    for mydict in mylist:
        if type(mydict) != type({}):
            raise ValueError("Error")
    # ----
    mydict = mylist[0]
    filename = mydict["npc_file"]
    mykey = filename.replace(".txt", "")
    filepath = os.path.join("data", "master_files", "npcs", filename)
    npc_list = read_file(filepath)
    # ----
    # print("***************")
    new_list_of_dict = merge_two_dictionaries(npc_list[0], mylist[0])
    # ----
    if new_list_of_dict is None:
        raise ValueError("Error")
    if len(new_list_of_dict) == 0:
        raise ValueError("Error")
    return new_list_of_dict

def find_model_name():
    user_info = get_user_data()
    filepath = os.path.join("data", "playing_characters", user_info["character_name"], "player_data_file.txt")
    if os.path.isfile(filepath) == False:
        s = "This isn't a valid filepath: {}".format(filepath)
        raise (s)
    mydict = read_file(filepath)[0]
    # ----
    try:
        temp = mydict["image_model"]
    except Exception as e:
        print(mydict)
        s = "The field <image_model> is not included in mydict."
        t = "e: {}\ns: {}".format(e, s)
    model_name = mydict["image_model"]
    return model_name

def get_initial_player_position(zone_name, map_name):
    filepath = os.path.join("data", "zones", zone_name, map_name, "player.txt")
    mylines = read_file(filepath)[0]
    return mylines["npc_position"].lower().strip()

def zone_files_valid(zone_name, map_name):
    basepath = os.path.join("data", "zones", zone_name, map_name)
    # ----
    f1 = os.path.join(basepath, "actions.txt")
    f2 = os.path.join(basepath, "events.txt")
    f3 = os.path.join(basepath, "npcs.txt")
    f4 = os.path.join(basepath, "persistents.txt")
    f5 = os.path.join(basepath, "player.txt")
    f6 = os.path.join(basepath, "triggers.txt")
    # ----
    g1 = os.path.join(basepath, "{}_actions.txt".format(map_name))
    g2 = os.path.join(basepath, "{}_npcs.txt".format(map_name))
    g3 = os.path.join(basepath, "{}_obstacles.txt".format(map_name))
    g4 = os.path.join(basepath, "{}_persistents.txt".format(map_name))
    g5 = os.path.join(basepath, "{}_player.txt".format(map_name))
    g6 = os.path.join(basepath, "{}_triggers.txt".format(map_name))
    g7 = os.path.join(basepath, "{}_walkables.txt".format(map_name))
    # ----
    mylist = [f1, f2, f3, f4, f5, f6, g1, g2, g3, g4, g5, g6, g7]
    need_to_be_created = []
    for filepath in mylist:
        if os.path.isfile(filepath) == False:
            s = "You need this file: {}".format(filepath)
            need_to_be_created.append(filepath)
    if len(need_to_be_created) == 0:
        print("Everything looks good in {} - {}!".format(zone_name, map_name))
    else:
        s = "{} files need to be created.".format(len(need_to_be_created))
        print(s)
        print("zone_name: {}, map_name: {}".format(zone_name, map_name))
        print(need_to_be_created)

def check_validity_of_zone():
    # zone_name = "swindon_pub"
    zone_name = "dark_alley"
    map_name = "map03"
    zone_files_valid(zone_name, map_name)

def get_highest_index(mylist):
    if type(mylist) != type([]):
        raise ValueError("Error")
    for elem in mylist:
        if type(elem) != type({}):
            raise ValueError("Error")
    # ----
    indexes_list = [i["index"] for i in mylist]
    indexes_set = list(set(indexes_list))
    if len(indexes_set) != len(indexes_list):
        repeated_indexes = get_repeated_indexes(indexes_list)
        s = "Error! These indexes are repeated: {}".format(repeated_indexes)
        raise ValueError(s)
    # ----
    highest_index = max(indexes_list)
    lowest_index = min(indexes_list)
    # highest_index = -1
    # for i in indexes_list:
    #     if i > highest_index:
    #         highest_index = i
    # # ----
    # lowest_index = -1
    # ----
    mycounter = lowest_index
    while mycounter <= highest_index:
        if not mycounter in indexes_list:
            s = "Error! An index was skipped!!!!!\n"
            s += "highest_index: {}, lowest_index: {}\n"
            s += "counter ({}) was NOT in the index list."
            s = s.format(highest_index, lowest_index, mycounter)
            raise ValueError(s)
        mycounter += 1
    # print(indexes_list)
    # ----
    return highest_index

def is_file(filepath):
    # Note: Does not work with .png files.
    try:
        with open(filepath, "r") as f:
            temp = f.readlines()
        return True
    except:
        return False

def get_player_weapons_from_file(player_name):
    filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    new_list = []
    mylist = utils.read_data_file(filepath, 11)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name":
                new_list.append(value)
    if len(new_list) == 0: raise ValueError("Error")
    return new_list

def get_player_consumables_from_file(player_name):
    filepath = os.path.join("data", "playing_characters", player_name, "inventory", "consumable_items.txt")
    new_list = []
    mylist = utils.read_data_file(filepath, 9)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name":
                new_list.append(value)
    if len(new_list) == 0: raise ValueError("Error")
    return new_list

def get_npc_weapons_from_local_file(player_name):
    filepath = os.path.join("data", "playing_characters", player_name, "npc_inventories", "weapon_items.txt")
    new_list = []
    mylist = utils.read_data_file(filepath, 11)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name":
                new_list.append(value)
    if len(new_list) == 0: raise ValueError("Error")
    return new_list

def get_all_npc_names_by_player(player_name):
    filepath = os.path.join("data", "playing_characters", player_name, "npcs")
    file_names = os.listdir(filepath)
    print(file_names)
    return [i.replace(".txt", "") for i in file_names]

def get_unused_tile_names():
    def get_all_possible_indexes():
        all_possible_names = []
        for a_letter in constants.ALPHABET:
            for a_number in range(10):
                s = "{}{}".format(a_letter, a_number)
                all_possible_names.append(s)
        return all_possible_names
    # ----
    filepath = os.path.join("data", "master_files", "tiles.txt")
    mylist = read_data_file(filepath, 4)
    used_indexes = [value for mydict in mylist for key, value in mydict.items() if key=="name"]
    if len(used_indexes) != len(list(set(used_indexes))):
        s = "{} != {}\n".format(len(used_indexes), len(list(set(used_indexes))))
        duplicates = get_repeated_indexes(used_indexes)
        s += "Duplicate(s): {}".format(duplicates)
        raise ValueError(s)
    # print(used_indexes)
    # ----
    all_possible_indexes = get_all_possible_indexes()
    # ----
    unused_indexes = []
    for an_index in all_possible_indexes:
        if not an_index in used_indexes:
            unused_indexes.append (an_index)
    return unused_indexes

def get_all_map_names_in_zone(zone_name):
    if not zone_name in constants.ZONE_NAMES:
        raise ValueError("Error")
    filepath = os.path.join("data", "zones", zone_name)
    # ----
    map_names = get_subdirectories(filepath)
    # ----
    if map_names is None: raise ValueError("Error")
    if len(map_names) == 0: raise ValueError("Error")
    return map_names

def log_text(filename, text):
    filepath = os.path.join("data", "logs", filename)
    with open(filepath, "a") as f:
        s = "{}\n".format(text)
        f.write(s)

def get_repeated_indexes(list_of_indexes):
    newlist = []
    repeats = []
    for elem in list_of_indexes:
        if not elem in newlist:
            newlist.append(elem)
        else:
            repeats.append(elem)
    return repeats

def check_for_invalid_tile_kinds():
    filepath = os.path.join("data", "master_files", "tiles.txt")
    tiles = read_data_file(filepath, 4)
    for mytile in tiles:
        for key, value in mytile.items():
            if key == "kind":
                if not value in constants.TILE_KINDS:
                    s = "{} is not in {}".format(value, constants.TILE_KINDS)
                    raise ValueError(s)

def has_hit(change_to_hit):
    myint = random.randint(1, 100)
    if myint < change_to_hit: return True
    return False

def in_range(x_current, y_current, x_end, y_end, myincrement):
    x_low = x_end - myincrement
    y_low = y_end - myincrement
    x_high = x_end + myincrement
    y_high = y_end + myincrement
    # ----
    print("{} < {} and {} < {}".format(x_low, x_current, x_current, x_high))
    if (x_low < x_current) and (x_current < x_high):
        print("x is in range")
    else:
        print("x NOT in range")
        return False

    print(y_low, y_current, y_high)
    if y_low < y_current < y_high:
        print("y is in range")
    else:
        print("y NOT in range")
        return False
    return True

def _move_toward_helper(x1, y1, y2, x2):
    if x1 == x2 and y1 != y2:
        if abs((y1-1)-y2) < abs((y1+1)-y2):
            y1 = y1 - 1
        else:
            y1 = y1 + 1
    elif x1 != x2 and y1 == y2:
        if abs((x1-1)-x2) < abs((x1+1)-x2):
            x1 = x1 - 1
        else:
            x1 = x1 + 1
    elif x1 != x2 and y1 != y2:
        myrand = random.randint(0, 1)
        if myrand == 0:
            if abs((y1 - 1) - y2) < abs((y1 + 1) - y2):
                y1 = y1 - 1
            else:
                y1 = y1 + 1
        elif myrand == 1:
            if abs((x1 - 1) - x2) < abs((x1 + 1) - x2):
                x1 = x1 - 1
            else:
                x1 = x1 + 1
    else:
        s = "x1: {}; x2: {}; y1: {}, y2: {}".format(x1, x2, y1, y2)
        raise ValueError(s)
    return (y1, x1)

def _is_blocked(x, y, obstacles):
    for elem in obstacles:
        if elem.x == x and elem.y == y:
            return True
    return False

def _random_change(x, y):
    new_x, new_y = x, y
    def one_axis(foo):
        myint = random.randint(0, 1)
        if myint == 0:
            foo += 1
        else:
            foo -= 1
        return foo
    # ----
    myint_xy = random.randint(0, 1)
    if myint_xy == 0:
        new_x = one_axis(x)
    elif myint_xy == 1:
        new_y = one_axis(y)
    else:
        pass
    return new_x, new_y

def move_toward(x1, y1, x2, y2, obstacles):
    # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
    old_x = x1
    old_y = y1
    if x1 == x2 and y1 == y2:
        raise ValueError("They are already on the same tile!")
    new_x1, new_y1 = _move_toward_helper(x1, y1, x2, y2)
    print("output of _move_toward_helper: {},{}".format(new_x1, new_y1))
    # ----
    besafe = 0
    is_clear = False
    while _is_blocked(new_x1, new_y1, obstacles) == True:
        new_x1, new_y1 = _random_change(new_x1, new_y1)
        besafe += 1
        if besafe > 1000:
            raise ValueError("Error")
    # ----
    return new_x1, new_y1

def walk_toward():
    from graphics_environment import Obstacles
    myobstacles = Obstacles("swindon", "map00")
    myobstacles.read_data()
    # ----
    x1, y1 = 1, 1
    x2, y2 = 1, 8
    besafe = 0
    arrived = False
    while arrived == False:
        x1, y1 = move_toward(x1, y1, x2, y2, myobstacles)
        if x1 == x2 and y1 == y2:
            arrived = True
        else:
            arrived = False
        print("new_x, new_y: {},{}; destination_x, destiation_y: {},{}".format(x1, y1, x2, y2))
        besafe += 1
        if besafe > 1000:
            raise ValueError("Error")

def search_for_phrase(the_phrase, basepath):
    if os.path.isdir(basepath) == False:
        raise ValueError("Error")
    path_list = []
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file.lower() == ".ds_store":
                continue
            if file.find(".txt") == -1:
                continue
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) == False:
                raise ValueError("Error")
            with open(filepath, "r") as f:
                try:
                    mylist = f.readlines()
                except Exception as e:
                    t = "This is the filepath: {}".format(filepath)
                    s = "{}\n{}\n".format(e, t)
                    raise ValueError(s)
            # ----
            for elem in mylist:
                if elem.find(the_phrase) != -1:
                    path_list.append(filepath)
                    continue
    if len(path_list) > 0: return list(set(path_list))
    return None

def points_are_close(x1, x2):
    increment = 0.5
    if type(x1) == type(123):
        x1 = float(x1)
    if type(x2) == type(123):
        x2 = float(x2)
    if type(x1) != type(0.0):
        raise ValueError("Error")
    if type(x2) != type(0.0):
        raise ValueError("Error")
    # ----
    # print("{} < {}".format(abs(x1 - x2), increment))
    if abs(x1 - x2) <= increment: return True
    return False

def check_for_all(mylist):
    # use health potion all
    if not len(mylist) in [3, 4]: raise ValueError("Error")
    if is_int(mylist[-1]) == True:
        return False
    if mylist[-1].lower().strip() == "all":
        return True
    return False

def _no_quest_duplicates():
    basepath = os.path.join("data", "zones")
    filepaths = get_histories_filenames(basepath)
    names = []
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        if not mydict["quest_name"] in names:
            names.append(mydict["quest_name"])
        else:
            # return False
            s = "({}) is a duplicate.\n".format(mydict["quest_name"])
            s += "Here is the filepath: {}\n".format(filepath)
            s += "Here are the names: {}\n".format(names)
            s += ', '.join(filepaths)
            raise ValueError(s)
    return True

def get_histories_filenames(basepath):
    if os.path.isdir(basepath) == False:
        raise ValueError("Error")
    # ----
    mylist = []
    for root, dirs, files in os.walk(basepath):
        for a_file in files:
            if a_file.find("history") == -1:
                continue
            if a_file == "placeholder_history.txt":
                continue
            myint = a_file.find("_")
            # myint = a_file.find("_")
            npc_name = a_file[0:myint]
            if not npc_name in constants.NPC_NAMES:
                continue
            the_path = os.path.join(root, a_file)
            # print("the path: {}".format(the_path))
            mylist.append(the_path)
    return mylist

def get_all_quests():
    basepath = os.path.join("data", "zones")
    # looking for duplicates
    if _no_quest_duplicates() == False:
        raise ValueError("Error: There are duplicate quests!")
    # ----
    """Gets all quests and indicates whether they are accepted or completed."""
    filepaths = get_histories_filenames(basepath)
    mylist = []
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        s = "{} {} {}".format("-*-", mydict["quest_name"], "-*-")
        mylist.append(s)
        s = "accepted: {} completed: {}".format(mydict["quest_accepted"], mydict["quest_completed"])
        mylist.append(s)
        s = "zone: {} ({}) npc: {}".format(mydict["zone_name_giver"].upper(), mydict["map_name_giver"], mydict["npc_name_giver"])
        mylist.append(s)
        mylist.append(" ")
        # ----
    return mylist

def get_accepted_quests():
    # looking for duplicates
    if _no_quest_duplicates() == False:
        raise ValueError("Error: There are duplicate quests!")
    # ----
    """Gets all quests and indicates whether they are accepted or completed."""
    basepath = os.path.join("data", "zones")
    filepaths = get_histories_filenames(basepath)
    mylist = []
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        if mydict["quest_accepted"].lower().strip() == "true":
            mylist.append(mydict["quest_name"])
            s = "accepted: {} || completed: {}".format(mydict["quest_accepted"], mydict["quest_completed"])
            mylist.append(s)
            s = "zone: {} ({}) npc: {}".format(mydict["zone_name_giver"].upper(), mydict["map_name_giver"],
                                               mydict["npc_name_giver"])
            mylist.append(s)
            mylist.append(" ")
    return mylist

def get_completed_quests():
    # looking for duplicates
    if _no_quest_duplicates() == False:
        raise ValueError("Error: There are duplicate quests!")
    # ----
    """Gets all quests and indicates whether they are accepted or completed."""
    basepath = os.path.join("data", "zones")
    filepaths = get_histories_filenames(basepath)
    mylist = []
    names = []
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        if mydict["quest_completed"].lower().strip() == "true":
            mylist.append(mydict["quest_name"])
            s = "accepted: {} || completed: {}".format(mydict["quest_accepted"], mydict["quest_completed"])
            mylist.append(s)
            s = "zone: {} ({}) npc: {}".format(mydict["zone_name_giver"].upper(), mydict["map_name_giver"],
                                               mydict["npc_name_giver"])
            mylist.append(s)
            mylist.append(" ")
    return mylist

def reset_conversation(npc_name, zone_name, map_name):
    filename = "{}_history.txt".format(npc_name)
    filepath = os.path.join("data", "zones", zone_name, map_name, "conversations", filename)
    if os.path.isfile(filepath) == False:
        s = "This is not a file: {}".format(filepath)
        raise ValueError(s)
    if file_is_empty(filepath) == True: return False
    # ----
    mydict = read_file(filepath)[0]
    mydict["quest_accepted"] = False
    mydict["quest_completed"] = False
    s = ""
    for key, value in mydict.items():
        s += "{}: {}\n".format(key, value)
    with open(filepath, "w") as f:
        f.write(s)
    # print("Conversation has been reset: {}".format(filepath))

def reset_conversation_by_name(quest_name):
    if len(quest_name) == 0:
        raise ValueError("Error")
    if not quest_name in constants.QUEST_NAMES:
        raise ValueError("{} is not a quest name.".format(quest_name))
    # ----
    basepath = os.path.join("data", "zones")
    # looking for duplicates
    if _no_quest_duplicates() == False:
        raise ValueError("Error: There are duplicate quests!")
    # ----
    """Gets all quests and indicates whether they are accepted or completed."""
    filepaths = get_histories_filenames(basepath)
    mylist = []
    quest_found = False
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        if mydict["quest_name"] == quest_name:
            mydict["quest_accepted"] = False
            mydict["quest_completed"] = False
            quest_found = True
            # ----
            # filepath = os.path.join("data", "testing.txt")
            with open(filepath, "w") as f:
                for key, value in mydict.items():
                    s = "{}: {}\n".format(key, value)
                    f.write(s)
    return quest_found

def get_all_npc_names():
    filepath = os.path.join("data", "master_files", "npcs")
    files = os.listdir(filepath)
    mylist = []
    for a_name in files:
        if a_name == ".DS_Store":
            continue
        temp = a_name.replace(".txt", "")
        mylist.append(temp)
    # [print(i) for i in mylist]
    return mylist

def get_all_npc_names_by_zone(zone_name, map_name):
    filepath = os.path.join("data", "zones", zone_name, map_name, "conversations")
    if os.path.isdir(filepath) == False:
        s = "This isn't a valid directory: {}".format(filepath)
        print(s)
        # raise ValueError(s)
        return None
    filenames = os.listdir(filepath)
    if len(filenames) == 0:
        s = "There are no files in this directory: {}".format(filepath)
        raise ValueError(s)
    mylist = []
    for filename in filenames:
        myint = filename.find("_")
        name = filename[0:myint].lower()
        # print("name: {}\nnames: {}".format(name, constants.NPC_NAMES))
        if name in constants.NPC_NAMES:
            mylist.append(filename[0:myint].lower())
    mylist = list(set(mylist))
    if len(mylist) == 0:
        s = "There are no files in this directory: {}".format(filepath)
        raise ValueError(s)
    return mylist

def get_quest(quest_name):
    basepath = os.path.join("data", "zones")
    # looking for duplicates
    if _no_quest_duplicates() == False:
        raise ValueError("Error: There are duplicate quests!")
    # ----
    """Gets all quests and indicates whether they are accepted or completed."""
    filepaths = get_histories_filenames(basepath)
    mylist = []
    for filepath in filepaths:
        mydict = read_file(filepath)[0]
        if mydict["quest_name"] == quest_name:
            return mydict
    return None

def get_all_weapon_names():
    # data/master_files/inventory_files/weapon_items.txt
    all_names = []
    filepath = os.path.join("data", "master_files", "inventory_files", "weapon_items.txt")
    mylist = read_data_file(filepath, 11)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name":
                all_names.append(value)
    if len(all_names) == 0: raise ValueError("Error")
    return all_names

def get_all_consumable_names():
    # data/master_files/inventory_files/weapon_items.txt
    all_names = []
    filepath = os.path.join("data", "master_files", "inventory_files", "consumable_items.txt")
    mylist = read_data_file(filepath, 11)
    for mydict in mylist:
        for key, value in mydict.items():
            if key == "name":
                all_names.append(value)
    if len(all_names) == 0: raise ValueError("Error")
    return all_names

def get_map_names(zone_name):
    filedirectory = os.path.join("data", "zones", zone_name)
    directory_names = os.listdir(filedirectory)
    mylist = []
    for elem in directory_names:
        if elem.find("map") > -1:
            mylist.append(elem)
    return mylist

def find_an_image_file(basepath, search_term):
    mylist = []
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file.find(search_term) > -1:
                temp = os.path.join(root, file)
                mylist.append(temp)
    return mylist

def check_that_player_has_a_gold_coin(player_name):
    filepath = os.path.join("data", "playing_characters", player_name, "inventory", "weapon_items.txt")
    if os.path.isfile(filepath) == False: raise ValueError("Error")
    mylist = read_data_file(filepath, 11)
    for mydict in mylist:
        if mydict["name"] == "gold coin":
            return True
    return False

def get_least_used_letter():
    all_npc_names = get_all_npc_names()
    first_letters = []
    mylist = []
    remainders = []
    used_letters = {}
    for a_letter in constants.ALPHABET:
        used_letters[a_letter] = 0
    for a_name in all_npc_names:
        first_letter = a_name[0:1].lower()
        # print(a_name[0:1].lower())
        used_letters[first_letter] += 1
    # ----
    least_used_value = 1000
    least_used_letter = ""
    for key, value in used_letters.items():
        # print(key, value)
        if value < least_used_value:
            least_used_letter = key
            least_used_value = value
    return least_used_letter

# def get_random_noun():
#     filepath = os.path.join("data", "master_files", "nouns.txt")
#     with open(filepath, "r") as f:
#         mylines = f.readlines()
#         mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
#     myindex = random.randint(0, len(mylines))
#     myint = mylines[myindex]
#     return myint

# def get_random_adjective():
#     filepath = os.path.join("data", "master_files", "adjectives.txt")
#     with open(filepath, "r") as f:
#         mylines = f.readlines()
#         mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
#     myindex = random.randint(0, len(mylines))
#     myint = mylines[myindex]
#     return myint

def get_random_word(number_of_words, part_of_speech):
    if part_of_speech == "verb":
        filepath = os.path.join("data", "master_files", "verbs.txt")
    elif part_of_speech == "noun":
        filepath = os.path.join("data", "master_files", "nouns.txt")
    elif part_of_speech == "adjective":
        filepath = os.path.join("data", "master_files", "adjectives.txt")
    else:
        s = "I do not recognize this part of speech: {}".format(part_of_speech)
        raise ValueError(s)
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    # ----
    mylist = []
    for i in range(number_of_words):
        myindex = random.randint(0, len(mylines))
        myword = mylines[myindex]
        mylist.append(myword)
    return mylist

def vowel_substitution(a_word):
    new_word = ""
    for a_letter in a_word:
        if a_letter in constants.VOWELS:
            rand_int = random.randint(0, len(constants.VOWELS)-1)
            random_vowel = constants.VOWELS[rand_int]
            new_word += random_vowel
        else:
            new_word += a_letter
    # print(a_word)
    # print(new_word)
    return new_word

def form_words_01():
    random_verbs = get_random_word(4, "verb")
    print(random_verbs)
    random_nouns = get_random_word(4, "noun")
    print(random_nouns)
    random_adjectives = get_random_word(4, "adjective")
    print(random_adjectives)
    # ----
    for x, y, z in zip(random_verbs, random_adjectives, random_nouns):
        print("----------")
        print(x, y, z)
        print(vowel_substitution(x), vowel_substitution(y), vowel_substitution(z))

def read_verbs():
    filepath = os.path.join("data", "master_files", "verbs.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    # [print(i) for i in mylines]
    mylist = []
    new_list = []
    temp_list = []
    for a_line in mylines:
        temp = ""
        for a_char in a_line:
            # print(a_char, ord(a_char))
            # if ord(a_char) == 9:
            if a_char in constants.ALPHABET:
                temp += a_char
            else:
                temp_list.append(temp)
                temp = ""
    temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
    temp_list = list(set(temp_list))
    [print(i) for i in temp_list]

def first_name_stems():
    filepath = os.path.join("data", "master_files", "first_names_medieval.txt")
    with open(filepath, "r") as f:
        medieval_first_names = f.readlines()
        medieval_first_names = [i.strip() for i in medieval_first_names if len(i.strip()) > 0]
    # ----
    stems = []
    for a_name in medieval_first_names:
        # print(a_name)
        name = ""
        counter = 0
        for mychar in a_name:
            # print(mychar)
            if mychar in constants.VOWELS:
                counter += 1
                # print("counter: {}".format(counter))
            if counter < 2:
                name += mychar
            else:
                stems.append(name)
                name = ""
                continue
    stems = [i.strip() for i in stems if len(i.strip()) > 0]
    print(stems)
    # ----
    filepath = os.path.join("data", "master_files", "first_names_stem.txt")
    with open(filepath, "w") as f:
        for elem in stems:
            s = "{}\n".format(elem)
            f.write(s)

def make_NPC_first_name(race, sex):
    if not race in ["human", "hobbit", "elf"]: raise ValueError("Error")
    if not sex in ["female", "male"]: raise ValueError("Error")
    # ----
    filepath = os.path.join("data", "master_files", "names", "first_names_stem.txt")
    with open(filepath, "r") as f:
        stem_names = f.readlines()
        stem_names = [i.strip() for i in stem_names if len(i.strip()) > 0]
    if race == "human":
        male_endings = ["ael", "ert", "ach", "aith", "dil", "ion", "orn", "rin"]
        female_endings = ["nel", "in", "el", "inel", "ian", "ar", "iel", "eth", "ry"]
        names = []
        for stem_name in stem_names:
            if sex == "male":
                for male_ending in male_endings:
                    s = "{}{}".format(stem_name, male_ending)
                    names.append(s)
            elif sex == "female":
                for female_ending in female_endings:
                    s = "{}{}".format(stem_name, female_ending)
                    names.append(s)
            elif sex == "other":
                raise NotImplemented
            else:
                s = "I don't recognize this sex: {}".format(sex)
                raise ValueError(s)
    elif race == "hobbit":
        male_endings = ["gar", "grim", "rod", "wise", "ger", "ard", "son", "bo"]
        female_endings = ["a", "yst", "ica", "del", "ins", "is", "rida", "nda", "ta"]
        raise NotImplemented
    elif race == "elf":
        male_endings = ["dir", "ras", "nor", "rod", "roth", "del", "gon", "nas", "eg", "thir", "born"]
        female_endings = ["ian", "hel", "ian", "wen", "dis", "las", "riel", "ril", "is", "ieu", "as"]
        raise NotImplemented
    else:
        s = "I don't recognize this race: {}".format(race)
        raise ValueError(s)
    return names

def make_NPC_last_name():
    """For now, I'm just reading the names from a file."""
    filepath = os.path.join("data", "master_files", "names", "last_names_medieval.txt")
    with open(filepath, "r") as f:
        names = f.readlines()
        names = [i.strip() for i in names if len(i.strip()) > 0]
    return names

def medieval_name():
    filepath = os.path.join("data", "master_files", "last_names_medieval.txt")
    with open(filepath, "r") as f:
        medieval_last_names = f.readlines()
        medieval_last_names = [i.strip() for i in medieval_last_names if len(i.strip()) > 0]
    filepath = os.path.join("data", "master_files", "first_names_medieval.txt")
    with open(filepath, "r") as f:
        medieval_first_names = f.readlines()
        medieval_first_names = [i.strip() for i in medieval_first_names if len(i.strip()) > 0]
    # ----
    last_names = []
    for i in range(len(medieval_last_names)):
        myindex = random.randint(0, len(medieval_last_names)-1)
        myword = medieval_last_names[myindex]
        last_names.append(myword)
    first_names = []
    for i in range(len(medieval_first_names)):
        myindex = random.randint(0, len(medieval_first_names)-1)
        myword = medieval_first_names[myindex]
        first_names.append(myword)
    # ----
    first_names = list(set(first_names))
    last_names = list(set(last_names))
    for first_name, last_name in zip(first_names, last_names):
        print(first_name, last_name)

def get_random_NPC_name(race, sex, number_of_names, first_letter=""):
    def get_name(first, last):
        myint1 = random.randint(0, len(first)-1)
        first_name = first[myint1]
        myint2 = random.randint(0, len(last)-1)
        last_name = last[myint2]
        return first_name, last_name
    # ----
    first = make_NPC_first_name(race, sex)
    last = make_NPC_last_name()
    names = []
    besafe = 0
    counter = 0
    while len(names) < number_of_names:
        f, l = get_name(first, last)
        s = "{} {}".format(f, l)
        if len(first_letter) == 1:
            # print(s[0:1])
            if s[0:1].lower() == first_letter:
                names.append(s)
        else:
            names.append(s)
        # ----
        besafe += 1
        if besafe > 2000:
            s = "Runaway counter!"
            raise ValueError(s)
        names = list(set(names))
    return names

def list_int_to_str(mylist):
    a_list = []
    for elem in mylist:
        s = "{}".format(elem)
        a_list.append(s)
    return a_list

def has_two_vowels(name):
    counter = 0
    for mychar in name:
        if mychar in constants.VOWELS:
            counter += 1
    if counter == 2: return True
    return False

def _get_first_vowel(name):
    position = 0
    for mychar in name:
        if mychar in constants.VOWELS:
            return mychar, position
        position += 1
    return None, None

def _get_second_vowel(name):
    position = 0
    counter = 1
    for mychar in name:
        if mychar in constants.VOWELS:
            if counter == 2:
                return mychar, position
            counter += 1
        position += 1

def _get_last_vowel(name):
    for mychar in reversed(name):
        if mychar in constants.VOWELS:
            return mychar

def swap_first_vowel_and_last_vowel(name):
    try:
        first_vowel, location = _get_first_vowel(name)
    except Exception as e:
        t = "name: {}".format(name)
        s = "{}\n{}".format(e, t)
        raise ValueError(s)
    last_vowel = _get_last_vowel(name)
    temp = []
    for mychar in name:
        if mychar == first_vowel:
            temp.append(last_vowel)
        elif mychar == last_vowel:
            temp.append(first_vowel)
        else:
            temp.append(mychar)
    print(temp)
    return ''.join(temp)

def swap_vowels(name):
    if has_two_vowels(name) == False:
        raise ValueError("Error")
    first_vowel, location01 = _get_first_vowel(name)
    second_vowel, location02 = _get_second_vowel(name)
    temp = []
    for mychar in name:
        if mychar == first_vowel:
            temp.append(second_vowel)
        elif mychar == second_vowel:
            temp.append(first_vowel)
        else:
            temp.append(mychar)
    return ''.join(temp)

def put_last_letter_second(name):
    last_letter = name[len(name)-1]
    name = name[:-1]
    counter = 0
    temp = []
    for mychar in name:
        if counter == 1:
            temp.append(last_letter)
            temp.append(mychar)
        else:
            temp.append(mychar)
        counter += 1
    return ''.join(temp)

def get_file_name_from_dir_path(directory_path):
    myint = directory_path.rfind("/")
    mystring = directory_path[myint+1:]
    return mystring

def is_even(myint):
    if (myint % 2) == 0: return True
    return False

def get_images_indexes(rows, columns):
    pick = 2
    if pick == 1:
        myinc = -64
        for i in range(rows):
            print(i * myinc, (columns - 1) * myinc)
    elif pick == 2:
        xy = [(0, 0), (60, 0), (120, 0), (180, 0), (240, 0), (300, 0)]
        for x, y in xy:
            print(x, y)

    # fx1 = 0
    # fy1 = 0
    # fx2 = (fx1 + row_inc)
    # fy2 = 0
    # fx3 = fx2 + row_inc
    # fy3 = 0
    # fx4 = fx3 + row_inc
    # fy4 = 0
    # fx5 = fx4 + row_inc
    # fy5 = 0
    # fx6 = fx5 + row_inc
    # fy6 = 0
    # fx7 = fx6 + row_inc
    # fy7 = 0
    # fx8 = fx7 + row_inc
    # fy8 = 0
    # fx9 = fx8 + row_inc
    # fy9 = 0

if __name__ == "__main__":
    get_images_indexes(9, 1)