import os, sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cmd
import json
import utils
from shutil import copyfile
import constants as con

class MyShell(cmd.Cmd):
    program_name = "Pick a Portrait"
    intro = "Welcome to {}! Type help or ? to list commands.\n".format(program_name)
    intro += "If this is the first time you've run the program:\n1. loadchoices default\n2. alterproperty eye_color 0 3\n3. loadfaces personal\n4. savechoices"
    intro += "\n-------------------------------------------------"
    prompt = "> "
    file = None

    def __init__(self):
        super().__init__()
        self.choices = []
        self.inner = []

    def read_in_all_images(self):
        """
        Reads in all the faces in the directory.
        :return: Returns a list that contains information about each image in the directory.
        """
        all_files = os.listdir(con.IMAGES_DIRECTORY)
        output_list = []
        for filename in all_files:
            extension = filename[-3:]
            if extension == "png":
                continue
            new_path = os.path.join(con.IMAGES_DIRECTORY, filename)
            # print(new_path)
            with open(new_path, "r") as f:
                mylist = f.readlines()
                mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
            parsed_list = utils.parse_line(mylist)
            parsed_list.insert(0, filename)
            output_list.append(parsed_list)
        return output_list

    def read_in_image_subset(self):
        """
        Parses and reads in the csv files in the image directory. Looking for only
        those images that fit the user's requirements/choices.
        :return: Returns a list that contains information about certain images in the directory.
        """
        if len(self.choices) == 0:
            raise ValueError("self.choices array is EMPTY.")
        all_files = os.listdir(con.IMAGES_DIRECTORY)
        output_list = []
        for filename in all_files:
            extension = filename[-3:]
            if extension == "png":  # skip the image files
                continue
            new_path = os.path.join(con.IMAGES_DIRECTORY, filename)
            mylist = []
            # opens a .csv file and reads in its contents.
            with open(new_path, "r") as f:
                mylist = f.readlines()
                # The following line strips out newline characters and makes sure the line isn't empty.
                mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
            # print(mylist)
            mylist = utils.parse_line(mylist)
            mylist.insert(0, filename)
            output_list.append(mylist)
        # ----------------------------
        output_list = self.apply_choices(output_list)
        # ----------------------------
        return output_list

    def select_faces(self, face):
        for choice in self.choices:
            for face_element in face:
                if face_element[0] == choice[0]:
                    if not face_element[1] in choice[1]:
                        return False
        return True

    def apply_choices(self, face_lines):
        if len(self.choices) == 0:
            raise ValueError("The choice array is empty.")
        selected_faces = []
        for face in face_lines:
            # face[0] = eye_angle ; face[1] = eye_lashes ; face[2] = eye_lid , etc.
            if self.select_faces(face[1:]):
                selected_faces.append(face)
        return selected_faces

    # ----------------------------------------------------------

    def do_checkinvaliddata(self, arg):
        """
        Searcher for illegal/invalid values in the dataset.
        :return:
        """
        number_of_illegal_values = 0
        all_images = self.read_in_all_images()
        for face in all_images:
            for count, feature in enumerate(face):
                if count == 0:
                    continue
                print("feature: {}".format(feature))
                print("{} -- {}".format(feature[1], feature[2]))
                if feature[1] + 1 > feature[2]:
                    number_of_illegal_values += 1
                    print("Illegal value found!!\n{}\n{}".format(face, feature))
                print("--------------------------------")
        print("**** End of checking for illegal values ****")
        print("Number of illegal values found: {}".format(number_of_illegal_values))

    # ----------------------------------------------------------

    def do_savefaces(self, arg):
        """
        Makes a copy of the selected faces/portraits and puts them in a directory called 'faces.'
        :param arg: None
        :return: None
        """
        if len(self.inner) == 0:
            print("There are no portraits to save.")
            return False
        elif len(self.inner) > con.MAX_PORTRAITS:
            s = "You have opted to save {} portraits. Currently the most that can be saved are {} portraits.\n".format(len(self.inner), MAX_PORTRAITS)
            s += "If you would like to change this, alter MAX_PORTRAITS in myclasses.py."
            print(s)
            return False
        for face in self.inner:
            filename = face[0]
            filename = filename.replace(".csv", ".png")
            filepath_out = os.path.join("data/faces", filename)
            filepath_in = os.path.join(con.IMAGES_DIRECTORY, filename)
            print("in: ", filepath_in)
            print("OUT: ", filepath_out)
            print("----------------------")
            copyfile(filepath_in, filepath_out)


    def do_viewfaces(self, arg):
        """
        View all the selected faces.
        :param arg: None
        :return: None
        """
        if len(self.inner) == 0:
            print("There are no faces to view. 1. loadchoices default 2. alterproperty 3. loadfaces personal 4. savechoices")
        if len(self.inner) > con.MAX_PORTRAITS:
            print("Over 50 images have been selected. If you would like to view all fifty then adjust def do_viewfaces(self, arg)")
            print("Otherwise, narrow your selection.")
            return False
        filenames = []
        for face in self.inner:
            filename = face[0][0:-3]
            filenames.append("{}png\n".format(filename))
        with open(con.SAVE_IMAGE_NAMES, 'w') as f:
            for filename in filenames:
                # print(filename)
                f.write(filename)
        # for face in self.inner:
        #     print("elem[0]: ", face[0])
        #     # ----
        #     filename = face[0][0:-3]
        #     filename = "{}png".format(filename)
        #     filepath = os.path.join(IMAGES_DIRECTORY, filename)
        #     # print(filepath)
        #     print(filepath)
        #     img = mpimg.imread(filepath)
        #     imgplot = plt.imshow(img)
        #     plt.show()

    def do_alterproperty(self, arg):
        """
        Alters a property.
        Use: alterproperty eye_color 3
        Use: alterproperty eye_color [0,1,3]
        :param arg: property name ; property value
        :return: None
        """
        arg = arg.strip().lower()
        arg = arg.replace(",", "")
        if "showvalues" in arg:
            mylist = arg.split(" ")
            for a_property in self.choices:
                if a_property[0] == mylist[0]:
                    print("0 to {}".format(a_property[2]-1))
            return False
        if len(arg) == 0:
            raise ValueError("Nothing was entered!")
        values = arg.split(" ")
        # ------------------------
        # Make sure this property is valid.
        if utils.valid_property(values[0], con.DEFAULT_CHOICES) == False:
            s= "That property is NOT valid: {}".format(values[0])
            print(s)
            return False
        # ------------------------
        mylist = []
        for mycount, elem in enumerate(values):
            if mycount == 0:
                continue
            # print("elem: ", elem)
            mylist.append(int(elem.strip()))
            # print("values: ", values[0])
            # print("mylist: ", mylist)
            # print(self.inner[values[0]])
        # ------------------------
        mylist.sort()
        # print(values[0], mylist)
        # ------------------------
        if not utils.values_are_valid(self.choices, values[0], mylist):
            s = "Those values are not valid: {}, {}".format(values[0], mylist)
            print(s)
            return False
        # ------------------------
        for choice in self.choices:
            if choice[0] == values[0]:
                choice[1] = mylist
        # ------------------------

    def do_loadfaces(self, arg):
        """
        Personal: Loads all the faces in the directory based on the user's selections.
        Default: Loads all the faces in the directory.
        :param arg: 'personal' or 'default'
        :return: A list of faces.
        """
        arg = arg.strip().lower()
        if len(arg) == 0:
            print("Would you like to load the DEFAULT choices or your PERSONAL choices?")
            print("Use: loadfaces personal")
            print("Use: loadfaces default")
            return False
        if arg == "default":
            print("Loading all the faces ....")
            self.inner = self.read_in_all_images()
            print("{} faces loaded.".format(len(self.inner)))
        elif arg == "personal":
            print("Loading only thoses faces that have the characteristics the user has specified ....")
            self.inner = self.read_in_image_subset()
            if len(self.inner) == 0:
                print("!!! NO FACES HAVE BEEN SELECTED !!!")
        else:
            s = "Sorry, I don't understand that: {}".format(arg)
            raise ValueError(s)
        print("{} faces loaded.".format(len(self.inner)))
        # --------------------------------------------------
        with open(con.SAVE_IMAGE_NAMES, "w") as f:
            for elem in self.inner:
                temp = elem[0].replace(".csv", ".png") + "\n"
                f.write(temp)
        print("{} faces saved to {}".format(len(self.inner), con.SAVE_IMAGE_NAMES))

    def do_loadchoices(self, arg):
        """
        Loads either choice dataset or the default dataset.
        :param arg: Possible arguments: 'default' and 'personal'.
        :return: does not return anything
        """
        arg = arg.strip().lower()
        if len(arg) == 0:
            raise ValueError("This function requires an argument.")
        if arg == "default":
            print("Loading DEFAULT choices ....")
            with open(con.DEFAULT_CHOICES, 'r') as f:
                self.choices = json.load(f)
        elif arg == "personal":
            print("Loading PERSONAL choices.")
            with open(con.PERSONAL_CHOICES, 'r') as f:
                self.choices = json.load(f)
        else:
            s = "This argument ({}) was NOT recognized.".format(arg)
            raise ValueError(s)
        print("{} choices loaded.".format(len(self.choices)))

    def do_savechoices(self, arg):
        """
        Saves the choices the user has made.
        :param: None
        :return: Does not return anything.
        """
        print("Saving PERSONAL choices.")
        with open(con.PERSONAL_CHOICES, 'w') as f:
            json.dump(self.choices, f)

    # ----------------------------------------------------------

    def do_printchoices(self, arg):
        """
        Prints out the characteristics the user has specified.
        :param arg: None
        :return: None
        """
        for elem in self.choices:
            print(elem)
        print("There are {} lines of choices.".format(len(self.choices)))

    def do_printfaces(self, arg):
        """
        Prints out the faces that fulfill the specifications the user has set.
        :param arg: None
        :return: None
        """
        if len(self.inner) == 0:
            print("!!! Cannot print the contents of self.inner !!!")
        else:
            for elem in self.inner:
                print(elem)
            print("There are {} lines of faces.".format(len(self.inner)))

    def do_printpropertieschanged(self, arg):
        """
        Prints out all and only the properties that were changed/adjusted by the user.
        :param arg: None
        :return: None
        """
        for choice in self.choices:
            if len(choice[1]) != choice[2]:
                print(choice)

    # ----------------------------------------------------------

    def do_bye(self, arg):
        'Close the window and exit the program:  BYE'
        print('Thank you for using {}!'.format(self.program_name))
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

# ==========================================================
# ==========================================================

if __name__ == "__main__":
    MyShell().cmdloop()