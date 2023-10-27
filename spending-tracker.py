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

FILENAME = "transactions-year.csv"

class HEADER :
    SPEND_TYPE = "Type"
    LOCATION =  "Details"
    PARTICULARS = "Particulars"
    DATE = "Date"
    CODE =  "Code"
    REF =  "Reference"
    QUANTITY =  "Amount"
    FOREIGN = "ForeignCurrencyAmount"
    CONVERSION_COST=  "ConversionCharge"


def main():
    """Main function for my code"""
    data = pd.read_csv(FILENAME)
    data[HEADER.DATE] = pd.to_datetime(data[HEADER.DATE])

    spends = data.loc[(data[HEADER.QUANTITY] < 0) & (data[HEADER.SPEND_TYPE] != "Transfer")]
    earnings = data.loc[data[HEADER.QUANTITY] >= 0]

    general_spending = data.loc[data[HEADER.SPEND_TYPE] == "Visa Purchase"]
    general_spending_per_day = get_total_spending_per_day(general_spending)

    perform_k_means_clustering(data, 5)


def get_spending_types(data):
    """returns a 1-d numpy array containing the unique types of spending that occured"""
    return data[HEADER.SPEND_TYPE].unique()

def get_total_spending_per_day(data):
    """returns a new dataset of the form date, quantity which describes how much was spent on any set day"""
    daily_spendings = data.groupby(HEADER.DATE)[HEADER.QUANTITY].sum().to_frame()
    daily_spendings.index.name = HEADER.DATE
    daily_spendings.reset_index(inplace=True)
    return daily_spendings

def perform_k_means_clustering(data, k):
    """performs k-means clusteringing on the data to provide each entry a catagory based on similarity.
    """

    # Step one: reduce data to be entirely numberical
    # In the data set, we have all of the variables in HEADER to consider
    # However, date likely will not affect the data
    # Try: using number for date, or day of week
    # For now I will ignore it

    dates = data[HEADER.DATE]
    codes = data[HEADER.CODE]
    foreign = data[HEADER.FOREIGN]
    conversion = data[HEADER.CONVERSION_COST]

    chopped_data = data.drop([HEADER.DATE, HEADER.CODE, HEADER.FOREIGN, HEADER.CONVERSION_COST], axis=1, inplace=False)
    #one-hot encoding:
    spending_types = chopped_data[HEADER.SPEND_TYPE].unique()
    locations = chopped_data[HEADER.LOCATION].unique()
    references = chopped_data[HEADER.REF].unique()
    particulars = chopped_data[HEADER.PARTICULARS].unique()

    encoded_data = pd.get_dummies(chopped_data, columns=[HEADER.SPEND_TYPE, HEADER.LOCATION, HEADER.REF, HEADER.PARTICULARS])
    encoded_data[HEADER.QUANTITY] = (encoded_data[HEADER.QUANTITY] - encoded_data[HEADER.QUANTITY].min()) / (encoded_data[HEADER.QUANTITY].max()-encoded_data[HEADER.QUANTITY].min())
    # For now normalise linearly, but investigate normal?
    

    # Step two: randomly allocate k-means in the search space
    vector_dimension = encoded_data.shape[1]
    k_means = np.random.rand(k, vector_dimension)
    k_means = pd.DataFrame(k_means)
    print(k_means.head())


    

    # Step three: assign each point to the closest mean, and then move that mean to the average of all the points it is assigned to
        # repeat until 
    
    # Step 4: add the catagories to the original dataset
    #return

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