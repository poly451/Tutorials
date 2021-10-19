import sys, os
import constants
import utils
from inventory_classes import Consumables, Weapons
import pygame

# -----------------------------------------------------------
#                      class MerchantConversation
# -----------------------------------------------------------
class MerchantCoversation:
    def __init__(self, player_name,
                 npc_name, zone_name, map_name):
        self.player_name = player_name
        self.npc_name = npc_name
        self.zone_name = zone_name
        self.map_name = map_name
        # ----


# -----------------------------------------------------------
#                      class SearchMasterQuest
# -----------------------------------------------------------
class SearchMasterQuest:
    def __init__(self, mydict):
        # self.zone_name = zone_name
        # self.map_name = map_name
        # ----
        self.index = -1
        self.quest_name = ""
        self.quest_summary = ""
        self.quest_display_text = ""
        self.zone_name_giver = ""
        self.map_name_giver = ""
        self.npc_name_giver = ""
        self.zone_name_receiver = ""
        self.map_name_receiver = ""
        self.npc_name_receiver = ""
        self.quest_area_zone_name = ""
        self.quest_area_map_name = ""
        self.quest_area_npc = ""
        self.quest_area_success_item = ""
        self.quest_area_number_of_success_items = ""
        self.quest_reward_item = ""
        self.quest_reward_item_number = -1
        self.quest_reward_gold = -1
        self.quest_accepted = False
        self.quest_completed = False
        # ----
        self.filename = ""
        # ----
        self.read_data(mydict)
        # ----

    def read_data(self, mydict):
        # print("mydict: {}".format(mydict))
        self.index = int(mydict["index"])
        self.quest_name = mydict["quest_name"].lower().strip()
        if not self.quest_name in constants.QUEST_NAMES:
            if self.quest_name.find("quest name 2021") == -1:
                s = "I don't recognize this quest name: {}".format(self.quest_name)
                raise ValueError(s)
        self.quest_summary = mydict["quest_summary"]
        self.quest_display_text = mydict["quest_display_text"]
        self.zone_name_giver = mydict["zone_name_giver"]
        if not self.zone_name_giver in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(self.zone_name_giver)
            raise ValueError(s)
        self.map_name_giver = mydict["map_name_giver"]
        if not self.map_name_giver in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.map_name_giver)
            raise ValueError(s)
        self.npc_name_giver = mydict["npc_name_giver"].lower().strip()
        if not self.npc_name_giver in constants.NPC_NAMES:
            s = "I don't recognize this npc name: {}".format(self.npc_name_giver)
            raise ValueError(s)
        self.zone_name_receiver = mydict["zone_name_receiver"]
        if not self.zone_name_receiver in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(self.zone_name_receiver)
            raise ValueError(s)
        self.map_name_receiver = mydict["map_name_receiver"]
        if not self.map_name_receiver in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.map_name_receiver)
            raise ValueError(s)
        self.npc_name_receiver = mydict["npc_name_receiver"].lower().strip()
        if not self.npc_name_receiver in constants.NPC_NAMES:
            s = "I don't recognize this npc name: {}".format(self.npc_name_receiver)
            raise ValueError(s)
        self.quest_area_zone_name = mydict["quest_area_zone_name"]
        if not self.quest_area_zone_name in constants.ZONE_NAMES:
            temp = self.quest_area_zone_name.replace(" ", "_")
            if not temp in constants.ZONE_NAMES:
                s = "I don't recognize this zone name: {}".format(temp)
                raise ValueError(s)
        self.quest_area_map_name = mydict["quest_area_map_name"]
        if not self.quest_area_map_name in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.quest_area_map_name)
            raise ValueError(s)
        self.quest_area_npc = mydict["quest_area_npc"].lower().strip()
        if self.quest_area_npc == "none": self.quest_area_npc = None
        if not self.quest_area_npc in constants.NPC_NAMES:
            if not self.quest_area_npc is None:
                s = "I don't recognize this npc name: {} ({})".format(self.quest_area_npc, type(self.quest_area_npc))
                raise ValueError(s)
        self.quest_area_success_item = mydict["quest_area_success_item"].lower().strip()
        if self.quest_area_success_item == "none": self.quest_area_success_item = None
        if not self.quest_area_success_item in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
            if not self.quest_area_success_item is None:
                s = "I don't recognize this item name: {}".format(self.quest_area_success_item)
                raise ValueError(s)
        self.quest_area_number_of_success_items = mydict["quest_area_number_of_success_items"]
        if utils.is_int(self.quest_area_number_of_success_items) == False:
            raise ValueError("Error")
        self.quest_reward_item = mydict["quest_reward_item"].lower().strip()
        if not self.quest_reward_item in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
            if self.quest_reward_item == "none":
                self.quest_reward_item = None
            else:
                s = "I don't recognize this: {}".format(self.quest_reward_item)
                raise ValueError(s)
        self.quest_reward_item_number = mydict["quest_reward_item_number"]
        if utils.is_int(self.quest_reward_item_number) == True:
            self.quest_reward_item_number = int(self.quest_reward_item_number)
        elif utils.is_int(self.quest_reward_item_number) == False:
            if self.quest_reward_item_number.lower().strip() =="none":
                self.quest_reward_item_number = None
            else:
                s = "This is the value: {}".format(self.quest_reward_item_number)
                raise ValueError(s)
        self.quest_reward_gold = mydict["quest_reward_gold"]
        if self.quest_reward_gold == "none":
            self.quest_reward_gold = None
        if utils.is_int(self.quest_reward_gold) == False:
            s = "This is the value: {}".format(self.quest_reward_gold)
            raise ValueError(s)
        else:
            self.quest_reward_gold = int(self.quest_reward_gold)
        if utils.is_int(self.quest_reward_gold) == False:
            if not self.quest_reward_gold == None:
                raise ValueError("Error")
        self.quest_accepted = mydict["quest_accepted"].lower().strip()
        if self.quest_accepted == "true": self.quest_accepted = True
        if self.quest_accepted == "false" : self.quest_accepted = False
        if not self.quest_accepted in [True, False]:
            raise ValueError("Error")
        self.quest_completed = mydict["quest_completed"].lower().strip()
        if self.quest_completed == "true": self.quest_completed = True
        if self.quest_completed == "false": self.quest_completed = False
        if not self.quest_completed in [True, False]:
            raise ValueError("Error")
        # ----
        self.filename = mydict["filename"]

    def debug_print(self):
        s = "index: {}\n".format(self.index)
        s += "quest_name: {}\n".format(self.quest_name)
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
        s += "filename: {}\n\n".format(self.filename)
        print(s)

    # def save_data(self):
    #     filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "conversations", "tyla_history.txt")
    #     # filepath = os.path.join("data", "testing.txt")
    #     s = "index: {}\n".format(self.index)
    #     s += "quest_name: {}\n".format(self.quest_name)
    #     s += "quest_summary: {}\n".format(self.quest_summary)
    #     s += "quest_display_text: {}\n".format(self.quest_display_text)
    #     s += "zone_name_giver: {}\n".format(self.zone_name_giver)
    #     s += "map_name_giver: {}\n".format(self.map_name_giver)
    #     s += "npc_name_giver: {}\n".format(self.npc_name_giver)
    #     s += "zone_name_receiver: {}\n".format(self.zone_name_receiver)
    #     s += "map_name_receiver: {}\n".format(self.map_name_receiver)
    #     s += "npc_name_receiver: {}\n".format(self.npc_name_receiver)
    #     s += "quest_area_zone_name: {}\n".format(self.quest_area_zone_name)
    #     s += "quest_area_map_name: {}\n".format(self.quest_area_map_name)
    #     s += "quest_area_npc: {}\n".format(self.quest_area_npc)
    #     s += "quest_area_success_item: {}\n".format(self.quest_area_success_item)
    #     s += "quest_area_number_of_success_items: {}\n".format(self.quest_area_number_of_success_items)
    #     s += "quest_reward_item: {}\n".format(self.quest_reward_item)
    #     s += "quest_reward_item_number: {}\n".format(self.quest_reward_item_number)
    #     s += "quest_reward_gold: {}\n".format(self.quest_reward_gold)
    #     s += "quest_accepted: {}\n".format(self.quest_accepted)
    #     s += "quest_completed: {}\n".format(self.quest_completed)
    #     with open(filepath, "w") as f:
    #         f.write(s)

# -----------------------------------------------------------
#                      class SearchMasterQuests
# -----------------------------------------------------------
class SearchMasterQuests:
    def __init__(self):
        self.inner = []
        # ----
        self.read_data()

    def read_data(self):
        self.inner = []
        # ----
        basepath = os.path.join("data", "zones")
        list_of_filenames = utils.get_histories_filenames(basepath)
        if list_of_filenames is None: return False
        if len(list_of_filenames) == 0: return False
        mylist = []
        print(list_of_filenames)
        for filename in list_of_filenames:
            if filename.find("history") == -1:
                raise ValueError("Error")
            if os.path.isfile(filename) == False:
                s = "This doesn't seem to be a valid filepath: --{}--".format(filename)
                raise ValueError(s)
            mydict = utils.read_file(filename)[0]
            mydict["filename"] = filename
            mylist.append(mydict)
        # ----
        for mydict in mylist:
            myobject = SearchMasterQuest(mydict)
            self.inner.append(myobject)

    def get_quest_by_quest_name(self, quest_name):
        mylist = []
        # print("number of quests: {}".format(len(self.inner)))
        for elem in self.inner:
            # print("{} == {}".format(elem.quest_name, quest_name))
            # print("elem.quest_name: {}".format(elem.quest_name))
            if elem.quest_name == quest_name:
                mylist.append(elem)
        if len(mylist) == 0:
            s = "Error!!!! You do not have ANY quests with this name: {}".format(quest_name)
            raise ValueError(s)
        elif len(mylist) > 1:
            s = "Error!!!! You have more than one quest with the same name: {}".format(quest_name)
            print(s)
            print("---- the quests ----")
            print("number of elements in mylist: {}".format(len(mylist)))
            for elem in mylist:
                elem.debug_print()
                print("---- elem ----")
            # [i.debug_print() for i in mylist]
            print("--------------------")
            raise ValueError("Error")
        return mylist[0]

    def get_all_accepted_quests_by_name(self, quest_name):
        """Returns all the quests the player has
        accepted by the name of the quest."""
        mylist = []
        for a_quest_name in constants.QUEST_NAMES:
            print("-----------------------------------------------------")
            print("-----------------------------------------------------")
            print("Looking for quest name: {}".format(a_quest_name))
            a_quest = self.get_quest_by_quest_name(a_quest_name)
            if a_quest.quest_accepted == True:
                mylist.append(a_quest.quest_name)
                mylist.append("accepted: {}".format(a_quest.quest_accepted))
                mylist.append("completed: {}".format(a_quest.quest_completed))
                mylist.append("required: {} of {}".format(a_quest.quest_area_success_item,
                                                          a_quest.quest_area_number_of_success_items))
                mylist.append("----")
        return mylist

    def get_all_quests_by_npc(self, npc_name):
        mylist = []
        # print("number of quests: {}".format(len(self.inner)))
        for elem in self.inner:
            # print("{} == {}".format(elem.quest_name, quest_name))
            # print("elem.quest_name: {}".format(elem.quest_name))
            if elem.npc_name_giver.lower().strip() == npc_name.lower().strip():
                mylist.append(elem)
            elif elem.elem.npc_name_receiver.lower().strip() == npc_name.lower().strip():
                mylist.append(elem)
        return mylist


    def this_quest_has_been_accepted(self, quest_name):
        quest = self.get_quest_by_quest_name(quest_name)
        s = "quest: {}".format(quest)
        print(s)

    def quest_accepted(self, quest_name):
        if not quest_name in constants.QUEST_NAMES:
            raise ValueError("Error")
        quest = self.get_quest_by_quest_name(quest_name)
        if quest is None:
            raise ValueError("Error")
        return quest.quest_accepted

    def quest_completed(self, quest_name):
        if not quest_name in constants.QUEST_NAMES:
            raise ValueError("Error")
        quest = self.get_quest_by_quest_name(quest_name)
        if quest is None:
            raise ValueError("Error")
        return quest.quest_completed

    def debug_print(self):
        if len(self.inner) == 0:
            s = "len(self.inner) == 0"
            raise ValueError(s)
        for a_quest in self.inner:
            a_quest.debug_print()

