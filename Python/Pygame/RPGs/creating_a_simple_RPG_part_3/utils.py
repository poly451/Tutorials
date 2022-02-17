import os, sys
import math

import constants


def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def get_filepath(filename, basepath="data"):
    if os.path.isdir(filename) == True:
        s = "This is a directory NOT a filename: {}".format(filename)
        raise ValueError(s)
    if filename is None:
        return None
    if len(filename) == 0:
        return None
    # ----
    if basepath == "data":
        basepath = os.path.join("data")
    elif basepath == "images":
        basepath = os.path.join("data", "images")
    # dir_contents = os.listdir(basepath)
    # ----
    the_path_01 = None
    the_path_02 = None
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if filename.lower().strip() == file.lower().strip():
                the_path_01 = os.path.join(root, file)
                the_path_02 = file
    if the_path_01 is None and the_path_02 is None:
        return None
    if os.path.isfile(the_path_01) == True:
        return the_path_01
    if os.path.isfile(the_path_02) == True:
        return the_path_02
    # ----
    raise ValueError("Error")

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
            # if len(mylines) >= i+j:
            #     s = "mylines: {}\n".format(mylines)
            #     s += "number of fields: {}\n".format(num_of_fields)
            #     s += "i+j: {}".format(i+j)
            #     raise ValueError(s)
            try:
                elem = mylines[i + j]
            except Exception as e:
                t = "the index: {}, filepath: {}\n".format(i+j, filepath)
                t += "mylines = {}, len(mylines) = {}, i+j={}".format(mylines, len(mylines), i+j)
                s = "{}\n{}\n".format(e, t)
                raise ValueError(s)
            try:
                mydict = key_value(elem, mydict)
            except Exception as e:
                print("**********************")
                s = "----------\n"
                s += "filepath: {}, fields: {}".format(filepath, num_of_fields)
                t = "{}\n{}\n".format(e, s)
                raise ValueError(t)
        big_list.append(mydict)
    return big_list

def get_record(filepath, key_name, value_name, number_of_fields):
    mylist = read_data_file(filepath, number_of_fields)
    for elem in mylist:
        if elem[key_name] == value_name:
            return elem
    return None

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

def key_value(mystring, mydict):
    if len(mystring) == 0:
        s = "The length of this string is 0."
        raise ValueError(s)
    if mystring.find(":") == -1:
        s = "Error! A colon (:) was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    # ----
    myint = mystring.find(":")
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error: mystring = {}".format(mystring))
    if len(value) == 0:
        s = "mystring: {}; type: {}, len(mystring): {}\n".format(mystring, type(mystring), len(mystring))
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

def get_map_values(zone_name, map_name, mapkind):
    filename = "{}_{}.txt".format(map_name, mapkind)
    filepath = os.path.join("data", "zones", zone_name, map_name, filename)
    if os.path.isfile(filepath) == False:
        s = "This is not a valid file path: {}".format(filepath)
        raise ValueError(s)
    if file_is_empty(filepath) == True:
        return None
    # ---- ----
    if file_is_empty(filepath) == True:
        return False
    with open(filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    mytiles = [i[3:] for i in mytiles[2:]]
    # ------------------------------------------------------------------
    big_list = []
    for map_row in mytiles:
        mylist = map_row.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        big_list.append(mylist)
    new_list = []
    for j, a_row in enumerate(big_list):
        for i, tile_name in enumerate(a_row):
            if tile_name == "...":
                pass
            else:
                new_list.append(tile_name)
    return list(set(new_list))

def distance_between_two_points(A, B):
    dA = B[0] - A[0]
    dB = B[1] - A[1]
    dA = dA * dA
    dB = dB * dB
    return math.sqrt(dA + dB)

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

def get_player_direction(zone_name, map_name):
    filepath = os.path.join("data", "zones", zone_name, map_name, "player.txt")
    if os.path.isfile(filepath) == False: raise ValueError("Error")
    mydict = read_file(filepath)[0]
    return mydict["player_position"]

def get_all_possible_model_names():
    # data/images/characters/baldric
    dir_path = os.path.join(constants.IMAGES, "animations", "lpc")
    dir_contents = os.listdir(dir_path)
    return [i for i in dir_contents if i != '.DS_Store']

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

def testing():
    if 1 == 1.0:
        print("True")
    else:
        print("Fals")

if __name__ in "__main__":
    testing()
