# -----------------------------------------------------------
#                      class Quest
# -----------------------------------------------------------
class Quest:
    def __init__(self, mydict):
        self.index = mydict["index"]
        self.name = mydict["name"]
        self.text = mydict["text"]

# -----------------------------------------------------------
#                      class Quests
# -----------------------------------------------------------
class Quests:
    def __init__(self):
        pass

    def read_data(self):
        pass

    def main(self):
        pass

if __name__ == "__name__":
    myobject = Quests()
    myobject.read_data()
    myobject.main()