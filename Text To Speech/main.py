import utils
import sys, os
from strange_sound import StrangeSound, Voices
import pyttsx3

def change_rate():
    def is_valid(mystring):
        if len(mystring) == 0: return False
        if not utils.is_int(mystring): return False
        myint = int(mystring)
        if not (myint <= 400 and myint >= 0): return False
        return True
    mysound = StrangeSound()
    print("The defaut for 'rate' is 200. What would you like to change it to? (0 to 400)")
    user_input = ""
    while not is_valid(user_input):
        user_input = input("> ").lower().strip()
    user_input = int(user_input)
    mysound.set_sound_property("rate", user_input)
    mysound.speak("The rate has been chnaged")

def change_volume():
    def is_valid(mystring):
        if not utils.is_int(mystring): return False
        myint = int(mystring)
        if myint >= 0 and myint <= 2:
            return True
        return False
    # ------------------------------------
    mysound = StrangeSound()
    print("The defaut for 'volume' is 1. What would you like to change it to? (0 --> 2)")
    user_input = ""
    while not is_valid(user_input):
        user_input = input("> ").lower().strip()
    user_input = int(user_input)
    mysound.set_sound_property("volume", user_input)
    mysound.speak("The volume has been changed")

def cycle_through_voices():
    engine = pyttsx3.init()
    myvoices = Voices()
    ids = myvoices.get_ids()
    for id in ids[0:5]:  # <-- Change to: for id in ids: (in order to hear ALL the voices.)
        print("playing {} ...".format(id))
        engine.setProperty("voice", id)
        engine.say("The cat sat on the mat.")
        engine.runAndWait()
        print("-" * 40)

def turn_textfile_into_sountfile():
    def soundfile_valid(mystring):
        if len(mystring) == 0: return False
        if mystring.find("mpg") > -1: return False
        if mystring.find("mp3") > -1: return False
        if mystring.find(".") > -1: return False
        return True
    def textfiles_valid(mystring, mylist):
        if len(mystring) == 0: return False
        if not utils.is_int(mystring): return False
        myint = int(mystring)
        print("myint:", myint)
        print("mylist:", mylist)
        try:
            temp = mylist[myint-1]
            # print("Debugging: {}".format(temp))
            return True
        except:
            return False
    # -------------------------------------------
    print("Enter the name of the file you would like me to read:")
    # ----
    dir = os.path.join("data", "texts")
    files = os.listdir(dir)
    files = [i.strip() for i in files if i.find(".DS_Store") == -1]
    for count in range(len(files)):
        print("{}) {}".format(count + 1, files[count]))
    # ----
    user_input = ""
    while not textfiles_valid(user_input, files):
        user_input = input("> ").lower().strip()
    # ---- Opening Textfile ----
    filename = files[int(user_input) - 1]
    print("You chose the file: {}".format(filename))
    filepath = os.path.join(dir, filename)
    with open(filepath, "r") as f:
        mytext = f.read()
    # -------------------------------------------
    print("Enter the name of the soundfile you would like me to create:")
    user_input = ""
    while not soundfile_valid(user_input):
        user_input = input("> ").lower().strip()
    filename = "{}.mpg".format(user_input)
    soundfile = os.path.join("data", filename)
    # -------------------------------------------
    engine = pyttsx3.init()
    print("Being saved to: {}".format(soundfile))
    engine.save_to_file(mytext , soundfile)
    engine.runAndWait()

def play_shorter_file():
    def textfiles_valid(mystring, mylist):
        if not utils.is_int(mystring): return False
        myint = int(mystring)
        try:
            temp = mylist[myint-1]
            return True
        except:
            return False
    # -------------------------------------------
    print("Enter the name of the file you would like me to read:")
    # ----
    dir = os.path.join("data", "texts")
    files = os.listdir(dir)
    files = [i.strip() for i in files if i.find("DS_Store") == -1]
    for count in range(len(files)):
        print("{}) {}".format(count + 1, files[count]))
    # ----
    user_input = ""
    while not textfiles_valid(user_input, files):
        user_input = input("> ").lower().strip()
    # ---- Opening Textfile ----
    filename = files[int(user_input) - 1]
    print("You chose the file: {}".format(filename))
    filepath = os.path.join(dir, filename)
    with open(filepath, "r") as f:
        mytext = f.read()
    mysound = StrangeSound()
    mysound.speak(mytext)
    # -------------------------------------------

def speak_typed_text():
    print("What would you like me to say?")
    user_input = ""
    while len(user_input) == 0:
        user_input = input("> ").strip()
    myvoice = StrangeSound()
    myvoice.speak(user_input)

def main():
    def is_valid(mystring, mylist):
        if not utils.is_int(mystring): return False
        myint = int(mystring)
        for i in range(len(mylist)):
            if myint == i + 1:
                return True
        return False
    # ----
    first = "Speak typed text"
    second = "Play shorter file"
    third = "Play script"
    fourth = "Turn a textfile into a soundfile"
    fifth = "Cycle through all the voices"
    sixth = "Change the voice"
    seventh = "Change the volume"
    eighth = "Change the rate"
    ninth = "Write voices to file"
    tenth = "Quit"
    choices = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
    print("What would you like to do?")
    keep_looping = True
    while keep_looping:
        for count, elem in enumerate(choices):
            print("{}) {}".format(count + 1, elem))
        user_input = ""
        while not is_valid(user_input, choices):
            user_input = input("> ").strip()
            if user_input == "quit": sys.exit()
        user_input = int(user_input)
        user_choice = choices[user_input-1]
        # ---------------------------
        if user_choice == first:
            speak_typed_text()
        elif user_choice == second:
            play_shorter_file()
        elif user_choice == third:
            mysound = StrangeSound()
            mysound.play_script()
        elif user_choice == fourth:
            turn_textfile_into_sountfile()
        elif user_choice == fifth:
            cycle_through_voices()
        elif user_choice == sixth:
            mysound = StrangeSound()
            mysound.change_voice_by_name()
        elif user_choice == seventh:
            change_volume()
        elif user_choice == eighth:
            change_rate()
        elif user_choice == ninth:
            sounds = StrangeSound()
            sounds.write_voices_to_file()
            print("Done!")
        elif user_choice == tenth:
            print("Quitting ...")
        else:
            raise ValueError("I don't recognize this: {}".format(user_choice))

if __name__ == "__main__":
    main()