# -----------------------------------------------------------
#                      class MasterQuest
# -----------------------------------------------------------
class MasterQuest:
    def __init__(self, zone_name, map_name, npc_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.npc_name = npc_name
        self.read_history()

    def read_history(self):
        filename = "{}_history.txt".format(self.npc_name)
        filepath = os.path.join("data", "zones", self.zone_name,
                                self.map_name, "conversations",
                                filename)
        mydict = utils.read_file(filepath)[0]
        self.read_from_dict(mydict)
        # ----

    def read_from_dict(self, mydict):
        print("mydict: {}".format(mydict))
        # ----
        self.index = int(mydict["index"])
        self.quest_name = mydict["quest_name"].lower().strip()
        if not self.quest_name in constants.QUEST_NAMES:
            s = "I don't recognize this quest name: --{}--".format(self.quest_name)
            raise ValueError(s)
        self.quest_summary = mydict["quest_summary"]
        self.quest_display_text = mydict["quest_display_text"]
        self.zone_name_giver = mydict["zone_name_giver"]
        if not self.zone_name_giver in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(self.zone_name_giver)
            raise ValueError(s)
        self.map_name_giver = mydict["map_name_giver"]
        if not self.map_name_giver in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.map_name_giver)
            raise ValueError(s)
        self.npc_name_giver = mydict["npc_name_giver"].lower().strip()
        if not self.npc_name_giver in constants.NPC_NAMES:
            s = "I don't recognize this npc name: {}".format(self.npc_name_giver)
            raise ValueError(s)
        self.zone_name_receiver = mydict["zone_name_receiver"]
        if not self.zone_name_receiver in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(self.zone_name_receiver)
            raise ValueError(s)
        self.map_name_receiver = mydict["map_name_receiver"]
        if not self.map_name_receiver in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.map_name_receiver)
            raise ValueError(s)
        self.npc_name_receiver = mydict["npc_name_receiver"].lower().strip()
        if not self.npc_name_receiver in constants.NPC_NAMES:
            s = "I don't recognize this npc name: {}".format(self.npc_name_receiver)
            raise ValueError(s)
        self.quest_area_zone_name = mydict["quest_area_zone_name"]
        if not self.quest_area_zone_name in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}\n".format(self.quest_area_zone_name)
            s += ', '.join(constants.ZONE_NAMES)
            raise ValueError(s)
        self.quest_area_map_name = mydict["quest_area_map_name"]
        if not self.quest_area_map_name in constants.MAP_CHOICES:
            s = "I don't recognize this map name: {}".format(self.quest_area_map_name)
            raise ValueError(s)
        self.quest_area_npc = mydict["quest_area_npc"].lower().strip()
        if self.quest_area_npc == "none": self.quest_area_npc = None
        if self.quest_area_npc != None:
            if not self.quest_area_npc in constants.NPC_NAMES:
                s = "I don't recognize this npc name: {}".format(self.quest_area_npc)
                raise ValueError(s)
        self.quest_area_success_item = mydict["quest_area_success_item"].lower().strip()
        if self.quest_area_success_item == "none":
            self.quest_area_success_item = None
        if not self.quest_area_success_item is None:
            if not self.quest_area_success_item in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
                s = "I don't recognize this item name: {}".format(self.quest_area_success_item)
                raise ValueError(s)
        self.quest_area_number_of_success_items = mydict["quest_area_number_of_success_items"]
        if utils.is_int(self.quest_area_number_of_success_items) == False:
            raise ValueError("Error")
        self.quest_reward_item = mydict["quest_reward_item"].lower().strip()
        if self.quest_reward_item == "none": self.quest_reward_item = None
        if not self.quest_reward_item is None:
            if not self.quest_reward_item in (constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES):
                s = "I don't recognize this: {}".format(self.quest_reward_item)
                raise ValueError(s)
        self.quest_reward_item_number = mydict["quest_reward_item_number"]
        if utils.is_int(self.quest_reward_item_number) == True:
            self.quest_reward_item_number = int(self.quest_reward_item_number)
        elif utils.is_int(self.quest_reward_item_number) == False:
            if self.quest_reward_item_number.lower().strip() =="none":
                self.quest_reward_item_number = None
            else:
                s = "This is the value: {}".format(self.quest_reward_item_number)
                raise ValueError(s)
        self.quest_reward_gold = mydict["quest_reward_gold"]
        if self.quest_reward_gold == "none":
            self.quest_reward_gold = None
        if utils.is_int(self.quest_reward_gold) == False:
            s = "This is the value: {}".format(self.quest_reward_gold)
            raise ValueError(s)
        else:
            self.quest_reward_gold = int(self.quest_reward_gold)
        if utils.is_int(self.quest_reward_gold) == False:
            if not self.quest_reward_gold == None:
                raise ValueError("Error")
        self.quest_accepted = mydict["quest_accepted"].lower().strip()
        if self.quest_accepted == "true": self.quest_accepted = True
        if self.quest_accepted == "false" : self.quest_accepted = False
        if not self.quest_accepted in [True, False]:
            raise ValueError("Error")
        self.quest_completed = mydict["quest_completed"].lower().strip()
        if self.quest_completed == "true": self.quest_completed = True
        if self.quest_completed == "false": self.quest_completed = False
        if not self.quest_completed in [True, False]:
            raise ValueError("Error")
        # ----
        if not (self.npc_name_giver == self.npc_name or self.npc_name_receiver == self.npc_name):
            s = "npc_name: {}\n".format(self.npc_name)
            s += "npc_name_giver: {}, npc_name_receiver: {}".format(self.npc_name_giver, self.npc_name_receiver)
            raise ValueError(s)
        if not (self.zone_name_giver == self.zone_name or self.zone_name_receiver == self.zone_name):
            a = "quest name: {}".format(self.quest_name)
            s = "zone_name_giver: {}".format(self.zone_name_giver)
            u = "zone_name_receiver: {}".format(self.zone_name_receiver)
            t = "self.zone_name: {}".format(self.zone_name)
            w = "npc_name_giver: {}".format(self.npc_name_giver)
            v= "\n{}\n{}\n{}\n{}\n{}".format(a, w, s, u, t)
            raise ValueError(v)
        if not (self.map_name_giver == self.map_name or self.map_name_receiver == self.map_name):
            s = "map_name_giver: {}\n".format(self.map_name_giver)
            s += "map_name: {}\n".format(self.map_name)
            s += "map_name_receiver: {}\n".format(self.map_name_receiver)
            raise ValueError(s)

    def debug_print(self):
        s = "index: {}\n".format(self.index)
        s += "quest_name: {}\n".format(self.quest_name)
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
        s += "quest_completed: {}\n\n".format(self.quest_completed)
        print(s)

    def save_data(self):
        filename = "{}_history.txt".format(self.npc_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "conversations", filename)
        # filepath = os.path.join("data", "testing.txt")
        s = "index: {}\n".format(self.index)
        s += "quest_name: {}\n".format(self.quest_name)
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
        with open(filepath, "w") as f:
            f.write(s)


# -----------------------------------------------------------
#                      class MasterQuests
# -----------------------------------------------------------
class MasterQuests:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.inner = []

    def read_data(self):
        self.inner = []
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "conversations")
        if os.path.isdir(filepath) == False:
            raise ValueError("Error")
        filenames = os.listdir(filepath)
        for filename in filenames:
            path = os.path.join(filepath, filename)
            if path.find("history") == -1:
                continue
            # ----
            myint = filename.find("_")
            if myint == -1: raise ValueError("Error")
            npc_name = filename[0:myint]
            # ----
            mydict = utils.read_data_file(path, 20)[0]
            new_object = MasterQuest(self.zone_name, self.map_name, npc_name)
            self.inner.append(new_object)

    def main(self):
        pass

    def filter(self, condition):
        if not condition in ["accepted", "completed"]:
            raise ValueError("Error")
        mylist = []
        for elem in self.inner:
            if condition == "accepted":
                if elem.quest_accepted == True:
                    mylist.append(elem)
            elif condition == "completed":
                if elem.quest_completed == True:
                    mylist.append(elem)
            else:
                raise ValueError("Error")
        self.inner = mylist

    def display_print(self):
        mylist = []
        print("--------------------------------------")
        for a_quest in self.inner:
            s = "{}, accepted: {}, completed: {}".format(a_quest.quest_name, a_quest.quest_accepted, a_quest.quest_completed)
            mylist.append(s)
        # ----
        [print(i) for i in mylist]

    def get_display_list(self):
        mylist = []
        print("--------------------------------------")
        for a_quest in self.inner:
            s = "{}, accepted: {}, completed: {}, ".format(a_quest.quest_name, a_quest.quest_accepted, a_quest.quest_completed)
            s += "zone: {}, npc_name: {}".format(self.zone_name, a_quest.npc_name_giver)
            mylist.append(s)
        return mylist

    def debug_print(self):
        for a_quest in self.inner:
            a_quest.debug_print()
# -----------------------------------------------------------
#                      class CardUserChoice
# -----------------------------------------------------------
class CardUserChoice:
    def __init__(self, mydict):
        # ['Alfred says, "I have water and dry bread for sale."', ' ',
        # '1) You say, "I would like to buy a flask of bitter water (you have {} flasks)."', ' ',
        # '2) You say, "I would like to buy a loaf of dry bread (you have {} loaves)."', ' ',
        # '3) You say, "Now that I think of it, I really don\'t need any food."', ' ', ' ',
        # 'You say, "I would like to buy a loaf of dry bread (you have {} loaves)."', ' ',
        # 'Alfred nods, "Okay, one moment..."', ' ', 'Press <Enter> to continue.']
        self.user_choice = -1
        self.command = mydict["command"]
        self.prompt = mydict["prompt"]
        self.choice_1 = mydict["choice_1"]
        self.choice_2 = mydict["choice_2"]
        self.choice_3 = mydict["choice_3"]
        self.response_1 = mydict["response_1"].strip()
        self.response_2 = mydict["response_2"].strip()
        self.response_3 = mydict["response_3"].strip()
        if len(self.response_1) == 0: raise ValueError("Error")
        if len(self.response_2) == 0: raise ValueError("Error")
        if len(self.response_3) == 0: raise ValueError("Error")
        # ----
        self.display_list_1 = []
        self.display_list_2 = []

    def read_data_1(self):
        # self.command = "buy" if todo.find("buy") > -1 else todo
        # self.command = "sell" if todo.find("sell") > -1 else todo
        # ----
        self.display_list_1 = []
        self.display_list_1.append(self.prompt)
        self.display_list_1.append(" ")
        # ----
        self.display_list_1.append("1) {}".format(self.choice_1))
        self.display_list_1.append(" ")
        self.display_list_1.append("2) {}".format(self.choice_2))
        self.display_list_1.append(" ")
        self.display_list_1.append("3) {}".format(self.choice_3))

    def read_data_2(self, user_choice, command, player_inventory, the_item, player_gold):
        if player_inventory is None:
            raise ValueError("Error")
        if not user_choice in [1, 2, 3]: raise ValueError("Error")
        if not command in constants.CONVERSATION_ENDINGS:
            print(constants.CONVERSATION_ENDINGS)
            raise ValueError("I couldn't find this: -{}- ({})".format(command, type(command)))
        # ----
        self.user_choice = user_choice
        # ----
        if self.user_choice == 1:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if command == "sell" and get_item is None:
                    choice = "1) {} ({} (0) | {} gold.)".format(self.choice_1, the_item, player_gold)
                else:
                    choice = "1) {} ({} ({}) | {} gold.)".format(self.choice_1, the_item, get_item.units, player_gold)
            else:
                choice = "1) {}".format(self.choice_1)
            response = self.response_1
        elif self.user_choice == 2:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if command == "sell" and get_item is None:
                    choice = "2) {} ({} (0) | {} gold.)".format(self.choice_2, the_item, player_gold)
                else:
                    choice = "2) {} ({} ({}) | {} gold.)".format(self.choice_2, the_item, get_item.units, player_gold)
            else:
                choice = "2) {}".format(self.choice_2)
            response = self.response_2
        elif self.user_choice == 3:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if command == "sell" and get_item is None:
                    choice = "3) {} ({} (0) | {} gold.)".format(self.choice_3, the_item, player_gold)
                else:
                    choice = "3) {} ({} ({}) | {} gold.)".format(self.choice_3, the_item,get_item.units, player_gold)
            else:
                choice = "3) {}".format(self.choice_3)
            response = self.response_3
        else:
            raise ValueError("Error")
        # ----------------------------
        self.display_list_2 = []
        self.display_list_2.append(self.prompt)
        self.display_list_2.append(" ")
        self.display_list_2.append(choice)
        self.display_list_2.append(" ")
        self.display_list_2.append(response)

    def read_data_3(self, user_choice, command, player_inventory, the_item, player_gold):
        if player_inventory is None:
            raise ValueError("Error")
        if not user_choice in [1, 2, 3]: raise ValueError("Error")
        if not command in constants.CONVERSATION_ENDINGS:
            print(constants.CONVERSATION_ENDINGS)
            raise ValueError("I couldn't find this: -{}- ({})".format(command, type(command)))
        # ----
        self.user_choice = user_choice
        # ----
        if self.user_choice == 1:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if get_item is None:
                    s = "I don't recognize this item name: ".format(the_item)
                    raise ValueError("Error")
                if command == "sell" and get_item is None:
                    choice = "1) {} ({} (0) | {} gold.)".format(self.choice_1, the_item, player_gold)
                else:
                    choice = "1) {} ({} ({}) | {} gold.)".format(self.choice_1, the_item, get_item.units, player_gold)
            else:
                choice = "1) {}".format(self.choice_1)
            response = self.response_1
        elif self.user_choice == 2:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if command == "sell" and get_item is None:
                    choice = "2) {} ({} (0) | {} gold.)".format(self.choice_2, the_item, player_gold)
                else:
                    choice = "2) {} ({} ({}) | {} gold.)".format(self.choice_2, the_item, get_item.units, player_gold)
            else:
                choice = "2) {}".format(self.choice_2)
            response = self.response_2
        elif self.user_choice == 3:
            if command in ["buy", "sell"]:
                get_item = player_inventory.get_item_by_name(the_item)
                if command == "sell" and get_item is None:
                    choice = "3) {} ({} (0) | {} gold.)".format(self.choice_3, the_item, player_gold)
                else:
                    choice = "3) {} ({} ({}) | {} gold.)".format(self.choice_3, the_item,get_item.units, player_gold)
            else:
                choice = "3) {}".format(self.choice_3)
            response = self.response_3
        else:
            raise ValueError("Error")
        # ----------------------------
        self.display_list_2 = [" "]
        self.display_list_2.append(" ")
        self.display_list_2.append(choice)
        self.display_list_2.append(" ")
        self.display_list_2.append(response)

    def _process_user_choice(self, choice_number, command, player_inventory, npc_inventory, item_name):
        print("---- debugging ----")
        print("choice_number: {}".format(choice_number))
        print("command: {}".format(command))
        print("item_name: {}".format(item_name))
        # print("player_gold: {}".format(player_gold))
        if not choice_number in [1, 2, 3]:
            raise ValueError("Error")
        # if type(item_name) != type("abc"):
        #     s = "This item_name isn't a string! {} ({})".format(item_name, type(item_name))
        #     raise ValueError(s)
        # if item_name is None:
        #     raise ValueError("Error")
        choice = ""
        response = ""
        print("---- debugging ----")
        # ----
        # raise ValueError(command)
        if command in ["buy", "sell"]:
            gold_item = player_inventory.get_item_by_name("gold coin")
            if gold_item is None: raise ValueError("Error")
            the_item = None
            if command == "sell":
                # player must have the item in his/her/+ inventory.
                the_item = player_inventory.get_item_by_name(item_name)
                if the_item is None:
                    # s = "The player cannot sell this item. He does not have it in his inventory: ".format(item_name)
                    # raise ValueError("Error")
                    # choice = "1) {} ({} (0) | {} gold.)".format(self.choice_1, item_name, player_gold)
                    choice = "Error! You do not have any of these ({}) and therefore cannot sell.".format(item_name)
                else:
                    gold_item = player_inventory.get_item_by_name("gold coin")
                    if gold_item is None: raise ValueError("Error")
                    # ----
                    if choice_number == 1:
                        choice = "{}) {} ({} ({}) | You have {} gold.)".format(choice_number, self.choice_1,
                                                                               item_name, the_item.units,
                                                                               gold_item.units)
                        response = self.response_1
                    elif choice_number == 2:
                        choice = "{}) {} ({} ({}) | You have {} gold.)".format(choice_number, self.choice_2,
                                                                               item_name, the_item.units,
                                                                               gold_item.units)
                        response = self.response_2
                    elif choice_number == 3:
                        choice = "{}) {} ({} ({}) | You have {} gold.)".format(choice_number, self.choice_3,
                                                                               item_name, the_item.units,
                                                                               gold_item.units)
                        response = self.response_3
            elif command == "buy":
                try:
                    the_item = npc_inventory.get_item_by_name(item_name)
                except Exception as e:
                    s = "{}\nApparently there is no npc_inventory! This is the item name: {} ({})"
                    s = s.format(e, item_name, type(item_name))
                    raise ValueError(s)
                if the_item is None:
                    s = "You tried to buy an item with this name: {}".format(item_name)
                    raise ValueError(s)
                choice = "{}) {} ({}) | You have {} gold.)".format(choice_number, self.choice_1,
                                                                       item_name, gold_item.units)
            else:
                # choice = "{}) {} ({} ({}) | {} gold.)".format(choice_number, self.choice_1, item_name, the_item.units, player_gold)
                raise ValueError("Error")
        else:
            if choice_number == 1:
                choice = "{}) {}".format(choice_number, self.choice_1)
                response = self.response_1
            elif choice_number == 2:
                choice = "{}) {}".format(choice_number, self.choice_2)
                response = self.response_2
            elif choice_number == 3:
                choice = "{}) {}".format(choice_number, self.choice_3)
                response = self.response_3
            else:
                s = "This isn't a valid choice number: {} ({})\n".format(choice_number, type(choice_number))
                s += "Valid choice numbers: 1, 2, 3"
                raise ValueError(s)
        return choice, response

    def read_data_4(self, user_choice, command, player_inventory, npc_inventory, the_item):
        # raise ValueError(user_choice)
        if player_inventory is None:
            raise ValueError("Error")
        if npc_inventory is None:
            raise ValueError("Error")
        if not user_choice in [1, 2, 3]: raise ValueError("Error")
        if not command in constants.CONVERSATION_ENDINGS:
            print(constants.CONVERSATION_ENDINGS)
            raise ValueError("I couldn't find this: -{}- ({})".format(command, type(command)))
        # if the_item is None: raise ValueError("Error")
        # ----
        self.user_choice = user_choice
        # ----
        print("debugging: before self.process_user_choice")
        choice, response = self._process_user_choice(
            choice_number=self.user_choice,
            command=command,
            player_inventory=player_inventory,
            npc_inventory=npc_inventory,
            item_name=the_item)
        print("debugging: after self.process_user_choice")
        print("debugging: choice: {}, response: {}".format(choice, response))
        # raise ValueError(choice)
        # ----
        self.display_list_2 = [" "]
        self.display_list_2.append(" ")
        self.display_list_2.append(choice)
        self.display_list_2.append(" ")
        self.display_list_2.append(response)

    def display_card(self):
        mylist = []
        mylist.append(self.prompt)
        return mylist

