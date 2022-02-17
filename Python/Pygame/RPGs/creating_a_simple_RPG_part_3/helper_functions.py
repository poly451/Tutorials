from dialogs import DialogInput_New

# *******************************************************

def main():
    choices = ["LPC humanoid spritesheet --> lists"]
    choices += ["Exit/Quit"]
    # ---- ----
    dialog_list = ["{}) {}".format(count+1, i) for count, i in enumerate(choices)]
    possible_responses = list(range(1, len(choices)+1))
    mydialog = DialogInput_New(dialog_list, possible_responses)
    user_choice = mydialog.main()
    user_index = int(user_choice)-1
    print(choices[user_index])
    choice = choices[user_index]
    # ---- ---- ---- ----
    if choice == "LPC humanoid spritesheet --> lists":
        # This function reads a spritesheet into memory,
        # displays it and allows the user to save it
        # as lists. The command is: save base
        import spritesheet_to_lists
        spritesheet_to_lists.main()
    elif choice == "Exit/Quit":
        pass
    else:
        s = "I don't recognize this: {}".format(choice)
        raise ValueError(s)

if __name__ == "__main__":
    main()