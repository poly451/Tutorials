import random
import sys

TOP_NUMBER = 20

def goodbye():
    print("Goodbye! Thanks for playing.")
    sys.exit()

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def is_valid(mystring):
    if not is_int(mystring): return False
    elif int(mystring) < 1: return False
    elif int(mystring) > TOP_NUMBER: return False
    return True

def evaluate_guess(chosen_number, guess, number_of_tries):
    if guess == chosen_number:
        print("Correct! You guessed the number in {} guesses.".format(number_of_tries))
        return False
    elif guess > chosen_number:
        print("The number I am thinking of is LOWER than {}.".format(guess))
        return True
    elif guess < chosen_number:
        print("The number I am thinking of is HIGHER than {}.".format(guess))
        return True

def get_guess():
    user_guess = ""
    while not is_valid(user_guess):
        user_guess = input("> ").lower().strip()
        if user_guess == "quit": goodbye()
    return int(user_guess)

def main():
    chosen_number = random.randint(1, TOP_NUMBER)
    print("I am thinking of a number between 1 and {}. What is the number?".format(TOP_NUMBER))
    continue_looping = True
    number_of_tries = 0
    while continue_looping:
        number_of_tries += 1
        user_choice = get_guess()
        continue_looping = evaluate_guess(chosen_number, user_choice, number_of_tries)
    goodbye()

if __name__ == "__main__":
    main()
