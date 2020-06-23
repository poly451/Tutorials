import sys, os
import subprocess as sp
import constants as con
from shutil import copyfile

# ---------------------------------------------

def get_char_info():
    with open(os.path.join("data", "current_char.txt"), "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        char_name = mylines[0]
        char_kind = mylines[1]
    return char_name, char_kind

def save_char_info(char_name, char_kind):
    filepath = os.path.join("data", "current_char.txt")
    with open(filepath, "w") as f:
        f.write("{}\n".format(char_name))
        f.write(char_kind)


def _name_is_valid(player_name):
    if not (len(player_name) >= con.MIN_LENGTH_FOR_NAME and
            len(player_name) <= con.MAX_LENGTH_FOR_NAME):
        return False
    if " " in player_name:
        return False
    return True

def get_player_info():
    player_name = ""
    player_kind = ""
    while not _name_is_valid(player_name):
        print("What is your character's name?")
        player_name = input("> ").lower().strip()
    while not player_kind in con.CHARACTER_KINDS:
        print("What is your character's class?")
        print("Choices: ", ', '.join(con.CHARACTER_KINDS).upper())
        player_kind = input("> ").lower().strip()
    return player_name, player_kind

# ---------------------------------------------

# def set_up_player_directory(player_name, player_kind):
#     """Sets up a player directory and adds required files."""
#     directory_name = ""
#     s = "{}_{}".format(player_name, player_kind)
#     directory_path = os.path.join("data", "saved_player_data", s)
#     try:
#         if not os.path.exists(directory_path):
#             os.mkdir(directory_path)
#     except Exception as e:
#         raise ValueError(e)
#     for elem in con.ZONE_KINDS:
#         filename = "{}.txt".format(elem)
#         source = os.path.join("data", "master_files", "tiles", filename)
#         destination = os.path.join("data", "saved_player_data", "tiles", filename)
#         copyfile(source, destination)

# ---------------------------------------------

def copy_directory(char_name, char_kind):
    """
    Copies all moster files over to the new character's directory
    :param char_name: The new character's name
    :param char_kind: The class of the new character
    :return: None
    """
    char_dir = "{}_{}".format(char_name, char_kind)
    source_directory = "data/master_files"
    destination_directory = os.path.join("data/player_files/", char_dir)
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower() == ".ds_store":
                continue
            old_path = os.path.join(root, file)
            new_path = root.replace(source_directory, destination_directory)
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            new_path = os.path.join(new_path, file)
            if not os.path.exists(new_path):
                with open(new_path, "w") as f:
                    f.write("")
            copyfile(old_path, new_path)

def list_directory():
    # traverse root directory, and list directories as dirs and files as files
    # from: https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
    root = "/Users/BigBlue/Documents/Programming/Python/tutorials/YouTube_2020/YouTube_2020_02/rpg_simple/version14/data/master_files"
    for root, dirs, files in os.walk(root):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            print(len(path) * '---', file)

def walk_directory(base_root):
    # traverse root directory, and list directories as dirs and files as files
    print("base_root: ", base_root)
    for root, dirs, files in os.walk(base_root):
        # print("root: ", root)
        # print("dirs: ", dirs)
        for file in files:
            if file.lower() == ".ds_store":
                continue
            mypath = os.path.join(root, file)
            # print("file: ", file)
            print(mypath)

# ---------------------------------------------

def capitalize(mystring):
    s ="{}{}".format(mystring[0:1].upper(), mystring[1:])
    return s

def clear_screen():
    tmp = sp.call('clear', shell=True)

def strip_list_elements(mylist):
    list01 = []
    for elem in mylist:
        # print("elem[0][0]: ", elem[0][0])
        if elem[0][0].strip() == "#":
            continue
        list02 = []
        for j in elem:
            list02.append(j.strip())
        list01.append(list02)
    return list01

def _capitalize_compass_names(a_sentence):
    my_dir = ["north", "south", "west", "east"]
    for compass in my_dir:
        a_sentence = a_sentence.replace(compass, compass.upper())
    return a_sentence

# def _break_string_into_sentences(a_sentence):
#     if not " " in a_sentence: return capitalize(a_sentence)
#     temp = ""
#     mylist = []
#     look_for = ". "
#     temp_sentence = a_sentence
#     while look_for in temp_sentence:
#         # print("a_sentence: ", a_sentence)
#         myint = temp_sentence.find(look_for) + len(look_for)
#         new_sentence = temp_sentence[:myint]
#         new_sentence = _capitalize_compass_names(new_sentence)
#         mylist.append(capitalize(new_sentence))
#         temp_sentence = temp_sentence[myint:].strip()
#     mylist.append(capitalize(temp_sentence))
#     return mylist

def _break_string_into_sentences(a_sentence):
    if len(a_sentence) == 0:
        raise ValueError("The text string used as input cannot be empty!")
    mylist = []
    if not ". " in a_sentence:
        a_sentence = _capitalize_compass_names(a_sentence)
        a_sentence = capitalize(a_sentence)
        mylist.append(a_sentence)
        return mylist
    look_for = ". "
    while len(a_sentence) > 0:
        if not ". " in a_sentence:
            a_sentence = _capitalize_compass_names(a_sentence)
            a_sentence = capitalize(a_sentence)
            mylist.append(a_sentence)
            a_sentence = ""
        else:
            myint = a_sentence.find(look_for) + len(look_for)
            new_sentence = a_sentence[:myint]
            new_sentence = _capitalize_compass_names(new_sentence)
            new_sentence = capitalize(new_sentence)
            mylist.append(new_sentence)
            a_sentence = a_sentence[myint:].strip()
    return mylist

def capitalize_sentences(a_sentence):
    sentence_list = _break_string_into_sentences(a_sentence)
    # print("sentence list: ", sentence_list, type(sentence_list))
    # [print(i) for i in sentence_list]
    if len(sentence_list) > 1:
        return '\n'.join(sentence_list)
    return ''.join(sentence_list)

def open_text_file(filepath):
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    return mylines

def key_value_pair(mydict_elem, mydict):
    myint = mydict_elem.find(":")
    key = mydict_elem[0:myint].strip()
    if key == -1:
        raise ValueError("Error! Separator character not found.")
    value = mydict_elem[myint+1:].strip()
    # print("key: {}, value: {}".format(key, value))
    mydict[key] = value
    return mydict
# ===============================================
# ===============================================

def copy_a_directory():
    # player_name = capitalize("bob")
    # print(player_name)
    char_name = "bob"
    char_kind = "warrior"
    # user_directory = "{}_{}".format(char_name, char_kind)
    # base_root = "/Users/BigBlue/Documents/Programming/Python/tutorials/YouTube_2020/YouTube_2020_02/rpg_simple/tutorial04/data/master_files"
    # new_root = "/Users/BigBlue/Documents/Programming/Python/tutorials/YouTube_2020/YouTube_2020_02/rpg_simple/tutorial04/data/saved_player_data/{}".format(user_directory)
    copy_directory(char_name, char_kind)

if __name__ == "__main__":
    player_name, player_kind = get_player_info()
    print("Player name: ", player_name)
    print("Player kind: ", player_kind)
