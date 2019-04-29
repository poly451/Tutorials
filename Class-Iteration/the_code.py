class Player:
    def __init__(self, a_sword):
        self.sword = a_sword

    def get_good_sword(self, weapons):
        self.sword = weapons.get_good_sword()

"""
===============================================
                class Sword
===============================================
"""

class Sword:

    def __init__(self, durability, max_damage, min_damage, name):
        self.durability = durability
        self.max_damage = max_damage
        self.min_damage = min_damage
        self.name = name

    def debug_print(self):
        s = """
        durability:     {}
        maximum damage: {}
        minimum damage: {}
        name:           {}
        """.format(self.durability, self.max_damage, self.min_damage, self.name)
        print(s)

"""
===============================================
                class Swords
===============================================
"""

class Swords:
    def __init__(self):
        self.all_swords = [Sword(2, 0, 1, "Rusty Wonder"), Sword(10, 8, 3, "Old Glory"), Sword(3, 2, 1, "Meh")]
        self.i = 0
        # self.end = len(self.all_swords)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.all_swords):
            self.i += 1
            return self.all_swords[self.i-1]
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.all_swords)
    
    def __getitem__(self, item):
        if item >= 0 and item < len(self.all_swords):
            return self.all_swords[item]
        else:
            raise ValueError

    def __setitem__(self, key, value):
        if key >= 0 and key < len(self.all_swords):
            self.all_swords[key] = value
        else:
            raise ValueError

    def __delitem__(self, key):
        new_list = []
        counter = 0
        if key >= 0 and key < len(self.all_swords):
            for each_sword in self.all_swords:
                if counter == key:
                    pass
                else:
                    new_list.append(each_sword)
                counter += 1
            self.all_swords = new_list
        else:
            raise ValueError

    def get_new_sword(self, player):
        for a_sword in self.all_swords:
            if a_sword.name == "Old Glory":
                player.sword = a_sword

    def debug_print(self):
        print("--------- Swords debug_print (begin) -----------")
        for a_sword in self.all_swords:
            a_sword.debug_print()
        print("--------- Swords debug_print (end) -----------")

"""
===============================================
                class Weapons
===============================================
"""

class Weapons:
    def __init__(self, swords, daggers=[], flamethrowers=[]):
        self.swords = swords
        self.daggers = daggers
        self.flamethrowers = flamethrowers

    def get_good_sword(self):
        print("-------- beginning of get_good_sword ----------")
        # return Sword(5, 5, 3, "Reliable")
        # print(self.swords)
        counter = 0
        for a_sword in self.swords:
            counter += 1
            if a_sword.durability > 5 and a_sword.max_damage > 7:
                print("durability: {}".format(a_sword.durability))
                return a_sword
        print("counter = {}".format(counter))
        print("len(self.swords) = {}".format(len(self.swords)))
        print("-------- end of get_good_sword ----------")

"""
===============================================
===============================================
"""

def main():
    player = Player(Sword(3, 3, 2, "The Toothpick"))
    print("before:")
    player.sword.debug_print()

    swords = Swords()
    weapons = Weapons(swords)
    player.get_good_sword(weapons)
    # swords.debug_print()
    print("after:")
    print("type: {}".format(player.sword))
    # player.sword.debug_print()

if __name__=="__main__":
    main()
