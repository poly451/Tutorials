#
#
#
# class MyShell(cmd.Cmd):
#     # program_name = "Pick a Portrait"
#     # intro = "Welcome to {}! Type help or ? to list commands.\n".format(program_name)
#     # prompt = "> "
#     # file = None
#
#     def __init__(self):
#         # super().__init__()
#         list_hair = []
#         for elem in range(111):
#             list_hair.append(elem)
#         # print("hair list: ", list_hair)
#         self.choices = []
#         self.choices.append(["eye_angle", [0,1,2], 3])
#         self.choices.append(["eye_lashes", [0, 1], 2])
#         self.choices.append(["eye_lid", [0, 1], 2])
#         self.choices.append(["chin_length", [0, 1, 2], 3])
#         self.choices.append(["eyebrow_weight", [0, 1], 2])
#         self.choices.append(["eyebrow_shape", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 14])
#         self.choices.append(["chin_length", [0, 1, 2], 3])
#         self.choices.append(["eyebrow_weight", [0, 1], 2])
#         self.choices.append(["eyebrow_shape", [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 14])
#         self.choices.append(["eyebrow_thickness", [0, 1, 2, 3], 4])
#         self.choices.append(["face_shape", [0, 1, 2, 3, 4, 5, 6], 7])
#         # self.choices.append(["face_shape", [5], 7])
#         self.choices.append(["facial_hair", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 15])
#         self.choices.append(["hair", list_hair, 111])
#         self.choices.append(["eye_color", [0, 1, 2, 3, 4], 5])
#         # self.choices.append(["eye_color", [2], 5])
#         self.choices.append(["face_color", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11])
#         self.choices.append(["hair_color", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 10])
#         self.choices.append(["glasses", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 12])
#         self.choices.append(["glasses_color", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 10])
#         self.choices.append(["eye_slant", [0, 1, 2], 3])
#         self.choices.append(["eyebrow_width", [0, 1, 2], 3])
#         directory = "/Users/BigBlue/Downloads/cartoonset10k"
#         self.inner = self.read_in_images(directory)
#
#     def add(self, property, values):
#         # in form [property, value1, value2, value3, etc.]
#         # filepath = "/Users/BigBlue/Documents/Programming/Python/misc/data/properties.txt"
#         # with open(filepath, "r") as f:
#         #     mylist = f.readlines()
#         #     mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#         if not property in FACE_PROPERTIES:
#             raise ValueError("Sorry, that property was not found: {}".format(property))
#         for choice in self.choices:
#             if choice[0] == property:
#                 choice[1] = values
#         # [print(i) for i in self.choices]
#
#
#     # def read_in_images(self, mydir):
#     #     all_files = os.listdir(mydir)
#     #     output_list = []
#     #     for filename in all_files:
#     #         extension = filename[-3:]
#     #         if extension == "png":
#     #             continue
#     #         new_path = os.path.join(mydir, filename)
#     #         # print(new_path)
#     #         with open(new_path, "r") as f:
#     #             mylist = f.readlines()
#     #             mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#     #         parsed_list = parse_line(mylist)
#     #         parsed_list.insert(0, filename)
#     #         output_list.append(parsed_list)
#     #     return output_list
#
#     # def do_savechoices(self, arg):
#     #     with open(SAVE_CHOICES, 'w') as f:
#     #         json.dump(self.choices, f)
#     #
#     # def do_loadchoices(self, arg):
#     #     with open(SAVE_CHOICES, 'r') as f:
#     #         self.choices = json.load(f)
#     #     self.applychoices()
#     #     for elem in self.choices:
#     #         print(elem)
#
#     def do_alterproperty(self, arg):
#         # print("In add property: ", arg)
#         if len(arg.strip()) == 0:
#             raise ValueError("Nothing was entered!")
#         if "," in arg:
#             raise ValueError("Illegal comma found.")
#         values = arg.split(" ")
#         # print("values: ", values)
#         # print(values)
#         # ------------------------
#         mylist = []
#         for mycount, elem in enumerate(values):
#             if mycount == 0:
#                 continue
#             # print("elem: ", elem)
#             mylist.append(int(elem.strip()))
#             # print("values: ", values[0])
#             # print("mylist: ", mylist)
#             # print(self.inner[values[0]])
#         # ------------------------
#         mylist.sort()
#         # print(mylist)
#         self.add(values[0], mylist)
#         self.applychoices()
#
#     def do_applychoices(self, arg):
#         self.applychoices()
#
#     def elem_test(self, elem):
#         for choice in self.choices:
#             print("choice: ", choice)
#             if choice[0] == elem[0]:
#                 print("choice: ", choice[0])
#                 print("elem: ", elem[0])
#                 if elem[1] in choice[1]:
#                     return True
#         return False
#
#     def examine_element(self, choice_element, line_element):
#         print("match found")
#         if line_element[1] in choice_element[1]:
#             print("{} in range {} in {}".format(choice_element[0], line_element[1], choice_element[1]))
#         else:
#             return False
#         return True
#
#     def examine_line(self, choice_element, lines):
#         lines = []
#         for line_element in lines:
#             line = line_element[1:]
#             print("line: ", line)
#             print("line[0]: {}, choice[0]: {}".format(line[0], choice_element[0]))
#             for elem in line:
#                 if elem[0] == choice_element[0]:
#                     if not self.examine_element(choice_element[0], elem[0]):
#                         return False
#
#     def helper(self, choice, temp_line):
#         for line_bit in temp_line:
#             print("choice: ", choice[0], "line: ", line_bit)
#             print(choice[1])
#             print("line_bit[1]: ", line_bit[1], "choice[1]: ", choice[1])
#             if choice[0] == line_bit[0]:
#                 if not line_bit[1] in choice[1]:
#                     return False
#         return True
#
#     def analyse_choice(self, choice, lines):
#         """
#         Looks at one property, one choice property, and analyses each line.
#         :param choice: # "chin_length", [1], 3]
#         :param lines: # ['cs10571477962556972748.csv', ['eye_angle', 1, 3], ['eye_lashes', 0, 2], ['eye_lid', 0, 2], ['chin_length', 1, 3], ['eyebrow_weight', 1, 2], ['eyebrow_shape', 1, 14], ['eyebrow_thickness', 0, 4], ['face_shape', 3, 7], ['facial_hair', 14, 15], ['hair', 87, 111], ['eye_color', 2, 5], ['face_color', 4, 11], ['hair_color', 2, 10], ['glasses', 11, 12], ['glasses_color', 5, 7], ['eye_slant', 0, 3], ['eyebrow_width', 1, 3], ['eye_eyebrow_distance', 1, 3]]
#         :return: True or False
#         """
#         print("analyse_choice:")
#         total_lines = []
#         # ---------------------
#         print("-----------------------")
#         for line in self.inner:
#             temp_line = line[1:]
#             questionable = self.helper(choice, temp_line)
#             print("questionable: ", questionable)
#             if questionable:
#                 total_lines.append(line)
#         print("Total Lines:")
#         [print(i) for i in total_lines]
#         return total_lines
#
#     def analyse_line(self, line):
#         'Determins whether a face is included given the criteria/choices.'
#         temp_line = line[1:]
#         for line_elem in temp_line:
#             for choice in self.choices:
#                 if line_elem[0] == choice[0]:
#                     # print(line_elem[1], choice[1])
#                     if not line_elem[1] in choice[1]:
#                         return False
#         return True
#
#     def applychoices(self):
#         lines = []
#         for line in self.inner:
#             if self.analyse_line(line):
#                 lines.append(line)
#         self.inner = lines
#         [print(i) for i in self.inner]
#         print(" ")
#         print("Number of elements: ", len(self.inner))
#
#     # def do_applychoices(self, arg):
#     #     new_lines = []
#     #     for property in FACE_PROPERTIES:
#     #         for line in self.inner:
#     #             self.analyse_property(property, line)
#     #     for fileline in self.inner:
#     #         if self.test_line(fileline):
#     #             print("test_line returned True")
#     #             new_lines.append(fileline)
#     #     self.inner = new_lines
#
#     def do_printchoices(self, arg):
#         for elem in self.choices:
#             print(elem)
#
#     def do_printfaces(self, arg):
#         for elem in self.inner:
#             print(elem)
#         print("Number of faces chosen: ", len(self.inner))
#
#     def do_listfaces(self, arg):
#         debugging = True
#         mylist = faces_possible(self.inner)
#         filenames = []
#         for elem in mylist:
#             filenames.append(elem[0])
#         if debugging == False:
#             for filename in filenames:
#                 self.open_image(filename)
#         else:
#             for fileline in mylist:
#                 print(fileline)
#             print("Number of faces: ", len(mylist))
#
#     def do_loaddefault(self, arg):
#         with open(DEFAULT_CHOICES, 'r') as f:
#             self.choices = json.load(f)
#         # self.applychoices()
#         for elem in self.choices:
#             print(elem)
#
#     def do_savetofile(self, arg):
#         with open(DEBUGGING_SAVE, "w") as f:
#             for elem in self.inner:
#                 f.write(elem[0])
#
#     def do_viewfaces(self, arg):
#         for elem in self.inner:
#             print("elem[0]: ", elem[0])
#             self.open_image(elem[0])
#
#     # def open_image(self, filename):
#     #     filename = filename[0:-3]
#     #     filename = "{}png".format(filename)
#     #
#     #     directory = "/Users/BigBlue/Downloads/cartoonset10k/"
#     #     filepath = os.path.join(directory, filename)
#     #     print(filepath)
#     #     img = mpimg.imread(filepath)
#     #     imgplot = plt.imshow(img)
#     #     plt.show()
#
#     # def do_bye(self, arg):
#     #     'Close the window and exit the program:  BYE'
#     #     print('Thank you for using {}!'.format(self.program_name))
#     #     self.close()
#     #     return True
#
#     def close(self):
#         if self.file:
#             self.file.close()
#             self.file = None
#
# # ===============================================================
# # ===============================================================
#
# # abc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
# #        "w", "x", "y", "z", "_"]
# # efg = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
# # myinclude = abc + efg
# hair_chars = []
#
# def display_finalists():
#     finalists = "/Users/BigBlue/Documents/Programming/Python/misc/data/finalists.txt"
#     # directory = "/Users/BigBlue/Downloads/cartoonset10k/"
#     with open(finalists, "r") as f:
#         mylist = f.readlines()
#         mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#     for filename in mylist:
#         open_image(filename)
#
# # def clean_string(astring):
# #     newstring = ""
# #     for elem in astring:
# #         if elem in myinclude:
# #             newstring += elem
# #     return newstring
# #
# # def is_number(astring):
# #     try:
# #         int(astring)
# #         return True
# #     except:
# #         return False
#
# # def parse_line(list_line):
# #     newlist = []
# #     output_list = []
# #     for elem in list_line:
# #         newlist = elem.split(",")
# #         new_string = ""
# #         this_list = []
# #         for elem2 in newlist:
# #             cleaned_string = clean_string(elem2)
# #             if is_number(cleaned_string):
# #                 this_list.append(int(cleaned_string))
# #             else:
# #                 this_list.append(cleaned_string)
# #         output_list.append(this_list)
# #     newlist.append(output_list)
# #     return output_list
#
# # def open_image(filename):
# #     filename = filename[0:-3]
# #     filename = "{}png".format(filename)
# #
# #     directory = "/Users/BigBlue/Downloads/cartoonset10k/"
# #     filepath = os.path.join(directory, filename)
# #     print(filepath)
# #     img = mpimg.imread(filepath)
# #     imgplot = plt.imshow(img)
# #     plt.show()
#
# def test_face_char(face_list, characteristic, value):
#     print(face_list)
#     if face_list[0] == characteristic:
#         if face_list[1] == value:
#             return True
#     return False
#
# def test_face(face):
#     global hair_chars
#     for facial_characteristic in face:
#         # if facial_characteristic[0] == "hair":  # 0 to 110
#         #     # hair_chars.append(facial_characteristic[1])
#         #     if facial_characteristic[1] != 50:
#         #         return False
#         if facial_characteristic[0] == "facial_hair":
#             if facial_characteristic[1] != 14:
#                 return False
#         # if facial_characteristic[0] == "eye_color":
#         #     if facial_characteristic[1] in [0, 1, 4]:
#         #         return False
#         if facial_characteristic[0] == "face_color": # 0 to 10
#             if facial_characteristic[1] != 8:
#                 return False
#         if facial_characteristic[0] == "face_shape": # 0 to 6
#             if facial_characteristic[1] != 5:
#                 return False
#         if facial_characteristic[0] == "hair_color":
#             if facial_characteristic[1] in [0,1,2,3,4,5,7,8,9]:
#                 return False
#         if facial_characteristic[0] == "eyebrow_width":
#             if facial_characteristic[1] in [1,2]:
#                 return False
#     return True
#
# def test_face02(face, choices):
#     global hair_chars
#     for facial_characteristic in face:
#         for choice in choices:
#             if facial_characteristic[0] == choice[0]:  # 0 to 110
#                 if not facial_characteristic[1] in choice[1]:
#                     return False
#     return True
#
# def viewing_a_face():
#     filepath = "/Users/BigBlue/Downloads/cartoonset10k"
#     all_files = os.listdir(filepath)
#     output_list = []
#     for filename in all_files:
#         extension = filename[-3:]
#         if extension == "png":
#             continue
#         new_path = os.path.join(filepath, filename)
#         # print(new_path)
#         with open(new_path, "r") as f:
#             mylist = f.readlines()
#             mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#         parsed_list = parse_line(mylist)
#         parsed_list.insert(0, filename)
#         output_list.append(parsed_list)
#     # -----------------------------------------
#     mylist = []
#     for elem in output_list:
#         if test_face(elem):
#             open_image(elem[0])
#             print(elem)
#             # sys.exit()
#     print(hair_chars)
#         # for elem1 in elem:
#         #     if not test_face_char(elem1, "facial_hair", 14):
#         #         pass
#         #     else:
#         #
#         #     if test_face_char(elem1, "eye_color", 4):
#         #         print("Yes")
#         #         open_image(elem[0])
#     # mylist = list(set(mylist))
#     # print(mylist)
#         # print(elem[14]) # glasses
#         # print(elem[11]) # eye_color
#         # open_image(elem[0])
#         # for counter, elem1 in enumerate(elem):
#         #     print(counter, elem1)
#
# def faces_possible(choices):
#     filepath = "/Users/BigBlue/Downloads/cartoonset10k"
#     all_files = os.listdir(filepath)
#     output_list = []
#     for filename in all_files:
#         extension = filename[-3:]
#         if extension == "png":
#             continue
#         new_path = os.path.join(filepath, filename)
#         # print(new_path)
#         with open(new_path, "r") as f:
#             mylist = f.readlines()
#             mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#         parsed_list = parse_line(mylist)
#         parsed_list.insert(0, filename)
#         output_list.append(parsed_list)
#     # -----------------------------------------
#     return output_list
#     # mylist = []
#     # print(len(output_list))
#     # for elem in output_list:
#     #     if test_face02(elem, choices):
#     #         mylist.append(elem)
#     #         # sys.exit()
#     # return mylist
#         # for elem1 in elem:
#         #     if not test_face_char(elem1, "facial_hair", 14):
#         #         pass
#         #     else:
#         #
#         #     if test_face_char(elem1, "eye_color", 4):
#         #         print("Yes")
#         #         open_image(elem[0])
#     # mylist = list(set(mylist))
#     # print(mylist)
#         # print(elem[14]) # glasses
#         # print(elem[11]) # eye_color
#         # open_image(elem[0])
#         # for counter, elem1 in enumerate(elem):
#         #     print(counter, elem1)
#
#
# def main():
#     filepath = "/Users/BigBlue/Downloads/cartoonset10k"
#     all_files = os.listdir(filepath)
#     output_list = []
#     for filename in all_files:
#         extension = filename[-3:]
#         if extension == "png":
#             continue
#         new_path = os.path.join(filepath, filename)
#         # print(new_path)
#         with open(new_path, "r") as f:
#             mylist = f.readlines()
#             mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
#         parsed_list = parse_line(mylist)
#         parsed_list.insert(0, filename)
#         output_list.append(parsed_list)
#     # -----------------------------------------
#     mylist = []
#     for elem in output_list:
#         for elem1 in elem:
#             if elem1[0] == "hair":
#                 print(elem1)
#                 mylist.append(elem1[1])
#     mylist = list(set(mylist))
#     print(mylist)
#         # print(elem[14]) # glasses
#         # print(elem[11]) # eye_color
#         # open_image(elem[0])
#         # for counter, elem1 in enumerate(elem):
#         #     print(counter, elem1)
#
# def get_choices():
#     facial_specs = []
#     facial_specs.append(["eye_color", [2,3]]) # 0 to 4 ; 0 --> brown, 2 --> green, 3 --> gray
#     facial_specs.append(["face_color", [4,5,6,7,8]]) # 0 to 10 ; 8 --> my shade
#     facial_specs.append(["face_shape", [0,1,2,3,4,5,6]]) # 0 to 6 ; 5 -- me.
#     facial_specs.append(["hair_color", [5,6,7]]) # 0 to 9 ; 1 --> blond, 2 --> light red, 3 --> red, 5 --> light brown, 6 --> darkish brown 7 --> darkest brown, 8 --> gray
#     facial_specs.append(["facial_hair", [14]]) # 0 to 14 ; 14 = no hair
#     facial_specs.append(["glasses_color", [0,1,2,3,4,5,6]])  # 0 to 6 ;
#     facial_specs.append(["glasses", [0,3,5,6,7,9,11]])  # 0 to 11 ; 5 --> round, 6 --> normal, 7 --> round & thin, 8 --> cat, 9 --> round, 10 --> heart, 11 --> no glasses
#     mylist = faces_possible(facial_specs)
#     filenames = []
#     for elem in mylist:
#         filenames.append(elem[0])
#     for filename in filenames:
#         open_image(filename)
#
# if __name__ == "__main__":
#     # display_finalists()
#     # myimages = read_in_images()
#     # for elem in myimages:
#     #     print(elem)
#     MyShell().cmdloop()
#
