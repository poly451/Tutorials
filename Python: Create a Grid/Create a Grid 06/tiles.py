import os, sys

import constants
import utils

# -----------------------------------------------------------
#                      class Tile
# -----------------------------------------------------------
class Tile:
    def __init__(self, mydict):
        self.index = mydict["index"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        self.image = mydict["image"]

    def debug_print(self):
        s = "index: {}, name: {}, kind: {}, image: {}"
        s = s.format(self.index, self.name, self.kind, self.image)
        print(s)

# -----------------------------------------------------------
#                      class Tiles
# -----------------------------------------------------------
class Tiles:
    def __init__(self):
        self.inner = []

    def read_data(self):
        self.inner = []
        filepath = os.path.join("data", "master_files", "tiles.txt")
        mylist = utils.read_data_file(filepath, 4)
        for mydict in mylist:
            new_object = Tile(mydict)
            self.inner.append(new_object)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

    def get_unused_letters(self):
        used_letters = []
        for elem in self.inner:
            # print(elem.name[0:1])
            used_letters.append(elem.name[0:1])
        my_alph = constants.ALPHABET
        available_letters = []
        for mychar in my_alph:
            if not mychar in used_letters:
                available_letters.append(mychar)
        print(available_letters)

# ==========================================
if __name__ == "__main__":
    myobject = Tiles()
    myobject.read_data()
    # myobject.debug_print()
    myobject.get_unused_letters()