# -----------------------------------------------------------
#                      class Card
# -----------------------------------------------------------
class ConversationCard:
    def __init__(self, mydict):
        self.user_choice = -1
        # ----
        self.index = mydict["index"]
        self.prompt = mydict["prompt"]
        self.choice_1 = mydict["choice_1"]
        self.choice_2 = mydict["choice_2"]
        self.choice_3 = mydict["choice_3"]
        self.response_1 = mydict["response_1"]
        self.response_2 = mydict["response_2"]
        self.response_3 = mydict["response_3"]
        self.todo_1 = mydict["todo_1"].lower().strip()
        self.todo_2 = mydict["todo_2"].lower().strip()
        self.todo_3 = mydict["todo_3"].lower().strip()
        if self.todo_1 == "none": self.todo_1 = None
        if self.todo_2 == "none": self.todo_2 = None
        if self.todo_3 == "none": self.todo_3 = None
        self.item_1 = mydict["item_1"].lower().strip()
        self.item_2 = mydict["item_2"].lower().strip()
        self.item_3 = mydict["item_3"].lower().strip()
        if not utils.is_int(self.item_1): self.item_1.lower().strip()
        if not utils.is_int(self.item_2): self.item_2.lower().strip()
        if not utils.is_int(self.item_3): self.item_3.lower().strip()
        self.next_card_1 = mydict["next_card_1"]
        self.next_card_2 = mydict["next_card_2"]
        self.next_card_3 = mydict["next_card_3"]
        if type(self.next_card_1) == type("abc"): self.next_card_1 = self.next_card_1.lower().strip()
        if type(self.next_card_2) == type("abc"): self.next_card_2 = self.next_card_2.lower().strip()
        if type(self.next_card_3) == type("abc"): self.next_card_3 = self.next_card_3.lower().strip()
        if self.next_card_1 == "none": self.next_card_1 = None
        if self.next_card_2 == "none": self.next_card_2 = None
        if self.next_card_3 == "none": self.next_card_3 = None
        # ----
        if self.item_1 == "none": self.item_1 = None
        if self.item_2 == "none": self.item_2 = None
        if self.item_3 == "none": self.item_3 = None
        # ----
        if self.is_a_valid_item(self.item_1) == False: raise ValueError("Error! item_1 = {}".format(self.item_1))
        if self.is_a_valid_item(self.item_2) == False: raise ValueError("Error! item_2 = {}".format(self.item_2))
        if self.is_a_valid_item(self.item_3) == False: raise ValueError("Error! item_3 = {}".format(self.item_3))
        # ----
        self.quest_accepted_1 = mydict["quest_accepted_1"].lower().strip()
        if self.quest_accepted_1 == "none": self.quest_accepted_1 = None
        self.quest_accepted_1 = True if self.quest_accepted_1 == "true" else False
        # --
        self.quest_accepted_2 = mydict["quest_accepted_2"].lower().strip()
        if self.quest_accepted_2 == "none": self.quest_accepted_2 = None
        self.quest_accepted_2 = True if self.quest_accepted_2 == "true" else False
        # --
        self.quest_accepted_3 = mydict["quest_accepted_3"].lower().strip()
        if self.quest_accepted_3 == "none": self.quest_accepted_3 = None
        self.quest_accepted_3 = True if self.quest_accepted_3 == "true" else False
        # ---- ----
        self.quest_reward_1 = mydict["quest_reward_1"].lower().strip()
        if self.quest_reward_1 == "none": mydict["quest_reward_1"] = None
        # self.quest_reward_1 = True if self.quest_reward_1 == "true" else False
        # --
        self.quest_reward_2 = mydict["quest_reward_2"].lower().strip()
        if self.quest_reward_2 == "none": mydict["quest_reward_2"] = None
        # self.quest_reward_2 = True if self.quest_reward_2 == "true" else False
        # --
        self.quest_reward_3 = mydict["quest_reward_3"].lower().strip()
        if self.quest_reward_3 == "none": mydict["quest_reward_3"] = None
        # self.quest_reward_3 = True if self.quest_reward_3 == "true" else False
        # ----
        mydict["command"] = "none"
        mydict["user_choice"] = self.user_choice
        self.card_user_choice = CardUserChoice(mydict)
        # ----

    def is_a_valid_item(self, this_item):
        if this_item is None: return True
        if this_item in constants.CONSUMABLE_NAMES: return True
        if this_item in constants.WEAPON_NAMES: return True
        if utils.is_int(this_item) == True: return True
        print("this_item looks as though it isn't valid: {} ({})".format(this_item, type(this_item)))
        return False

    def display_card_1(self):
        # command = utils.only_alphabetical(self.todo_3)
        # if not command in constants.CONVERSATION_ENDINGS: raise ValueError("Error")
        # ----
        self.card_user_choice.read_data_1()
        return self.card_user_choice.display_list_1

    def display_card_2(self, user_choice, player_inventory, npc_inventory):
        # raise ValueError(user_choice)
        if player_inventory is None: raise ValueError("Error")
        if npc_inventory is None: raise ValueError("Error")
        if not utils.is_int(user_choice): raise ValueError("Error")
        self.user_choice = int(user_choice)
        if not self.user_choice in [1, 2, 3]: raise ValueError("Error")
        print("DEBUGGING")
        print("item_1: {}".format(self.item_1))
        print("item_2: {}".format(self.item_2))
        print("item_3: {}".format(self.item_3))
        # raise NotImplemented
        # ----
        todo = ""
        the_item = ""
        command = ""
        self.user_choice = user_choice
        if self.user_choice == 1:
            todo = self.todo_1
            the_item = self.item_1
            command = utils.only_alphabetical(self.todo_1)
        elif self.user_choice == 2:
            print("debugging: YES user choice was 2 <<<<============== *****")
            todo = self.todo_2
            the_item = self.item_2
            command = utils.only_alphabetical(self.todo_2)
        elif self.user_choice == 3:
            todo = self.todo_3
            the_item = self.item_3
            command = utils.only_alphabetical(self.todo_3)
        else:
            raise ValueError("Error")
        if not command in constants.CONVERSATION_ENDINGS:
            s = "I don't recognize this command: {}\n".format(command)
            s += "self.todo_3: {}\n".format(self.todo_3)
            s += "Here are the possible valid commands: {}".format(constants.CONVERSATION_ENDINGS)
            raise ValueError(s)
        if todo is None: raise ValueError("Error")
        print("debugging: in display_card_2: user_choice: {}".format(self.user_choice))
        self.card_user_choice.read_data_4(user_choice=self.user_choice,
                                          command=command,
                                          player_inventory=player_inventory,
                                          npc_inventory=npc_inventory,
                                          the_item=the_item)
        return self.card_user_choice.display_list_2

    def debug_print(self):
        print("index: {}".format(self.index))
        print("prompt: {}".format(self.prompt))
        print("choice_1: {}".format(self.choice_1))
        print("choice_2: {}".format(self.choice_2))
        print("choice_3: {}".format(self.choice_3))
        print("response_1: {}".format(self.response_1))
        print("response_2: {}".format(self.response_2))
        print("response_3: {}".format(self.response_3))
        print("todo_1: {}".format(self.todo_1))
        print("todo_2: {}".format(self.todo_2))
        print("todo_3: {}".format(self.todo_3))
        print("item_1: {}".format(self.item_1))
        print("item_2: {}".format(self.item_2))
        print("item_3: {}".format(self.item_3))
        print("next_card_1: {}".format(self.next_card_1))
        print("next_card_2: {}".format(self.next_card_2))
        print("next_card_3: {}".format(self.next_card_3))
        print("quest_accepted_1: {}".format(self.quest_accepted_1))
        print("quest_accepted_2: {}".format(self.quest_accepted_2))
        print("quest_accepted_3: {}".format(self.quest_accepted_3))
        print("quest_reward_1: {}".format(self.quest_reward_1))
        print("quest_reward_2: {}".format(self.quest_reward_2))
        print("quest_reward_3: {}".format(self.quest_reward_3))

