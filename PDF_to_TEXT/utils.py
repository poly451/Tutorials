import os, sys
import subprocess

def get_next_sentence(parent_string):
    myint = parent_string.find(".")
    if myint == -1: return parent_string, None
    return parent_string[myint+1:].strip(), parent_string[0:myint+1].strip()

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def find_all(sentences, search_phrase, filepath, context):
    if len(filepath) == 0:
        raise ValueError("I need a filename!")
    if not type(sentences) == type([]):
        raise ValueError("Error! Expecting type list.")
    if not type(search_phrase) == type([]):
        raise ValueError("Error! Expecting type list.")
    # -----------------------
    phrase_list = []
    for elem in search_phrase:
        phrase_list.append(elem.lower().strip())
    p = False
    mylist = []
    staysafe = 0
    for count, line in enumerate(sentences):
        for phrase in phrase_list:
            # print("phrase: ", phrase)
            # print("line: ", line)
            if phrase in line:
                # t = "[**** {} ****]".format(phrase.upper())
                line = line.replace(phrase, phrase.upper())
                s = ""
                if context:
                    if count-2 >= 0: s += "{}\n".format(sentences[count-2])
                    if count-1 >= 0: s += "{}\n".format(sentences[count-1])
                    s += "{}\n".format(line)
                    if count+1 < len(sentences): s += "{}\n".format(sentences[count+1])
                    if count+2 < len(sentences): s += "{}\n".format(sentences[count+2])
                    s += "{}\n".format("-" * 20)
                else:
                    s += "{}\n".format(line)
                mylist.append([s, filepath])
    return mylist

def max_line_width(mystring, max_length):
    mylist = []
    besafe = 0
    while max_length <= len(mystring):
        temp = mystring[0:max_length].strip()
        myint = temp.rfind(" ")
        temp = temp[0:myint]
        mystring = mystring[myint:].strip()
        mylist.append(temp)
        besafe += 1
        if besafe > 30000:
            raise ValueError("Be Safe!")
    mylist.append(mystring)
    return mylist

def walk_directories_rename(base_dir):
    """
    Changes .pdf to .txt
    :param base_dir:
    :return: None
    """
    #base_dir = "/Volumes/LaCie/Multimedia Archive/Carl G. Jung"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().find(".pdf") > -1:
                old_path = os.path.join(root, file)
                new_file = file.replace(".pdf", ".txt")
                new_path = os.path.join(root, new_file)
                os.rename(old_path, new_path)
                # print("old: ", old_path)
                # print("new: ", new_path)
                # print("-" * 20)

def walk_directories(base_dir):
    #base_dir = "/Volumes/LaCie/Multimedia Archive/Carl G. Jung"
    mylist = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().find(".pdf") == -1:
                continue
            temp = os.path.join(root, file)
            if temp.find("Non-English - LT") == -1:
                mylist.append(temp)
    [print(i) for i in mylist]

def get_directories(root_directory):
    mylist = []
    for root, dirs, files in os.walk(root_directory):
        for dir in dirs:
            temp = os.path.join(root, dir)
            if temp.find("Non-English - LT") == -1:
                mylist.append(temp)
    return mylist

def get_all_files(root_directory):
    mylist = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            mylist.append(file)
    mylist = list(set(mylist))
    mylist = sorted(mylist, reverse=False)
    return mylist

def _get_filepath(filename, base_dir):
    mylist = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    raise ValueError("Error! Couldn't find file: {}".format(filename))

def get_filepaths(path):
    mylist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            temp = os.path.join(root, file)
            mylist.append(temp)
    return mylist

def get_texts(root_path, phrases):
    mylist = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            for phrase in phrases:
                if phrase.lower().strip() in file.lower().strip():
                    filepath = os.path.join(root, file)
                    mylist.append(filepath)
    return mylist

# def input_valid(mystring):
#     if len(mystring) == 0: return False

def process_input(mystring):
    mylist = []
    myint = mystring.find(",")
    if myint == -1:
        if mystring.find(" ") > -1:
            mylist = mystring.split(" ")
            mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
            return mylist
        else:
            return [mystring]
    mylist = mystring.split(",")
    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
    return mylist

def open_file(filename, base_dir):
    # filepath = "/Users/BigBlue/Documents/Programming/Python/data/texts/carl_jung/Awakening to Dreams.txt"
    # subprocess.call("atom {}".format(filepath))
    filepath = _get_filepath(filename, base_dir)
    mycmd = "{}".format(filepath)
    subprocess.run(["atom", mycmd])
    # subprocess.run(["ls", "-l"])

# ==============================================

# ===============================================

# ===========================================================
# ===========================================================

def read_file(path):
    with open(path, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    print("{} lines read".format(len(mylines)))
    # [print(i) for i in mylines]
    mytext = ''.join(mylines)
    return mytext

def main():
    output_path = "data/maps_of_meaning.txt"
    mytext = read_file(output_path)
    sentences = mytext.split(".")
    sentences = [i.strip() for i in sentences if len(i.strip()) > 0]
    search_phrases = ["meaning", "ameaning", "ofmeaning", "good", "chapter"]
    sentences = find_all(sentences, search_phrases)
    [print(i) for i in sentences]

def limit_line_length(mystring, line_length):
    s = ""
    be_safe = 0
    while len(mystring) >= line_length:
        temp_string = mystring[0:line_length]
        myint = temp_string.rfind(" ")
        if myint == -1:
            return mystring
        temp_string = temp_string[0:myint]
        mystring = mystring[myint+1:]
        s += "{}\n".format(temp_string)
        be_safe += 1
        if be_safe > 1000:
            raise ValueError("Error! mystring: {}".format(mystring))
    s += mystring
    return s

def scrape(filepath):
    temp = filepath.split(os.sep)[-1]
    myint = temp.find(".")
    return temp[0:myint]

if __name__ == "__main__":
    text = "eraistoblamethatthespiritbecamenon-spiritualandthatthevitalizingarchetypegraduallydegeneratedintorationalism,intellectualism"
    filepath = "/Users/BigBlue/Documents/Programming/Python/data/texts/carl_jung/Awakening to Dreams.txt"
    print(scrape(filepath))
    # mydict = Dictionary()
    # long_string = "This is a string. Leaves are yummy. This is another string. Will is a be a cool her. The cat sat on the mat."
    # mylist = max_line_width(long_string, 20)
    # [print(i) for i in mylist]