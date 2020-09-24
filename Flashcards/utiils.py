import constants as con
import os, sys
import random

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def key_value(mystring, mydict):
    myint = mystring.find(":")
    if myint == -1:
        raise ValueError("Colon not found in string! String: {}".format(mystring))
    mykey = mystring[0:myint].strip()
    myvalue = mystring[myint+1:].strip()
    if is_int(myvalue):
        myvalue = int(myvalue)
    mydict[mykey] = myvalue
    return mydict

def key_value_line(mystring):
    myint = mystring.find(":")
    if myint == -1:
        raise ValueError("Colon not found in string! String: {}".format(mystring))
    mykey = mystring[0:myint].strip()
    myvalue = mystring[myint+1:].strip()
    if is_int(myvalue):
        myvalue = int(myvalue)
    return myvalue

# ---------------------------------------------------

def clear_screen():
    os.system('clear')

def top_height(text_list, font):
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

def get_percent():
    def is_valid(mystring):
        if len(mystring) == 0: return False
        if not is_int(mystring): return False
        myint = int(mystring)
        if (myint >= 0 and myint <= 99):
            return True
        return False
    print("What level of mastery would you like to set? (0 to 99)")
    print("(All questions falling beneath the indicated level will be displayed.)")
    user_input = ""
    while not is_valid(user_input):
        user_input = input("> ").lower().strip()
        print("user input: {}".format(user_input))
    return int(user_input)


def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def draw_multiple_lines_to_right_window(screen, text, font, width_offset,
                                        height_offset, line_length=45, color=(0,0,0)):
    text_list = []
    if type(text) == type("bla"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        text_list = text
    else:
        s = "Doh! That type of data ({}) shouldn't be here!".format(type(text))
        raise ValueError(s)
    text_height = top_height(text_list, font)
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset + height_offset
        top = (text_height * count) + height_offset
        screen.blit(surface, (left, top))

def read_in_scores(filepath):
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    if len(mylines) == 0:
        raise ValueError("Error!")
    mylist = []
    for i in range(0, len(mylines), 3):
        mydict = {}
        for j in range(3):
            elem = mylines[i + j]
            mydict = key_value(elem, mydict)
        mylist.append(mydict)
    return mylist

def init_file_change(field, value):
    s = "{}: {}".format(field, value)
    # -----------------------------------
    filepath = os.path.join("data", "init.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    mylist = []
    for line in mylines:
        # print("field: ", field)
        # print("value: ", value)
        if field in line:
            mylist.append(s)
        else:
            mylist.append(line)
    print("{} Init File {}".format("-" * 20, "-" * 20))
    # [print(i) for i in mylist]
    print("-" * 40)
    with open(filepath, "w") as f:
        for elem in mylist:
            f.write("{}\n".format(elem))

def read_init_file():
    filepath = os.path.join("data", "init.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    mydict = {}
    for line in mylines:
        mydict = key_value(line, mydict)
    return mydict

def goodbye():
    s = "Goodbye! Thanks for playing."
    sys.exit(s)

def get_accuracy_scores(scores, myindex):
    # print(scores, type(scores))
    # print(myindex, type(myindex))
    # print("myindex: {} ({})".format(myindex, type(myindex)))
    elem = scores[myindex]
    return elem["times_presented"], elem["times_correct"]

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
    text_height = top_height(text_list, font)
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))

def numbers_from_string(mystring):
    if type(mystring) == type(123): return [mystring]
    mylist = mystring.split(";")
    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
    return mylist

def is_valid_range(mystring, length_of_list):
    if not is_int(mystring): return False
    myint = int(mystring)
    if myint == 0: return False
    if myint <= len(length_of_list):
        return True
    return False


def print_banner(mystring):
    middle = "{} {} {}".format("#" * 10, mystring, "#" * 10)
    middle_length = len(middle)
    print("#" * middle_length)
    print(middle)
    print("#" * middle_length)

def init_file_exists(filepath):
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    if len(mylines) == 0:
        return False
    # ----
    mydict = {}
    for i in range(len(mylines)):
        try:
            mydict = key_value(mylines[i], mydict)
        except:
            print("My lines: {}".format(mylines))
            raise ValueError("Error")
    # print("length: {}".format(len(mydict)))
    # for key, value in mydict.items():
    #     print("key:", key)
    #     print("value:", value)
    if len(mydict["quiz_name"]) == 0: return False
    if len(mydict["selection_method"]) == 0: return False
    if type(mydict["selection_number"]) != type(123): return False
    if type(mydict["selection_mastery"]) != type(123): return False
    return True

def read_tarot():
    filepath = "/Users/BigBlue/Documents/Programming/images/rider_waite_tarot"
    major_arcana = ["the_fool", "the_magician", "the_high_priestess", "the_empress", "the_emperor", "the_hierophant"]
    major_arcana += ["the_lovers", "the_chariot", "justice", "the_hermit", "wheel_of_fortune", "strength", "the_hanged_man"]
    major_arcana += ["death", "temperance", "the_star", "the_moon", "the_sun", "judgement", "the_world"]
    numerals = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    suits = ["wands", "cups", "swords", "pentacles"]
    # ----
    mylist = []
    for numeral in numerals:
        for suit in suits:
            mylist.append(os.path.join(filepath, "{}_of_{}.jpg".format(numeral, suit)))
    for elem in mylist:
        print(elem)
        with open(elem, "r") as f:
            f.close()

def randomize_cards(mycards):
    indexes = []
    cards_selected = []
    be_safe = 0
    while len(indexes) < len(mycards):
        this_card = random.choice(mycards)
        if not this_card.index in indexes:
            indexes.append(this_card.index)
            cards_selected.append(this_card)
        be_safe += 1
        if be_safe > 1000:
            raise ValueError("Not safe!!!!")
    return cards_selected

def get_directories(filepath):
    filenames = os.listdir(filepath)
    mylist = []
    for elem in filenames:
        if elem != ".DS_Store":
            mylist.append(elem.replace("_", " "))
    # [print(i) for i in mylist]
    return mylist



# ======================================================

if __name__ == "__main__":
    filepath = os.path.join("data", "quizes")
    get_directories()
    # read_init_file()
    # read_tarot()
    # field = ""
    # value = ""
    # init_file_change(field, value)
