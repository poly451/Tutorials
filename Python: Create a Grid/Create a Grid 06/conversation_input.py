import os, sys
import utils

# -----------------------------------------------------------
#                      class ConversationInput
# -----------------------------------------------------------
class ConversationInput:
    def __init__(self, npc_name, zone_name, map_name):
        self.npc_name = npc_name
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.index = 0
        self.quest_name = "quest name {}"
        self.quest_summary = "this is a quest summary"
        self.quest_display_text = "this is the quest display text"
        self.zone_name_giver = "{}".format(zone_name)
        self.map_name_giver = "{}".format(map_name)
        self.npc_name_giver = "{}".format(npc_name)
        self.zone_name_receiver = "{}".format(zone_name)
        self.map_name_receiver = "{}".format(map_name)
        self.npc_name_receiver = "{}".format(npc_name)
        self.quest_area_zone_name = "{}".format(zone_name)
        self.quest_area_map_name = "{}".format(map_name)
        self.quest_area_npc = "{}".format(npc_name)
        self.quest_area_success_item = "none"
        self.quest_area_number_of_success_items = 0
        self.quest_reward_item = "none"
        self.quest_reward_item_number = 0
        self.quest_reward_gold = 0
        self.quest_accepted = False
        self.quest_completed = False
        # ----

    def _get_history(self):
        s = ""
        s += "index: {}\n".format(self.index)
        s += "quest_name: {}\n".format(self.quest_name.format(utils.get_unique_number()))
        s += "quest_summary: {}\n".format(self.quest_summary)
        s += "quest_display_text: {}\n".format(self.quest_display_text)
        s += "zone_name_giver: {}\n".format(self.zone_name_giver)
        s += "map_name_giver: {}\n".format(self.map_name_giver)
        s += "npc_name_giver: {}\n".format(self.npc_name_giver)
        s += "zone_name_receiver: {}\n".format(self.zone_name_receiver)
        s += "map_name_receiver: {}\n".format(self.map_name_receiver)
        s += "npc_name_receiver: {}\n".format(self.npc_name_receiver)
        s += "quest_area_zone_name: {}\n".format(self.quest_area_zone_name)
        s += "quest_area_map_name: {}\n".format(self.quest_area_map_name)
        s += "quest_area_npc: {}\n".format(self.quest_area_npc)
        s += "quest_area_success_item: {}\n".format(self.quest_area_success_item)
        s += "quest_area_number_of_success_items: {}\n".format(self.quest_area_number_of_success_items)
        s += "quest_reward_item: {}\n".format(self.quest_reward_item)
        s += "quest_reward_item_number: {}\n".format(self.quest_reward_item_number)
        s += "quest_reward_gold: {}\n".format(self.quest_reward_gold)
        s += "quest_accepted: {}\n".format(self.quest_accepted)
        s += "quest_completed: {}\n".format(self.quest_completed)
        return s

    def _get_conservation(self):
        s = "index: 0\n"
        s += "prompt: This is the prompt.\n"
        s += "choice_1: choice 1\n"
        s += "choice_2: choice 2\n"
        s += "choice_3: choice 3\n"
        s += "response_1: response 1\n"
        s += "response_2: response 2\n"
        s += "response_3: response 3\n"
        s += "todo_1: end conversation\n"
        s += "todo_2: end conversation\n"
        s += "todo_3: end conversation\n"
        s += "item_1: none\n"
        s += "item_2: none\n"
        s += "item_3: none\n"
        s += "next_card_1: none\n"
        s += "next_card_2: none\n"
        s += "next_card_3: none\n"
        s += "quest_accepted_1: none\n"
        s += "quest_accepted_2: none\n"
        s += "quest_accepted_3: none\n"
        s += "quest_reward_1: none\n"
        s += "quest_reward_2: none\n"
        s += "quest_reward_3: none\n"
        return s

    def write_to_file(self):
        file_directory = os.path.join("data", "zones", self.zone_name, self.map_name, "conversations")
        if os.path.isdir(file_directory) == False: raise ValueError("Error")
        filenames = os.listdir(file_directory)
        filenames = [i for i in filenames if i.lower() != ".ds_store"]
        # print(len(filenames))
        # print(filenames)
        if len(filenames) == 0:
            filepath = os.path.join(file_directory, "placeholder_history.txt")
            s = self._get_history()
            with open(filepath, "w") as f:
                f.write(s)
            # ----
            filepath = os.path.join(file_directory, "placeholder_conversation.txt")
            s = self._get_conservation()
            with open(filepath, "w") as f:
                f.write(s)
            # ----
            filepath = os.path.join(file_directory, "placeholder_conversation_accepted.txt")
            with open(filepath, "w") as f:
                f.write(s)
            # ----
            filepath = os.path.join(file_directory, "placeholder_conversation_completed.txt")
            with open(filepath, "w") as f:
                f.write(s)

# -----------------------------------------------------------
#                      class ConversationPlaceholders
# -----------------------------------------------------------

class ConversationPlaceholders:
    def __init__(self):
        npc_name = "placeholder"
        zone_name = "apple_grove"
        map_name = "map00"
        maps = ["map00", "map01", "map02", "map03", "map04", "map05"]
        zones = ["apple_grove", "cliffs", "dark_alley", "easthaven", "swindon_pub"]
        zones += ["green_lawn", "harrogate", "testing", "jeweler", "the_orchard", "swindon"]
        for zone in zones:
            for map in maps:
                mydir = os.path.join("data", "zones", zone, map, "conversations")
                if os.path.isdir(mydir) == True:
                    myobject = ConversationInput(npc_name=npc_name, zone_name=zone, map_name=map)
                    myobject.write_to_file()

if __name__ == "__main__":
    myobject = ConversationPlaceholders()