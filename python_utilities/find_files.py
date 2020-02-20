import os, sys

def find_largest(mydir, number_of_largest_files):
    print("Scanning directory:\n{}.".format(mydir))
    print("Looking for the {} largest files.".format(number_of_largest_files))
    myfiles = []
    for root, dirs, files in os.walk(mydir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                statinfo = os.stat(filepath)
                myfiles.append([filepath, statinfo.st_size])
            except:
                print("-" * 20)
                print("File not found: {}".format(file))
                print("root: {}".format(root))
                print("dirs: ")
                print("-" * 20)
    print("{} files were found.".format(len(myfiles)))
    myfiles = sorted(myfiles, key=lambda bla: bla[1], reverse=True)
    # [print(i) for i in myfiles]
    return myfiles[0:number_of_largest_files]

if __name__ == "__main__":
    starting_directory = "/Users/BigBlue/Downloads"
    find_biggest(starting_directory, 10)