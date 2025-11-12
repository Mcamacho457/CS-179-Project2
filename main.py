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
from print import output
from datetime import datetime, timedelta

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
    with open(f"{filename.split('/')[-1]}_SOLUTION_{int(round(collectionOfDistance))}.txt", "w") as outFile:
        for i in finalPath:
            outFile.write(f"{i.number} \n")
    return outFile.name

filename = input("Enter the name of file: ")
directory = "test_cases"
filename = os.path.join(directory, filename)
listOfPoints = FileRead(filename)
olddictionary = KM(listOfPoints)

oldlanding1_center1 = olddictionary['dict1']['center1']
oldlanding1_cluster1 = olddictionary['dict1']['cluster1']

oldlanding2_center1 = olddictionary['dict2']['center1']
oldlanding2_cluster1 = olddictionary['dict2']['cluster1']

oldlanding2_center2 = olddictionary['dict2']['center2']
oldlanding2_cluster2 = olddictionary['dict2']['cluster2']

oldlanding3_center1 = olddictionary['dict3']['center1']
oldlanding3_cluster1 = olddictionary['dict3']['cluster1']

oldlanding3_center2 = olddictionary['dict3']['center2']
oldlanding3_cluster2 = olddictionary['dict3']['cluster2']

oldlanding3_center3 = olddictionary['dict3']['center3']
oldlanding3_cluster3 = olddictionary['dict3']['cluster3']

oldlanding4_center1 = olddictionary['dict4']['center1']
oldlanding4_cluster1 = olddictionary['dict4']['cluster1']

oldlanding4_center2 = olddictionary['dict4']['center2']
oldlanding4_cluster2 = olddictionary['dict4']['cluster2']

oldlanding4_center3 = olddictionary['dict4']['center3']
oldlanding4_cluster3 = olddictionary['dict4']['cluster3']

oldlanding4_center4 = olddictionary['dict4']['center4']
oldlanding4_cluster4 = olddictionary['dict4']['cluster4']

