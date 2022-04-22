import random

MAJOR_ARCANA = 22
MINOR_ARCANA = 56
TOTAL_CARDS = MAJOR_ARCANA + MINOR_ARCANA
MAJORS = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor"]
MAJORS += ["The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit"]
MAJORS += ["Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance"]
MAJORS += ["The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement"]
MAJORS += ["The World"]
# ----------------------------------------------------------------------------

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

def get_element(suit):
    suit = suit.lower().strip()
    if suit == "cups": return "Water"
    elif suit == "wands": return "Fire"
    elif suit == "swords": return "Air"
    elif suit == "pentacles": return "Earth"
    else:
        s = "I don't recognize this: {}".format(suit)
        raise ValueError(s)

def minor_arcana_suit(my_adjusted_card, suit):
    if my_adjusted_card in list(range(1, 11)):
        if my_adjusted_card == 1:
            s = "Ace of {} | {}".format(suit, get_element(suit))
            print(s)
        else:
            s =  "{} of {} | {}".format(number_convert(my_adjusted_card), suit, get_element(suit))
            print(s)
    else:
        face = ""
        specific_element = ""
        if my_adjusted_card == 11:
            face = "Page"
            specific_element = "Earth"
        elif my_adjusted_card == 12:
            face = "Knight"
            specific_element = "Air"
        elif my_adjusted_card == 13:
            face = "Queen"
            specific_element = "Water"
        elif my_adjusted_card == 14:
            face = "King"
            specific_element = "Fire"
        s = "{} of {} | {} of {}".format(face, suit, specific_element, get_element(suit))
        print(s)

def sort_minor_arcana(my_card):
    if my_card in list(range(22, 36)):
        minor_arcana_suit(my_card - 21, "Wands")
    elif my_card in list(range(36, 50)):
        minor_arcana_suit(my_card - 35, "Cups")
    elif my_card in list(range(50, 64)):
        minor_arcana_suit(my_card - 49, "Swords")
    elif my_card in list(range(64, 78)):
        minor_arcana_suit(my_card - 63, "Pentacles")
    else:
        raise ValueError("Error")

def randomly_select_card():
    print(" ")
    my_card = random.randint(0, TOTAL_CARDS-1)
    if my_card in list(range(22)):
        print("Major Arcana: {}, {}".format(my_card, MAJORS[my_card]))
    elif my_card in list(range(22, 78)):
        print("Minor Arcana: {}".format(my_card))
        sort_minor_arcana(my_card)
    else:
        raise ValueError("Error")
    print(" ")

def main():
    randomly_select_card()

if __name__ == "__main__":
    main()
