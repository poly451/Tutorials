import random

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def get_direction():
    myint = random.randint(0, 3)
    retvar = ""
    if myint == 0:
        retvar = "north"
    elif myint == 1:
        retvar = "east"
    elif myint == 2:
        retvar = "south"
    elif myint == 3:
        retvar = "west"
    return retvar

def pad_digit(the_digit, padding):
    if the_digit > 999:
        raise ValueError("Did not code for this.")
    if not padding in [2, 3]:
        raise ValueError("Did not code for this.")
    if the_digit > 9 and the_digit < 100:
        if padding == 2:
            return the_digit
        elif padding == 3:
            return "0{}".format(the_digit)
        else:
            raise ValueError("Error!")
    elif the_digit >= 100 and the_digit <= 999:
        if padding == 3:
            return the_digit
        else:
            raise ValueError("Error!")
    elif the_digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if padding == 1:
            return the_digit
        elif padding == 2:
            return "0{}".format(the_digit)
        elif padding == 3:
            return "00{}".format(the_digit)
        else:
            raise ValueError("Error!")
    else:
        return "0{}".format(the_digit)

def key_value(mystring, mydict):
    myint = mystring.find(":")
    if myint == -1:
        print("mystring: {}".format(mystring))
        s = "Error! : was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error")
    if len(value) == 0:
        raise ValueError("Error")
    try:
        mydict[tag] = int(value) if is_int(value) else value
    except Exception as e:
        print("tag: {}".format(tag))
        print(e)
    return mydict

def create_new_direction_path(length_of_path):
    s = ""
    for _ in range(length_of_path):
        the_direction = get_direction()
        s += "{} -1, ".format(the_direction)
    return s[:-2]