def error(x1, y1, x2, y2):
    e = abs(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    return e

total_ses = []
clusters = []
centers = []

for i in range(10):
    newdictionary = KM(listOfPoints)
    landing1_center1 = newdictionary['dict1']['center1']
    landing1_cluster1 = newdictionary['dict1']['cluster1']
    
    totalse = 0.0
    for i in range(len(listOfPoints)):
        se = error(landing1_cluster1[i].x, landing1_cluster1[i].y, landing1_center1.x, landing1_center1.y)
        totalse += se
    total_ses.append(totalse)
    clusters.append(landing1_cluster1)
    centers.append(landing1_center1)

best_idx11 = total_ses.index(min(total_ses))
best_cluster11 = clusters[best_idx11]
best_center11 = centers[best_idx11]
landing1_center1 = best_center11
landing1_cluster1 = best_cluster11

total_ses = []
clusters1 = []
centers1 = []
clusters2 = []
centers2 = []

for i in range(10):
    newdictionary = KM(listOfPoints)
    landing2_center1 = newdictionary['dict2']['center1']
    landing2_cluster1 = newdictionary['dict2']['cluster1']
    landing2_center2 = newdictionary['dict2']['center2']
    landing2_cluster2 = newdictionary['dict2']['cluster2']

    totalse = 0.0
    for i in range(len(landing2_cluster1)):
        se = error(landing2_cluster1[i].x, landing2_cluster1[i].y, landing2_center1.x, landing2_center1.y)
        totalse += se

    for i in range(len(landing2_cluster2)):
        se = error(landing2_cluster2[i].x, landing2_cluster2[i].y, landing2_center2.x, landing2_center2.y)
        totalse += se

    total_ses.append(totalse)
    clusters1.append(landing2_cluster1)
    centers1.append(landing2_center1)
    clusters2.append(landing2_cluster2)
    centers2.append(landing2_center2)
    
best_idx2 = total_ses.index(min(total_ses))
best_cluster1 = clusters1[best_idx2]
best_center1 = centers1[best_idx2]
best_cluster2 = clusters2[best_idx2]
best_center2 = centers2[best_idx2]
landing2_center1 = best_center1
landing2_cluster1 = best_cluster1
landing2_center2 = best_center2
landing2_cluster2 = best_cluster2

total_ses = []
clusters1 = []
centers1 = []
clusters2 = []
centers2 = []
clusters3 = []
centers3 = []

for i in range(10):
    newdictionary = KM(listOfPoints)
    landing3_center1 = newdictionary['dict3']['center1']
    landing3_cluster1 = newdictionary['dict3']['cluster1']
    landing3_center2 = newdictionary['dict3']['center2']
    landing3_cluster2 = newdictionary['dict3']['cluster2']
    landing3_center3 = newdictionary['dict3']['center3']
    landing3_cluster3 = newdictionary['dict3']['cluster3']

    totalse = 0.0
    for i in range(len(landing3_cluster1)):
        se = error(landing3_cluster1[i].x, landing3_cluster1[i].y, landing3_center1.x, landing3_center1.y)
        totalse += se

    for i in range(len(landing3_cluster2)):
        se = error(landing3_cluster2[i].x, landing3_cluster2[i].y, landing3_center2.x, landing3_center2.y)
        totalse += se
    
    for i in range(len(landing3_cluster3)):
        se = error(landing3_cluster3[i].x, landing3_cluster3[i].y, landing3_center3.x, landing3_center3.y)
        totalse += se

    total_ses.append(totalse)
    clusters1.append(landing3_cluster1)
    centers1.append(landing3_center1)
    clusters2.append(landing3_cluster2)
    centers2.append(landing3_center2)
    clusters3.append(landing3_cluster3)
    centers3.append(landing3_center3)
    
best_idx3 = total_ses.index(min(total_ses))
best_cluster1 = clusters1[best_idx3]
best_center1 = centers1[best_idx3]
best_cluster2 = clusters2[best_idx3]
best_center2 = centers2[best_idx3]
best_cluster3 = clusters3[best_idx3]
best_center3 = centers3[best_idx3]
landing3_center1 = best_center1
landing3_cluster1 = best_cluster1
landing3_center2 = best_center2
landing3_cluster2 = best_cluster2
landing3_center3 = best_center3
landing3_cluster3 = best_cluster3

total_ses = []
clusters1 = []
centers1 = []
clusters2 = []
centers2 = []
clusters3 = []
centers3 = []
clusters4 = []
centers4 = []

for i in range(10):
    newdictionary = KM(listOfPoints)
    landing4_center1 = newdictionary['dict4']['center1']
    landing4_cluster1 = newdictionary['dict4']['cluster1']
    landing4_center2 = newdictionary['dict4']['center2']
    landing4_cluster2 = newdictionary['dict4']['cluster2']
    landing4_center3 = newdictionary['dict4']['center3']
    landing4_cluster3 = newdictionary['dict4']['cluster3']
    landing4_center4 = newdictionary['dict4']['center4']
    landing4_cluster4 = newdictionary['dict4']['cluster4']

    totalse = 0.0
    for i in range(len(landing4_cluster1)):
        se = error(landing4_cluster1[i].x, landing4_cluster1[i].y, landing4_center1.x, landing4_center1.y)
        totalse += se

    for i in range(len(landing4_cluster2)):
        se = error(landing4_cluster2[i].x, landing4_cluster2[i].y, landing4_center2.x, landing4_center2.y)
        totalse += se
    
    for i in range(len(landing4_cluster3)):
        se = error(landing4_cluster3[i].x, landing4_cluster3[i].y, landing4_center3.x, landing4_center3.y)
        totalse += se
    
    for i in range(len(landing4_cluster4)):
        se = error(landing4_cluster4[i].x, landing4_cluster4[i].y, landing4_center4.x, landing4_center4.y)
        totalse += se

    total_ses.append(totalse)
    clusters1.append(landing4_cluster1)
    centers1.append(landing4_center1)
    clusters2.append(landing4_cluster2)
    centers2.append(landing4_center2)
    clusters3.append(landing4_cluster3)
    centers3.append(landing4_center3)
    clusters4.append(landing4_cluster4)
    centers4.append(landing4_center4)
    
best_idx4 = total_ses.index(min(total_ses))
best_cluster1 = clusters1[best_idx4]
best_center1 = centers1[best_idx4]
best_cluster2 = clusters2[best_idx4]
best_center2 = centers2[best_idx4]
best_cluster3 = clusters3[best_idx4]
best_center3 = centers3[best_idx4]
best_cluster4 = clusters4[best_idx4]
best_center4 = centers4[best_idx4]
landing4_center1 = best_center1
landing4_cluster1 = best_cluster1
landing4_center2 = best_center2
landing4_cluster2 = best_cluster2
landing4_center3 = best_center3
landing4_cluster3 = best_cluster3
landing4_center4 = best_center4
landing4_cluster4 = best_cluster4

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

    now = datetime.now() #link for refrences https://www.programiz.com/python-programming/datetime/current-time
    now = now + timedelta(minutes = 5)
    if now.hour > 12:
        now = now - timedelta(hours=12)
        current = now.strftime("%H:%M")
        print(f"There are {len(listOfPoints)} nodes: Solutions will be available by {current}pm")
    elif now.hour < 12:
         current = now.strftime("%H:%M")
         print(f"There are {len(listOfPoints)} nodes: Solutions will be available by {current}am")
    else:
         current = now.strftime("%H:%M")
         print(f"There are {len(listOfPoints)} nodes: Solutions will be available by {current}pm")
    for i, j, k in landing1:
        finalDistance, time_so_far = output(i, j)
        landing1_distances.append((finalDistance, time_so_far))
    
    print(f"1) If you use {len(landing1)} drone (s), the total route will be {sum(d[0] for d in landing1_distances)} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing1[0][2].x)},{int(landing1[0][2].y)}], serving {len(landing1[0][0])} locations, route is {landing1_distances[0][0]} meters")

    for i, j, k in landing2:
        finalDistance, time_so_far = output(i, j)
        landing2_distances.append((finalDistance, time_so_far))
    
    print(f"2) If you use {len(landing2)} drone (s), the total route will be {sum(d[0] for d in landing2_distances)} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing2[0][2].x)},{int(landing2[0][2].y)}], serving {len(landing2[0][0])} locations, route is {landing2_distances[0][0]} meters")
    print(f"    ii. Landing pad 2 should be at [{int(landing2[1][2].x)},{int(landing2[1][2].y)}], serving {len(landing2[1][0])} locations, route is {landing2_distances[1][0]} meters")

    for i, j, k in landing3:
        finalDistance, time_so_far = output(i, j)
        landing3_distances.append((finalDistance, time_so_far))
    
    print(f"3) If you use {len(landing3)} drone (s), the total route will be {sum(d[0] for d in landing3_distances)} meters")
    print(f"    i. Landing pad 1 should be at [{int(landing3[0][2].x)},{int(landing3[0][2].y)}], serving {len(landing3[0][0])} locations, route is {landing3_distances[0][0]} meters")
    print(f"    ii. Landing pad 2 should be at [{int(landing3[1][2].x)},{int(landing3[1][2].y)}], serving {len(landing3[1][0])} locations, route is {landing3_distances[1][0]} meters")
    print(f"    iii. Landing pad 3 should be at [{int(landing3[2][2].x)},{int(landing3[2][2].y)}], serving {len(landing3[2][0])} locations, route is {landing3_distances[2][0]} meters")


    for i, j, k in landing4:
        finalDistance, time_so_far = output(i, j)
        landing4_distances.append((finalDistance, time_so_far))
    
    print(f"4) If you use {len(landing4)} drone (s), the total route will be {sum(d[0] for d in landing4_distances)} meters")
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

clusters = [t[0] for t in best_cluster]
centers = [t[2] for t in best_cluster]

clusterPaths = []

saveClusterRoutesImg(listOfPoints, clusters, centers, clusterPaths, filename)
# While the function input is awaiting input from user print sum runs
#input()
# After input the loop condition is set to true so it stops
#NNisDone = True

#if (collectionOfDistanceNN[-1][0] > 10000):
        #print(f"Warning: Solution is {collectionOfDistanceNN[-1][0]}, greater than the 6000-meter constraint.")

filename = os.path.splitext(os.path.basename(filename))[0]
# this writes the solution for which nodes to visit e.g. "1 2 10 3 1"



for i in range(len(best_cluster)):
    outFile = finalPathToFile(filename, best_cluster[i][0], best_distance[i][0])
    print(f"Writting {filename}_{i + 1}_SOLUTION_{best_distance[i][0]}.txt")

writeToDistanceFileNN(collectionOfDistanceNN)

#nameFileOne = "distanceFileRandomNN.txt"

#analyzeDistance(nameFileOne)
        