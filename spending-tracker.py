"""
This is the main file for my spending tracker app.

- Things I need to be able to do:
Classify what different entries mean,
Store stuff in a database
Track my total funds over time

For example, I need to be able to dump all the data in, and then classify the different types of data

@author Ben Shirley
@date 27 Oct 2023
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from kmodes.kprototypes import KPrototypes

from transaction_structure import *
from classification import *
FILENAME = "transactions-year.csv"

PERSONAL_SPENDING_TYPES = ["Rent", "Bills", "Flat things", "Groceries", "work payments", ""]

def main():
    """Main function for my code"""
    data = pd.read_csv(FILENAME)
    data[HEADER.DATE] = pd.to_datetime(data[HEADER.DATE])

    spends = data.loc[(data[HEADER.QUANTITY] < 0) & (data[HEADER.SPEND_TYPE] != "Transfer")]
    earnings = data.loc[data[HEADER.QUANTITY] >= 0]

    general_spending = data.loc[data[HEADER.SPEND_TYPE] == "Visa Purchase"]
    general_spending_per_day = get_total_spending_per_day(general_spending)

    #elbow_method_for_number_clusters(data)
    classified_data = prompt_for_spending_types(data)
    print(classified_data.head(50))
    classified_data.to_csv("classified_dataset.csv")
    #for classification in classified_data["classification"].unique():
    #    classified_data[classified_data["classification"] == classification, "Amount"].plot(kind="hist", figsize=(10,8), label=classification, legend=True)
    #plt.show()



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
    print("Label the catagories of things that you spend money on (type q to stop):\n")
    catagories = []
    
    new_data, inertia = perform_k_prototypes_clustering(data, 6)

    mapping = {}
    for catagory in new_data["classification"].unique():
        print("Please assign a label to spends that look like this:\n")
        print(data[data["classification"] == catagory].head(15))
        for i in range(len(catagories)):
            print(f"{catagories[i]}: {(i)}")
        for i in range(len(catagories)):
            print(f"{catagories[i]}: ({i})")
        print("New: (-)")
        choice = input(": ")
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

def display_csv_info(data):
    """funciton that prints information about a csv spending file""" 
    print(data.info())
    print(data.head())

    spending_types = data[HEADER.SPEND_TYPE].unique()
    print(f"The types of purchases you made were: \n {spending_types}")
if __name__ == "__main__":
    main()