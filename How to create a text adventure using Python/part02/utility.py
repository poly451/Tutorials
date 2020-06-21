import utils
import os, sys

def main(path_in, path_out):
    with open(path_in, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # mylines = [i.replace(";", "") for i in mylines]
    mylist = []
    for i in range(0, len(mylines), 8):
        mydict = {}
        for j in range(8):
            elem = mylines[i+j]
            # print("elem: ", elem)
            mydict = utils.key_value_pair(elem, mydict)
        mylist.append(mydict)
    print("=" * 20)
    for elem in mylist:
        print(elem)
    print("=" * 20)
    with open(path_out, "w") as f:
        for mydict in mylist:
            for key, value in mydict.items():
                s = "{}: {}\n".format(key, value)
                # print(s)
                f.write(s)


if __name__ == "__main__":
    char_name, char_kind = utils.char_info()
    char_dir = "{}_{}".format(char_name, char_kind)
    path_in = "data/master_files/tiles/dungeon.txt"
    path_out = "data/master_files/tiles/dungeon01.txt"
    main(path_in=path_in, path_out=path_out)