# # -----------------------------------------------------------
# #                      class Conversation_OLD
# # -----------------------------------------------------------
# class Conversation_OLD:
#     def __init__(self, player_name,
#                  npc_name, zone_name, map_name,
#                  conversation_only=False):
#         npc_name = npc_name.replace(" ", "_")
#         # ----
#         if utils.validate_player_name(player_name) == False:
#             raise ValueError("Error!")
#         if utils.is_a_valid_npc_name(player_name=player_name, npc_name=npc_name) == False:
#             raise ValueError("This is not a valid npc_name: {}".format(npc_name))
#         if not zone_name in constants.ZONE_NAMES:
#             raise ValueError("Error!")
#         if not map_name in constants.MAP_CHOICES:
#             raise ValueError("Error!")
#         # if utils.is_int(player_gold) == False:
#         #     raise ValueError("Error!")
#         # --------------------------------------
#         self.conversation_only = conversation_only
#         self.filepath = ""
#         self.init_pygame()
#         self.all_sprites = pygame.sprite.Group()
#         # self.display_choices = True
#         self.message = ""
#         # --------------------------------------
#         self.quest_history = None
#         # --------------------------------------
#         self.player_name = player_name
#         self.npc_name = npc_name
#         self.zone_name = zone_name
#         self.map_name = map_name
#         # self.player_gold = player_gold
#         # ----
#         self.keep_looping = True
#         self.stop_looping = False
#         self.display_list = []
#         self.text = ""
#         self.user_text = ""
#         # ----
#         self.player_inventory = Inventory(player_name=player_name,
#                                           npc_name=npc_name,
#                                           character_type="player")
#         self.npc_inventory = Inventory(player_name=player_name,
#                                        npc_name=npc_name,
#                                        character_type="npc")
#         self.current_card_index = 0
#         self.current_card = None
#         # ----
#         self.inner = []
#
#     def init_pygame(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
#         pygame.display.set_caption("{}".format(constants.TITLE))
#         self.clock = pygame.time.Clock()
#         self.BG_COLOR = constants.WHITE
#         self.font = pygame.font.Font(None, 35)
#
#     def read_data(self):
#         # read quest history
#         self.quest_history = MasterQuest(zone_name=self.zone_name,
#                                          map_name=self.map_name,
#                                          npc_name=self.npc_name)
#         filepath = ""
#         if self.quest_history.quest_completed == True:
#             filename = "{}_conversation_completed.txt".format(self.npc_name)
#             filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
#                                     "conversations", filename)
#         elif self.quest_history.quest_accepted == True:
#             filename = "{}_conversation_accepted.txt".format(self.npc_name)
#             filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
#                                     "conversations", filename)
#         elif self.quest_history.quest_completed == False and self.quest_history.quest_accepted == False:
#             filename = "{}_conversation.txt".format(self.npc_name)
#             filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
#                                     "conversations", filename)
#         # elif self.quest_history.quest_accepted == True and self.quest_history.quest_completed == False:
#         #     filename = "{}_conversation_accepted.txt".format(self.npc_name)
#         #     filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
#         #                             "conversations", filename)
#         # elif self.quest_history.quest_completed == True:
#         #     filename = "{}_conversation_completed.txt".format(self.npc_name)
#         #     filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
#         #                             "conversations", filename)
#         else:
#             raise ValueError("Error")
#         # ----
#         # print("filepath:", filepath)
#         # raise NotImplemented
#         if os.path.isfile(filepath) == False:
#             s = "This isn't a valid filename: {}".format(filepath)
#             raise ValueError(s)
#         mylist = utils.read_data_file(filepath, num_of_fields=23)
#         for mydict in mylist:
#             myobject = ConversationCard(mydict)
#             self.inner.append(myobject)
#         # ----
#         self.player_inventory.read_data()
#         self.npc_inventory.read_data()
#         self.current_card = self.get_card(self.current_card_index)
#         # self.current_card.debug_print()
#         # raise NotImplemented
#         # ----
#         self.display_list = self.current_card.display_card_1()
#         # print(self.display_list)
#         # raise NotImplemented
#
#     def get_card(self, index):
#         for a_card in self.inner:
#             if a_card.index == index:
#                 return a_card
#         return None
#
#     def debug_print(self):
#         # print("Player's gold: {}".format(self.player_gold))
#         for elem in self.inner:
#             print("------------")
#             elem.debug_print()
#         print("============")
#
#     def goto_next_card(self, card_index_number):
#         print("going to next card: {}".format(card_index_number))
#         self.current_card = self.get_card(card_index_number)
#         if self.current_card is None:
#             s = "card_index_number: {}".format(card_index_number)
#             raise ValueError(s)
#         # self.current_card.debug_print()
#         # raise NotImplemented
#
#     def _required_item_absent(self):
#         self.display_list = []
#         self.stop_looping = True
#         mylist = ["{} frowns at you.".format(self.npc_name.title())]
#         mylist.append(" ")
#         # ----
#         s = ""
#         if self.quest_history.quest_area_number_of_success_items == 1:
#             s = "We agreed that you would deliver a {}. Come back when you can."
#             s = s.format(self.quest_history.quest_area_success_item)
#         elif self.quest_history.quest_area_number_of_success_items > 1:
#             s = "We agreed that you would deliver {} {}s. Come back when you can."
#             s = s.format(self.quest_history.quest_area_number_of_success_items,
#                          self.quest_history.quest_area_success_item)
#         mylist.append(s)
#         self.display_list = mylist
#
#     def _give_player_reward(self):
#         # is it gold or an item?
#         if not self.quest_history.quest_reward_item is None:
#             # if self.quest_history.quest_reward_item.find("gold") == -1:
#             s = "The reward is an ITEM: {}. Adding the item to the player's inventory..."
#             s = s.format(self.quest_history.quest_reward_item)
#             print(s)
#             # the reward is an ITEM
#             reward_item = self.npc_inventory.get_item_by_name(self.quest_history.quest_reward_item)
#             if reward_item is None:
#                 raise ValueError("Error")
#             if self.quest_history.quest_reward_item_number is None:
#                 raise ValueError("Error")
#             self.player_inventory.add_item_by_name(self.quest_history.quest_reward_item, self.quest_history.quest_reward_item_number)
#         # ----
#         if self.quest_history.quest_reward_gold > 0:
#             # self.player_gold += self.quest_history.quest_reward_gold
#             my_item = self.player_inventory.get_item_by_name("gold coin")
#             my_item.units += self.quest_history.quest_reward_gold
#         elif self.quest_history.quest_reward_gold < 0:
#             raise ValueError("Error")
#         elif self.quest_history.quest_reward_gold == 0:
#             pass
#         else:
#             raise ValueError("Error")
#
#     def _process_choice(self, todo_list, item_name, next_card, quest_accepted, quest_reward):
#         # print(next_card)
#         # raise NotImplemented
#         if (not utils.is_int(next_card)) and (not next_card is None):
#             s = "This is next_card: {} ({})".format(next_card, type(next_card))
#             raise ValueError(s)
#         if not item_name is None:
#             if not item_name in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
#                 print(constants.CONSUMABLE_NAMES)
#                 print(constants.WEAPON_NAMES)
#                 s = "I don't recognize this item_name: {}, ({}).".format(item_name, type(item_name))
#                 raise ValueError(s)
#         temp = ' '.join(todo_list).lower()
#         command = utils.only_alphabetical(temp)
#         # utils.log_text("testing.txt", command)
#         if command not in constants.CONVERSATION_ENDINGS: raise ValueError("Error")
#         # ----
#         print("def _process_choice: ", todo_list)
#         print("command: {}".format(command))
#         # todo_string = ""
#         # if len(todo_list) == 3:
#         #     todo_string = "{} {} {}".format(todo_list[0], todo_list[1], todo_list[2])
#         if command == "load next map":
#             print("todo_string == load next map")
#             self.message = command
#             self.stop_looping = True
#             # if next_card is None: raise ValueError("Error")
#             # print("Going to next card: {}".format(next_card))
#             # self.goto_next_card(next_card)
#             # ---------------------------------------------------
#         elif command == "buy":
#             if not item_name in constants.PROVISIONERS_GOODS:
#                 s = "I don't recognize this item name: {}".format(item_name)
#                 raise ValueError(s)
#             if len(todo_list) != 2:
#                 # It should be of the form: buy 2 or sell 4
#                 if len(todo_list) == 1:
#                     s = "If the todo command is to BUY, it has to be of this form: Buy 4"
#                     raise ValueError(s)
#                 if len(todo_list) > 2:
#                     s = "There are too many terms in this list. It should be of the form 'buy 3'"
#                     raise ValueError(s)
#             if not utils.is_int(todo_list[1]):
#                 # s = "I don't recognize this: {} ({})\n".format(todo_list[1], type(todo_list[1]))
#                 s = "This is todo_list: {}\n".format(todo_list)
#                 s += "It should be of the form 'buy 4'"
#                 raise ValueError(s)
#             # ----
#             # does player have enough gold?
#             number_of_items = int(todo_list[1])
#             this_item = self.npc_inventory.get_item_by_name(item_name)
#             if this_item is None: raise ValueError("Error")
#             # ----
#             # Figure out if the player has enough gold.
#             amount_of_gold = this_item.cost * number_of_items
#             gold_item = self.player_inventory.get_item_by_name("gold coin")
#             if gold_item is None: raise ValueError("Error")
#             if gold_item.units < amount_of_gold:
#                 self.display_list = ["It looks like you don't have enough money."]
#                 raise ValueError("Error")
#             self.player_inventory.add_item_by_name(item_name, number_of_items)
#             self.player_inventory.save_data()
#             gold_item.units -= amount_of_gold
#             # add item(s) to the player's inventory
#             if not next_card is None:
#                 # print("next card:", next_card)
#                 # raise NotImplemented
#                 self.goto_next_card(next_card)
#         elif command == "sell":
#             if not item_name in constants.PROVISIONERS_GOODS:
#                 s = "I don't recognize this item name: {}".format(item_name)
#                 raise ValueError(s)
#             if len(todo_list) != 2:
#                 # It should be of the form: buy 2 or sell 4
#                 if len(todo_list) == 1:
#                     s = "If the todo command is to BUY, it has to be of this form: Buy 4"
#                     raise ValueError(s)
#                 elif len(todo_list) > 2:
#                     s = "There are too many terms in this list. It should be of the form 'buy 3'"
#                     raise ValueError(s)
#                 else:
#                     raise ValueError("Error")
#             if not utils.is_int(todo_list[1]):
#                 # s = "I don't recognize this: {} ({})\n".format(todo_list[1], type(todo_list[1]))
#                 s = "This is todo_list: {}\n".format(todo_list)
#                 s += "It should be of the form 'buy 4'"
#                 raise ValueError(s)
#             todo_list[1] = int(todo_list[1])
#             # ----
#             number_of_items = int(todo_list[1])
#             this_item = self.player_inventory.get_item_by_name(item_name)
#             if this_item is None:
#                 # Player does not have the item.
#                 s = "{} squints at you. 'Hey! what are you trying to pull! This isn't a {}. Go away!'"
#                 s = s.format(self.npc_name, item_name)
#                 self.display_list = [s]
#                 self.stop_looping = True
#                 return False
#             else:
#                 gold_item = self.player_inventory.get_item_by_name("gold coin")
#                 if gold_item is None: raise ValueError("Error")
#                 amount_of_gold = this_item.cost * number_of_items
#                 gold_item.units += amount_of_gold
#                 self.player_inventory.remove_item_by_name(item_name, number_of_items)
#                 self.player_inventory.save_data()
#                 # print("---- player inventory ----")
#                 # self.player_inventory.debug_print()
#                 # raise NotImplemented
#             if not next_card is None:
#                 # print("next card:", next_card)
#                 # raise NotImplemented
#                 self.goto_next_card(next_card)
#         elif command == "sell all":
#             raise NotImplemented
#             # the_item = self.player_inventory.get_item_by_name(item_name)
#             # if the_item is None:
#             #     self._required_item_absent()
#             #     return False
#             # gold_coin = self.player_inventory.get_item_by_name("gold coin")
#             # if gold_coin is None: raise ValueError("Error")
#             # number_of_units = the_item.units
#             # gold_gained = number_of_units * the_item.cost
#             # gold_coin.units += gold_gained
#             # if self.player_inventory.remove_item_by_name(item_name, number_of_units) == False:
#             #     raise ValueError("Error")
#             # else:
#             #     print("Have removed {} units of {} from the inventory.".format(number_of_units, item_name))
#             # if not next_card is None:
#             #     self.goto_next_card(next_card)
#         elif command == "end conversation":
#             print("todo_list[0] == end and todo_list[1] == conversation")
#             self.stop_looping = True
#             self.message = "end conversation"
#             if not item_name is None and len(item_name) > 0:
#                 print("NPC has given the command to end the conversation. item_name is NOT none.")
#                 print("The conversation will end, but there will also be a mildly negative outcome for the player.")
#                 print("The player will be given the indicated item.")
#                 print("In this case it is: {}".format(item_name).upper())
#                 self.player_inventory.add_item_by_name(item_name, 1)
#                 print("This is the message: {}".format(self.message))
#             # ---------------------------------------------------
#         elif command == "end game":
#             print("todo_list[0] == end and todo_list[1] == game")
#             self.stop_looping = True
#             self.message = "end game"
#             # elif todo_list[0] == "npc" and todo_list[1] == "fight":
#             #     # Sets the on_contact fild in class Npc to "fight".
#             #     utils.npc_fight_on_contact(self.player_name, self.npc_name)
#             #     self.message = "reload npc"
#             #     self.stop_looping = True
#             # ---------------------------------------------------
#         elif command == "continue":
#             print("todo_list[0] == continue")
#             self.message = "continue"
#             # if utils.is_int(item_name) == True:
#             #     # If there is a number in this field it is taken to be gold.
#             #     self.reward_offered = "{} gold".format(item_name)
#             if not next_card is None:
#                 # print("next card:", next_card)
#                 # raise NotImplemented
#                 self.goto_next_card(next_card)
#                 # print(next_card)
#                 # raise NotImplemented
#             # ---------------------------------------------------
#         elif command == "accepted":
#             print("todo_list[0] == accepted")
#             # The quest has been accepted
#             self.message = "accepted"
#             self.stop_looping = True
#             if not item_name is None and len(item_name) > 0:
#                 self.player_inventory.add_item_by_name(item_name, 1)
#                 print("{} was added to the player's inventory".format(item_name))
#             self.quest_history.reward_offered = quest_reward
#             self.quest_history.quest_accepted = True
#             self.quest_history.result_of_conversation = "accepted"
#             # ---------------------------------------------------
#         elif command == "completed":
#             # print(self.display_list)  # <<-- OKay
#             # raise NotImplemented
#             # print("todo_list[0] == completed")
#             self.message = "completed"
#             self.stop_looping = True
#             self.quest_history.quest_completed = True
#             if not item_name is None:
#                 self.player_inventory.add_item_by_name(item_name, 1)
#                 # self.player_inventory.debug_print()
#             # ----
#             # Check to see that the quest really has been completed.
#             # That is, check to make sure that the player as the
#             # required item(s) in the inventory.
#             # print("self.conversation_only: {}".format(self.conversation_only))
#             if self.conversation_only == True:
#                 # Since this is only a conversation, we don't care about rewards or items.
#                 return True
#             required_item = self.player_inventory.get_item_by_name(self.quest_history.quest_area_success_item)
#             # required_item.debug_print()
#             # raise ValueError("")
#             if required_item is None:
#                 self._required_item_absent()
#                 self.quest_history.quest_completed = False
#                 # s = "Error! The player has not finished the quest!!!!!\n"
#                 # s += "The player does not have the reqired item: {}".format(self.quest_history.required_item)
#                 # raise ValueError(s)
#                 return False
#             if required_item.units < self.quest_history.quest_area_number_of_success_items:
#                 self._required_item_absent()
#                 self.quest_history.quest_completed = False
#                 # s = "Error! The player has not finished the quest!!!!!\n"
#                 # s += "They do not have the required number of items: {}.".format(self.quest_history.number_of_items)
#                 # raise ValueError(s)
#                 return False
#             # The items need to be removed from the player's inventory.from
#             if self.player_inventory.remove_item_by_name(self.quest_history.quest_area_success_item,
#                                                          self.quest_history.quest_area_number_of_success_items) == False:
#                 raise ValueError("Error")
#             # print("*******************")
#             # print("*******************")
#             # self.player_inventory.debug_print()
#             # if (not item_name is None) and len(item_name) > 0:
#             #     # If an item is present (this isn't the required item)
#             #     # it is put in the player's avatar's inventory.
#             #     self.player_inventory.add_item_by_name(item_name, 1)
#             # add reward (if any offered)
#             self._give_player_reward()
#             # print("****")
#             # self.player_inventory.debug_print()
#             # self.quest_history.debug_print()
#             # raise NotImplemented
#             # print("**** ****")
#             # ---------------------------------------------------
#         elif command == "conversation empcliated":
#             raise NotImplemented
#             # The npc and player simply had a one time conversation.
#             # This is NOT a quest.
#             if self.quest_history.required_item is None:
#                 pass
#             else:
#                 if self.quest_history.number_of_items == 0:
#                     pass
#                 else:
#                     raise ValueError("Error!!!")
#             self.quest_history.quest_accepted = True
#             self.quest_history.quest_completed = True
#             if not item_name is None and len(item_name) > 0:
#                 self.player_inventory.add_item_by_name(item_name, 1)
#             self.stop_looping = True
#             self.message = "conversation completed"
#             # ----
#             s = "conversation_with_{}_completed".format(self.npc_name).replace(" ", "_")
#             filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", "event_record.txt")
#             mydict = utils.read_file(filepath)[0]
#             mydict[s] = True
#             with open(filepath, "w") as f:
#                 for key, value in mydict.items():
#                     s = "{}: {}\n".format(key, value)
#                     f.write(s)
#         else:
#             raise ValueError("Error! I don't recognize this: -{}- ({})".format(command, type(command)))
#         print("This is the last line of def _process_choice")
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.keep_looping = False
#             elif event.type == pygame.KEYDOWN:
#                 # self.text_background_color = constants.LIGHTGREY
#                 if event.key == pygame.K_ESCAPE:
#                     self.keep_looping = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     self.user_text = self.user_text[:-1]
#                 elif event.key == pygame.K_RETURN:
#                     print("in handle_events self.stop_looping = {}".format(self.stop_looping))
#                     print("in handle_events self.keep_looping = {}".format(self.keep_looping))
#                     if self.stop_looping == True:
#                         self.keep_looping = False
#                     else:
#                         self.display_list = self.current_card.display_card_1()
#                 elif event.key == pygame.K_1:
#                     if self.stop_looping == True: return False
#                     self.display_choices = False
#                     # ----
#                     self.display_list += self.current_card.display_card_2(user_choice=1,
#                                                                          player_inventory=self.player_inventory,
#                                                                          npc_inventory=self.npc_inventory)
#                     if self.current_card.todo_1 is None:
#                         raise ValueError("Error")
#                     todo_list = self.current_card.todo_1.split(" ")
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     self._process_choice(todo_list,
#                                          self.current_card.item_1,
#                                          self.current_card.next_card_1,
#                                          self.current_card.quest_accepted_1,
#                                          self.current_card.quest_reward_1)
#                     self.goto_next_card(self.current_card.index)
#                 elif event.key == pygame.K_2:
#                     if self.stop_looping == True: return False
#                     self.display_choices = False
#                     # ----
#                     print(";aldjf;asjf -- before self.current_card.display_card_2")
#                     print("here is self.display_list:", self.display_list)
#                     self.display_list += self.current_card.display_card_2(user_choice=2,
#                                                                          player_inventory=self.player_inventory,
#                                                                          npc_inventory=self.npc_inventory)
#                     # raise ValueError(self.display_list)
#                     # print(";aldjf;asjf -- after self.current_card.display_card_2")
#                     # print("here is self.display_list:", self.display_list)
#                     if self.current_card.todo_2 is None:
#                         raise ValueError("Error")
#                     todo_list = self.current_card.todo_2.split(" ")
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     # print(";aldjf;asjf -- before _process_choice")
#                     # print("here is self.display_list:", self.display_list)
#                     # raise ValueError(self.current_card.next_card_2)
#                     it_worked = self._process_choice(todo_list,
#                                          self.current_card.item_2,
#                                          self.current_card.next_card_2,
#                                          self.current_card.quest_accepted_2,
#                                          self.current_card.quest_reward_2)
#                     # print(";aldjf;asjf -- after _process_choice")
#                     # print(self.display_list)
#                     self.goto_next_card(self.current_card.index)
#                     print("---- self.player_inventory ----")
#                     self.player_inventory.debug_print()
#                     print("-------------------------------")
#                     # raise NotImplemented
#                 elif event.key == pygame.K_3:
#                     if self.stop_looping == True: return False
#                     self.display_choices = False
#                     self.display_list += self.current_card.display_card_2(user_choice=3,
#                                                                          player_inventory=self.player_inventory,
#                                                                          npc_inventory=self.npc_inventory)
#                     if self.current_card.todo_3 is None:
#                         raise ValueError("Error")
#                     todo_list = self.current_card.todo_3.split(" ")
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     self._process_choice(todo_list,
#                                          self.current_card.item_3,
#                                          self.current_card.next_card_3,
#                                          self.current_card.quest_accepted_3,
#                                          self.current_card.quest_reward_3)
#                     self.goto_next_card(self.current_card.index)
#                 else:
#                     self.user_text += event.unicode
#
#     def draw(self):
#         # -----------------------------------------
#         self.screen.fill(self.BG_COLOR)
#         # -----------------------------------------
#         utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
#                           height_offset=50, line_length=60,
#                           color=constants.BLACK)
#         # print(self.display_list)
#         # raise NotImplemented
#         pygame.display.flip()
#
#     def save_data(self):
#         self.player_inventory.save_data()
#         # self.quest_history.debug_print()
#         # raise NotImplemented
#         self.quest_history.save_data()
#
#     def main(self):
#         while self.keep_looping == True:
#             # self.clock.tick(constants.FRAME_RATE)
#             self.clock.tick(10)
#             self.handle_events()
#             self.draw()
#             # self.main_helper()
#         self.save_data()
#         # print("This is the player inventory at the end of Quest:")
#         # self.player_inventory.debug_print()
#         # raise NotImplemented
#         # self.player_inventory.debug_print()
#         # raise NotImplemented
#         return self.message, self.player_inventory

# -----------------------------------------------------------
#                      class Conversation
# -----------------------------------------------------------
class Conversation:
    def __init__(self, player_name,
                 npc_name, zone_name, map_name,
                 conversation_only=False):
        npc_name = npc_name.replace(" ", "_")
        # ----
        if utils.validate_player_name(player_name) == False:
            raise ValueError("Error!")
        if utils.is_a_valid_npc_name(player_name=player_name, npc_name=npc_name) == False:
            raise ValueError("This is not a valid npc_name: {}".format(npc_name))
        if not zone_name in constants.ZONE_NAMES:
            raise ValueError("Error!")
        if not map_name in constants.MAP_CHOICES:
            raise ValueError("Error!")
        # --------------------------------------
        self.conversation_only = conversation_only
        self.filepath = ""
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # self.display_choices = True
        self.message = ""
        # --------------------------------------
        self.quest_history = None
        # --------------------------------------
        self.player_name = player_name
        self.npc_name = npc_name
        self.zone_name = zone_name
        self.map_name = map_name
        # self.player_gold = player_gold
        # ----
        self.keep_looping = True
        self.stop_looping = False
        self.display_list = []
        self.text = ""
        self.user_text = ""
        # ----
        self.player_inventory = Inventory(player_name=player_name,
                                          npc_name=npc_name,
                                          character_type="player")
        self.npc_inventory = Inventory(player_name=player_name,
                                       npc_name=npc_name,
                                       character_type="npc")
        self.current_card_index = 0
        self.current_card = None
        # ----
        self.inner = []

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def read_data(self):
        # read quest history
        self.quest_history = MasterQuest(zone_name=self.zone_name,
                                         map_name=self.map_name,
                                         npc_name=self.npc_name)
        filepath = ""
        if self.quest_history.quest_completed == True:
            filename = "{}_conversation_completed.txt".format(self.npc_name)
            filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
                                    "conversations", filename)
        elif self.quest_history.quest_accepted == True:
            filename = "{}_conversation_accepted.txt".format(self.npc_name)
            filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
                                    "conversations", filename)
        elif self.quest_history.quest_completed == False and self.quest_history.quest_accepted == False:
            filename = "{}_conversation.txt".format(self.npc_name)
            filepath = os.path.join("data", "zones", self.zone_name, self.map_name,
                                    "conversations", filename)
        else:
            raise ValueError("Error")
        # ----
        if os.path.isfile(filepath) == False:
            s = "This isn't a valid filename: {}".format(filepath)
            raise ValueError(s)
        mylist = utils.read_data_file(filepath, num_of_fields=23)
        for mydict in mylist:
            myobject = ConversationCard(mydict)
            self.inner.append(myobject)
        # ----
        self.player_inventory.read_data()
        self.npc_inventory.read_data()
        self.current_card = self.get_card(self.current_card_index)
        # ----
        self.display_list = self.current_card.display_card_1()

    def get_card(self, index):
        for a_card in self.inner:
            if a_card.index == index:
                return a_card
        return None

    def debug_print(self):
        # print("Player's gold: {}".format(self.player_gold))
        for elem in self.inner:
            print("------------")
            elem.debug_print()
        print("============")

    def goto_next_card(self, card_index_number):
        print("going to next card: {}".format(card_index_number))
        self.current_card = self.get_card(card_index_number)
        if self.current_card is None:
            s = "card_index_number: {}".format(card_index_number)
            raise ValueError(s)
        # self.current_card.debug_print()
        # raise NotImplemented

    def _required_item_absent(self):
        self.display_list = []
        self.stop_looping = True
        mylist = ["{} frowns at you.".format(self.npc_name.title())]
        mylist.append(" ")
        # ----
        s = ""
        if self.quest_history.quest_area_number_of_success_items == 1:
            s = "We agreed that you would deliver a {}. Come back when you can."
            s = s.format(self.quest_history.quest_area_success_item)
        elif self.quest_history.quest_area_number_of_success_items > 1:
            s = "We agreed that you would deliver {} {}s. Come back when you can."
            s = s.format(self.quest_history.quest_area_number_of_success_items,
                         self.quest_history.quest_area_success_item)
        mylist.append(s)
        self.display_list = mylist

    def _give_player_reward(self):
        # is it gold or an item?
        if not self.quest_history.quest_reward_item is None:
            # if self.quest_history.quest_reward_item.find("gold") == -1:
            s = "The reward is an ITEM: {}. Adding the item to the player's inventory..."
            s = s.format(self.quest_history.quest_reward_item)
            print(s)
            # the reward is an ITEM
            reward_item = self.npc_inventory.get_item_by_name(self.quest_history.quest_reward_item)
            if reward_item is None:
                raise ValueError("Error")
            if self.quest_history.quest_reward_item_number is None:
                raise ValueError("Error")
            self.player_inventory.add_item_by_name(self.quest_history.quest_reward_item, self.quest_history.quest_reward_item_number)
        # ----
        if self.quest_history.quest_reward_gold > 0:
            # self.player_gold += self.quest_history.quest_reward_gold
            gold_coins = self.player_inventory.get_item_by_name("gold coin")
            if gold_coins is None: raise ValueError("Error")
            gold_coins.units += self.quest_history.quest_reward_gold
        elif self.quest_history.quest_reward_gold < 0:
            raise ValueError("Error")
        elif self.quest_history.quest_reward_gold == 0:
            pass
        else:
            raise ValueError("Error")

    def _sell(self, todo_list, item_name):
        if not item_name in constants.PROVISIONERS_GOODS:
            s = "I don't recognize this item name: {}".format(item_name)
            raise ValueError(s)
        if len(todo_list) != 2:
            # It should be of the form: buy 2 or sell 4
            if len(todo_list) == 1:
                s = "If the todo command is to BUY, it has to be of this form: Buy 4"
                raise ValueError(s)
            elif len(todo_list) > 2:
                s = "There are too many terms in this list. It should be of the form 'buy 3'"
                raise ValueError(s)
            else:
                raise ValueError("Error")
        if not utils.is_int(todo_list[1]):
            if not todo_list[1] in ["all", "All"]:
                s = "This is todo_list: {}\n".format(todo_list)
                s += "It should be of the form 'sell 4' or sell all"
                raise ValueError(s)
        # todo_list[1] = int(todo_list[1])
        # ----
        number_of_items = todo_list[1]
        if utils.is_int(number_of_items) == True:
            number_of_items = int(number_of_items)
        # print("number of items: {}".format(number_of_items))
        # raise NotImplemented
        if self.player_inventory.sell_item_by_name(item_name, number_of_items) == True:
            return True
        else:
            # Player does not have the item.
            return False

    def _process_choice(self, todo_list, item_name, next_card, quest_accepted, quest_reward):
        if (not utils.is_int(next_card)) and (not next_card is None):
            s = "This is next_card: {} ({})".format(next_card, type(next_card))
            raise ValueError(s)
        if not item_name is None:
            if not item_name in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
                print(constants.CONSUMABLE_NAMES)
                print(constants.WEAPON_NAMES)
                s = "I don't recognize this item_name: {}, ({}).".format(item_name, type(item_name))
                raise ValueError(s)
        print("todo_list: {}".format(todo_list))
        # I need to make sure that any integer in the list is
        # converted to a string.
        temp = utils.list_int_to_str(todo_list)
        temp = ' '.join(temp).lower()
        command = ""
        if todo_list[0] in ["sell", "buy"]:
            command = utils.only_alphabetical(temp)
        else:
            command = temp
        if not command in constants.CONVERSATION_COMMANDS:
            s = "I don't recognize this: {}".format(temp)
            raise ValueError(s)
        # ----
        print("def _process_choice: ", todo_list)
        print("command: {}".format(command))
        if command == "load next map":
            print("todo_string == load next map")
            self.message = command
            self.stop_looping = True
            # ---------------------------------------------------
        elif command == "take item":
            if item_name is None: raise ValueError("Error")
            if len(item_name) == 0: raise ValueError("Error")
            if self.player_inventory.add_item_by_name(item_name, 1) == False:
                raise ValueError("Error")
            if not next_card is None:
                self.goto_next_card(next_card)
        elif command == "buy":
            # the following is error checking.
            if not item_name in constants.PROVISIONERS_GOODS:
                s = "I don't recognize this item name: {}".format(item_name)
                raise ValueError(s)
            if len(todo_list) != 2:
                # It should be of the form: buy 2 or sell 4
                if len(todo_list) == 1:
                    s = "If the todo command is to BUY, it has to be of this form: Buy 4"
                    raise ValueError(s)
                if len(todo_list) > 2:
                    s = "There are too many terms in this list. It should be of the form 'buy 3'"
                    raise ValueError(s)
            if not utils.is_int(todo_list[1]):
                s = "This is todo_list: {}\n".format(todo_list)
                s += "It should be of the form 'buy 4'"
                raise ValueError(s)
            # ----
            self.player_inventory.buy_item_by_name(item_name=item_name,
                                                   number_of_items=int(todo_list[1]))
            if not next_card is None:
                self.goto_next_card(next_card)
        elif command == "sell":
            if self._sell(todo_list=todo_list, item_name=item_name) == False:
                s = "{} squints at you. 'Hey! what are you trying to pull! This isn't a {}. Go away!'"
                s = s.format(self.npc_name, item_name)
                self.display_list = [s]
                self.stop_looping = True
            if not next_card is None:
                self.goto_next_card(next_card)
        elif command == "sell all":
            if self._sell(todo_list=todo_list, item_name=item_name) == False:
                s = "{} squints at you. 'Hey! what are you trying to pull! This isn't a {}. Go away!'"
                s = s.format(self.npc_name, item_name)
                self.display_list = [s]
                self.stop_looping = True
            else:
                print("It seems to have worked!")
            if not next_card is None:
                self.goto_next_card(next_card)
        elif command == "end conversation":
            print("todo_list[0] == end and todo_list[1] == conversation")
            self.stop_looping = True
            self.message = "end conversation"
            if not item_name is None and len(item_name) > 0:
                print("NPC has given the command to end the conversation. item_name is NOT none.")
                print("The conversation will end, but there will also be a mildly negative outcome for the player.")
                print("The player will be given the indicated item.")
                print("In this case it is: {}".format(item_name).upper())
                self.player_inventory.add_item_by_name(item_name, 1)
                print("This is the message: {}".format(self.message))
            # ---------------------------------------------------
        elif command == "end game":
            print("todo_list[0] == end and todo_list[1] == game")
            self.stop_looping = True
            self.message = "end game"
            # ---------------------------------------------------
        elif command == "continue":
            print("todo_list[0] == continue")
            self.message = "continue"
            if not next_card is None:
                self.goto_next_card(next_card)
            # ---------------------------------------------------
        elif command == "accepted":
            print("todo_list[0] == accepted")
            # The quest has been accepted
            self.message = "accepted"
            self.stop_looping = True
            if not item_name is None and len(item_name) > 0:
                self.player_inventory.add_item_by_name(item_name, 1)
                print("{} was added to the player's inventory".format(item_name))
            self.quest_history.reward_offered = quest_reward
            self.quest_history.quest_accepted = True
            self.quest_history.result_of_conversation = "accepted"
            # ---------------------------------------------------
        elif command == "completed":
            self.message = "completed"
            self.stop_looping = True
            self.quest_history.quest_completed = True
            if not item_name is None:
                self.player_inventory.add_item_by_name(item_name, 1)
            # ----
            if self.conversation_only == True:
                # Since this is only a conversation, we don't care about rewards or items.
                return True
            # Check to see that the quest really has been completed.
            # That is, check to make sure that the player has the
            # required item(s) in the inventory.
            required_item = self.player_inventory.get_item_by_name(self.quest_history.quest_area_success_item)
            if required_item is None:
                self._required_item_absent()
                self.quest_history.quest_completed = False
                return False
            if required_item.units < self.quest_history.quest_area_number_of_success_items:
                self._required_item_absent()
                self.quest_history.quest_completed = False
                return False
            # The items need to be removed from the player's inventory.from
            if self.player_inventory.remove_item_by_name(self.quest_history.quest_area_success_item,
                                                         self.quest_history.quest_area_number_of_success_items) == False:
                raise ValueError("Error")
            self._give_player_reward()
            # ---------------------------------------------------
        else:
            raise ValueError("Error! I don't recognize this: -{}- ({})".format(command, type(command)))
        print("This is the last line of def _process_choice")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                # self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print("in handle_events self.stop_looping = {}".format(self.stop_looping))
                    print("in handle_events self.keep_looping = {}".format(self.keep_looping))
                    if self.stop_looping == True:
                        self.keep_looping = False
                    else:
                        self.display_list = self.current_card.display_card_1()
                elif event.key == pygame.K_1:
                    if self.stop_looping == True: return False
                    self.display_choices = False
                    # ----
                    self.display_list += self.current_card.display_card_2(user_choice=1,
                                                                         player_inventory=self.player_inventory,
                                                                         npc_inventory=self.npc_inventory)
                    if self.current_card.todo_1 is None:
                        raise ValueError("Error")
                    todo_list = self.current_card.todo_1.split(" ")
                    todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
                    mylist = []
                    for elem in todo_list:
                        if utils.is_int(elem) == True:
                            mylist.append(int(elem))
                        else:
                            mylist.append(elem)
                    todo_list = mylist
                    # ----
                    self._process_choice(todo_list,
                                         self.current_card.item_1,
                                         self.current_card.next_card_1,
                                         self.current_card.quest_accepted_1,
                                         self.current_card.quest_reward_1)
                    self.goto_next_card(self.current_card.index)
                elif event.key == pygame.K_2:
                    if self.stop_looping == True: return False
                    self.display_choices = False
                    # ----
                    # print("here is self.display_list:", self.display_list)
                    self.display_list += self.current_card.display_card_2(user_choice=2,
                                                                         player_inventory=self.player_inventory,
                                                                         npc_inventory=self.npc_inventory)
                    if self.current_card.todo_2 is None:
                        raise ValueError("Error")
                    todo_list = self.current_card.todo_2.split(" ")
                    todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
                    it_worked = self._process_choice(todo_list,
                                         self.current_card.item_2,
                                         self.current_card.next_card_2,
                                         self.current_card.quest_accepted_2,
                                         self.current_card.quest_reward_2)
                    self.goto_next_card(self.current_card.index)
                    # print("---- self.player_inventory ----")
                    # self.player_inventory.debug_print()
                    # print("-------------------------------")
                elif event.key == pygame.K_3:
                    if self.stop_looping == True: return False
                    self.display_choices = False
                    self.display_list += self.current_card.display_card_2(user_choice=3,
                                                                         player_inventory=self.player_inventory,
                                                                         npc_inventory=self.npc_inventory)
                    if self.current_card.todo_3 is None:
                        raise ValueError("Error")
                    todo_list = self.current_card.todo_3.split(" ")
                    todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
                    self._process_choice(todo_list,
                                         self.current_card.item_3,
                                         self.current_card.next_card_3,
                                         self.current_card.quest_accepted_3,
                                         self.current_card.quest_reward_3)
                    self.goto_next_card(self.current_card.index)
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=50, line_length=60,
                          color=constants.BLACK)
        pygame.display.flip()

    def save_data(self):
        self.player_inventory.save_data()
        # self.quest_history.debug_print()
        # raise NotImplemented
        self.quest_history.save_data()

    def main(self):
        while self.keep_looping == True:
            # self.clock.tick(constants.FRAME_RATE)
            self.clock.tick(10)
            self.handle_events()
            self.draw()
        self.save_data()
        return self.message, self.player_inventory

