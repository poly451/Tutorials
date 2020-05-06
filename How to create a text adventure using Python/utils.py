
import subprocess as sp
import constants as con

def get_player_info():
    char_name = ""
    char_kind = ""
    while len(char_name) == 0 or " " in char_name:
        print("What is your character's name?")
        char_name = input("> ").lower().strip()
    while not char_kind in con.CHARACTER_KINDS:
        print("What is your character's class?")
        print("Choices: ", ', '.join(con.CHARACTER_KINDS).upper())
        char_kind = input("> ").lower().strip()
    return char_name, char_kind

def capitalize(mystring):
    s ="{}{}".format(mystring[0:1].upper(), mystring[1:])
    return s

def clear_screen():
    tmp = sp.call('clear', shell=True)


