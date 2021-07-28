
import utils
import constants
import os, sys

# ------------------------------------------------------------
#                    class SpeechInstance
# ------------------------------------------------------------

class SpeechInstance:
    def __init__(self, mydict):
        self.index = mydict["index"]
        self.prompt = mydict["prompt"]
        self.choice_1 = mydict["choice_1"]
        self.choice_2 = mydict["choice_2"]
        self.choice_3 = mydict["choice_3"]
        print("***** mydict: {}".format(mydict))
        r_1 = mydict["response_1"]
        r_2 = mydict["response_2"]
        r_3 = mydict["response_3"]
        # ----
        mylist1 = r_1.split(";")
        mylist1 = [i.strip() for i in mylist1 if len(i.strip()) > 0]
        if not mylist1[1].lower().strip() in constants.WHAT_HAPPENS_NOW:
            raise ValueError("Error! Couldn't find: {}".format(mylist1[1].lower().strip()))
        mylist2 = r_2.split(";")
        mylist2 = [i.strip() for i in mylist2 if len(i.strip()) > 0]
        if not mylist2[1].lower().strip() in constants.WHAT_HAPPENS_NOW:
            raise ValueError("Error! Couldn't find: {}".format(mylist2[1]))
        mylist3 = r_3.split(";")
        mylist3 = [i.strip() for i in mylist3 if len(i.strip()) > 0]
        if not mylist3[1].lower().strip() in constants.WHAT_HAPPENS_NOW:
            raise ValueError("Error! Couldn't find: {}".format(mylist3[1]))
        # ----
        self.response_1, self.response_2, self.response_3 = mylist1, mylist2, mylist3
        self.response_1[1] = self.response_1[1].lower().strip()
        self.response_2[1] = self.response_2[1].lower().strip()
        self.response_3[1] = self.response_3[1].lower().strip()

    def debug_print(self):
        s = "index: {}, prompt: {}, choice_1: {}, choice_2: {} choice_3: {}, response_1: {}, response_2: {}, response_3: {}"
        s = s.format(self.index, self.prompt, self.choice_1, self.choice_2, self.choice_3, self.response_1, self.response_2, self.response_3)
        print(s)

# ------------------------------------------------------------
#                    class Speech
# ------------------------------------------------------------

class Speech:
    def __init__(self, npc_name):
        if not type(npc_name) == type("abc"):
            raise ValueError("Error!")
        if utils.validate_merchant_name(npc_name) == False:
            s = "Error! {} is not a valid character name."
            s = s.format(npc_name.upper())
            raise ValueError(s)
        # ----
        user_data = utils.get_user_data()
        self.zone_name = user_data["zone_name"]
        self.map_name = user_data["map_name"]
        # ----
        self.npc_name = npc_name.replace(" ", "_").lower().strip()
        # self.npc_dict = None
        self.keep_looping = True
        # ----
        self.index = 1
        self.inner = []

    def read_data(self):
        self.inner = []
        filepath = os.path.join("data", "zones", self.zone_name,
                                self.map_name, "texts",
                                "{}.txt".format(self.npc_name))
        mylist = utils.read_data_file(filepath, 8)
        for elem in mylist:
            new_item = SpeechInstance(elem)
            self.inner.append(new_item)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

    def process_player_choice(self, text, result):
        if result == "end game":
            print(text)
            print("Ending game ...")
            return result
        elif result == "end conversation":
            print(text)
            print("Ending conversation ...")
            return result
        elif result == "continue":
            print(text)
            print("Continue ...")
            return result
        else:
            raise ValueError("I don't understand this: {}".format(result))

    def get_prompt(self, index):
        """
        retrieves the prompt from the specified record.
        :param index: can be 1, 2 or 3
        :return: the prompt (string)
        """
        if not index <= len(self.inner):
            raise ValueError("Error! This doesn't fit: {}".format(index))
        return self.inner[index-1].prompt

    def get_choices(self, index):
        """
        The choices are returned as a list
        :param index: 1, 2 or 3
        :return: a list containing the choices
        """
        if not index <= len(self.inner):
            s = "index: {}, len(self.inner): {}".format(index, len(self.inner))
            raise ValueError(s)
        text1 = self.inner[index - 1].choice_1
        text2 = self.inner[index - 1].choice_2
        text3 = self.inner[index - 1].choice_3
        text1 = "1) {}".format(text1)
        text2 = "2) {}".format(text2)
        text3 = "3) {}".format(text3)
        mylist = utils.separate_text_into_lines(text1, 50)
        mylist += utils.separate_text_into_lines(text2, 50)
        mylist += utils.separate_text_into_lines(text3, 50)
        return mylist

    def get_response(self, index, choice_int):
        if not index <= len(self.inner):
            raise ValueError("Error!")
        if choice_int == 1:
            return self.inner[index-1].response_1
        elif choice_int == 2:
            return self.inner[index-1].response_2
        elif choice_int == 3:
            return self.inner[index-1].response_3
        else:
            raise ValueError("Error! I don't understand this: {}".format(choice_int))

    def main(self):
        for elem in self.inner:
            print(elem.prompt)
            print("1) ", elem.choice_1)
            print("2) ", elem.choice_2)
            print("3) ", elem.choice_3)
            user_response = ""
            while not utils.is_int(user_response):
                user_response = input("> ")
            user_choice = int(user_response)
            print("You chose {}".format(user_choice))
            result = ""
            if user_choice == 1:
                result = self.process_player_choice(elem.response_1[0], elem.response_1[1])
            elif user_choice == 2:
                result = self.process_player_choice(elem.response_2[0], elem.response_2[1])
            elif user_choice == 3:
                result = self.process_player_choice(elem.response_3[0], elem.response_3[1])
            if result == "end game":
                return result
            elif result == "end conversation":
                return result
            elif result == "continue":
                pass
            else:
                raise ValueError("Error! I don't understand this: {}".format(result))

    def __len__(self):
        return len(self.inner)

# **************************************************
if __name__ == "__main__":
    npc_name = "old_ben"
    # ----
    player_name = "henry"
    zone_name = "dark_alley"
    map_name = "map01"
    profession_name = "warrior"
    utils.set_user_data(player_name, zone_name, map_name, profession_name)
    # ----
    myspeech = Speech(npc_name)
    myspeech.read_data()
    myspeech.main()
    # myspeech.debug_print()