# -----------------------------------------------------------
#                      class Card
# -----------------------------------------------------------
class Card:
    def __init__(self, mydict):
        raise NotImplemented
        self.index = mydict["index"]
        self.prompt = mydict["prompt"]
        self.choice_1 = mydict["choice_1"]
        self.choice_2 = mydict["choice_2"]
        self.choice_3 = mydict["choice_3"]
        self.response_1 = mydict["response_1"]
        self.response_2 = mydict["response_2"]
        self.response_3 = mydict["response_3"]
        self.todo_1 = mydict["todo_1"].lower().strip()
        self.todo_2 = mydict["todo_2"].lower().strip()
        self.todo_3 = mydict["todo_3"].lower().strip()
        if self.todo_1 == "none": self.todo_1 = None
        if self.todo_2 == "none": self.todo_2 = None
        if self.todo_3 == "none": self.todo_3 = None
        self.item_1 = mydict["item_1"]
        self.item_2 = mydict["item_2"]
        self.item_3 = mydict["item_3"]
        if not utils.is_int(self.item_1): self.item_1.lower().strip()
        if not utils.is_int(self.item_2): self.item_2.lower().strip()
        if not utils.is_int(self.item_3): self.item_3.lower().strip()
        self.next_card_1 = mydict["next_card_1"]
        self.next_card_2 = mydict["next_card_2"]
        self.next_card_3 = mydict["next_card_3"]
        if self.next_card_1 == "none": self.next_card_1 = None
        if self.next_card_2 == "none": self.next_card_2 = None
        if self.next_card_3 == "none": self.next_card_3 = None
        # ----
        if self.item_1.lower().strip() == "none": self.item_1 = None
        if self.item_2.lower().strip() == "none": self.item_2 = None
        if self.item_3.lower().strip() == "none": self.item_3 = None
        # ----
        if self.is_a_valid_item(self.item_1) == False:
            s = "Error! item_1 = {} ({})".format(self.item_1, type(self.item_1))
            raise ValueError(s)
        if self.is_a_valid_item(self.item_2) == False: raise ValueError("Error! item_2 = {}".format(self.item_2))
        if self.is_a_valid_item(self.item_3) == False: raise ValueError("Error! item_3 = {}".format(self.item_3))
        # ----

    def is_a_valid_item(self, this_item):
        if this_item is None: return True
        if this_item in constants.CONSUMABLE_NAMES: return True
        if this_item in constants.WEAPON_NAMES: return True
        if utils.is_int(this_item) == True: return True
        return False

    def debug_print(self):
        print("index: {}".format(self.index))
        print("prompt: {}".format(self.prompt))
        print("choice_1: {}".format(self.choice_1))
        print("choice_2: {}".format(self.choice_2))
        print("choice_3: {}".format(self.choice_3))
        print("response_1: {}".format(self.response_1))
        print("response_2: {}".format(self.response_2))
        print("response_3: {}".format(self.response_3))
        print("todo_1: {}".format(self.todo_1))
        print("todo_2: {}".format(self.todo_2))
        print("todo_3: {}".format(self.todo_3))
        print("item_1: {}".format(self.item_1))
        print("item_2: {}".format(self.item_2))
        print("item_3: {}".format(self.item_3))
        print("next_card_1: {}".format(self.next_card_1))
        print("next_card_2: {}".format(self.next_card_2))
        print("next_card_3: {}".format(self.next_card_3))

