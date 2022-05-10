import os, sys

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
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
                s += "filepath: {}, fields: {}\n".format(filepath, num_of_fields)
                s += "elem: {}, mydict: {}\n".format(elem, mydict)
                t = "{}\n{}\n".format(e, s)
                raise ValueError(t)
        big_list.append(mydict)
    return big_list

def get_line_break(text, line_length=50):
    if is_int(line_length) == False: raise ValueError("Error")
    if type(line_length) != type(123):
        s = "line_length: {}, type: {}".format(line_length, type(line_length))
        raise ValueError(s)
    if len(text.split(" ")[0]) > line_length:
        # raise ValueError("Error")
        return None
    # ---- ---- ---- ----
    if line_length >= len(text):
        # s = "line_length: {}\n".format(line_length)
        # s += "len(text): {}".format(len(text))
        # raise ValueError(s)
        return None
    if text[line_length] == " ":
        return line_length
    line_length = line_length - 1
    while line_length > 0:
        if text[line_length] == " ":
            return line_length
        line_length -= 1
        if type(line_length) != type(123):
            s = "temp_length: {}".format(line_length)
            raise ValueError(s)
    return line_length

def parse_line(mytext, line_length):
    new_list = []
    besafe = 0
    while len(mytext) > 0:
        break_at = get_line_break(mytext, line_length)
        if break_at is None:
            new_list.append(mytext)
            return new_list
        # ----
        # print("break_at: {}".format(break_at))
        a_line = mytext[0:break_at]
        # print(a_line)
        # raise NotImplemented
        mytext = mytext[break_at:]
        new_list.append(a_line)
        mytext = mytext.strip()
        # ---- ----
        besafe += 1
        if besafe > 2000:
            s = "mytext: {}\n".format(mytext)
            s += "break_at: {}\n".format(break_at)
            s += "a_line: {}\n".format(a_line)
            raise ValueError(s)
    return new_list

def parse_text(mytext, line_length):
    mylist = mytext.split("@")
    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
    # ---- ----
    new_list = []
    for a_line in mylist:
        a_list = parse_line(a_line, line_length)
        new_list += a_list
    return new_list

def tidy_text(text, line_length):
    if len(text) > line_length:
        text_list = parse_text(text, line_length)
        text = "\n".join(text_list)
        return text
    return text

def count_characters(text):
    text = text.strip()
    s = "This text is {} characters long.".format(len(text))
    print(text)
    print(s)
# ****************************************************
# ****************************************************

# -----------------------------------------------
#             class ProgramLoop
# -----------------------------------------------
class ProgramLoop:
    def __init__(self, card_data_file):
        self.cards = Cards(card_data_file)
        self.cards.read_data()

    def _loop_okay(self, user_choice, number_of_choices):
        if is_int(user_choice) == False: return False
        user_choice = int(user_choice)
        if user_choice <= 0: return False
        if user_choice > number_of_choices: return False
        return True

    def main(self):
        index = 1
        keep_looping = True
        while keep_looping == True:
            a_card = self.cards.get_card(index=index)
            if a_card is None:
                s = "Cannot find a card that matches the given index: {}".format(index)
                raise ValueError(s)
            if a_card.command == "quit": self.goodbye()
            # ---- ---- ---- ----
            display_string, number_of_choices = a_card.get_display_string()
            print("\n" * 10)
            print(display_string)
            # ---- ----
            user_choice = input("Your choice: > ").lower().strip()
            if user_choice in ["quit", "q", "exit", "e"]: self.goodbye()
            while self._loop_okay(user_choice, number_of_choices) == False:
                user_choice = input("Your choice: > ").lower().strip()
            user_choice = int(user_choice)
            index = a_card.get_goto(user_choice)

    def goodbye(self):
        print("Goodbye!")
        sys.exit()
# ****************************************************
# ****************************************************

