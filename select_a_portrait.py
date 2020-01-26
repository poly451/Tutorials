# import os, sys
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
#
# abc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
#        "w", "x", "y", "z", "_"]
# efg = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
# myinclude = abc + efg
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
# def clean_string(astring):
#     newstring = ""
#     for elem in astring:
#         if elem in myinclude:
#             newstring += elem
#     return newstring
#
# def is_number(astring):
#     try:
#         int(astring)
#         return True
#     except:
#         return False
#
# def parse_line(list_line):
#     newlist = []
#     output_list = []
#     for elem in list_line:
#         newlist = elem.split(",")
#         new_string = ""
#         this_list = []
#         for elem2 in newlist:
#             cleaned_string = clean_string(elem2)
#             if is_number(cleaned_string):
#                 this_list.append(int(cleaned_string))
#             else:
#                 this_list.append(cleaned_string)
#         output_list.append(this_list)
#     newlist.append(output_list)
#     return output_list
#
# def open_image(filename):
#     filename = filename[0:-3]
#     filename = "{}png".format(filename)
#
#     directory = "/Users/BigBlue/Downloads/cartoonset10k/"
#     filepath = os.path.join(directory, filename)
#     print(filepath)
#     img = mpimg.imread(filepath)
#     imgplot = plt.imshow(img)
#     plt.show()
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
#     mylist = []
#     print(len(output_list))
#     for elem in output_list:
#         if test_face02(elem, choices):
#             mylist.append(elem)
#             # sys.exit()
#     return mylist
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
# def read_in_images():
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
#     return output_list
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
#     myimages = read_in_images()
#     print("There are {} images.".format(len(myimages)))