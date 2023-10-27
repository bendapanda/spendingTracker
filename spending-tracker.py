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


PERSONAL_SPENDING_TYPES = ["Rent", "Bills", "Flat things", "Groceries", "work payments", ""]

def main():
    """Main function for my code"""
    data = pd.read_csv(FILENAME)
    data[HEADER.DATE] = pd.to_datetime(data[HEADER.DATE])

    spends = data.loc[(data[HEADER.QUANTITY] < 0) & (data[HEADER.SPEND_TYPE] != "Transfer")]
    earnings = data.loc[data[HEADER.QUANTITY] >= 0]

    general_spending = data.loc[data[HEADER.SPEND_TYPE] == "Visa Purchase"]
    general_spending_per_day = get_total_spending_per_day(general_spending)

    print(prompt_for_spending_types(data).head(50))


def prompt_for_spending_types(data):
    """ask user to list the types of things they spend money on.
    then perfroms k-means classification and asks the user to assign them """
    print("Label the catagories of things that you spend money on (type q to stop):\n")
    catagories = []
    
    new_data, inertia = perform_k_means_clustering(data, 10)

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

    chopped_data = data.drop([HEADER.DATE, HEADER.CODE, HEADER.FOREIGN, HEADER.CONVERSION_COST, HEADER.REF], axis=1, inplace=False)
    #one-hot encoding:
    spending_types = chopped_data[HEADER.SPEND_TYPE].unique()
    locations = chopped_data[HEADER.LOCATION].unique()
    particulars = chopped_data[HEADER.PARTICULARS].unique()

    encoded_data = pd.get_dummies(chopped_data, columns=[HEADER.SPEND_TYPE, HEADER.LOCATION, HEADER.PARTICULARS])
    encoded_data[HEADER.QUANTITY] = (encoded_data[HEADER.QUANTITY] - encoded_data[HEADER.QUANTITY].min()) / (encoded_data[HEADER.QUANTITY].max()-encoded_data[HEADER.QUANTITY].min())
    # For now normalise linearly, but investigate normal?
    

    # Step two: randomly allocate k-means in the search space
    k_means = KMeans(n_clusters=10)
    k_means.fit(encoded_data)
    cluster_assignments = k_means.labels_


    
    #result, inertia = k_means_no_library(encoded_data, k)
        

    
    # Step 4: add the catagories to the original dataset
    data["classification"] = cluster_assignments
    return data, k_means.inertia_

def k_means_no_library(encoded_data, k):
    """This is my own implementation of the k-means algorithm. It needs a tidy up but I wanted to see if i could 
    do it without a library"""
    vector_dimension = encoded_data.shape[1]
    k_means = {tuple(np.random.rand(vector_dimension)): [] for i in range(k)}
    
   
    last_error = np.inf
    error = 0
    TARGET = 0.0001
    # Step three: assign each point to the closest mean, and then move that mean to the average of all the points it is assigned to
    while(abs(error - last_error) > TARGET):
        last_error = error
        error = 0
        for id, data_point in encoded_data.iterrows(): # go through and assign all points to their closest neigbour
            min_distance = np.inf
            current_closest = None
            for vector in k_means.keys():
                k_vector = np.array(vector)
                new_dist = np.sum((k_vector * data_point) ** 2) 
                if new_dist < min_distance:
                    min_distance = new_dist
                    current_closest = vector
            k_means[current_closest].append(data_point)
            error += min_distance
        new_means = {}
        for vector, elements in k_means.items():
            if len(elements) > 0:
                new_k = np.sum(np.array(elements), axis=0) / len(elements)
            else:
                new_k = vector
            new_means[tuple(new_k)] = []
        k_means = new_means
        print(error, last_error)

    result = []
    k_means = list(k_means.keys())
    for id, data_point in encoded_data.iterrows():
        min_distance = np.inf
        current_closest = None
        for i in range(len(k_means)):
            print(len(k_means))
            k_vector = np.array(k_means[i])
            new_dist =  np.sum((k_vector * data_point) ** 2)
            if new_dist < min_distance:
                    min_distance = new_dist
                    current_closest = i
        result.append(current_closest)
    return result, last_error

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