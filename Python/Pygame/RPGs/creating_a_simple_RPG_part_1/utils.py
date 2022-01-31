import os, sys
import math

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
    if len(mystring) == "": raise ValueError("Error")
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

if __name__ in "__main__":
    print("hi")
