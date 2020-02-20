import os, sys
import shutil
import constants as con
from find_files import find_largest

def remove_file(filepath):
    os.remove(filepath)

def move_file(move_file_from_dir, move_file_to_dir, filename):
    filepath_old = os.path.join(move_file_from_dir, filename)
    filepath_new = os.path.join(move_file_to_dir, filename)
    os.rename(filepath_old, filepath_new)

def find_external_drives():
    # mydir = "/Volumes/LaCie/Movies"
    mydir = "/Volumes"
    all_files = []
    for root, dirs, files in os.walk(mydir):
        all_files = all_files + files
        for file in files:
            filepath = os.path.join(root, file)
            print("{}".format(filepath))
    if len(all_files) == 0:
        print("#########################")
        print("No external drives found!")
        print("#########################")

def prompt_for_filepath():
    print("Filename:")
    filename = input(con.PROMPT).strip().lower()
    print("Directory:")
    directory = input(con.PROMPT).strip().lower()
    filepath = os.path.join(directory, filename)
    return filepath

def main():
    choices = ["1", "2", "3", "4", "5", "6"]
    run_program = True
    while run_program:
        s = "{}\n".format("#" * 40)
        s += "What would you like to do?\n"
        s += "1. Move file.\n"
        s += "2. List external drives.\n"
        s += "3. Remove file.\n"
        s += "4. Create file.\n"
        s += "5. Find the biggest files.\n"
        s += "6. Exit/Quit"
        print(s)
        ur = input(con.PROMPT).strip().lower()
        while not ur in choices:
            print(choices)
            ur = input(con.PROMPT).strip().lower()
        # -----------------------------------------
        destination_directory = con.DESTINATION_DIRECTORY
        filename = "cookies.txt"
        # ---- Move File ----
        if ur == "1":
            origin_directory = con.ORIGIN_DIRECTORY
            filename = "youtube_script_utilities.wav"
            print("Moving file {}\nfrom here {}\nto here {}".format(filename.upper(), origin_directory.upper(),
                                                                    destination_directory.upper()))
            print("(yes/no)")
            ur = input(con.PROMPT).strip().lower()
            if ur == "yes":
                print("Moving file ...")
                move_file(origin_directory, destination_directory, filename)
            else:
                print("Operation Cancelled.")
        elif ur == "2": # ---------------------------
            print("Priting out external drives.")
            find_external_drives()
        elif ur == "3": # ---------------------------
            print("What file would you like to remove?")
            filepath = prompt_for_filepath()
            print("Removing file: {}".format(filepath))
            print("Proceed? (yes/no)")
            ur = input(con.PROMPT)
            if ur == "yes":
                remove_file(filepath)
                print("File removed.")
            else:
                print("Operation cancelled.")
        elif ur == "4": # ---------------------------
            filepath = prompt_for_filepath()
            try:
                with open(filepath, "w") as f:
                    f.write("")
                print("File created: {}".format(filepath))
            except:
                print("Sorry! I couldn't create that file:")
                print(filepath)
        elif ur == "5": # -----4----------------------
            print("Finding the biggest files.")
            print("Which directory do you want to look in?")
            mydir = input(con.PROMPT).strip().lower()
            if len(ur) == 0:
                mydir = input(con.PROMPT).strip().lower()
            largest_files = find_largest(mydir, number_of_largest_files=10)
            [print(i) for i in largest_files]
        elif ur == "6": # ---------------------------
            print("Exiting ...")
            sys.exit()
        else:
            print("I didn't understand that: {}".format(ur))

if __name__ == "__main__":
    main()
