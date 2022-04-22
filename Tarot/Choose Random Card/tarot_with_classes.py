# import utils
import os, random
# import constants
MAJOR_ARCANA = 22
MINOR_ARCANA = 56
TOTAL_CARDS = MAJOR_ARCANA + MINOR_ARCANA

MAJORS = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor"]
MAJORS += ["The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit"]
MAJORS += ["Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance"]
MAJORS += ["The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement"]
MAJORS += ["The World"]
# --------------------------------------------------------------

def number_convert(myint):
    if not myint in range(1, 11):
        raise ValueError("Error")
    s = ""
    if myint == 1:
        s = "Ace"
    elif myint == 2:
        s = "Two"
    elif myint == 3:
        s = "Three"
    elif myint == 4:
        s = "Four"
    elif myint == 5:
        s = "Five"
    elif myint == 6:
        s = "Six"
    elif myint == 7:
        s = "Seven"
    elif myint == 8:
        s = "Eight"
    elif myint == 9:
        s = "Nine"
    elif myint == 10:
        s = "Ten"
    return s

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
    except Exception as e:
        print("tag: {}; value: {}".format(tag, value))
        raise ValueError(e)
    return mydict

# ------------------------------------------------------
#                      class Cards
# ------------------------------------------------------
class Cards:
    def __init__(self):
        filepath = os.path.join("card_numbers.txt")
        if os.path.isfile(filepath) == False:
            self.reset_file()
        self.cards = self._read_card_data()
        self.current_card = None

    def choose_random_card(self):
        my_card = random.randint(0, TOTAL_CARDS - 1)
        card_min = self._get_min()
        besafe = 0
        while self.cards[str(my_card)] > card_min:
            my_card = random.randint(0, TOTAL_CARDS - 1)
            besafe += 1
            if besafe > 9000: raise ValueError("Error")
        # ---- ----
        self.current_card = my_card
        self.cards[str(my_card)] += 1
        return my_card, self.cards[str(my_card)]

    def _get_min(self):
        minimum = 100
        for key, value in self.cards.items():
            if value < minimum:
                minimum = value
        if minimum == 100: raise ValueError("Error")
        return minimum

    def _read_card_data(self):
        filepath = os.path.join("card_numbers.txt")
        if os.path.isfile(filepath) == False: raise ValueError("Error")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        mydict = {}
        for elem in mylines:
            mydict = key_value(elem, mydict)
        return mydict

    def save_cards(self):
        filepath = os.path.join("card_numbers.txt")
        if os.path.isfile(filepath) == False: raise ValueError("Error")
        with open(filepath, "w") as f:
            for key, value in self.cards.items():
                s = "{}: {}\n".format(key, value)
                f.write(s)

    def reset_file(self):
        """Creates a file from scratch"""
        filepath = os.path.join("card_numbers.txt")
        with open(filepath, "w") as f:
            for i in range(78):
                s = "{}: {}\n".format(i, 0)
                f.write(s)

    def debug_print(self):
        for key, value in self.cards.items():
            print("{}: {}".format(key, value))

# ------------------------------------------------------
#                  class Display_Cards
# ------------------------------------------------------
class DisplayCards:
    def __init__(self):
        self.cards = Cards()
        random_card = self.cards.choose_random_card()
        self.card_number = random_card[0]
        self.suit = None
        self.card_number_adjusted = None
        self.break_dow_card_number()

    def get_direction(self):
        if self.suit == "wands": return "south"
        elif self.suit == "cups": return "west"
        elif self.suit == "swords": return "east"
        elif self.suit == "pentacles": return "north"
        else: raise ValueError("Error")

    def get_general_element(self):
        if self.suit == "wands": return "fire"
        elif self.suit == "cups": return "water"
        elif self.suit == "swords": return "air"
        elif self.suit == "pentacles": return "earth"
        else: raise ValueError("Error")

    def break_dow_card_number(self):
        if self.card_number in list(range(22)):
            self.suit = "major"
            self.card_number_adjusted = self.card_number
        elif self.card_number in list(range(22, 36)):
            self.suit = "wands"
            self.card_number_adjusted = self.card_number - 21
        elif self.card_number in list(range(36, 50)):
            self.suit = "cups"
            self.card_number_adjusted = self.card_number - 35
        elif self.card_number in list(range(50, 64)):
            self.suit = "swords"
            self.card_number_adjusted = self.card_number - 49
        elif self.card_number in list(range(64, 78)):
            self.suit = "pentacles"
            self.card_number_adjusted = self.card_number - 63
        else:
            raise ValueError("Error")

    def _display_minor_arcana_suit(self):
        if self.card_number_adjusted in list(range(1, 11)):
            # placement = "Numbered Card"
            if self.card_number_adjusted == 1:
                s = "Ace of {} | {}".format(self.suit, self.get_general_element())
                print(s)
            else:
                s = "{} of {} | {}".format(number_convert(self.card_number_adjusted), self.suit, self.get_general_element())
                print(s)
        else:
            face = ""
            specific_element = ""
            if self.card_number_adjusted == 11:
                face = "Page"
                specific_element = "Earth"
            elif self.card_number_adjusted == 12:
                face = "Knight"
                specific_element = "Air"
            elif self.card_number_adjusted == 13:
                face = "Queen"
                specific_element = "Water"
            elif self.card_number_adjusted == 14:
                face = "King"
                specific_element = "Fire"
            s = "{} of {} | {} of {}".format(face, self.suit, specific_element, self.get_general_element())
            print(s)

    def reset_file(self):
        self.cards.reset_file()

    def save_data(self):
        self.cards.save_cards()

    def display_card(self):
        if self.card_number in list(range(22)):
            print("Major Arcana: {}, {}".format(self.card_number, MAJORS[self.card_number]))
        elif self.card_number in list(range(22, 78)):
            print("Minor Arcana")
            self._display_minor_arcana_suit()
        else:
            raise ValueError("Error")

if __name__ == "__main__":
    mycards = DisplayCards()
    mycards.display_card()
    mycards.reset_file()