# -----------------------------------------------------------
#                      class Conversation
# -----------------------------------------------------------
# class Conversation:
#     def __init__(self, player_name, npc_name, zone_name, map_name, player_gold):
#         if utils.validate_player_name(player_name) == False:
#             raise ValueError("Error!")
#         if utils.is_a_valid_npc_name(player_name=player_name, npc_name=npc_name) == False:
#             raise ValueError("This is not a valid npc_name: {}".format(npc_name))
#         if not zone_name in constants.ZONE_NAMES:
#             raise ValueError("Error!")
#         if not map_name in constants.MAP_CHOICES:
#             raise ValueError("Error!")
#         if utils.is_int(player_gold) == False:
#             raise ValueError("Error!")
#         # --------------------------------------
#         self.init_pygame()
#         self.all_sprites = pygame.sprite.Group()
#         # self.display_choices = True
#         self.message = ""
#         # --------------------------------------
#         self.player_name = player_name
#         self.npc_name = npc_name
#         self.zone_name = zone_name
#         self.map_name = map_name
#         self.player_gold = player_gold
#         # ----
#         self.keep_looping = True
#         self.stop_looping = False
#         self.display_list = []
#         self.text = ""
#         self.user_text = ""
#         # ----
#         self.player_inventory = Inventory(player_name=player_name,
#                                           npc_name= npc_name,
#                                           character_type="player")
#         self.npc_inventory = Inventory(player_name=player_name,
#                                        npc_name=npc_name,
#                                        character_type="npc")
#         self.current_card_index = 0
#         self.current_card = None
#         # ----
#         self.inner = []
#
#     def init_pygame(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
#         pygame.display.set_caption("{}".format(constants.TITLE))
#         self.clock = pygame.time.Clock()
#         self.BG_COLOR = constants.WHITE
#         self.font = pygame.font.Font(None, 35)
#
#     def read_data(self):
#         filename = "{}.txt".format(self.npc_name.replace(" ", "_"))
#         filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", filename)
#         mylist = utils.read_data_file(filepath, num_of_fields=17)
#         for mydict in mylist:
#             myobject = Card(mydict)
#             self.inner.append(myobject)
#         # ----
#         self.player_inventory.read_data()
#         # self.player_inventory.debug_print()
#         self.npc_inventory.read_data()
#         # self.npc_inventory.debug_print()
#         self.current_card = self.get_card(self.current_card_index)
#         # self.current_card.debug_print()
#         # ----
#         self.display_list.append(self.current_card.prompt)
#         self.display_list.append(" ")
#         self.display_list.append(" ")
#         self.display_list.append("1) {}".format(self.current_card.choice_1))
#         self.display_list.append("2) {}".format(self.current_card.choice_2))
#         self.display_list.append("3) {}".format(self.current_card.choice_3))
#         self.display_list.append(" ")
#         self.display_list.append("Press 1, 2 or 3 to continue.")
#         # ----
#         # The following is only for DEBUGGING
#         # self.player_inventory.add_item_by_name("wild strawberries", 1)
#         # self.player_inventory.add_item_by_name("rusty sword", 1)
#
#     def get_card(self, index):
#         for a_card in self.inner:
#             if a_card.index == index:
#                 return a_card
#         return None
#
#     def debug_print(self):
#         print("Player's gold: {}".format(self.player_gold))
#         for elem in self.inner:
#             print("------------")
#             elem.debug_print()
#         print("============")
#
#     def goto_next_card(self, card_index_number):
#         print("going to next card: {}".format(card_index_number))
#         self.current_card = self.get_card(card_index_number)
#         if self.current_card is None:
#             raise ValueError("Error!")
#
#     def player_buys_item(self, item_name, number_of_items):
#         # print("number_of_items: {} ({})".format(number_of_items, type(number_of_items)))
#         # raise NotImplemented
#         if item_name is None:
#             s = "item_name is None"
#             raise ValueError(s)
#         if len(item_name) == 0:
#             raise ValueError("item_name is 0")
#         the_cost = 0
#         this_item = self.npc_inventory.get_item_by_name(item_name)
#         if this_item is None:
#             s = "this item ({}) was None".format(item_name)
#             raise ValueError(s)
#         if number_of_items > 0:
#             the_cost = number_of_items * this_item.cost
#             # print("{} * {}".format(number_of_items, this_item.cost))
#             # raise NotImplemented
#         else:
#             the_cost = this_item.cost
#         # ----
#         if self.player_gold < the_cost:
#             print("Doh! You don't have enough gold to buy this: {}".format(item_name))
#             print("You have {} gold, but the item costs {} gold.".format(self.player_gold, this_item.cost))
#             self.display_list = []
#             self.display_list.append("Oh. It looks as though you can't afford that.")
#             self.display_list.append("Perhaps you should come back later.")
#             self.display_list.append(" ")
#             self.display_list.append("Press <Return>")
#             self.stop_looping = True
#             # self.goto_next_card(1)
#             # self.current_card = self.get_card(1)
#             # if self.current_card is None:
#             #     raise ValueError("Error!")
#         else:
#             self.player_gold -= the_cost
#             self.player_inventory.add_item_by_name(item_name=item_name, number_of_items=number_of_items)
#             print("You successfully bought {} and added it to your inventory.".format(item_name.upper()))
#             # self.goto_next_card(1)
#
#     def player_sells_item(self, item_name):
#         """Player sells item to NPC."""
#         raise NotImplemented
#         this_item = self.player_inventory.get_item_by_name(item_name)
#         if this_item is None:
#             s = "Doh! It looks like you don't have any {}. Which means you can't sell me any!".format(item_name)
#             print(s)
#             self.current_card = self.get_card(5)
#             return False
#         it_worked = self.player_inventory.remove_item_by_name(item_name=this_item.name, number_of_items=1)
#         self.player_gold += this_item.cost
#         if it_worked == False: raise ValueError("Error!")
#         self.current_card = self.get_card(1)
#
#     def _process_choice(self, todo_list, item_name, next_card):
#         number_of_items = 0
#         if not utils.is_int(next_card) and not next_card is None:
#             next_card = None if next_card.lower().strip() == "none" else next_card
#         if not utils.is_int(next_card) and not next_card is None:
#             s = "This is next_card: {} ({})".format(next_card, type(next_card))
#             raise ValueError(s)
#         # if not next_card in [1, 2, 3,  "1", "2", "3", None]:
#         #     print("This is next_card: {}".format(next_card))
#         #     raise ValueError("Error")
#         # ----
#         # item_name = "{} {}".format(todo_list[1], todo_list[2])
#         print("def _process_choice: ", todo_list)
#         todo_string = ""
#         if len(todo_list) == 3:
#             todo_string = "{} {} {}".format(todo_list[0], todo_list[1], todo_list[2])
#             print(todo_string)
#             number_of_items = int(todo_list[2])
#         if todo_string == "load next map":
#             self.message = todo_string
#             self.stop_looping = True
#             # if next_card is None: raise ValueError("Error")
#             # print("Going to next card: {}".format(next_card))
#             # self.goto_next_card(next_card)
#         elif todo_list[0] == "end" and todo_list[1] == "conversation":
#             self.stop_looping = True
#             self.message = "end conversation"
#             if not item_name is None and len(item_name) > 0:
#                 print("NPC has given the command to end the conversation. item_name is NOT none.")
#                 print("The conversation will end, but there will also be a mildly negative outcome for the player.")
#                 print("The player will be given the indicated item.")
#                 print("In this case it is: {}".format(item_name).upper())
#                 self.player_inventory.add_item_by_name(item_name, 1)
#                 print("This is the message: {}".format(self.message))
#         elif todo_list[0] == "end" and todo_list[1] == "game":
#             if not item_name is None:
#                 self.stop_looping = True
#                 self.message = "end game"
#         elif todo_list[0] == "buy":
#             self.player_buys_item(item_name, number_of_items)
#             print("You have just bought {}".format(item_name.upper()))
#             print("next_card is: {}".format(next_card))
#             if not next_card is None:
#                 print("This is next_card: {}".format(next_card))
#                 self.goto_next_card(next_card)
#         elif todo_list[0] == "sell":
#             self.player_sells_item(item_name)
#             if not next_card is None:
#                 self.goto_next_card(next_card)
#         elif todo_list[0] == "continue":
#             self.message = "continue"
#             if not next_card is None:
#                 self.goto_next_card(next_card)
#         elif todo_list[0] == "completed":
#             self.message = "completed"
#             self.stop_looping = True
#             print("self.message = completed")
#             if not item_name is None and len(item_name) > 0:
#                 self.player_inventory.add_item_by_name(item_name, 1)
#                 print("{} was added to the player's inventory".format(item_name))
#                 print("This is the message: {}".format(self.message))
#             # ----
#             # s = "conversation with {} completed".format(self.npc_name).replace(" ", "_")
#             # filepath = os.path.join("data", "zones", self.zone_name, self.map_name, "texts", "event_record.txt")
#             # mydict = utils.read_file(filepath)[0]
#             # mydict[s] = True
#             # with open(filepath, "w") as f:
#             #     for key, value in mydict.items():
#             #         s = "{}: {}\n".format(key, value)
#             #         f.write(s)
#         else:
#             raise ValueError("Error! I don't recognize this: {}".format(todo_list[0]))
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.keep_looping = False
#             elif event.type == pygame.KEYDOWN:
#                 # self.text_background_color = constants.LIGHTGREY
#                 if event.key == pygame.K_ESCAPE:
#                     self.keep_looping = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     self.user_text = self.user_text[:-1]
#                 elif event.key == pygame.K_RETURN:
#                     print("in handle_events self.stop_looping = {}".format(self.stop_looping))
#                     print("in handle_events self.keep_looping = {}".format(self.keep_looping))
#                     if self.stop_looping == True:
#                         self.keep_looping = False
#                     else:
#                         self.display_list = []
#                         self.display_list.append(self.current_card.prompt)
#                         self.display_list.append(" ")
#                         self.display_list.append("1) {}".format(self.current_card.choice_1))
#                         self.display_list.append("2) {}".format(self.current_card.choice_2))
#                         self.display_list.append("3) {}".format(self.current_card.choice_3))
#                         self.display_list.append(" ")
#                         self.display_list.append("Press 1, 2 or 3 to continue.")
#                 elif event.key == pygame.K_1:
#                     if self.stop_looping == True: return False
#                     self.display_choices = False
#                     self.display_list = []
#                     self.display_list.append(self.current_card.choice_1)
#                     self.display_list.append(" ")
#                     self.display_list.append(self.current_card.response_1)
#                     self.display_list.append(" ")
#                     self.display_list.append("Press <Enter> to continue.")
#                     # print(self.current_card.response_1)
#                     # ----
#                     if self.current_card.todo_1 is None:
#                         print("todo_1 is None")
#                         self.goto_next_card(self.current_card.next_card_1)
#                         return True
#                     print("current_card.todo_1: {}".format(self.current_card.todo_1))
#                     # ----
#                     # At this point we know that todo_2 is a two or three word command.
#                     todo_list = self.current_card.todo_1.split(" ")
#                     # print("todo_list: {}".format(todo_list))
#                     # raise NotImplemented
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     # print("todo_list: {}".format(todo_list))
#                     # raise NotImplemented
#                     print(todo_list)
#                     self._process_choice(todo_list, self.current_card.item_1,
#                                          self.current_card.next_card_1)
#                 elif event.key == pygame.K_2:
#                     if self.stop_looping == True: return False
#                     self.display_choices = False
#                     # print(self.current_card.response_2)
#                     self.display_list = []
#                     self.display_list.append(self.current_card.choice_2)
#                     self.display_list.append(" ")
#                     self.display_list.append(self.current_card.response_2)
#                     self.display_list.append(" ")
#                     self.display_list.append("Press <Enter> to continue.")
#                     # ----
#                     if self.current_card.todo_2 is None:
#                         print("todo_2 is None")
#                         self.goto_next_card(self.current_card.next_card_2)
#                         return True
#                     print("current_card.todo_2: {}".format(self.current_card.todo_2))
#                     # ----
#                     # At this point we know that todo_2 is a three word command.
#                     todo_list = self.current_card.todo_2.split(" ")
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     # Checking for 'end conversation'
#                     self._process_choice(todo_list, self.current_card.item_2,
#                                          self.current_card.next_card_2)
#                 elif event.key == pygame.K_3:
#                     if self.stop_looping == True: return False
#                     # print(self.current_card.response_3)
#                     self.display_list = []
#                     self.display_list.append(self.current_card.choice_3)
#                     self.display_list.append(" ")
#                     self.display_list.append(self.current_card.response_3)
#                     self.display_list.append(" ")
#                     self.display_list.append("Press <Enter> to continue.")
#                     # self.display_list = self.current_card.response_3
#                     # ----
#                     if self.current_card.todo_3 is None:
#                         print("todo_3 is None")
#                         self.goto_next_card(self.current_card.next_card_3)
#                         return True
#                     print("current_card.todo_3: {}".format(self.current_card.todo_3))
#                     # ----
#                     # At this point we know that todo_3 is a three word command.
#                     todo_list = self.current_card.todo_3.split(" ")
#                     todo_list = [i.strip().lower() for i in todo_list if len(i.strip()) > 0]
#                     self._process_choice(todo_list, self.current_card.item_3,
#                                          self.current_card.next_card_3)
#                 else:
#                     self.user_text += event.unicode
#
#     def draw(self):
#         # -----------------------------------------
#         self.screen.fill(self.BG_COLOR)
#         # -----------------------------------------
#         utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
#                           height_offset=50, line_length=60,
#                           color=constants.BLACK)
#         pygame.display.flip()
#
#     def save_data(self):
#         self.player_inventory.save_data()
#
#     def main(self):
#         while self.keep_looping == True:
#             # self.clock.tick(constants.FRAME_RATE)
#             self.clock.tick(10)
#             self.handle_events()
#             self.draw()
#             # self.main_helper()
#         self.save_data()
#         return self.message, self.player_inventory, self.player_gold

