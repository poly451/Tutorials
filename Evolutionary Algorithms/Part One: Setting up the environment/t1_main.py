"""
This program simply loads the environment.
"""
from t1_classes import Game
import t1_constants as con

def main():
    mygame = Game(con.ENVIRONMENT_VARIABLE)
    mygame.main()

if __name__ == "__main__":
    main()
