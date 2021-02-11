"""
This program simply loads the environment.
"""
import sys, os
from t1_classes import Game
import t1_utils
import t1_constants as con

def main():
    mygame = Game(con.ENVIRONMENT_VARIABLE)
    mygame.do_loop()

if __name__ == "__main__":
    main()
