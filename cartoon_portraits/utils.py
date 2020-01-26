import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import constants as con

myletters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
       "w", "x", "y", "z", "_"]
mynumbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
myinclude = myletters + mynumbers

def parse_line(list_line):
    newlist = []
    output_list = []
    for elem in list_line:
        newlist = elem.split(",")
        new_string = ""
        this_list = []
        for elem2 in newlist:
            cleaned_string = clean_string(elem2)
            if is_number(cleaned_string):
                this_list.append(int(cleaned_string))
            else:
                this_list.append(cleaned_string)
        output_list.append(this_list)
    newlist.append(output_list)
    return output_list

def clean_string(astring):
    newstring = ""
    for elem in astring:
        if elem in myinclude:
            newstring += elem
    return newstring

def is_number(astring):
    try:
        int(astring)
        return True
    except:
        return False

def valid_property(property_name, filepath):
    with open(filepath, 'r') as f:
        choices = json.load(f)
    # [print(i[0]) for i in choices]
    for choice in choices:
        if property_name == choice[0]:
            return True
    return False

def values_are_valid(choices: list, property: str, values: list):
    if len(choices) == 0:
        raise ValueError("Error! No choices were given.")
    for choice in choices:
        if choice[0] == property:
            for value in values:
                if value >= choice[2]:
                    return False
    return True

# def viewfaces():
#     """
#     View all the selected faces.
#     :param arg: None
#     :return: None
#     """
#     with open(constants.PNG_NAMES, "r") as f:
#         images = f.readlines()
#         images = [i.strip() for i in images if len(i.strip()) > 0]
#     if len(images) > 50:
#         print("Over 50 images have been selected. If you would like to view all fifty then adjust def do_viewfaces(self, arg)")
#         print("Otherwise, narrow your selection.")
#         return False
#     filenames = []
#     for filename in images:
#         filepath = os.path.join(constants.IMAGES_DIRECTORY, filename)
#         print(filepath)
#         img = mpimg.imread(filepath)
#         imgplot = plt.imshow(img)
#         plt.show()

def viewfaces():
    """
    View all the selected faces.
    :param arg: None
    :return: None
    """
    with open(con.SAVE_IMAGE_NAMES, "r") as f:
        facelist = f.readlines()
        facelist = [i.strip() for i in facelist if len(i.strip()) > 0]
    if len(facelist) == 0:
        print("No faces were selected. Run this program again and type S.")
        return False
    if len(facelist) > con.MAX_PORTRAITS:
        s = "Over 50 images have been selected.\n"
        s += "If you would like to view all fifty then adjust def do_viewfaces(self, arg)\n"
        s += "Otherwise, narrow your selection."
        print(s)
        return False
    for filename in facelist:
        filepath = os.path.join(con.IMAGES_DIRECTORY, filename)
        print(filepath)
        img = mpimg.imread(filepath)
        imgplot = plt.imshow(img)
        plt.show()


if __name__ == "__main__":
    viewfaces()
