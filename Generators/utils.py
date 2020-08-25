import datetime
import random

def get_time():
    t = datetime.datetime.now()
    s = "minutes: {}, seconds: {}, microseconds: {}".format(t.minute,
                                                            t.second,
                                                            t.microsecond)
    s = "{} {} {}".format("-" * 20, s, "-" * 20)
    return t, s

def time_difference_format(start_time, end_time):
    t = end_time - start_time
    s = "{}".format(t)
    mylist = s.split(":")
    m = mylist[1]
    s = mylist[2]
    mylist = s.split(".")
    s = "{} minutes, {} seconds, {} microseconds elapsed".format(int(m), int(mylist[0]), int(mylist[1]))
    return s

def time_difference_ms(start_time, end_time):
    t = end_time - start_time
    s = "{}".format(t)
    mylist = s.split(":")
    m = mylist[1]
    s = mylist[2]
    mylist = s.split(".")
    return int(mylist[1])

def get_moves(max):
    def get_xy():
        dirs = ["up", "down", "right", "left"]
        myran = random.randint(0, 3)
        return dirs[myran]
    counter = 0
    while counter < max:
        yield get_xy()
        counter += 1

if __name__ == "__main__":
    mylist = get_moves(100)
    print(mylist)
