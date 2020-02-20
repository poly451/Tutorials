# This program lives in:
# /Users/BigBlue/Documents/Programming/Python/utilities
import os, sys
from datetime import datetime, timedelta

# sys.path.append('/Users/BigBlue/Documents/Programming/Python/utilities')

def findDirectory_helper(startingDirectory, targetdir):
    numberOfDirectories = 0
    #startingDirectory = os.environ.get('HOME')
    os.chdir(startingDirectory)
    #print(dir(os))
    #print(os.listdir())
    returnList = []
    for dirpath, dirnames, filenames in os.walk(startingDirectory):
        # print("dirpath: {}".format(dirpath))
        #print("dirnames: {}".format(dirnames))
        #print("filenames: {}".format(filenames))
        numberOfDirectories += 1
        for dirname in dirnames:
            if targetdir in dirname:
                returnList.append(os.path.join(dirpath, dirname))
    return returnList

def findDirectory(targetdir, startingDirectory):
    # startingDirectory = os.getcwd()
    # ----------
    print("Searching ({}) for DIRECTORY ({}).".format(startingDirectory, targetdir))
    dirsFound = findDirectory_helper(startingDirectory, targetdir)
    print("{} paths found.".format(len(dirsFound)))

    print("target directory: {}".format(targetdir))
    #print("starting directory: {}".format(startingDirectory))
    if len(dirsFound) > 0:
        print("DIRECTORY FOUND!!! :-)")
        print("path(s) to directory:")
        for mystring in dirsFound:
            print(mystring)
    else:
        print("target directory ({}) was NOT found.".format(targetdir))

# ----------------------------------------------------------------

def findFile_helper(startingDirectory, targetFile):
    #print("startingDirectory: {}".format(startingDirectory))
    #print("targetFile: ".format(targetFile))
    numberOfFiles = 0
    #startingDirectory = os.environ.get('HOME')
    os.chdir(startingDirectory)
    #print(dir(os))
    #print(os.listdir())
    filelist = []
    for dirpath, dirnames, filenames in os.walk(startingDirectory):
        #print("dirpath: {}".format(dirpath))
        #print("dirnames: {}".format(dirnames))
        #print("filenames: {}".format(filenames))
        for afile in filenames:
            if targetFile in afile:
                filelist.append(os.path.join(dirpath, afile))

    if len(filelist) > 0:
        return True, filelist
    return False, ""

def findFile(targetFile, startingDirectory):
    print("Searching ({}) for FILE ({}).".format(startingDirectory, targetFile))
    targetFound, filepaths = findFile_helper(startingDirectory, targetFile)

    #print("path to file: {}".format(filepath))
    #print("starting directory: {}".format(startingDirectory))
    if targetFound == True:
        print("FILE FOUND!!! :-)")
        print("{} File(s) found:".format(len(filepaths)))
        [print(i) for i in filepaths]
    else:
        print("target file ({}) was NOT found.".format(targetFile))

# ----------------------------------------------------------------

def findRecent_helper(startingDirectory="/Users/BigBlue/Documents", past_date=2):
    print("startingDirectory: {}".format(startingDirectory))
    print("past_date: {}".format(past_date))
    print("searching ...")
    # -- Debugging --
    all_files = []
    # ---------------
    os.chdir(startingDirectory)
    filelist = []
    files_examined = []
    num_possible_files = 0
    num_files_examined = 0
    for dirpath, dirnames, filenames in os.walk(startingDirectory):
        # print("dirpath: {}".format(dirpath))
        # print("dirnames: {}".format(dirnames))
        # print("filenames: {}".format(filenames))
        for afile in filenames:
            all_files.append(afile)
            num_possible_files += 1
            try:
                # if os.path.isfile(os.path.join(dirpath, afile)):
                #     pass
                # last_mod = os.stat(afile).st_mtime
                myfile = os.path.join(dirpath, afile)
                # print("afile: {}".format(myfile))
                last_mod = os.path.getmtime(myfile)
                files_examined.append(afile)
                num_files_examined += 1
            except:
                continue
            last_mod = datetime.fromtimestamp(last_mod)
            if last_mod > past_date:
                filelist.append(os.path.join(dirpath, afile))
    print("-----------------------------------------------")
    print("Files that could have been examined: {}".format(num_possible_files))
    print("True num of files that could have been examined: {}".format(len(all_files)))
    print("Num of files examined: {}".format(len(files_examined)))
    print("Num of files returned: {}".format(len(filelist)))
    # print("&&&&&&&&&&& begin debugging: &&&&&&&&&&&&&&")
    # print("---- Debugging: Files that could have been examined: ----")
    # [print(i) for i in all_files]
    # print("---- Debugging: Files that were examined: ----")
    # [print(i) for i in files_examined]
    # print("&&&&&&&&&&& end debugging: &&&&&&&&&&&&&&")
    return filelist

def findRecent(time_in_past, startingDirectory="/Users/BigBlue"):
    """Gets a number of files that fall within a certain timeframe."""
    if type(time_in_past) == type("s"):
        time_in_past = int(time_in_past)
    currentDirectory = os.getcwd()
    # startingDirectory = "/Users/BigBlue/Documents/Programming/Python/games"
    # startingDirectory = "/Users/BigBlue/Documents/Programming/Python/games/game_of_life/"
    # --------------------------------------------------
    time_now = datetime.now()
    mytimedelta = timedelta(hours=time_in_past)
    past_date = time_now - mytimedelta
    # --------------------------------------------------
    print("Searching ALL FILES in DIRECTORY ({}) for files that were last modified within the last ({}) hours.".format(startingDirectory, time_in_past))
    print("Past date:{}".format(past_date))
    filepaths = findRecent_helper(startingDirectory, past_date)
    if len(filepaths) > 0:
        print("*****************************************************************************")
        print("Within directory: {}".format(startingDirectory))
        print("{} files were accessed within the last {} hours.".format(len(filepaths), time_in_past))
        [print(i) for i in filepaths]
        print("*****************************************************************************")
    else:
        print("No files were found.")

# ========================================================
# ========================================================

def main(switch, name, starting):
    accepted_switches = ["-f", "-d", "-t"]
    if switch == "-f":
        findFile(name, starting)
    elif switch == "-d":
        findDirectory(name, starting)
    elif switch == "-t":
        findRecent(name, starting)
    else:
        sys.exit("Input ({}) not recognized. Must be one of ({})".format(switch, accepted_switches))


if __name__=="__main__":
    startingDirectory = "/Users/BigBlue/Downloads"
    # startingDirectory = "/Users/BigBlue/Documents/Programming/Python"
    # startingDirectory = "/Users/BigBlue/Documents/Programming/Python/graphics/pygame/hello_world_programs"
    # startingDirectory = "/Users/BigBlue/Documents/Programming/Python/graphics/pygame/hello_world_programs"
    mystring = """
    This program walks the directory structure, starting from the given
    directory, and finds either the file name or the given directory name {}
    if it exists.
    Examples:
    >python py.py -d <directory name> <starting directory>
    >python py.py -f <filename> <starting direcctory>
    >python py.py -t <how many files to return> <date/time>
    >python py.py -t 20 /
    """.format(startingDirectory)

    arg1 = "-t"
    arg2 = "20" # return, at most, 10 files
    arg3 = 3 # last 24 hours

    # time_now = datetime.now()
    # mytimedelta = timedelta(hours=24)
    # #  year, month, day, hour, minute, second, microsecond, and tzinfo.
    # # past_date = datetime(2019, 6, 16, 9, 27, 28)
    # past_date = time_now - mytimedelta
    # print(past_date)

    main(arg1, arg2, arg3)
