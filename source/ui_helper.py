"""Module that contains general-purpose functions for ui functionality
    
    Author: Ben Shirley
    Date: 29 Oct 2023
"""
import datetime as datetime

def get_confirmation() -> bool:
    """gets user to confirm whether they want to proceed"""
    user_input = input('(y/n) : ')
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    else:
        print('Invalid input, try again')
        return get_confirmation()

def get_valid_datetime(message):
    """prompts the user for a valid datetime expression,
    otherwise prompts them again"""
    
    print("please enter date in dd-mm-yyyy")
    date = input(message)
    if date == '-':
        return None
    try:
        date = datetime.datetime(day=int(date[0:2]), month=int(date[3:5]), year=int(date[6:10]))
        return date
    except ValueError:
        print("Invalid Format, please try again.")
        return get_valid_datetime(message)

def get_natural_number(message: str) -> int:
    number = input(message)
    try:
        number = int(number)
        if number < 0:
            raise ValueError
        return number
    except ValueError:
        print("That was not a valid number!")
        return get_natural_number(message)

def display_new_screen_ribbon():
    """prints a banner for moving to a new screen"""
    print('')
    print('')
    print('-' * 30)
    print('')
    
