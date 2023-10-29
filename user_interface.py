"""
    Module that provides the user interface for the overall program

    Author: Ben Shirley
    Date: 29 Oct 2023
"""
from enum import Enum
import pandas as pd

QUITSTR = 'q!'
BACKSTR = 'q'

class UserAction(Enum):
    """Possible actions a user can take"""
    VALID = 1
    BACK = 2
    QUIT = 3

class UserResponse:
    """
    Defines a user response object. 

    Parameters:

    Methods
    """

    def __init__(self, message: str, action: UserAction):
        self.message = message
        self.status = action


def user_interface():
    """commandline interface for analysing bank details"""
    display_welcome()
    print("To get started, enter the name of the file you want to analyse")

    # prompt user for data, take action accordingly
    data, action = get_user_file()
    if action == UserAction.QUIT:
        return
    elif action == UserAction.BACK:
        user_interface()
        return
    
    # now display options for what we want to do with that data
    print("great!, now what would you like to do with this data?")
    options_screen(data)
    
    


def options_screen(data):
    """runs the options_screen for the application"""
    options = {
        "perform classification" : None,
        "graph amounts spent": None,
        "graph spending by week": None,
    }

    keys = list(options.keys())
    for i in range(len(options.keys())-1):
        print(f"({i}) : {keys[i]}")
    print("(q) : back")
    print("(q!) : quit")
    print("")
    # verify input
    user_input = get_input("Where to?: ")
    if user_input.status == UserAction.BACK:
        user_interface()
        return
    elif user_input.status == UserAction.QUIT:
        return
    
    try:
        user_input = int(user_input.message)
        if(user_input < 0 or user_input >= len(options.keys())):
            raise ValueError
    except ValueError:
        print("That wasn't part of the list!")
        options_screen(data)
        return
     
    # run the selected option
    options[keys[user_input]](data)
    options_screen()
        
    


    

def display_welcome():
    """prints welcome message to the screen"""
    print(f"""Hello World!
          Welcome to Ben's spending analyser program!
          At any time enter '{BACKSTR}' to go back and '{QUITSTR}' to exit the application entierly.""")

def get_user_file() -> pd.DataFrame:
    """prompts the user to enter the name of the file they want to analyse"""
    response = get_input("Please enter the name of the file you want to analyse: ")
    if response.status == UserAction.VALID:
        filename = response.message
        extension = filename.split('.')[-1]
        if extension == "csv":
            try:
                data = pd.read_csv(filename)
                return data, UserAction.VALID
            except FileNotFoundError:
                print("Soomething went wrong, try again")
                return get_user_file()
        elif extension == "xlsx":
            try:
                data = pd.read_excel(filename)
                return data, UserAction.VALID
            except FileNotFoundError:
                print("We couldn't find that file, try again")
                return get_user_file()
        else:
            print("We don't seem to support that type of file. Please try again")
            return get_user_file()
    elif response.status == UserAction.BACK:
        return None, UserAction.BACK
    elif response.status == UserAction.QUIT:
        return None, UserAction.QUIT

def get_input(propmt: str) -> UserResponse:
    """prompts the user for input, and checks if they want to quit"""
    user_input = input(propmt)
    if user_input == QUITSTR:
        return UserResponse(user_input, UserAction.QUIT)
    elif user_input == BACKSTR:
        return UserResponse(user_input, UserAction.BACK)
    else:
        return UserResponse(user_input, UserAction.VALID) 