# -----------------------------------------------
#             class Card
# -----------------------------------------------
class Card:
    def __init__(self, mydict):
        line_length = 50
        # ---- ----
        self.index = mydict["index"]
        self.title = mydict["title"]
        self.text = tidy_text(mydict["text"], line_length)
        # ----
        s = "This is not a string: {}"
        if type(mydict["choice_1"]) == type(123):
            raise ValueError(s.format(mydict["choice_1"]))
        if type(mydict["choice_2"]) == type(123):
            raise ValueError(s.format(mydict["choice_2"]))
        if type(mydict["choice_3"]) == type(123):
            raise ValueError(s.format(mydict["choice_3"]))
        # ----
        self.choice_1 = tidy_text(mydict["choice_1"], line_length)
        self.choice_2 = tidy_text(mydict["choice_2"], line_length)
        self.choice_3 = tidy_text(mydict["choice_3"], line_length)
        self.goto_1 = mydict["goto_1"]
        self.goto_2 = mydict["goto_2"]
        self.goto_3 = mydict["goto_3"]
        self.command = mydict["command"].lower().strip()
        # ---- ----
        if type(self.choice_1) == type("abc"):
            if self.choice_1.lower().strip() == "none":
                self.choice_1 = None
        if type(self.choice_2) == type("abc"):
            if self.choice_2.lower().strip() == "none":
                self.choice_2 = None
        if type(self.choice_3) == type("abc"):
            if self.choice_3.lower().strip() == "none":
                self.choice_3 = None
        # ----
        if type(self.goto_1) == type("abc"):
            if self.goto_1.lower().strip() == "none":
                self.goto_1 = None
        if type(self.goto_2) == type("abc"):
            if self.goto_2.lower().strip() == "none":
                self.goto_2 = None
        if type(self.goto_3) == type("abc"):
            if self.goto_3.lower().strip() == "none":
                self.goto_3 = None

    def get_goto(self, goto_number):
        if goto_number == 1:
            return self.goto_1
        elif goto_number == 2:
            return self.goto_2
        elif goto_number == 3:
            return self.goto_3
        else:
            return ValueError("Error")

    def get_display_string(self):
        s = "[{}] {}\n".format(self.index, self.title.upper())
        s += "{}\n".format(self.text)
        s += "1) {}\n".format(self.choice_1)
        if not self.choice_2 is None:
            s += "2) {}\n".format(self.choice_2)
        if not self.choice_3 is None:
            s += "3) {}\n".format(self.choice_3)
        # ---- ----
        number_of_choices = 0
        if not self.goto_1 is None:
            number_of_choices += 1
        if not self.goto_2 is None:
            number_of_choices += 1
        if not self.goto_3 is None:
            number_of_choices += 1
        return s, number_of_choices

    def debug_print(self):
        s = "index: {}, title: {}, text: {}\n".format(self.index, self.title, self.text)
        s += "choice_1: {}, choice_2: {}, choice_3: {}\n".format(self.choice_1, self.choice_2, self.choice_3)
        s += "goto_1: {}, goto_2: {}, goto_3: {}\n".format(self.goto_1, self.goto_2, self.goto_3)
        s += "command: {}\n".format(self.command)
        s += "   ***   "
        print(s)
# -----------------------------------------------
#             class Cards
# -----------------------------------------------
class Cards:
    def __init__(self, data_file):
        self.data_file = data_file
        self.inner = []

    def read_data(self):
        filepath = os.path.join(self.data_file)
        if os.path.isfile(filepath) == False:
            s = "I don't recognize this: {}".format(filepath)
            raise ValueError(s)
        list_of_dicts = read_data_file(filepath, 10)
        for a_dict in list_of_dicts:
            new_object = Card(a_dict)
            self.inner.append(new_object)

    def get_card(self, index):
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        for elem in self.inner:
            if elem.index == index:
                return elem
        return None

    def print_cards(self):
        for a_card in self.inner:
            a_card.print_card()

    def debug_print(self):
        print("---- Cards.debug_print() ----")
        if self.inner is None:
            print("self.inner is None")
        if len(self.inner) == 0:
            print("len(self.inner) == 0")
        for a_card in self.inner:
            a_card.debug_print()
        print("-----------------------------")

    def __len__(self):
        return len(self.inner)

# ==============================================================
def goodbye():
    print("Goodbye!")
    sys.exit()

def menu():
    def is_valid(user_choice, size_of_list):
        if is_int(user_choice) == False: return False
        user_resp = int(user_choice)
        if not (0 <= user_resp <= size_of_list): return False
        return True
    # ---- ----
    choices = ["A Night in the Wood"]
    choices.append("The Lost Tomb")
    [print("{}) {}".format(count+1, i)) for count, i in enumerate(choices)]
    # ----
    user_response = ""
    while is_valid(user_response, len(choices)) == False:
        user_response = input("> ").lower().strip()
        if user_response in ["quit", "q", "exit"]:
            goodbye()
    user_choice = int(user_response) - 1
    user_text = choices[user_choice]
    # ---- ----
    print("Loading {}...".format(user_text))
    if user_text == "A Night in the Wood":
        return "a_night_in_the_wood.txt"
    elif user_text == "The Lost Tomb":
        return "the_lost_tomb.txt"
    else:
        s = "I don't recognize this: {}".format(user_text)
        raise ValueError(s)

def main():
    card_data_file = menu()
    program_loop = ProgramLoop(card_data_file)
    program_loop.main()

if __name__ == "__main__":
    main()


