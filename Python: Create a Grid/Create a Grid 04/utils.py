import pygame
import constants
import os, sys

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def key_value(mystring, mydict):
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
    mydict[tag] = int(value) if is_int(value) else value
    return mydict

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
    text_height = top_height(text_list, font) + 3
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))

def get_quadrants(hit_points, quadrants):
    # print(hit_points % quadrants)
    # print(hit_points % quadrants)
    # if (hit_points % quadrants) > 0:
    #     s = "The number of hit points a critter/monster has must divide\n"
    #     s += "evenly into the number of quadrants.\n"
    #     s += "hit points: {}; quadrants: {}".format(hit_points, quadrants)
    #     raise ValueError(s)
    s = int(hit_points / quadrants)
    n = hit_points
    # print("n = {}".format(n))
    # ----
    x1 = n - ((s * 1) - 1)
    y1 = n - 1
    # print("x1 {} = {} - (({} * 1) - 1)".format(x1, n, s))
    # print("y1 {} = {} - 0".format(y1, s))
    # print("{},{}; s = {}".format(x1, y1, s))
    # print("----")
    # ----
    x2 = n - ((s * 2) - 1)
    y2 = n - s
    # print("x2 {} = {} - (({} * 1) - 1)".format(x2, n, s))
    # print("y2 {} = {} - 0".format(y2, s))
    # print("{},{}; s = {}".format(x2, y2, s))
    # print("----")
    # ----
    x3 = n - ((s * 3) - 1)
    y3 = n - (s * 2)
    # print("{},{}; s = {}".format(x3, y3, s))
    # ----
    x4 = n - ((s * 4) - 1)
    y4 = n - (s * 3)
    # print("{},{}; s = {}".format(x4, y4, s))
    # ----
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

def get_range(beginning, ending):
    mylist = []
    for elem in list(range(beginning, ending+1)):
        # print(elem)
        mylist.append(elem)
    return mylist

def get_ranges(number_of_max_hit_points, number_of_quadrants):
    print("number of hit points: {}; number of quadrants: {}".format(number_of_max_hit_points, number_of_quadrants))
    divisions = get_quadrants(number_of_max_hit_points, number_of_quadrants)
    # print("divisions: {}".format(divisions))
    # print("divisions 1: {}".format(divisions[0]))
    n = [divisions[0][1] + 1]
    range1 = get_range(divisions[0][0], divisions[0][1])
    range2 = get_range(divisions[1][0], divisions[1][1])
    range3 = get_range(divisions[2][0], divisions[2][1])
    range4 = get_range(divisions[3][0], divisions[3][1])
    # print("{}; {}; {}; {}; {}".format(n, range1, range2, range3, range4))
    return n, range1, range2, range3, range4

def check_hit_points(hit_points, quadrants):
    if (hit_points % quadrants) > 0:
        s = "The number of hit points a critter/monster has must divide\n"
        s += "evenly into the number of quadrants.\n"
        s += "hit points: {}; quadrants: {}".format(hit_points, quadrants)
        return False
    return True

def convert_direction(the_direction):
    s = ""
    if the_direction == 90:
        s = "UP"
    elif the_direction == -90:
        s = "DOWN"
    elif the_direction == 0:
        s = "RIGHT"
    elif the_direction == 180:
        s = "LEFT"
    else:
        t = "This was not found: {}".format(the_direction)
        raise ValueError(t)
    return s

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

def orient_image(the_image, direction_am_facing):
    """Default orientation of the image is DOWN (-90)."""
    if direction_am_facing == constants.DOWN:
        the_image = pygame.transform.rotate(the_image, 0)
    elif direction_am_facing == constants.UP:
        the_image = pygame.transform.rotate(the_image, 180)
    elif direction_am_facing == constants.LEFT:
        the_image = pygame.transform.rotate(the_image, -90)
    elif direction_am_facing == constants.RIGHT:
        the_image = pygame.transform.rotate(the_image, 90)
    return the_image

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def draw_text_button(screen, text, myrect, font, font_color=constants.BLACK, background_color=constants.WHITE, use_inner=False):
    inner_area = pygame.Rect((-28, -15, myrect[2], myrect[3]))
    pygame.draw.rect(screen, background_color, myrect)
    txt_surface = font.render(text, True, font_color)
    if use_inner == True:
        screen.blit(txt_surface, myrect, inner_area)
    else:
        screen.blit(txt_surface, myrect)

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

def read_data_file(filepath, num_of_fields):
    big_list = []
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    big_list = []
    for i in range(0, len(mylines), num_of_fields):
        mydict = {}
        for j in range(num_of_fields):
            elem = mylines[i + j]
            mydict = key_value(elem, mydict)
        big_list.append(mydict)
    return big_list



# ===================================================

if __name__ == "__main__":
    path = os.path.join("data", "map.txt")
    read_map_file(path)
    # num_of_fields = 9
    # filepath = os.path.join("data", "player_data.txt")
    # mylist = read_data_file(filepath, num_of_fields)
    # for elem in mylist:
    #     print(elem)
