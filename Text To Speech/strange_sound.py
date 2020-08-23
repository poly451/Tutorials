import pyttsx3
import os, sys
import utils

"""
rate — Integer speech rate in words per minute. The base value is 200.
voice — String identifier of the active voice
volume — Floating point volume in the range of 0.0 to 1.0 inclusive
voices — List of pyttsx3.voice.Voice descriptor objects
"""
# ----------------------------------------------------------
#                        class Voices
# ----------------------------------------------------------
class Voice:
    def __init__(self, mydict):
        # print(mydict)
        self.name = mydict["name"]
        self.id = mydict["id"]
        self.languages = mydict["voice languages"]
        self.gender = mydict["voice gender"]
        self.age = mydict["voice age"]

# ----------------------------------------------------------
#                        class Voices
# ----------------------------------------------------------

class Voices:
    def __init__(self):
        self.inner = []
        # ----
        filepath = os.path.join("data", "voices.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        for i in range(0, len(mylines), 5):
            mydict = {}
            for j in range(5):
                # print(mylines[i+j])
                mydict = utils.strip_value(mylines[i+j], mydict)
            new_voice = Voice(mydict)
            self.inner.append(new_voice)

    # -----------------------------------------------

    def get_voice_by_name(self, name):
        name = name.strip()
        for elem in self.inner:
            # print("elem.name: {}, name: {}".format(elem.name, name))
            if elem.name == name:
                return elem
        return None

    def get_voices_by_language(self, language):
        language = language.lower().strip()
        mylist = []
        for elem in self.inner:
            if elem.languages == language:
                mylist.append(elem)
        return mylist

    def get_voices_by_gender(self, gender):
        # ['voicegendermale', 'voicegenderneuter', 'voicegenderfemale']
        this_gender = ""
        gender = gender.lower().strip()
        if gender in ["female", "f", "voicegenderfemale"]:
            this_gender = 'voicegenderfemale'
        elif gender in ["male", "m", "voicegendermale"]:
            this_gender = 'voicegendermale'
        elif gender in ["neuter", "n", "voicegenderneuter"]:
            this_gender = 'voicegenderneuter'
        else:
            s = "I don't recognize this: {} ({})".format(gender, type(gender))
            raise ValueError(s)
        # ----
        mylist = []
        for elem in self.inner:
            if elem.gender == this_gender:
                mylist.append(elem)
        return mylist

    def get_voices_by_age(self, age):
        mylist = []
        for elem in self.inner:
            # print("age: {} ({}) == {} ({})".format(elem.age, type(elem.age), age, type(age)))
            if elem.age == age:
                mylist.append(elem)
        return mylist

    def filter_voices(self, age, gender, langauge):
        ages_filtered = self.get_voices_by_age(age)
        genders_filtered = self.get_voices_by_gender(gender)
        langages_filtered = self.get_voices_by_language(langauge)
        intersection = list(set(ages_filtered + genders_filtered))
        intersection = list(set(intersection + langages_filtered))
        if len(intersection) == 0:
            raise ValueError("Error!")
        return intersection

    # -----------------------------------------------

    def get_names(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.name)
        return mylist

    def get_ids(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.id)
        return mylist

    def get_languages(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.languages)
        return list(set(mylist))

    def get_genders(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.gender)
        return list(set(mylist))

    def get_gender(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.gender)
        return list(set(mylist))

    def get_ages(self):
        mylist = []
        for elem in self.inner:
            mylist.append(elem.age)
        return list(set(mylist))

    def update_init_file(self, this_voice, init_filepath):
        name = "name: {}\n".format(this_voice.name)
        id = "id: {}\n".format(this_voice.id)
        languages = "langauges: {}\n".format(this_voice.languages)
        gender = "gender: {}\n".format(this_voice.gender)
        age = "age: {}\n".format(this_voice.age)
        with open(init_filepath, "w") as f:
            f.write(name)
            f.write(id)
            f.write(languages)
            f.write(gender)
            f.write(age)

# ----------------------------------------------------------
#                        class PySound
# ----------------------------------------------------------

class StrangeSound:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.keep_looping = True
        # ------------------------
        self.load_initialization_file()

    def load_initialization_file(self):
        with open(os.path.join("data", "init.txt"), "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        mydict = {}
        for i in range(5):
            mydict = utils.strip_value(mylines[i], mydict)
        self.engine.setProperty("voice", mydict["id"])

    def change_voice_by_name(self):
        print("Here are names of the voices I know. Which one would you like?\n")
        voices = Voices()
        names = voices.get_names()
        utils.print_elements(names, 8)
        user_input = ""
        while not user_input in names:
            user_input = input("> ").strip()
            if user_input == "quit": return False
        this_voice = voices.get_voice_by_name(user_input)
        filepath = os.path.join("data", "init.txt")
        self.engine.setProperty("voice", this_voice.id)
        voices.update_init_file(this_voice, filepath)
        self.speak("Hi! My name is {}.".format(this_voice.name))

    def change_volume(self):
        print("The defaut for 'volume' is 1. What would you like to change it to? (0 to 3)")
        user_input = ""
        while not user_input in ["0", "1", "2", "3"]:
            user_input = input("> ").lower().strip()
        user_input = int(user_input)
        self.set_sound_property("volume", user_input)
        self.speak("The volume has been chnaged")

    def play_script(self):
        line_length = 60
        indy = "com.apple.speech.synthesis.voice.daniel.premium"
        satipo = "com.apple.speech.synthesis.voice.Alex"
        serena = "com.apple.speech.synthesis.voice.moira.premium"
        # ------------------------------------------
        text = "Indy and Satipo fan out to fight their way through the entwined "
        text += "trees that guard the temple. Visibility is cut to five feet "
        text += "in the heavy mist. Satipo extracts a short, native dart from "
        text += "a tree and examines the point gingerly. ... As Satipo shows Indy the dart, he says,"
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "The Hovitos are near. The poison is still fresh...three days. "
        text += "I tell you, they’re following us."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", satipo)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 400)
        self.speak(text)
        # -----
        text = "If they knew we were here, they would have killed us already."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", indy)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "In the undergrowth, there is a slithering movement. Their eyes "
        text += "are drawn to one of the trees that surround them. There is something ..."
        text += "A dessicated corpse is attached to the trunk of the tree with arrows. Sapito screams."
        text += "Indy examins the corpse."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "So this is where Forestal cashed in."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        self.engine.setProperty("voice", indy)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "A friend of yours?"
        print(text)
        print("")
        self.engine.setProperty("voice", satipo)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 400)
        self.speak(text)
        # -----
        text = "Competitor. He was good, very good."
        print(text)
        print("")
        self.engine.setProperty("voice", indy)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "No one has ever come out of there alive. Why should we put our faith in you?"
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", satipo)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 400)
        self.speak(text)
        # -----
        text = "Indy shows Satipo his map. Satipo looks at it with naked greed. "
        text += "Indy spreads out the map on the grass. Minutes go by as the men study it. "
        text += "Satipo leans closer. He says,"
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "It's the floor plan of the temple! It has to be!"
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", satipo)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 400)
        self.speak(text)
        # -----
        text = "Indy nodded."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        print("")
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "That's how I figure it."
        text_list = utils.separate_text_into_lines(text, line_length)
        [print(i) for i in text_list]
        self.engine.setProperty("voice", indy)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "No one else had this ... Only us."
        print(text)
        self.engine.setProperty("voice", satipo)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 400)
        self.speak(text)
        # -----
        text = "Will Indy survive the dangers that await him in the tunnel, "
        text += "or will he die an agonizing death like all those before him?"
        print(text)
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)
        # -----
        text = "The end."
        print(text)
        self.engine.setProperty("voice", serena)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("rate", 200)
        self.speak(text)

    def print_out_properties(self):
        print("rate: ", self.engine.getProperty('rate'))
        print("volume: ", self.engine.getProperty('volume'))

    def print_out_all_voices(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print("Voice name: {}".format(voice.name))
            print("Voice ID: {}".format(voice.id))
            print("Voice Languages: {}".format(voice.languages))
            print("Voice Gender: {}".format(voice.gender))
            print("Voice Age: {}".format(voice.age))
            print("-" * 40)

    def write_voices_to_file(self):
        filepath = os.path.join("data", "voices_text.txt")
        voices = self.engine.getProperty('voices')
        mylist = []
        for voice in voices:
            language = ''.join(voice.languages).strip()
            s = "name: {}\n".format(voice.name)
            s += "ID: {}\n".format(voice.id)
            s += "Voice Languages: {}\n".format(language)
            s += "Voice Gender: {}\n".format(voice.gender)
            s += "Voice Age: {}\n".format(voice.age)
            s += "\n"
            mylist.append(s)
        # [print(i) for i in mylist]
        with open(filepath, "w") as f:
            for elem in mylist:
                f.write(elem)

    def set_properties(self):
        self.engine.setProperty('volume', 1)
        self.engine.setProperty('rate', 200)
        voices = self.engine.getProperty('voices')
        # self.engine.setProperty("voice", voices[1].id)
        id = "com.apple.speech.synthesis.voice.BadNews"
        id = "com.apple.speech.synthesis.voice.Bahh"
        id = "com.apple.speech.synthesis.voice.diego"
        id = "com.apple.speech.synthesis.voice.daniel.premium"
        id = "com.apple.speech.synthesis.voice.carmit"
        id = "com.apple.speech.synthesis.voice.GoodNews"
        self.engine.setProperty("voice", id)
        # self.engine.setProperty('age', 300)

    def test(self):
        self.speak()
        self.set_properties()
        self.print_out_properties()
        self.speak()
        self.print_out_properties()

    def print_voices_to_file(self):
        self.write_voices_to_file()

    # ************************************************

    def speak(self, text=""):
        # this_text = "Though I speak with the tongues of men and of angels, and have not charity, I am become as sounding brass, or a tinkling cymbal."
        this_text = "The cat is on the mat."
        if len(text) == 0:
            self.engine.say(this_text)
        else:
            self.engine.say(text)
        self.engine.runAndWait()
        # file_to_save = os.path.join("data", "exp_my_exp")
        # engine.save_to_file('the text I want to save as audio', file_to_save)

    def cycle_through_voices(self):
        myvoices = Voices()
        ids = myvoices.get_ids()
        for id in ids:
            print("playing {} ...".format(id))
            self.engine.setProperty("voice", id)
            self.speak()
            print("-" * 40)

    def speak_some_text(self):
        def is_valid(mystring, mylist):
            if not utils.is_int(mystring): return False
            myint = int(mystring)
            for i in range(len(mylist)):
                if myint - 1 == i:
                    return True
            return False
        # -----------------------------------------
        first_choice = "enter the text you would like me to speak"
        second_choice = "Enter the filename you would like me to read"
        choices = [first_choice, second_choice, "quit"]
        text = ""
        default_text = """Though I speak with the tongues of men and of angels, 
        and have not charity, I am become as sounding brass, 
        or a tinkling cymbal."""
        # -----------------------------------------
        for count, elem in enumerate(choices):
            print("{}) {}".format(count + 1, elem))
        user_input = input("> ").lower().strip()
        while not is_valid(user_input, choices):
            user_input = input("> ").lower().strip()
            if user_input == "quit": return False
        user_input = int(user_input)
        user_choice = choices[user_input - 1].lower().strip()
        # -----------------------------------------
        if user_choice == first_choice:
            print("Enter the text you would like me to speak:")
            user_input = input("> ").lower().strip()
            while len(user_input) == 0:
                user_input = input("> ").lower().strip()
                if user_input == "quit": sys.exit()
            self.engine.say(user_input)
            self.engine.runAndWait()
            print("Finished speaking.")
        elif user_choice == second_choice:
            print("Entering the filename you would like me to read :..")
            filepath = os.path.join("data", "text_files")
            files = os.listdir(filepath)
            for count, file in enumerate(files):
                print("{}) {}".format(count + 1, file))
            user_input = input("> ").lower().strip()
            while not utils.is_int(user_input):
                user_input = input("> ").lower().strip()
                if user_input == "quit": sys.exit()
            filename = files[int(user_input)-1]
            print("Reading file: ", filename)
            filepath = os.path.join("data", "text_files", filename)
            mytext = ""
            with open(filepath, "r") as f:
                mytext = f.read()
            # -----------------------------------------
            self.engine.say(mytext)
            self.engine.runAndWait()
            print("Finished speaking.")
        elif user_choice == "quit":
            pass
        else:
            raise ValueError("I don't recognize that: {}".format(user_choice))

    def choose_by_age(self):
        def is_valid(mystring, name_list):
            if not mystring in name_list:
                return False
            return True
        myvoices = Voices()
        age_list = myvoices.get_ages()
        utils.print_elements(age_list, 6)
        # ----
        print("What age would you like to choose?")
        age = input("> ").lower().strip()
        while len(age) == 0:
            age = input("> ").lower().strip()
        age = int(age)
        voices_found = myvoices.get_voices_by_age(age)
        if len(voices_found) == 0:
            raise ValueError("Error!")
        [print(i.name) for i in voices_found]
        # ----
        print("What name would you like to choose?")
        the_name = input("> ").strip()
        while not is_valid(the_name, myvoices.get_names()):
            the_name = input("> ").strip()
        this_voice = myvoices.get_voice_by_name(the_name)
        # print("This is the voice id: {}".format(this_voice.id))
        # ----
        self.engine.setProperty("voice", this_voice.id)
        self.speak()

    def set_sound_property(self, property, value):
        def is_valid_volume(mystring):
            if not utils.is_int(mystring): return False
            myint = int(mystring)
            if myint >= 0 and myint <= 2:
                return True
            return False
        # ------------------------------------
        if not property in ["volume", "rate"]:
            raise ValueError("Error!")
        if value < 0:
            raise ValueError("Error!")
        # ---------------------------------------
        if property == "volume":
            if not is_valid_volume(value):
                raise ValueError("Error")
            self.engine.setProperty('volume', value)
        elif property == "rate":
            if not (value <= 400 and value >= 0):
                raise ValueError("Error")
            self.engine.setProperty('rate', value)
        else:
            raise ValueError("Error")

    def select_voice(self):
        def is_valid(mystring, thelist):
            # print("the name: {}".format(mystring))
            # print("the list: {}".format(thelist))
            if len(mystring) == 0: return False
            if not mystring in thelist:
                return False
            return True
        # ----
        print("Select by 1) Name, 2) Language, 3) Gender, 4) Age")
        user_input = input("> ").strip()
        while not user_input in ["1", "2", "3", "4", "5"]:
            user_input = input("> ").strip()
            if user_input == "quit": return False
        user_input = int(user_input)
        # -----------------------------------------
        if user_input == 1: # Name
            myvoices = Voices()
            name_list = myvoices.get_names()
            utils.print_elements(name_list, 6)
            # ----
            print("What name would you like to choose?")
            the_name = input("> ").strip()
            while not is_valid(the_name, name_list):
                the_name = input("> ").strip()
                if the_name == "quit": sys.exit()
            this_voice = myvoices.get_voice_by_name(the_name)
            # this_voice_id = utils.format_voice_id(this_voice.name)
            self.engine.setProperty("voice", this_voice.id)
            # self.engine.setProperty("voice", "com.apple.speech.synthesis.voice.Hysterical")
            self.speak()
        elif user_input == 2: # language
            myvoices = Voices()
            languages_list = myvoices.get_languages()
            utils.print_elements(languages_list, 6)
            # ----
            print("What language would you like to choose?")
            langauge = input("> ").lower().strip()
            while len(langauge) == 0:
                langauge = input("> ").lower().strip()
            voices_found = myvoices.get_voices_by_language(langauge)
            if len(voices_found) == 0:
                raise ValueError("Error!")
            [print(i.name) for i in voices_found]
            # ----
            print("What name would you like to choose?")
            the_name = input("> ").lower().strip()
            while len(the_name) == 0:
                the_name = input("> ").lower().strip()
            this_voice = myvoices.get_voice_by_name(the_name)
            # ----
            self.engine.setProperty("voice", utils.format_voice_id(this_voice.name))
            self.speak()
        elif user_input == 3: # gender
            # ['voicegendermale', 'voicegenderneuter', 'voicegenderfemale']
            myvoices = Voices()
            gender_list = myvoices.get_genders()
            utils.print_elements(gender_list, 6)
            # ----
            print("What gender would you like to choose?")
            gender = input("> ").lower().strip()
            while len(gender) == 0:
                gender = input("> ").lower().strip()
            voices_found = myvoices.get_voices_by_gender(gender)
            if len(voices_found) == 0:
                raise ValueError("Error!")
            [print(i.name) for i in voices_found]
            # ----
            print("What name would you like to choose?")
            the_name = input("> ").lower().strip()
            while len(the_name) == 0:
                the_name = input("> ").lower().strip()
            this_voice = myvoices.get_voice_by_name(the_name)
            print("This is the voice id: {}".format(this_voice.id))
            print("This is the new id: {}".format(utils.format_voice_id(this_voice.name)))
            # ----
            self.engine.setProperty("voice", utils.format_voice_id(this_voice.name))
            self.speak()
        elif user_input == 4: # age
            self.choose_by_age()
        else:
            raise ValueError("Error!")

    def change_program_properties(self):
        def is_valid(mystring, mybeg, myend):
            if not utils.is_int(mystring): return False
            myint = int(mystring)
            while not (myint >= mybeg and myint <= myend):
                return False
            return True
        # -----------------------------------------
        print("Entering procedure change_program_properties")
        voice_properties = ["change rate", "change volume", "change voice", "quit"]
        for count, elem in enumerate(voice_properties):
            print("{}) {}".format(count + 1, elem))
        user_input = input("> ").lower().strip()
        while not utils.is_valid(user_input, voice_properties):
            user_input = input("> ").lower().strip()
            if user_input == "quit": sys.exit()
        print("You chose: {}".format(user_input))
        user_input = int(user_input)
        user_choice = voice_properties[user_input-1]
        print(user_choice)
        # -----------------------------------------
        if user_choice == "change rate":
            print("The defaut for 'rate' is 200. What would you like to change it to? (1 to 400)")
            user_input = input("> ").lower().strip()
            while not is_valid(user_input, mybeg=1,myend=400):
                user_input = input("> ").lower().strip()
            self.engine.setProperty('rate', user_input)
            self.speak()
        elif user_choice == "change volume":
            print("The defaut for 'volume' is 1. What would you like to change it to? (0 to 3)")
            user_input = input("> ").lower().strip()
            while not is_valid(user_input, 0, 3):
                user_input = input("> ").lower().strip()
            self.engine.setProperty('volume', user_input)
            self.speak()
        elif user_choice == "change voice":
            print("You are about to change the voice.")
            # print("Would you like more information about the available voices? (y/n)")
            # user_input = ""
            # while not user_input in ["y", "yes", "n", "no"]:
            #     user_input = input("> ").lower().strip()
            # if user_input in ["y", "yes"]:
            self.select_voice()
        elif user_choice == "quit":
            raise NotImplemented
        else:
            raise ValueError("Error!")

    def main(self):
        choices = ["Speak some text"]
        choices += ["cycle through voices"]
        choices += ["Settings: Change one or more program properties"]
        choices += ["quit"]
        while self.keep_looping:
            print("What would you like to do?")
            for count, elem in enumerate(choices):
                print("{}) {}".format(count + 1, elem))
            user_input = ""
            while not user_input in ["1", "2", "3", "4"]:
                user_input = input("Main menu > ").lower().strip()
                if user_input == "quit": return False
            user_input = choices[int(user_input) - 1]
            # -----------------------------------------
            if user_input == "Speak some text":
                self.speak_some_text()
            elif user_input == "Settings: Change one or more program properties":
                print("In main menu: Calling change_program_properites")
                self.change_program_properties()
            elif user_input == "cycle through voices":
                self.cycle_through_voices()
            elif user_input == "quit":
                print("Quitting ...")
                self.keep_looping = False
            else:
                raise ValueError("I don't recognize this: {}".format(user_input))
        print("Goodtype! Have a great day! 😀😸")

# ******************************************************

if __name__ == "__main__":
    # voices = Voices()
    mysound = StrangeSound()
    # mysound.main()
    mysound.play_script()
