import math
import numpy as np
import DistanceMatrix
from euclideanDistance import Euclidean
from route import saveRouteImg
from distancePlot import analyzeDistance
from ClassicNN import ClassicNN
from ModifiedNN import ModifiedNN
from Location import Location
from kMeansAlg import KMeans
import threading
import time
import os

# This function reads in the input file which has coordinates for each location
def FileRead(filename):
    # Opens the file
    file = open(filename)
    # Create a list to store the location objects in
    listOfPoints = []
    # Keeps track of what location we are at 
    number = 0

    # This while loop runs while the file is not empty 
    while True:
        # This reads in a line from the file, it ends when it sees a newline
        line = file.readline()
        # If the line read is not an empty string we can proceed and try to create object called location
        if (line != ""):
            # Splits the line so we can get the x and y coordinates separately
            splitLine = line.split()
            # Checks if the split line has only one x and one y coordinate
            if (len(splitLine) == 2):
                # We try to type convert the input, if it can not be converted then it is invalid
                try:
                    # We create the object called node which is a location object
                    x = float(splitLine[0])
                    y = float(splitLine[1])
                    number = number + 1
                    node = Location(number, x, y)
                    # Add the node into our list of points which stores our object location
                    listOfPoints.append(node)
                except:
                    # If the exception triggers the file is in the wrong format
                    print("File in wrong format, here")
                    exit()
            # If the splitline has more than just one x and one y then the file is in the incorrect format
            else:
                print("File in wrong format")
                exit()
        # Here we break the loop if we reach an empty string
        else: 
            break

    # Once we are done with the file we need to close it    
    file.close()

    # If list of points remains empty, then we know the input file is empty
    if (listOfPoints == []):
        print("File is empty")
        exit()

    # The drone is allowed a maximum of 256 points that it can reach
    if (len(listOfPoints) > 10000):
        print("N is greater than 10000")
        exit()
    
    # This function returns the list of points array which contains object location
    return listOfPoints

filename = input("Enter the name of file: ")
directory = "test_cases"
filename = os.path.join(directory, filename)
print(filename)
listOfPoints = FileRead(filename)

km = KMeans(num_clusters = 2, num_random_seeds = 10, random_state = 42)
solution_dict = km.fit(listOfPoints)
cluster1 = solution_dict["cluster1"]
cluster2 = solution_dict["cluster2"]
for i in range(0, len(cluster1)):
    if i == 0:
        print("--Cluster1--")
    if i < 10:
        print(f"Number: {cluster1[i].number}, ({cluster1[i].x}, {cluster1[i].y})")

for i in range(0, len(cluster2)):
    if i == 0:
        print("--Cluster2--")
    if i < 10:
        print(f"Number: {cluster2[i].number}, ({cluster2[i].x}, {cluster2[i].y})")