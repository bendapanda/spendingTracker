"""
This is the main file for my spending tracker app.

- Things I need to be able to do:
Classify what different entries mean,
Store stuff in a database
Track my total funds over time

- compile information from multiple accounts into one mega balance

For example, I need to be able to dump all the data in, and then classify the different types of data

@author Ben Shirley
@date 27 Oct 2023
"""
import pandas as pd
import matplotlib.pyplot as plt
import glob

from transaction_structure import HEADER
import classification as classifier
import ui_helper as ui_helper
FILENAME = "transactions-year.csv"

PERSONAL_SPENDING_TYPES = ["Rent", "Bills", "Flat things",
                           "Groceries", "work payments", ""]

def get_valid_classifier_input(max_int) -> str:
    """prompts the user to enter a valid integer or '-' with value less than equal to the 
    max allowable integer"""
    choice  = input(" : ")
    try:
        if choice == '-':
            return choice
        else:
            int_choice = int(choice)
            return choice
    except ValueError:
        print("Invalid input, please try again.")
        return get_valid_classifier_input()


def prompt_for_spending_types(data):
    """ask user to list the types of things they spend money on.
    then perfroms k-means classification and asks the user to assign them 

    parameters:
        data: the data to be classified

    returns:
        new_data, the data together with a labeled classification column
    
    TODO: figure out how many catagories the data should be split into automatically
    TODO: add invalid input catching
    """
    print("Welcome to the data classification menu. Would you like to run a test for the ideal number of partitions?")
    if ui_helper.get_confirmation():
        # run elbow method, but without graph
        k = classifier.elbow_method_for_number_clusters()
    else:
        k = ui_helper.get_natural_number("How many partitions should your data be split into?")
        

    print("Label the catagories of things that you spend money on (type q to stop):\n")
    catagories = []
    
    new_data, inertia = classifier.perform_k_prototypes_clustering(data, 6)

    mapping = {}
    for catagory in new_data["classification"].unique():
        print("Please assign a label to spends that look like this:\n")
        print(data[data["classification"] == catagory].head(15))
        for i in range(len(catagories)):
            print(f"{catagories[i]}: {(i)}")
        for i in range(len(catagories)):
            print(f"{catagories[i]}: ({i})")
        print("New: (-)")
        choice = get_valid_classifier_input()
        if choice == "-":
            catagories.append(input("enter a new catagory: "))
            mapping[catagory] = catagories[-1]
        else:
            choice = int(choice)
            mapping[catagory] = catagories[choice]
    
    new_data["classification"] = new_data["classification"].replace(mapping)

    return new_data


def get_spending_types(data):
    """
    gets the types of spending that are present in the data

    parameters:
        data: the data to be analysed
    returns:
         a 1-d numpy array containing the unique types of spending that occured
    """
    return data[HEADER.SPEND_TYPE].unique()

def get_total_spending_per_day(data):
    """
    returns the total amount spent on each day
    parameters:
        data: The data to be analysed
    returns:
        a new dataset of the form date, quantity which describes how much was spent on any set day"""
    daily_spendings = data.groupby(HEADER.DATE)[HEADER.QUANTITY].sum().to_frame()
    daily_spendings.index.name = HEADER.DATE
    daily_spendings.reset_index(inplace=True)
    return daily_spendings


def plot_spending_by_time(data):
    """
    Takes in a set of data, and plots the spending of it by time
    """
    data.set_index(HEADER.DATE, inplace=True)
    data[HEADER.QUANTITY].plot(figsize=(10, 8), legend=True)
    plt.xlabel("Date")
    plt.ylabel("Quantity")
    plt.axes = True
    plt.title("Spending over time")
    plt.show()

def display_weekly_spending(data):
    """displays a time series that displays spending by week"""
    pass

def save_data(data: pd.DataFrame) -> None:
    """saves a data file as a .csv file for easy retreval at a later date"""
    filename = "../data/" + input("Please enter the name your file should be saved as: ") + ".csv"
    file_exists = glob.glob(filename)
    if not file_exists:
        data.to_csv(filename)
        print("File saved!")
    else:
        print("This file already exists! Are you sure you want to replace it?")
        if ui_helper.get_confirmation():
            data.to_csv(filename)
            print("File saved!")
    return




def display_spending_quantity_by_type(data, spend_type):
    """
    Displays the spending amounts of data with the specified spend_type.\n

    PARAMETERS:
    data: pandas Dataframe
    spend_type: String
    """
    data.loc[data[HEADER.SPEND_TYPE] == spend_type, HEADER.QUANTITY].plot(kind="hist", figsize=(10,8),
                                                                    title=f"Spendings of type {spend_type}",
                                                                    legend=True,
                                                                    label=spend_type)

def display_general_info(data):
    """funciton that prints information about a csv spending file""" 
    print(data.info())
    print(data.head())

    spending_types = data[HEADER.SPEND_TYPE].unique()
    print(f"The types of purchases you made were: \n {spending_types}")

def format_data(data: pd.DataFrame) -> pd.DataFrame:
    """formats inputted data into a more usable format"""

    data[HEADER.DATE] = pd.to_datetime(data[HEADER.DATE], dayfirst=True)
    return data
