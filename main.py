import math
import numpy as np
from DistanceMatrix import dist_matrix 
from euclideanDistance import Euclidean
from route import saveRouteImg
#from distancePlot import analyzeDistance
from ClassicNN import ClassicNN
from ModifiedNN import ModifiedNN
from Location import Location
import threading
import time
import os
from kMeansAlg import KM
from print import output

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
listOfPoints = FileRead(filename)
dictionary = KM(listOfPoints)

landing1_center1 = dictionary['dict1']['center1']
landing1_cluster1 = dictionary['dict1']['cluster1']

landing2_center1 = dictionary['dict2']['center1']
landing2_cluster1 = dictionary['dict2']['cluster1']

landing2_center2 = dictionary['dict2']['center2']
landing2_cluster2 = dictionary['dict2']['cluster2']

landing3_center1 = dictionary['dict3']['center1']
landing3_cluster1 = dictionary['dict3']['cluster1']

landing3_center2 = dictionary['dict3']['center2']
landing3_cluster2 = dictionary['dict3']['cluster2']

landing3_center3 = dictionary['dict3']['center3']
landing3_cluster3 = dictionary['dict3']['cluster3']

landing4_center1 = dictionary['dict4']['center1']
landing4_cluster1 = dictionary['dict4']['cluster1']

landing4_center2 = dictionary['dict4']['center2']
landing4_cluster2 = dictionary['dict4']['cluster2']

landing4_center3 = dictionary['dict4']['center3']
landing4_cluster3 = dictionary['dict4']['cluster3']

landing4_center4 = dictionary['dict4']['center4']
landing4_cluster4 = dictionary['dict4']['cluster4']


#testdistance1, testpath1, _, _ = ClassicNN(landing2_cluster1, dist_matrix(landing2_cluster1))
landing1 = []
landing2 = []
landing3 = []
landing4 = []

landing1.append((landing1_cluster1, dist_matrix(landing1_cluster1), landing1_center1))

landing2.append((landing2_cluster1, dist_matrix(landing2_cluster1), landing2_center1))
landing2.append((landing2_cluster2, dist_matrix(landing2_cluster2), landing2_center2))

landing3.append((landing3_cluster1, dist_matrix(landing3_cluster1), landing3_center1))
landing3.append((landing3_cluster2, dist_matrix(landing3_cluster2), landing3_center2))
landing3.append((landing3_cluster3, dist_matrix(landing3_cluster3), landing3_center3))

landing4.append((landing4_cluster1, dist_matrix(landing4_cluster1), landing4_center1))
landing4.append((landing4_cluster2, dist_matrix(landing4_cluster2), landing4_center2))
landing4.append((landing4_cluster3, dist_matrix(landing4_cluster3), landing4_center3))
landing4.append((landing4_cluster4, dist_matrix(landing4_cluster4), landing4_center4))

# Random NN Functions

NNisDone = False
collectionOfDistanceNN = []
finalPathNN = []
first_iter = True
prev = 0