# -----------------------------------------------------------
#                      class Inventory
# -----------------------------------------------------------

class Inventory:
    def __init__(self, player_name, npc_name, character_type="npc"):
        if utils.validate_player_name(player_name) == False:
            raise ValueError("Error! {} is not a valid player name.".format(player_name))
        if utils.is_a_valid_npc_name(player_name, npc_name) == False:
            raise ValueError("Error! {} is not a valid NPC name.".format(npc_name))
        if not character_type in constants.CHARACTER_TYPES:
            raise ValueError("Error!")
        # ----
        self.player_name = player_name
        self.npc_name = npc_name
        self.character_type = character_type
        # ----
        self.consumables = Consumables(player_name=self.player_name,
                                       npc_name=self.npc_name,
                                       character_type=self.character_type)
        self.weapons = Weapons(player_name=self.player_name,
                               npc_name=self.npc_name,
                               character_type=self.character_type)

    def read_data(self):
        self.consumables.read_data()
        self.weapons.read_data()

    def get_item_by_name(self, item_name):
        if item_name is None:
            s = "item_name is None"
            raise ValueError(s)
        if len(item_name) == 0:
            raise ValueError("Error")
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            s = "{} is neither a weapon nor a consumable.".format(item_name)
            raise ValueError(s)
        # ----
        if item_name in constants.CONSUMABLE_NAMES:
            an_item = self.consumables.get_item_by_name(item_name)
            if not an_item is None:
                return an_item
        elif item_name in constants.WEAPON_NAMES:
            an_item = self.weapons.get_item_by_name(item_name)
            if not an_item is None:
                return an_item
        # ----
        # debugging
        # self.consumables.debug_print()
        print("{} is neither a consumable nor a weapon".format(item_name))
        return None

    def add_item_by_name(self, item_name, number_of_items):
        if type(item_name) != type("abc"):
            s = "This {}\nshould be of type string, but it is of type {}."
            s = s.format(item_name, type(item_name))
            raise ValueError(s)
        if number_of_items < 0:
            raise ValueError("Error!")
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            raise ValueError("Error")
        # ----
        print("Adding {} items with the item_name: {}".format(number_of_items, item_name))
        if item_name in constants.CONSUMABLE_NAMES:
            self.consumables.add_item_by_name(item_name, number_of_items)
        elif item_name in constants.WEAPON_NAMES:
            self.weapons.add_item_by_name(item_name, number_of_items)
        else:
            s = "Error! I don't recognize this item_name: {}\n".format(item_name)
            s += "Perhaps you forgot to include the item_name in the list of CONSUMABLE_NAMES or WEAPON_NAMES."
            raise ValueError(s)

    def add_item_by_name_for_dialog(self, item_name, number_of_items):
        """This is exactly like "add_item_by_name but it doesn't
           stop the execution of the program."""
        if number_of_items <= 0:
            return False
        if item_name in constants.CONSUMABLE_NAMES:
            self.consumables.add_item_by_name(item_name, number_of_items)
            return True
        elif item_name in constants.WEAPON_NAMES:
            self.weapons.add_item_by_name(item_name, number_of_items)
            return True
        else:
            return False

    def sell_item_by_name(self, item_name, number_of_items):
        """This function will not sell the item TO any other
        character. This function will look at the value of the item and then
        'pay' the character for those items. The items are then
        taken from the inventory."""
        # ----
        if number_of_items in ["all", "All"]:
            # Get the number of items the inventory has of that item.
            # Replace "all" with the specific number of items.
            the_item = self.get_item_by_name(item_name)
            # print("the_item: ")
            # the_item.debug_print()
            # raise NotImplemented
            if the_item is None:
                s = "I (the inventory) do not contain this item: {}".format(item_name)
                print(s)
                return False
            number_of_items = the_item.units
        # ----
        gold_coins = self.weapons.get_item_by_name("gold coin")
        if gold_coins is None: raise ValueError("Error")
        # ----
        try:
            if number_of_items <= 0: return False
        except Exception as e:
            s = "number_of_items: {}".format(number_of_items)
            t = "{}\n{}".format(e, s)
            raise ValueError(t)
        if item_name in constants.CONSUMABLE_NAMES:
            # print("item name: {}".format(item_name))
            # print("number of items: {}".format(number_of_items))
            # raise NotImplemented
            if self.consumables.sell_item_by_name(item_name, number_of_items, gold_coins) == False:
                return False
            else: return True
        elif item_name in constants.WEAPON_NAMES:
            self.weapons.sell_item_by_name(item_name, number_of_items)
            return True
        else:
            return False

    def buy_item_by_name(self, item_name, number_of_items):
        """This function will not buy the item FROM any other
        character. This function will look at the value of the item and then
        subtract that amount of money from the player's inventory. The items
        are then placed in the inventory."""
        if number_of_items <= 0: return False
        # ----
        gold_coins = self.weapons.get_item_by_name("gold coin")
        if gold_coins is None: raise ValueError("Error")
        # ----
        if item_name in constants.CONSUMABLE_NAMES:
            self.consumables.buy_item_by_name(item_name, number_of_items, gold_coins)
            return True
        elif item_name in constants.WEAPON_NAMES:
            self.weapons.buy_item_by_name(item_name, number_of_items)
            return True
        else:
            return False

    def remove_item_by_name(self, item_name, number_of_items):
        if not utils.is_int(number_of_items):
            raise ValueError("Error!")
        if number_of_items < 0:
            raise ValueError("Error!")
        if type(item_name) != type("abc"):
            raise ValueError("Error!")
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            s = "Error! item_name ({}) is neither a CONSUMABLE or a WEAPON\n".format(item_name)
            s += "consumables: {}\n".format(constants.CONSUMABLE_NAMES)
            s += "weapons: {}\n".format(constants.WEAPON_NAMES)
            raise ValueError(s)
        # ----
        if number_of_items == 0:
            print("number_of_items == 0")
            return True
        # ----
        if self.consumables.remove_item_by_name(item_name, number_of_items) == True:
            print("consumable removed")
            return True
        if self.weapons.remove_item_by_name(item_name, number_of_items) == True:
            print("consumable removed")
            return True
        return False

    def remove_item_by_name_for_dialog(self, item_name, number_of_items):
        """This is for when a person is typing things in. Mistakes happen.
           I don't want to end the program, just indicate that a mistake,
           possibly a simple spelling mistke, occurred."""
        if not utils.is_int(number_of_items):
            return False
        if number_of_items < 0:
            return False
        if type(item_name) != type("abc"):
            return False
        if not item_name in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
            # s = "Error! item_name ({}) is neither a CONSUMABLE or a WEAPON\n".format(item_name)
            # s += "consumables: {}\n".format(constants.CONSUMABLE_NAMES)
            # s += "weapons: {}\n".format(constants.WEAPON_NAMES)
            return False
        # ----
        if number_of_items == 0: return True
        # ----
        if self.consumables.remove_item_by_name(item_name, number_of_items) == True:
            return True
        if self.weapons.remove_item_by_name(item_name, number_of_items) == True:
            return True
        return False

    # --------------------------------------------

    def display_list(self):
        consumables_list = self.consumables.display_list()
        weapons_list = self.weapons.display_list()
        return consumables_list + weapons_list

    def display_string(self):
        if self.character_type == "player":
            consumables_list = self.consumables.display_string()
            weapons_list = self.weapons.display_string()
            inventory_list = consumables_list + weapons_list
            # ret_list = utils.format_inventory_list(inventory_list)
            return inventory_list
        elif self.character_type == "npc":
            consumables_list = self.consumables.display_string()
            weapons_list = self.weapons.display_string()
            inventory_list = consumables_list + weapons_list
            # ret_list = utils.format_inventory_list(inventory_list)
            return inventory_list
        else:
            raise ValueError("Error!")

    # def display_string(self):
    #     s = "I split this into two, one gives a list one a string. Use:\n"
    #     s += "DISPLAY_STRING or DISPLAY_LIST"
    #     raise ValueError(s)

    def display_string_text(self):
        raise NotImplemented
        print("In display string text: ")
        consumables_list = self.consumables.display_string_text()
        print(consumables_list)
        weapons_list = self.weapons.display_string()
        inventory_list = consumables_list + weapons_list
        ret_list = utils.format_inventory_list(inventory_list)
        return ret_list

    def debug_print_names(self):
        self.consumables.debug_print_names()
        self.weapons.debug_print_names()

    def debug_print(self):
        print("============= Inventory.debug_print() =============")
        print("{} || {} --> character_type: {}".format(self.player_name, self.npc_name, self.character_type))
        self.consumables.debug_print()
        self.weapons.debug_print()
        print("===================================================")

    def save_data(self):
        """
        The only place we will ever want to save is to the player's file.
        Right now we are adjusting the food, drink, weapon, etc., files
        manually. SO all we do
        :return: None
        """
        print("------------------------------------------------")
        # self.consumables.debug_print()
        print("**** BEFORE save data ****")
        # ----
        self.consumables.save_data()
        self.weapons.save_data()
        # ----
        print("**** AFTER save data ****")
        # self.consumables.debug_print()
        # print("Leaving class Conversation")
        print("------------------------------------------------")

    def __len__(self):
        mylen = len(self.consumables)
        mylen += len(self.weapons)
        return mylen

