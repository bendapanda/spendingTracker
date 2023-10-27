"""
This is the main file for my spending tracker app.

@author Ben Shirley
@date 27 Oct 2023
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FILENAME = "transactions.csv"

class HEADER :
    SPEND_TYPE = "Type"
    LOCATION =  "Details"
    PARTICULARS = "Partuculars"
    CODE =  "Code"
    REF =  "Reference"
    QUANTITY =  "Amount"
    FOREIGN = "ForeignCurrencyAmount"
    CONVERSION_COST=  "ConversionCharge"


def main():
    """Main function for my code"""
    data = pd.read_csv(FILENAME)

    spends = data.loc[(data[HEADER.QUANTITY] < 0) & (data[HEADER.SPEND_TYPE] != "Transfer")]
    earnings = data.loc[data[HEADER.QUANTITY] >= 0]

    display_spending_quantity_by_type(data, "Visa Purchase")
    plt.show()


def get_spending_types(data):
    """returns a 1-d numpy array containing the unique types of spending that occured"""
    return data[HEADER.SPEND_TYPE].unique()

def plot_spending_by_time(data):
    """
    Takes in a set of data, and plots the spending of it by time
    """


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