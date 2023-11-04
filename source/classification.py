"""
    Module that handles the classification of data entries into spending types.

    author: Ben Shirley
    Date: 29 oct 2023
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from kmodes.kprototypes import KPrototypes
from transaction_structure import *

def encode_data_for_learning(data: pd.DataFrame) -> pd.DataFrame:
    """prepares the given data for learning by normalising it, removing unwanted attributes, and one-hot encoding""" 

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
    
    return encoded_data
def elbow_method_for_number_clusters(data):
    """graphs the overall cost of the k-prototype clustering varying values of k to 
    see which number of clusters fits the data best"""
    cost_values = []
    k=1
    old_cost = np.inf
    new_cost = 1000
    while old_cost / new_cost > 1.01:
        old_cost = new_cost
        new_data, new_cost = perform_k_prototypes_clustering(data, k)
        cost_values.append(new_cost)
        k += 1
    
    #plot the data
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(cost_values)+1), cost_values, marker='o', linestyle='--', color='b')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('cost')
    plt.title('Elbow Method for Optimal k (K-Prototypes)')
    plt.grid(True)
    plt.show()

def perform_k_prototypes_clustering(data: pd.DataFrame, k:int) -> pd.DataFrame:
    """performs k-prototypes clustering, which is a combination of k-means for the numerical data, and
    k-modes for the catagorical data
    """
    encoded_data = encode_data_for_learning(data)
    # currently the only numerical data is the amount
    k_proto = KPrototypes(n_clusters=k, init="Cao", verbose=2)

    clusters = k_proto.fit_predict(encoded_data, categorical=list(range(1, len(encoded_data.columns))))
    data["classification"] = clusters
    return data, k_proto.cost_

def perform_k_means_clustering(data: pd.DataFrame, k: int) -> pd.DataFrame:
    """
    performs k-means clusteringing on the data to provide each entry a catagory based on similarity.

    parameters:
        Data: data to be catagorised
        k: the number of clusters to be formed
    """
   
    encoded_data = encode_data_for_learning(data)
   
    cluster_assignments, inertia = k_means_no_library(encoded_data, k)
        
    data["classification"] = cluster_assignments
    return data, inertia

def k_means_no_library(encoded_data: pd.DataFrame, k: int) -> pd.Series:
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
                new_dist = np.sum((k_vector - data_point) ** 2) 
                if new_dist < min_distance:
                    min_distance = new_dist
                    current_closest = vector
                print(min_distance)
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

    result = []
    k_means = list(k_means.keys())
    print(len(k_means))
    for id, data_point in encoded_data.iterrows():
        min_distance = np.inf
        current_closest = None
        for i in range(len(k_means)):
            k_vector = np.array(k_means[i])
            new_dist =  np.sum((k_vector - data_point) ** 2)
            if new_dist < min_distance:
                    min_distance = new_dist
                    current_closest = i
        result.append(current_closest)
    return result, last_error