# ==============================================

# def debug_conversation():
#     player_name = "henry"
#     # npc_name = "brent"
#     npc_name = "alfred"
#     # npc_name = "laura"
#     # zone_name = "the_orchard"
#     zone_name = "provisioner"
#     map_name = "map00"
#     player_gold = 20
#     myobject = Conversation(player_name, npc_name, zone_name, map_name, player_gold)
#     myobject.read_data()
#     message, player_inventory, player_gold = myobject.main()
#     print("*****************************")
#     print("message: {}".format(message))
#     # print("*****************************")
#     # print("Player's Inventory:")
#     # player_inventory.debug_print()
#     # print("*****************************")
#     # print("PLayer's Gold: {}".format(player_gold))

def debug_inventory_buy_a_consumable(player_name, npc_name):
    print("This is {}'s inventory".format(player_name))
    myinventory = Inventory(player_name=player_name, npc_name=npc_name, character_type="player")
    myinventory.read_data()
    s = myinventory.display_string()
    gold_coins = myinventory.weapons.get_item_by_name("gold coin")
    gold_coins.debug_print()
    print(s)
    print("************************************")
    myinventory.buy_item_by_name(item_name="spoiled wine",
                                 number_of_items=10)
    # ----
    mylist = myinventory.display_string()
    gold_coins = myinventory.weapons.get_item_by_name("gold coin")
    gold_coins.debug_print()
    [print(i) for i in mylist]

def debug_inventory_sell_a_consumable(player_name, npc_name):
    print("This is {}'s inventory".format(player_name))
    myinventory = Inventory(player_name=player_name, npc_name=npc_name, character_type="player")
    myinventory.read_data()
    s = myinventory.display_string()
    gold_coins = myinventory.weapons.get_item_by_name("gold coin")
    gold_coins.debug_print()
    print(s)
    print("************************************")
    # ----SPOILED WINE
    item_name = "soupy stew"
    # item_name = "tough jerky"
    # item_name = "spoiled wine"
    number_of_items = "all"
    if myinventory.sell_item_by_name(item_name, number_of_items) == False:
        s = "Doh! I was not able to sell {} because I do not have any!".format(item_name.upper())
        raise ValueError(s)
    # ----
    mylist = myinventory.display_string()
    gold_coins = myinventory.weapons.get_item_by_name("gold coin")
    gold_coins.debug_print()
    [print(i) for i in mylist]

def debug_inventory(player_name, npc_name):
    print("This is {}'s inventory".format(player_name))
    myinventory = Inventory(player_name=player_name, npc_name=npc_name, character_type="player")
    myinventory.read_data()
    # ----
    mylist = myinventory.display_string()
    [print(i) for i in mylist]
    print("===============")
    print("This is {}'s inventory".format(npc_name))
    myinventory = Inventory(player_name=player_name, npc_name=npc_name, character_type="npc")
    myinventory.read_data()
    # ----
    mylist = myinventory.display_string()
    [print(i) for i in mylist]

def reset_conversation(npc_name, zone_name, map_name):
    filename = "{}_history.txt".format(npc_name)
    filepath = os.path.join("data", "zones", zone_name, map_name, "conversations", filename)
    if os.path.isfile(filepath) == False:
        s = "This is not a directory: {}".format(filepath)
        raise ValueError(s)
    # ----
    mydict = utils.read_file(filepath)[0]
    mydict["quest_accepted"] = False
    mydict["quest_completed"] = False
    s = ""
    for key, value in mydict.items():
        s += "{}: {}\n".format(key, value)
    # filepath = os.path.join("data", "testing.txt")
    # if os.path.isfile(filepath) == False:
    #     raise ValueError("Error")
    with open(filepath, "w") as f:
        f.write(s)

def debug_conversation():
    # zone_name = "jeweler"
    # zone_name = "provisioner"
    zone_name = "swindon_pub"
    map_name = "map00"
    player_name = "henry"
    # npc_name = "matilda"
    # npc_name = "alfred"
    # npc_name = "alfred"
    # npc_name = "bertron"
    npc_name = "aiza"
    # player_gold = 20
    # ----
    # quest_history = QuestHistory(npc_name, zone_name, map_name)
    # get_conversation_filepath = quest_history.get_filepath(zone_name=zone_name, map_name=map_name)
    # ----
    myconversation = Conversation_NEW(player_name, npc_name, zone_name, map_name)
    myconversation.read_data()
    # myobject.debug_print()
    message, player_inventory = myconversation.main()
    # set the result of the interaction in the quests.txt file.
    print("message: {}".format(message))
    gold_coins = player_inventory.get_item_by_name("gold_coin")
    if gold_coins is None: raise ValueError("Error")
    print("player_gold: {}".format(gold_coins.units))

def debug_quest_card():
    index = 0
    prompt = "This is the prompt"
    choice_1 = "this is choice 1"
    choice_2 = "this is choice 2"
    choice_3 = "this is choice 3"
    response_1 = "this is response 1"
    response_2 = "this is response 2"
    response_3 = "this is response 3"
    todo_1 = "this is todo 1"
    todo_2 = "this is todo 2"
    todo_3 = "this is todo 3"
    item_1 = "dry bread"
    item_2 = "tough jerky"
    item_3 = "normal sword"
    next_card_1 = 1
    next_card_2 = 1
    next_card_3 = 1
    quest_accepted_1 = "none"
    quest_accepted_2 = "none"
    quest_accepted_3 = "none"
    quest_reward_1 = "none"
    quest_reward_2 = "none"
    quest_reward_3 = "none"
    mydict1 = {}
    mydict1["index"] = index
    mydict1["prompt"] = "This is the first prompt."
    mydict1["choice_1"] = choice_1
    mydict1["choice_2"] = choice_2
    mydict1["choice_3"] = choice_3
    mydict1["response_1"] = response_1
    mydict1["response_2"] = response_2
    mydict1["response_3"] = response_3
    mydict1["todo_1"] = todo_1
    mydict1["todo_2"] = todo_2
    mydict1["todo_3"] = todo_3
    mydict1["item_1"] = item_1
    mydict1["item_2"] = item_2
    mydict1["item_3"] = item_3
    mydict1["next_card_1"] = next_card_1
    mydict1["next_card_2"] = next_card_2
    mydict1["next_card_3"] = next_card_3
    mydict1["quest_accepted_1"] = quest_accepted_1
    mydict1["quest_accepted_2"] = quest_accepted_2
    mydict1["quest_accepted_3"] = quest_accepted_3
    mydict1["quest_reward_1"] = quest_reward_1
    mydict1["quest_reward_2"] = quest_reward_2
    mydict1["quest_reward_3"] = quest_reward_3
    mydict2 = {}
    mydict2["index"] = 1
    mydict2["prompt"] = "This is the second prompt."
    mydict2["choice_1"] = choice_1
    mydict2["choice_2"] = choice_2
    mydict2["choice_3"] = choice_3
    mydict2["response_1"] = response_1
    mydict2["response_2"] = response_2
    mydict2["response_3"] = response_3
    mydict2["todo_1"] = todo_1
    mydict2["todo_2"] = todo_2
    mydict2["todo_3"] = todo_3
    mydict2["item_1"] = item_1
    mydict2["item_2"] = item_2
    mydict2["item_3"] = item_3
    mydict1["next_card_1"] = next_card_1
    mydict1["next_card_2"] = next_card_2
    mydict1["next_card_3"] = next_card_3
    mydict1["quest_accepted_1"] = quest_accepted_1
    mydict1["quest_accepted_2"] = quest_accepted_2
    mydict1["quest_accepted_3"] = quest_accepted_3
    mydict1["quest_reward_1"] = quest_reward_1
    mydict1["quest_reward_2"] = quest_reward_2
    mydict1["quest_reward_3"] = quest_reward_3
    # ----
    myobject = ConversationQuestCard(mydict1)
    mylist1 = myobject.display_card_1()
    # ----
    user_choice = 2
    mylist2 = myobject.display_card_2(user_choice, None, None)
    print(mylist1)
    print(mylist2)

# def debug_master_quests():
#     myobject = MasterQuests("testing", "map00", "tyla")
#     myobject.read_data()
#     myobject.debug_print()

# def debug_master_quest():
#     myobject = MasterQuest("testing", "map00", "tyla")

def debug_print_out_all_quests():
    myobject = SearchMasterQuests()
    myobject.debug_print()

def debug_search_master_quests():
    # quest_name = "a hint"
    zone_name = "bridge"
    map_name = "map00"
    # quest_name = "The Three Feathers"
    quest_name = "buy a secret"
    # ----
    myobject = SearchMasterQuests()
    # myobject.debug_print()
    myquest = myobject.get_quest_by_quest_name(quest_name)
    myquest.debug_print()
    # myobject.debug_print()
    # quest = myobject.get_quest_by_quest_name(quest_name)
    # print("**************************")
    # print(quest)
    # is_accepted = myobject.quest_accepted(quest_name)
    # is_completed = myobject.quest_completed(quest_name)
    # if is_accepted == True:
    #     print("The quest ({}) was accepted.".format(quest_name))
    # else:
    #     print("The quest ({}) was NOT accepted.".format(quest_name))
    # if is_completed == True:
    #     print("The quest ({}) was completed.".format(quest_name))
    # else:
    #     print("The quest ({}) was NOT completed.".format(quest_name))

def debug_master_quests():
    completion_stage = "accepted"
    mydialog = MasterQuests(zone_name="swindon_pub", map_name="map00")
    mydialog.read_data()
    # mydialog.filter(completion_stage)
    display_list01 = mydialog.get_display_list()
    mylist = display_list01
    # # ----
    # mydialog02 = MasterQuests(zone_name="swindon_pub", map_name="map00")
    # mydialog02.read_data()
    # display_list02 = mydialog02.get_display_list()
    # # ----
    # mydialog03 = MasterQuests(zone_name="jeweler", map_name="map00")
    # mydialog03.read_data()
    # display_list03 = mydialog03.get_display_list()
    # # ---- ----
    # mylist = display_list01 + display_list02 + display_list03
    for elem in mylist:
        print(elem)
    # # mydialog.main()

if __name__ == "__main__":
    # char_type = "npc"
    # char_type = "player"
    # debug_inventory(player_name="henry", npc_name="aiza")
    # debug_inventory_buy_a_consumable(player_name="henry", npc_name="aiza")
    # debug_inventory_sell_a_consumable(player_name="henry", npc_name="aiza")
    # reset_conversation(npc_name="aiza", zone_name="swindon_pub", map_name="map00")
    debug_conversation()
    # debug_quest_card()
    # debug_quests()
    # debug_master_quests()
    # debug_master_quest()
    # ----
    # debug_print_out_all_quests()
    # debug_search_master_quests()