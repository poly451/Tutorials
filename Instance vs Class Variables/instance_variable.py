class Car:
    def __init__(self):
        self.tires = 0
        self.seats = 0
        self.number_of_cars = 0

    def add_car(self, tires, seats):
        self.tires = tires
        self.seats = seats
        self.number_of_cars += 1

    def print_car(self):
        print("tires: {}, seats: {}, number of cars: {}".format(self.tires, self.seats, self.number_of_cars))

print("The first car: ")
print("-" * 30)
ford = Car()
ford.add_car(tires=3, seats=4)
ford.print_car()
print("*" * 30)
print("\nThe second car: ")
print("-" * 30)
porsche = Car()
porsche.add_car(tires=4, seats=2)
porsche.print_car()
