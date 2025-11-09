import math
import numpy as np
from DistanceMatrix import dist_matrix 
from euclideanDistance import Euclidean
from route import saveClusterRoutesImg
#from distancePlot import analyzeDistance
from ClassicNN import ClassicNN
from ModifiedNN import ModifiedNN
from Location import Location
import threading
import time
import os
from kMeansAlg import KM

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
                    node = Location(number, 0, x, y)
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
        print("N is greater than 256")
        exit()
    
    # This function returns the list of points array which contains object location
    return listOfPoints


# This writes the collection of distances to the file distance file random s so we can access the for plotting
def writeToDistanceFile(collectionOfDistance):
    with open("distanceFileRandomS.txt", "a") as file:
        file.write(str(collectionOfDistance) + "\n")

# This writes the solution for which nodes to visit e.g. "1 2 10 3 1"
def finalPathToFile(filename, finalPath, collectionOfDistance):
    with open(f"{filename}_SOLUTION_{int(round(collectionOfDistance[-1][0]))}.txt", "w") as outFile:
        for i in finalPath:
            outFile.write(f"{i.number} \n")
    return outFile.name

filename = input("Enter the name of file: ")
directory = "test_cases"
filename = os.path.join(directory, filename)
listOfPoints = FileRead(filename)
dictionary = KM(listOfPoints)
c1 = dictionary['dict2']['center1']
cr1 = dictionary['dict2']['cluster1']

k = int(input("Please Select your choice 1 to 4:"))
kdict = dictionary[f'dict{k}']

# get cluster and centers for k chosen
clusters = [kdict[f'cluster{i}'] for i in range(1, k+1)]
centers = [kdict[f'center{i}'] for i in range(1, k+1)]

# dont have paths yet so nothing here
clusterPaths = []

saveClusterRoutesImg(listOfPoints, clusters, centers, clusterPaths, filename)

# for i in range(len(cr1)):
#     print (cr1[i].newNumber)

dm = dist_matrix(cr1)
# Random NN Functions

NNisDone = False
collectionOfDistanceNN = []
finalPathNN = []
first_iter = True
prev = 0

# This function prints the total distance of a path calculated using classic nn in the first iteration 
# It then uses a loop which calls our modified nn algorithm to try and find a shorter path
def printSumNN(sumOfDistance, listOfPoints, dist_mat):
    global collectionOfDistanceNN, finalPathNN, prev, first_iter 
    start_time = time.time()
    # If it is the first iteration classic nn should be performed
    if first_iter == True:
        time.sleep(0.25)
        sumOfDistance, path, _, _ = ClassicNN(listOfPoints, dist_mat)
        # Just like random search if the new distance is not the same as the old distance we found a new route
        if prev != sumOfDistance:
            # This gets the time it took to find a route
            time_So_Far = time.time() - start_time
            # For jason when making distance over time graph
            collectionOfDistanceNN.append((sumOfDistance, time_So_Far)) 
             # For jason when making route graph and kenny for file output
            finalPathNN = path
            print(f"          {sumOfDistance}")
        prev = sumOfDistance
        # Make sure to indicate this after one run so classic nn only runs once
        first_iter = False
    # While the user has not hit the entry key this loop will keep going 
    while not NNisDone:
        #code pauses a quarter of a second. Can change if needed to
        time.sleep(0.25) 
        sumOfDistance, path, _, _ = ModifiedNN(listOfPoints, dist_mat, finalPathNN, dist_to_beat=sumOfDistance)
        # This is utilized the same
        if prev != sumOfDistance:
            time_So_Far = time.time() - start_time
            collectionOfDistanceNN.append((sumOfDistance, time_So_Far)) #for jason when making distance over time graph
            finalPathNN = path #for jason when making route graph
            print(f"          {sumOfDistance}")
        prev = sumOfDistance  
       
    #saveRouteImg(listOfPoints, finalPathNN, prev, filename)


def writeToDistanceFileNN(collectionOfDistanceNN):
    with open("distanceFileRandomNN.txt", "a") as file:
        file.write(str(collectionOfDistanceNN) + "\n")

#print("--List of Points--")
#for i in range(0, len(listOfPoints)):
    #print(listOfPoints[i].number)


print(f"There are {(len(listOfPoints))} nodes, computing route..")
print("     Shortest Route Discovered So Far")

# Used threading so function can continously run without having to wait for input
threading.Thread(target=printSumNN, args=(math.inf, cr1, dm)).start() 

# While the function input is awaiting input from user print sum runs
input()
# After input the loop condition is set to true so it stops
NNisDone = True

if (collectionOfDistanceNN[-1][0] > 10000):
        print(f"Warning: Solution is {collectionOfDistanceNN[-1][0]}, greater than the 6000-meter constraint.")

filename = os.path.splitext(os.path.basename(filename))[0]
# this writes the solution for which nodes to visit e.g. "1 2 10 3 1"

outFile = finalPathToFile(filename, finalPathNN, collectionOfDistanceNN)

print(f"Route written to disk as {outFile}")

writeToDistanceFileNN(collectionOfDistanceNN)

#nameFileOne = "distanceFileRandomNN.txt"

#analyzeDistance(nameFileOne)
        