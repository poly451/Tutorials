import os, sys

def formatted_header(max_len, first_title):
    temp = max_len/2 - len(first_title)/2 - 1
    side_len = round(temp)
    second_line = "{} {} {}".format("#" * side_len, first_title, "#" * side_len)
    first_line = "#" * len(second_line)
    print(first_line)
    print(second_line)

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def view_directory(extension):
    myfiles = os.listdir("data")
    newlist = []
    for file in myfiles:
        if file.find(extension) != -1:
            newlist.append(file)
    # [print(i) for i in newlist]
    return newlist

def goodbye():
    print("Goodbye! 😀")

def m_con(myint):
    t = -1
    if myint == 1: t= "January"
    elif myint == 2: t = "February"
    elif myint == 3: t = "March"
    elif myint == 4: t = "April"
    elif myint == 5: t = "May"
    elif myint == 6: t = "June"
    elif myint == 7: t = "July"
    elif myint == 8: t = "August"
    elif myint == 9: t = "September"
    elif myint == 10: t = "October"
    elif myint == 11: t = "November"
    elif myint == 12: t = "December"
    else:
        s = "Opps! That value wasn't found: {}".format(myint)
        raise ValueError(s)
    return t

def is_valid(mystring, mylist):
    if not is_int(mystring): return False
    myint = int(mystring)
    for i in range(len(mylist)):
        if myint - 1 == i:
            return True
    return False

def strip_value(mystring, mydict):
    myint = mystring.find(":")
    if myint == -1:
        s = "Error! : was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    tag = mystring[0:myint].lower().strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error")
    if len(value) == 0:
        raise ValueError("Error")
    mydict[tag] = int(value) if is_int(value) else value
    return mydict

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def print_elements(mylist, elements_per_line):
    # if len(mylist) <= elements_per_line:
    #     print(mylist)
    mycounter = 0
    while mycounter <= len(mylist):
        lower = mycounter
        mycounter += elements_per_line
        s = ", ".join(mylist[lower:mycounter])
        print(s)

def format_voice_id(name):
    name = "{}{}".format(name[0:1].upper(), name[1:].lower())
    print("name: {}".format(name))
    full_name = "com.apple.speech.synthesis.voice.{}".format(name)
    print("full name: {}".format(full_name))
    return full_name

if __name__ == "__main__":
    # formatted_header(60, "first title")
    full_name = format_voice_id("whipper")
    print(full_name)