# This function prints the total distance of a path calculated using classic nn in the first iteration 
# It then uses a loop which calls our modified nn algorithm to try and find a shorter path
def printSumNN(listOfPoints, landing1, landing2, landing3, landing4):
    landing1_distances = []
    landing2_distances = []
    landing3_distances = []
    landing4_distances = []
    print(f"There are {len(listOfPoints)} nodes:")
    for i, j, k in landing1:
        finalDistance, time_so_far = output(i, j)
        landing1_distances.append((finalDistance, time_so_far))
    
    print(f"1) If you use {len(landing1)} drone (s), the total route will be {sum(landing1_distances[0])} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing1[0][2].x)},{int(landing1[0][2].y)}], serving {len(landing1[0][0])} locations, route is {landing1_distances[0][0]} meters")

    for i, j, k in landing2:
        finalDistance, time_so_far = output(i, j)
        landing2_distances.append((finalDistance, time_so_far))
    
    print(f"2) If you use {len(landing2)} drone (s), the total route will be {sum(landing2_distances[0])} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing2[0][2].x)},{int(landing2[0][2].y)}], serving {len(landing2[0][0])} locations, route is {landing2_distances[0][0]} meters")
    print(f"    ii. Landing pad 2 should be at [{int(landing2[1][2].x)},{int(landing2[1][2].y)}], serving {len(landing2[1][0])} locations, route is {landing2_distances[1][0]} meters")

    for i, j, k in landing3:
        finalDistance, time_so_far = output(i, j)
        landing3_distances.append((finalDistance, time_so_far))
    
    print(f"3) If you use {len(landing3)} drone (s), the total route will be {sum(landing3_distances[0])} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing3[0][2].x)},{int(landing3[0][2].y)}], serving {len(landing3[0][0])} locations, route is {landing3_distances[0][0]} meters")
    print(f"    ii. Landing pad 2 should be at [{int(landing3[1][2].x)},{int(landing3[1][2].y)}], serving {len(landing3[1][0])} locations, route is {landing3_distances[1][0]} meters")
    print(f"    iii. Landing pad 3 should be at [{int(landing3[2][2].x)},{int(landing3[2][2].y)}], serving {len(landing3[2][0])} locations, route is {landing3_distances[2][0]} meters")


    for i, j, k in landing4:
        finalDistance, time_so_far = output(i, j)
        landing4_distances.append((finalDistance, time_so_far))
    
    print(f"4) If you use {len(landing4)} drone (s), the total route will be {sum(landing4_distances[0])} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing4[0][2].x)},{int(landing4[0][2].y)}], serving {len(landing4[0][0])} locations, route is {landing4_distances[0][0]} meters")
    print(f"    ii. Landing pad 2 should be at [{int(landing4[1][2].x)},{int(landing4[1][2].y)}], serving {len(landing4[1][0])} locations, route is {landing4_distances[1][0]} meters")
    print(f"    iii. Landing pad 3 should be at [{int(landing4[2][2].x)},{int(landing4[2][2].y)}], serving {len(landing4[2][0])} locations, route is {landing4_distances[2][0]} meters")
    print(f"    iv. Landing pad 4 should be at [{int(landing4[3][2].x)},{int(landing4[3][2].y)}], serving {len(landing4[3][0])} locations, route is {landing4_distances[3][0]} meters")
    
    bestSolution = int(input("Please select your choice 1 to 4: "))
    if bestSolution == 1:
        return landing1, landing1_distances
    if bestSolution == 2:
        return landing2, landing2_distances
    if bestSolution == 3:
        return landing3, landing3_distances
    if bestSolution == 4:
        return landing4, landing4_distances
    

def writeToDistanceFileNN(collectionOfDistanceNN):
    with open("distanceFileRandomNN.txt", "a") as file:
        file.write(str(collectionOfDistanceNN) + "\n")

#print("--List of Points--")
#for i in range(0, len(listOfPoints)):
    #print(listOfPoints[i].number)


# Used threading so function can continously run without having to wait for input
#threading.Thread(target=printSumNN, args=(math.inf, landing1, landing2, landing3, landing4)).start() 

best_cluster, best_distance = printSumNN(listOfPoints, landing1, landing2, landing3, landing4)


# While the function input is awaiting input from user print sum runs
#input()
# After input the loop condition is set to true so it stops
#NNisDone = True

#if (collectionOfDistanceNN[-1][0] > 10000):
        #print(f"Warning: Solution is {collectionOfDistanceNN[-1][0]}, greater than the 6000-meter constraint.")

filename = os.path.splitext(os.path.basename(filename))[0]
# this writes the solution for which nodes to visit e.g. "1 2 10 3 1"

#outFile = finalPathToFile(filename, finalPathNN, collectionOfDistanceNN)

for i in range(len(best_cluster)):
    print(f"Writting {filename}_{i + 1}_SOLUTION_{best_distance[i][0]}.txt")

writeToDistanceFileNN(collectionOfDistanceNN)

#nameFileOne = "distanceFileRandomNN.txt"

#analyzeDistance(nameFileOne)
        