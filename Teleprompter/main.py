from myclasses import StrangeTeleprompter
from dialog import GetFilepathDialog
import sys, os

def main():
    get_filepath = GetFilepathDialog()
    filepath = get_filepath.main()
    # ----------------------
    # Checking to make sure it's a valid filepath
    if filepath[-1] == "/":
        s = "That's not a valid path!"
        sys.exit(s)
    # ----------------------
    teleprompter = StrangeTeleprompter(filepath)
    teleprompter.main()

if __name__ == "__main__":
    main()
