

from operator import attrgetter

class TallestBuildings:
    def __init__(self, name, city, country, feet_high, floors, year):
        self.name = name
        self.city = city
        self.country = country
        self.feet_high = feet_high
        self.floors = floors
        self.year = year

    def __repr__(self):
        # This code allows us to use print() to view the data.
        s = "name: {}, city: {}, country: {}, feet: {}, floors: {}, year: {}"
        s = s.format(self.name, self.city, self.country, self.feet_high, self.floors, self.year)
        return s

tallest_buildings = []
tallest_buildings.append(TallestBuildings("Burj Khalifa", "Dubai", "United Arab Smirates", 2717, 163, 2010))
tallest_buildings.append(TallestBuildings("Shanghai Tower", "Shanghai", "China", 2973, 128, 2015))
tallest_buildings.append(TallestBuildings("Abraj Al-Bait Clock Tower", "Mecca", "Saudi Arabia", 1971, 120, 2012))

# [print(i) for i in tallest_buildings]

# Sorting by building name
sorted_list = sorted(tallest_buildings, key=lambda TallestBuildings: TallestBuildings.name)
print("{} {} {}".format("-" * 20, "Sorting by building NAME", "-" * 20))
[print(i) for i in sorted_list]
# Sorting by hear built
sorted_list = sorted(tallest_buildings, key=lambda TallestBuildings: TallestBuildings.year)
print("{} {} {}".format("-" * 20, "Sorting by YEAR built", "-" * 20))
[print(i) for i in sorted_list]
# Sorting by country and height
sorted_list = sorted(tallest_buildings, key=attrgetter('country', 'feet_high'))
print("{} {} {}".format("-" * 20, "Sorting by FEET_HEIGHT and HEIGHT", "-" * 20))
[print(i) for i in sorted_list]
