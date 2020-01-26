from myclasses import MyShell
import utils

def main():
    s = "Select Images (s)\nView Images (v)\n"
    print(s)
    user_input = input("> ").strip().lower()
    print("You typed: ", user_input)
    if user_input == "s":
        MyShell().cmdloop()
    elif user_input == "v":
        utils.viewfaces()
    else:
        print("That input was not recognized: {}".format(user_input))

if __name__ == "__main__":
    main()
