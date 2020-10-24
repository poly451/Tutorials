import os
import constants as con

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def clean_text(mylines):
    def myfilter(mychar):
        chosen = [8216, 8212, 8217, 8220, 8221, 8230]
        if ord(mychar) in chosen:
            return True
        if (ord(mychar) >= 0 and ord(mychar)) <= 127:
            return True
        return False
    big_list = []
    for elem in mylines:
        s = ""
        for mychar in elem:
            if myfilter(mychar) == True:
            # if (ord(mychar) >= 0 and ord(mychar)) <= 127:
                s += mychar
            else:
                print("{} ({})".format(mychar, ord(mychar)))
        big_list.append(s)
    return big_list

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

def get_directories(filepath):
    filenames = os.listdir(filepath)
    mylist = []
    for elem in filenames:
        if elem != ".DS_Store":
            if elem.find(".txt") == -1:
                print("Filepath: {}".format(filepath))
                raise ValueError("This doesn't appear to be a text file: {}".format(elem))
            mylist.append(elem.replace("_", " "))
    # [print(i) for i in mylist]
    return mylist

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

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


    
