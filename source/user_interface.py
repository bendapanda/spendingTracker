"""
    Module that provides the user interface for the overall program

    Author: Ben Shirley
    Date: 29 Oct 2023
"""
from enum import Enum
import pandas as pd
import numpy as np
import spending_tracker as tracker
import ui_helper
from transaction_structure import HEADER

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

def display_welcome():
    """prints welcome message to the screen"""
    print(f"""Hello World!
          Welcome to Ben's spending analyser program!
          At any time enter '{BACKSTR}' to go back and '{QUITSTR}' to exit the application entierly.""")

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
        "Display general info" : tracker.display_general_info,
        "get payment methods" : tracker.get_spending_types,
        "plot spending by time" : tracker.plot_spending_by_time,
        "perform classification" : tracker.prompt_for_spending_types,
        "analyse segment of the data": section_data_screen,
        "save data" : tracker.save_data,
        "combine this data with another file" : None,
        "Add metadata": None
    }

    keys = list(options.keys())
    for i in range(len(options.keys())):
        print(f"({i}) : {keys[i]}")
    print("(q) : back")
    print("(q!) : quit")
    print("")
    # verify input
    user_input = get_input("Where to?: ")
    if user_input.status == UserAction.BACK:
        return UserAction.BACK
    elif user_input.status == UserAction.QUIT:
        return UserAction.QUIT
    
    try:
        user_input = int(user_input.message)
        if(user_input < 0 or user_input >= len(options.keys())):
            raise ValueError
    except ValueError:
        print("That wasn't part of the list!")
        options_screen(data)
        return
     
    # run the selected option
    if options[keys[user_input]] != None:
        res = options[keys[user_input]](data)
        if res == UserAction.QUIT:
            return UserAction.QUIT
    else:
        print("feature not yet implemented :()")
    input("press any key to continue...")
    print("")
    options_screen(data)
        
    


    
def get_user_file() -> pd.DataFrame:
    """prompts the user to enter the name of the file they want to analyse
    TODO: ensure file is in the correct format
    """
    response = get_input("Please enter the name of the file you want to analyse: ")
    if response.status == UserAction.VALID:
        filename = response.message
        extension = filename.split('.')[-1]
        if extension == "csv":
            try:
                data = pd.read_csv(filename)
                data = tracker.format_data(data)
                return data, UserAction.VALID
            except FileNotFoundError:
                print("We couldn't find that file, try again")
                return get_user_file()
        elif extension == "xlsx":
            try:
                data = pd.read_excel(filename)
                data = tracker.format_data(data)
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
    
def combine_two_files(data: pd.DataFrame) -> pd.DataFrame:
    """prompts the user for another file, combines it with the given file,
    and then combines the two, returning a new options menu with the new data"""
    print("Choose a dataset to combine with this one!")
    file_to_combine_with = get_user_file()

def get_file_metadata(data: pd.DataFrame):
    """prompts the user to input metadata such as the account number, the name of the bank account,
    the current balance of the file, et cetera"""

def get_input(propmt: str) -> UserResponse:
    """prompts the user for input, and checks if they want to quit"""
    user_input = input(propmt)
    if user_input == QUITSTR:
        return UserResponse(user_input, UserAction.QUIT)
    elif user_input == BACKSTR:
        return UserResponse(user_input, UserAction.BACK)
    else:
        return UserResponse(user_input, UserAction.VALID) 

def section_data_screen(data):
    """UI function to guide the user through the process of cutting up their data"""
    ui_helper.display_new_screen_ribbon()
    print("Welcome to the data partitioning menu!")
    print("please choose how you would like to section your data:")

    options = {
        "get spends only" : get_spends_only,
        "get balance increases only": get_balance_increases_only,
        "trim data based on transaction type": trim_data_based_on_transaction_type,
        "trim data based on date (super buggy)": trim_by_date,
        "trim data based on classification": None
    }

    keys = list(options.keys())
    for i in range(len(keys)):
        print(f"({i}) : {keys[i]}")
    print("(q) : back")
    print("(q!) : quit")
    print("")
    # verify input
    user_input = get_input("Where to?: ")
    if user_input.status == UserAction.BACK:
        return UserAction.BACK
    elif user_input.status == UserAction.QUIT:
        return UserAction.QUIT
    
    try:
        user_input = int(user_input.message)
        if(user_input < 0 or user_input >= len(options.keys())):
            raise ValueError
    except ValueError:
        print("That wasn't part of the list!")
        section_data_screen(data)
        return section_data_screen(data)
     
    # run the selected option
    if options[keys[user_input]] != None:
        action = options[keys[user_input]](data)
        if action == UserAction.QUIT:
            return UserAction.QUIT
    else:
        print("feature not yet implemented :()")
    input("press any key to continue...")
    print("")
    section_data_screen(data)

def trim_by_date(data):
    """prompts the user for a date they would like to trim the data by, then takes them to
    a new options screen
    TODO: This is super buggy at the moment, please do not use!
    """
    ui_helper.display_new_screen_ribbon()
    print(f"This data stretches between {data[HEADER.DATE].min()} and {data[HEADER.DATE].max()}")
    start_date = ui_helper.get_valid_datetime("Select starting date (input '-' to select no date).")
    end_date = ui_helper.get_valid_datetime("Select end date (input '-' to select no end date)")
    if start_date == None:
        start_date = data[HEADER.DATE].min()
    if end_date == None:
        end_date = data[HEADER.DATE].max()
    
    start_date = np.datetime64(start_date)
    end_date = np.datetime64(end_date)
    print("\nTrimming data:\n")
    print(data[HEADER.DATE].min(), data[HEADER.DATE].max())
    new_data = data.loc[(data[HEADER.DATE] >= start_date) & (data[HEADER.DATE] <= end_date)]
    return options_screen(new_data)


def get_spends_only(data):
    """takes the user to an options screen with a new dataset (spends only)"""
    ui_helper.display_new_screen_ribbon()
    print("sectioning data into only your spends:")
    sectioned_data = data[data[HEADER.QUANTITY] < 0]
    return options_screen(sectioned_data)

def get_balance_increases_only(data):
    """Takes the user to an oprions screen with only data increases"""
    ui_helper.display_new_screen_ribbon()
    print("sectioned data into only balance increases!")
    section_data = data[data[HEADER.QUANTITY >=0 ]]
    return options_screen(section_data)

def trim_data_based_on_transaction_type(data):
    """prompts the user for what transaction types they want to choose,
      then cuts the data accordingly"""
    
    ui_helper.display_new_screen_ribbon()
    print("Chose what transaction types you wish to restrict the data to:")
    transaction_types = data[HEADER.SPEND_TYPE].unique()
    for i in range(len(transaction_types)):
        print(f"({i}) : {transaction_types[i]}")
    print("Enter the numbers of the transaction types you want to choose, seperated by commas")
    user_input = input(": ")
    choices = user_input.split(',')
    results = []
    try:
        for choice in choices:
            results.append(int(choice))
    except ValueError:
        print("Invalid input, please try again")
        return
    
    new_data = data[data[HEADER.SPEND_TYPE].isin(results)]
    return options_screen(new_data)

    
if __name__ == "__main__":
    user_interface()
