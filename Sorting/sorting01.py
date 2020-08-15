from operator import itemgetter

def sort01():
    list_values = [18, 39, 13, 43, 9, 3, 97, 34, 29]
    sorted_list01 = sorted(list_values)
    print(sorted_list01)
    sorted_list02 = sorted(list_values, reverse=True)
    print(sorted_list02)

def sort03():
    tall_building_1 = ["Burj Khalifa", "Bubai", "United Arab Emirates", 2717, 163, 2010]
    tall_building_2 = ["Shanghai Tower", "Shanghai", "China", 2073, 128, 2015]
    tall_building_3 = ["Abraj Al-Bait Clock Tower", "Mecca", "Saudi Arabia", 1971, 120, 2012]
    tall_building_4 = ["Ping An Finance Center", "Shenzhen", "China", 1965, 115, 2017]
    tall_building_5 = ["Lotte World Tower", "Seoul", "South Korea", 1819, 123, 2016]
    tall_building_6 = ["One World Trade Center", "New York City", "United States", 1776, 104, 2014]
    tall_building_7 = ["Guangzhou CTF Finance Center", "Guangzhou", "China", 1739, 98, 2018]
    tall_building_8 = ["Tianjin CTF Finance Center", "Tianjin", "China", 1739, 98, 2018]
    tall_building_9 = ["China Zun", "Beijing", "China", 1732, 108, 2018]
    tall_building_10 = ["Taipei 101", "Taipei", "Taiwan", 1667, 101, 2004]
    tall_building = [tall_building_1, tall_building_2, tall_building_3, tall_building_4, tall_building_5,
                     tall_building_6, tall_building_6, tall_building_7, tall_building_8, tall_building_9,
                     tall_building_10]
    sorted_list = sorted(tall_building, key=itemgetter(5))
    [print(i) for i in sorted_list]

def sort02():
    def mykey(mypair):
        return mypair[1]
    list_values = [(18, "Horses"), (39, "Ducks"), (13, "Cats"), (43, "Panda"), (9, "Hamster"), (3, "Beaver"), (97, "Pigs"), (34, "Sheep"), (29, "Owls")]
    sorted_list01 = sorted(list_values)
    print(sorted_list01)
    sorted_list02 = sorted(list_values, reverse=True)
    print(sorted_list02)
    sorted_list01 = sorted(list_values, key=mykey)
    print(sorted_list01)

def multiply_elements(x, y):
    return x * y

def sort_on_last(mystring):
    return mystring[-1]

def sorted_length():
    sentence = "What is your favorite programming language"
    word_list = sentence.split((" "))
    print(word_list)
    # Sort the word list in order of the first character of each word
    word_list = sorted(word_list)
    print(word_list, " <--- Sorted on first character of first word")
    # Sort the list in order of lenfth
    word_list = sorted(word_list, key=len)
    print(word_list, " <--- Sorted on length of each word")
    # Sort the words in word_list on the LAST character of each word
    word_list = sorted(word_list, key=sort_on_last)
    print(word_list, " <--- Sorted on the LAST character of each word")
    # reverse
    word_list = sorted(word_list, key=sort_on_last, reverse=True)
    print(word_list, " <--- Sorted on the LAST character of each word, REVERSED")

def sorted_using_lambdas():
    word_list = [(9, ), (1, 2, 3), (1, 2)]
    print(word_list)
    word_list = sorted(word_list, key=lambda x: sum(x))
    print(word_list, " <--- Sorted on sum (3, 6, 9")

# ------------------------------------------------------

def a_sort(x):
  return x[1]	# return age

def slightly_more_complicated_sort():
    data = [('Alex', 35), ('Beth', 25), ('Carol', 30)]
    result_of_sort = sorted(data, key=a_sort)
    print(result_of_sort, " <--- Sorted on age")

# ------------------------------------------------------

def multiple_level_sorting():
    data = [('Alex', 1256, 1968), ('Beth', 25, 2002), ('Carol', 294, 1992), ('Ben', 30, 1954), ('Ben', 695, 1954)]
    sorted_list = sorted(data, key=itemgetter(0, 1))
    print(sorted_list, " <--- ")

if __name__ == "__main__":
    sort02()
