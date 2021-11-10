import tutorial_01, tutorial_02, tutorial_03, tutorial_04, tutorial_05, tutorial_06, tutorial_07


def main():
    mychoice = "tutorial_03"
    # ----
    if mychoice == "tutorial_01":
        """Graphic moves smoothly in all directions"""
        tutorial_01.main()
    elif mychoice == "tutorial_02":
        """Graphic takes discrete steps"""
        tutorial_02.main()
    elif mychoice == "tutorial_03":
        """Graphic takes discrete steps on a grid"""
        tutorial_03.main()
    elif mychoice == "tutorial_04":
        """Added animation to the graphic, but lost discrete step"""
        tutorial_03.main()
    elif mychoice == "tutorial_05":
        """
        Added an environment (a grid background) to the graphic, but lost discrete step
        Implemented Obstacles. Implmented two directions, left and right.
        """
        tutorial_04.main()
    elif mychoice == "tutorial_06":
        """
        Implemented Obstacles.
        Implemented walking and idling.
        Implemented a discrete step.
        Want to implemented modes: idle, jump, slide, walk, dead
        """
        tutorial_05.main()
    elif mychoice == "tutorial_07":
        """
        Implementing modes: idle, jump, slide, walk, dead
        """
        tutorial_06.main()
    elif mychoice == "tutorial_08":
        """ Done! """
        tutorial_07.main()
    else:
        raise ValueError("Error")

if __name__ == "__main__":
    main()