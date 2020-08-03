# -------------------------------------------------
#                      clas Car
# -------------------------------------------------

class Car:
    def __init__(self, name, tires, seats):
        self.name = name
        self.tires = tires
        self.seats = seats

    def print_car(self):
        s = "name: {}, tires: {}, seats: {}".format(self.name, self.tires, self.seats)
        print(s)

# -------------------------------------------------
#                      clas Cars
# -------------------------------------------------

class Cars:
    def __init__(self):
        self.cars = []
        self.current = 0

    def add_car(self, name, tires, seats):
        new_car = Car(name, tires, seats)
        self.cars.append(new_car)

    def print_car(self):
        print("Number of cars:", len(self.cars))
        print("-" * 30)
        for elem in self.cars:
            elem.print_car()

    def __len__(self):
        return len(self.cars)

    def __repr__(self):
        s = ""
        for elem in self.cars:
            s += "{}\n".format(elem.print_string())
        return(s.strip())

    def __iter__(self):
        return self

    def __next__(self):
        print("current:", self.current)
        try:
            item = self.cars[self.current]
        except IndexError:
            self.current = 0
            raise StopIteration()
        self.current += 1
        return item

# *************************************************

# mycars = Cars()
# mycars.add_car(name="ford", tires=4, seats=4)
# mycars.add_car(name="parsche", tires=4, seats=4)
# mycars.print_car()

mycars = Cars()
mycars.add_car(name="ford", tires=4, seats=4)
mycars.add_car(name="parsche", tires=4, seats=2)
print("You have {} cars.".format(len(mycars)))
print("=" * 40)
for a_car in mycars:
    a_car.print_car()

