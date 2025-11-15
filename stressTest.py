from main import printSumNN
from kMeansAlg import KM
from se import error
from DistanceMatrix import dist_matrix
import random
import math
from Location import Location
import time


# generate 4096 locations, time it for the kmeans alg and classic/modifiedNN
xCenterL = -1.0
yCenterL = -1.0
numPoints = 4096
xCenterR = 1.0
yCenterR = 1.0
listOfPointsR = []
listOfPointsL = []
number = 0

for i in range(0, int(numPoints/2)):
    rand_val = random.random()
    rand_radius = random.random()
    angle = rand_val * 2 * math.pi
    xL = rand_radius * math.cos(angle) + xCenterL
    yL = rand_radius * math.sin(angle) + yCenterL
    xR = rand_radius * math.cos(angle) + xCenterR
    yR = rand_radius * math.sin(angle) + yCenterR

    number += 1
    nodeL = Location(number, 0, float(xL), float(yL))
    listOfPointsL.append(nodeL)

    number += 1
    nodeR = Location(number, 0, float(xR), float(yR))
    listOfPointsR.append(nodeR)

listOfPoints = listOfPointsR + listOfPointsL

with open("test_cases/4096cluster_test.txt", "w") as outFile:
    for i in range(len(listOfPoints)):
        outFile.write(f"   {listOfPoints[i].x}   {listOfPoints[i].y} \n")



# # generate 8000 locations, time it for the kmeans alg and classic/modifiedNN
xCenterL = -1.0
yCenterL = -1.0
numPoints = 8000
xCenterR = 1.0
yCenterR = 1.0
listOfPointsR = []
listOfPointsL = []
number = 0

for i in range(0, int(numPoints/2)):
    rand_val = random.random()
    rand_radius = random.random()
    angle = rand_val * 2 * math.pi
    xL = rand_radius * math.cos(angle) + xCenterL
    yL = rand_radius * math.sin(angle) + yCenterL
    xR = rand_radius * math.cos(angle) + xCenterR
    yR = rand_radius * math.sin(angle) + yCenterR

    number += 1
    nodeL = Location(number, 0, float(xL), float(yL))
    listOfPointsL.append(nodeL)

    number += 1
    nodeR = Location(number, 0, float(xR), float(yR))
    listOfPointsR.append(nodeR)

listOfPoints = listOfPointsR + listOfPointsL

with open("test_cases/8000cluster_test.txt", "w") as outFile:
    for i in range(len(listOfPoints)):
        outFile.write(f"   {listOfPoints[i].x}   {listOfPoints[i].y} \n")