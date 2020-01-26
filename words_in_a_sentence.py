sentence = "Some of the owner men were kind because they hated what they had to do, and some of them were angry because they hated to be cruel, and some of them were cold because they had long ago found that one could not be an owner unless one were cold."

def main():
    mylist = sentence.split(" ")
    # [print(i) for i in mylist]
    print("Number of words in sentence: {}".format(len(mylist)))

if __name__ == "__main__":
    main()