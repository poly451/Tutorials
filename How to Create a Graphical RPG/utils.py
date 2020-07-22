import os, sys
import pygame
import constants as con
from shutil import copyfile

p = True

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def clean_int(mystring):
    if is_int(mystring): return int(mystring)
    return mystring

def create_file(filepath):
    with open(filepath, "w") as f:
        f.write("")

def get_unique_directories(root_directory):
    mylist = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            # print("root: ", root)
            # print("dirs: ", dirs)
            mylist.append(root)
    return list(set(mylist))

def strip_value(mystring, mydict):
    myint = mystring.find(":")
    if myint == -1:
        s = "Error! : was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error")
    if len(value) == 0:
        raise ValueError("Error")
    mydict[tag] = value
    return mydict

def set_users_directory(name, kind):
    filepath = os.path.join("data", "char_info.txt")
    with open(filepath, "w") as f:
        f.write("{}\n".format(name))
        f.write(kind)

def check_files_at_startup():
    if not os.path.isdir("data"):
        s = "Error! There is no data directory!"
        raise ValueError(s)
    filepath = os.path.join("data", "master_files")
    if not os.path.isdir(filepath):
        s = "Error! There is no directory: master_files!"
        raise ValueError(s)
    filepath = os.path.join("data", "character_files")
    if not os.path.isdir(filepath):
        os.mkdir(filepath)

def get_users_directory():
    filepath = os.path.join("data", "char_info.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    char_name = mylines[0]
    char_kind = mylines[1]
    return "{}_{}".format(char_name, char_kind)

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def create_character_directory(char_name, char_kind):
    # ----
    directory_name = "{}_{}".format(char_name, char_kind)
    source_directory = os.path.join("data", "master_files")
    destination_directory = os.path.join("data", "character_files", directory_name)
    if not os.path.isdir(destination_directory):
        os.mkdir(destination_directory)
    reproduce_directory(source_directory, char_name, char_kind)

def reproduce_directory(source_filepath, char_name, char_kind):
    char_dir = "{}_{}".format(char_name, char_kind)
    # ------------------------------------------------
    filename = "{}.txt".format(char_kind)
    s_path = os.path.join("data", "classes", filename)
    new_filename = "{}.txt".format(char_name)
    # d_path = os.path.join("data", "character_files", char_dir, "char.txt")
    d_path = os.path.join("data", "character_files", char_dir, new_filename)
    create_file(d_path)
    copyfile(s_path, d_path)
    # ------------------------------------------------
    unique_dirs = get_unique_directories(source_filepath)
    for dir in unique_dirs:
        temp = "{}{}{}".format("character_files", os.sep, char_dir)
        new_dir = dir.replace("master_files", temp)
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
    # ------------------------------------------------
    top_level_files = os.listdir(source_filepath)
    for file in top_level_files:
        if ".txt" in file:
            old_file = os.path.join("data", "master_files", file)
            new_file = os.path.join("data", "character_files", char_dir, file)
            if not os.path.exists(new_file):
                if p: print("Creating file: {}".format(new_file))
                create_file(new_file)
            if p: print("Copying file from: {}\nto: {}".format(old_file, new_file))
            copyfile(old_file, new_file)
    # ------------------------------------------------
    for root, dirs, files in os.walk(source_filepath):
        for file in files:
            file = file.lower().strip()
            if ".ds_store" == file:
                continue
            source_path = os.path.join(root, file)
            temp = "{}{}{}".format("character_files", os.sep, char_dir)
            dest_path = source_path.replace("master_files", temp)
            if p:
                print("source path:", source_path)
                print("dest path:", dest_path)
                print("-" * 40)
            # -----------------------
            if not os.path.exists(dest_path):
                if p: print("Creating file: {}".format(dest_path))
                create_file(dest_path)
            copyfile(source_path, dest_path)

def draw_text_button(screen, text, myrect, font, font_color=con.BLACK, background_color=con.WHITE, use_inner=False):
    inner_area = pygame.Rect((-28, -15, myrect[2], myrect[3]))
    pygame.draw.rect(screen, background_color, myrect)
    txt_surface = font.render(text, True, font_color)
    if use_inner == True:
        screen.blit(txt_surface, myrect, inner_area)
    else:
        screen.blit(txt_surface, myrect)

def draw_text_game_messages(screen, text, font):
    txt_surface = font.render(text, True, con.BLACK)
    left = 0
    # top = con.HEIGHT + con.HEIGHT - int(con.HEIGHT / 16)
    top = int(con.HEIGHT + 75)
    width = con.WIDTH
    height = con.HEIGHT
    myrect = (left, top, width, height)
    pygame.draw.rect(screen, con.LIGHTGREY, myrect)
    screen.blit(txt_surface, myrect)

# --------------------------------------------------

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

def draw_multiple_lines_to_right_window(screen, text, font, line_length=32):
    text_list = []
    if type(text) == type("bla"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        text_list = text
    else:
        s = "Doh! That type of data shouldn't be here!"
        raise ValueError(s)
    text_height = top_height(text_list, font)
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, (0, 0, 0))
        # ----------------------
        left = con.WIDTH + 20
        top = (text_height * count) + 20
        screen.blit(surface, (left, top))

def _draw_text(screen, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    # pygame.draw.rect(screen, con.LIGHTGREY, rect)
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        screen.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text

def draw_text_big_box(screen, text, font):
    left = con.WIDTH + 10
    top = 10
    width = int(con.WINDOW_WIDTH / 2) - 10
    height = 1000
    myrect = (left, top, width, height)
    _draw_text(screen, text, con.BLACK, myrect, font)
