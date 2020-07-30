def is_even(myint):
    if (myint % 2) == 0:
        return True
    return False

def convert_to_kind_of_tile(kind_of_tile):
    kind = ""
    if kind_of_tile == "r_":
        kind = "white_square"
    elif kind_of_tile == "b_":
        kind = "yellow_square"
    elif kind_of_tile == "bo":
        kind = "blue_checker"
    elif kind_of_tile == "bx":
        kind = "red_checker"
    else:
        raise ValueError("kind not found: {}".format(kind))
    return kind

# -------------------------------------------------

def _separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def draw_multiple_lines_to_screen(screen, text, font, line_length=50):
    text_list = []
    if type(text) == type("bla"):
        text_list = _separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        text_list = text
    else:
        s = "Doh! That type of data shouldn't be here!"
        raise ValueError(s)
    for count, elem in enumerate(text_list):
        text_width, text_height = 0, 0
        try:
            text_width, text_height = font.size(elem)
        except:
            print("elem: {}".format(elem))
        surface = font.render(elem, True, (0, 0, 0))
        # ----------------------
        left = 20
        top = (text_height * count) + 20
        screen.blit(surface, (left, top))

def draw_multiple_lines_to_screen_with_rect(screen, text, font, myrect, line_length=50):
    text_list = []
    if type(text) == type("bla"):
        text_list = _separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        text_list = text
    else:
        s = "Doh! That type of data shouldn't be here!"
        raise ValueError(s)
    for count, elem in enumerate(text_list):
        text_width, text_height = 0, 0
        try:
            text_width, text_height = font.size(elem)
        except:
            print("elem: {}".format(elem))
        surface = font.render(elem, True, (0, 0, 0))
        # ----------------------
        left = 20
        top = (text_height * count) + 20
        screen.blit(surface, (left + myrect[0], top + myrect[1]))

def in_range(value1, value2, tolerance):
    diff = abs(value1 - value2)
    print("tolerance: ", tolerance)
    print("diff: ", diff)
    if diff <= tolerance:
        return True
    return False

# ------------------------------------------------

if __name__ == "__main__":
    print(in_range(2, 3, .05))
