# kmeans algorithm implemented form scratch
import random 
import copy #here is link for refrence https://www.geeksforgeeks.org/python/copy-python-deep-copy-shallow-copy/#
from euclideanDistance import Euclidean
from Location import Location

def newCenter(cluster):
     # If the cluster is greater than size one, we need to take the average of the clusters 
     # The average of the locations will be the new coordinates
     if (len(cluster) > 1):
        sumX = 0
        sumY = 0
        for i in cluster:
            sumX += i.x
            sumY += i.y
        newCX = sumX/len(cluster)
        newCY = sumY/len(cluster)
        number = 0
        return Location(number, 0, newCX, newCY)

# k = 4 number of clusters 
# listOfPoints is list of location objects which have x y and a number
# center will be a randomly chosen location object
def KM(listOfPoints):
    clusterDict1 = {}
    clusterDict2 = {}
    clusterDict3 = {}
    clusterDict4 = {}

    #so each k has their own newNumber for indexing on CNN
    k1 = []
    k2 = []
    k3 = []
    k4 = []
    # For 1 to 4 clusters
    for j in range(4):
        # For 1 cluster
        if (j == 0):
            distToCenter01 = []
            cluster01 = []
            k1 = copy.deepcopy(listOfPoints)
            center01 = random.choice(listOfPoints)
            c01x = center01.x
            c01y = center01.y
            count = 0

            # Iterate through list of points, calc the distance for each from center and put it in the cluster
            for i in range(len(listOfPoints)):
                distToCenter01.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c01x, c01y))
                k1[i].newNumber = count + 1
                cluster01.append(k1[i])
            # Make a new center for 1 cluster this can only be done one time    
            center01 = newCenter(cluster01)
            # We clear the the cluster and dist from center after finding the new center
            distToCenter01.clear()
            cluster01.clear()
            count = 0
            # Same process calc the distance away from center and assign to cluster center in this case not to deep just one cluster
            for i in range(len(listOfPoints)):
                distToCenter01.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, center01.x, center01.y))
                k1[i].newNumber = count + 1
                cluster01.append(k1[i])
                count += 1

            # Return a dictionary that contains the cluster and the center
            # The cluster so we can iterate through it
            # The center so that we can display the point
            clusterDict1 = {'cluster1' : cluster01, 'center1' : center01}
        if (j == 1):
            distToCenter11 = []
            distToCenter12 = []
            cluster11 = []
            cluster12 = []
            k2 = copy.deepcopy(listOfPoints) #we use deepcopy so we manipulate the elements without messing with original array
            center11 = random.choice(listOfPoints)
            c11x = center11.x
            c11y = center11.y
            center12 = random.choice(listOfPoints)
            while ((center11.x == center12.x) & (center11.y == center12.y)):
                center12 = random.choice(listOfPoints)
            c12x = center12.x
            c12y = center12.y
            count = 0
            oldCenter11 = Location(0, 0, 0, 0)
            oldCenter12 = Location(0, 0, 0, 0)

            index = 0
            while True:
                for i in range(len(listOfPoints)):
                    distToCenter11.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c11x, c11y))
                    distToCenter12.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c12x, c12y))
                    if ((distToCenter11[-1] < distToCenter12[-1])):
                        cluster11.append(k2[i])
                    elif((distToCenter12[-1] < distToCenter11[-1])):
                        cluster12.append(k2[i])
                    #print(k2[i].newNumber)

                if ((count != 0) & (oldCenter11.x == center11.x) & (oldCenter11.y == center11.y) & (oldCenter12.x == center12.x) & (oldCenter12.y == center12.y)):
                    for k in range(len(cluster11)):
                        cluster11[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster12)):
                        cluster12[k].newNumber = index + 1
                        index += 1
                    

                if ((count != 0) & (oldCenter11.x == center11.x) & (oldCenter11.y == center11.y) & (oldCenter12.x == center12.x) & (oldCenter12.y == center12.y)):
                    for k in range(len(cluster11)):
                        cluster11[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster12)):
                        cluster12[k].newNumber = index + 1
                        index += 1

                    clusterDict2 = {'cluster1' : cluster11, 'center1' : oldCenter11, 'cluster2' : cluster12, 'center2' : oldCenter12}
                    break

                distToCenter11.clear()
                distToCenter12.clear()
                oldCenter11 = center11
                oldCenter12 = center12
                center11 = newCenter(cluster11)
                center12 = newCenter(cluster12)
                c11x = center11.x
                c11y = center11.y
                c12x = center12.x
                c12y = center12.y
                cluster11.clear()
                cluster12.clear()
                index = 0
                count += 1
        if (j == 2):
            distToCenter21 = []
            distToCenter22 = []
            distToCenter23 = []
            cluster21 = []
            cluster22 = []
            cluster23 = []
            k3 = copy.deepcopy(listOfPoints)
            center21 = random.choice(listOfPoints)
            c21x = center21.x
            c21y = center21.y
            center22 = random.choice(listOfPoints)
            while ((center21.x == center22.x) & (center21.y == center22.y)):
                center22 = random.choice(listOfPoints)
            c22x = center22.x
            c22y = center22.y
            center23 = random.choice(listOfPoints)
            while (((center21.x == center23.x) & (center21.y == center23.y)) | ((center22.x == center23.x) & (center22.y == center23.y))):
                center23 = random.choice(listOfPoints)
            c23x = center23.x
            c23y = center23.y
            count = 0
            index = 0
            oldCenter21 = Location(0, 0, 0, 0)
            oldCenter22 = Location(0, 0, 0, 0)
            oldCenter23 = Location(0, 0, 0, 0)

            index = 0 
            while True:
                for i in range(len(listOfPoints)):
                    distToCenter21.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c21x, c21y))
                    distToCenter22.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c22x, c22y))
                    distToCenter23.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c23x, c23y))
                    if ((distToCenter21[-1] < distToCenter22[-1]) & (distToCenter21[-1] < distToCenter23[-1])):
                        cluster21.append(k3[i])
                    elif((distToCenter22[-1] < distToCenter21[-1]) & (distToCenter22[-1] < distToCenter23[-1])):
                        cluster22.append(k3[i])
                    elif((distToCenter23[-1] < distToCenter21[-1]) & (distToCenter23[-1] < distToCenter22[-1])):
                        cluster23.append(k3[i])

                if ((count != 0) & (oldCenter21.x == center21.x) & (oldCenter21.y == center21.y) & (oldCenter22.x == center22.x) & (oldCenter22.y == center22.y) & (oldCenter23.x == center23.x) & (oldCenter23.y == center23.y)):
                    for k in range(len(cluster21)):
                        cluster21[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster22)):
                        cluster22[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster23)):
                        cluster23[k].newNumber = index + 1
                        index += 1
                    
                    clusterDict3 = {'cluster1' : cluster21, 'center1' : oldCenter21, 'cluster2' : cluster22, 'center2' : oldCenter22, 'cluster3' : cluster23, 'center3' : oldCenter23}
                if ((count != 0) & (oldCenter21.x == center21.x) & (oldCenter21.y == center21.y) & (oldCenter22.x == center22.x) & (oldCenter22.y == center22.y) & (oldCenter23.x == center23.x) & (oldCenter23.y == center23.y)):
                    for k in range(len(cluster21)):
                        cluster21[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster22)):
                        cluster22[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster23)):
                        cluster23[k].newNumber = index + 1
                        index += 1
                    index = 0

                    clusterDict3 = {'cluster1' : cluster21, 'center1' : oldCenter21, 'cluster2' : cluster22, 'center2' : oldCenter22, 'cluster3' : cluster23, 'center3' : oldCenter23}
                    break
                distToCenter21.clear()
                distToCenter22.clear()
                distToCenter23.clear()
                oldCenter21 = center21
                oldCenter22 = center22
                oldCenter23 = center23
                center21 = newCenter(cluster21)
                center22 = newCenter(cluster22)
                center23 = newCenter(cluster23)
                c21x = center21.x
                c21y = center21.y
                c22x = center22.x
                c22y = center22.y
                c23x = center23.x
                c23y = center23.y
                cluster21.clear()
                cluster22.clear()
                cluster23.clear()
                count += 1
        if (j == 3):
            distToCenter31 = []
            distToCenter32 = []
            distToCenter33 = []
            distToCenter34 = []
            cluster31 = []
            cluster32 = []
            cluster33 = []
            cluster34 = []
            k4 = copy.deepcopy(listOfPoints)
            center31 = random.choice(listOfPoints)
            c31x = center31.x
            c31y = center31.y
            center32 = random.choice(listOfPoints)
            while ((center31.x == center32.x) & (center31.y == center32.y)):
                center32 = random.choice(listOfPoints)
            c32x = center32.x
            c32y = center32.y
            center33 = random.choice(listOfPoints)
            while (((center31.x == center33.x) & (center31.y == center33.y)) | ((center32.x == center33.x) & (center32.y == center33.y))):
                center33 = random.choice(listOfPoints)
            c33x = center33.x
            c33y = center33.y
            center34 = random.choice(listOfPoints)
            while (((center31.x == center34.x) & (center31.y == center34.y)) | ((center32.x == center34.x) & (center32.y == center34.y)) | ((center33.x == center34.x) & (center33.y == center34.y))):
                center34 = random.choice(listOfPoints)
            c34x = center34.x
            c34y = center34.y
            count = 0
            index = 0
            oldCenter31 = Location(0, 0, 0, 0)
            oldCenter32 = Location(0, 0, 0, 0)
            oldCenter33 = Location(0, 0, 0, 0)
            oldCenter34 = Location(0, 0, 0, 0)

            index = 0
            while True:
                for i in range(len(listOfPoints)):
                    distToCenter31.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c31x, c31y))
                    distToCenter32.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c32x, c32y))
                    distToCenter33.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c33x, c33y))
                    distToCenter34.append(Euclidean(listOfPoints[i].x, listOfPoints[i].y, c34x, c34y))
                    if ((distToCenter31[-1] < distToCenter32[-1]) & (distToCenter31[-1] < distToCenter33[-1]) & (distToCenter31[-1] < distToCenter34[-1])):
                        cluster31.append(k4[i])
                    elif((distToCenter32[-1] < distToCenter31[-1]) & (distToCenter32[-1] < distToCenter33[-1]) & (distToCenter32[-1] < distToCenter34[-1])):
                        cluster32.append(k4[i])
                    elif((distToCenter33[-1] < distToCenter31[-1]) & (distToCenter33[-1] < distToCenter32[-1]) & (distToCenter33[-1] < distToCenter34[-1])):
                        cluster33.append(k4[i])
                    elif((distToCenter34[-1] < distToCenter31[-1]) & (distToCenter34[-1] < distToCenter32[-1]) & (distToCenter34[-1] < distToCenter33[-1])):
                        cluster34.append(k4[i])

                if ((count != 0) & (oldCenter31.x == center31.x) & (oldCenter31.y == center31.y) & (oldCenter32.x == center32.x) & (oldCenter32.y == center32.y) & (oldCenter33.x == center33.x) & (oldCenter33.y == center33.y) & (oldCenter34.x == center34.x) & (oldCenter34.y == center34.y)):
                    for k in range(len(cluster31)):
                        cluster31[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster32)):
                        cluster32[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster33)):
                        cluster33[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster34)):
                        cluster34[k].newNumber = index + 1
                        index += 1
                    clusterDict4 = {'cluster1' : cluster31, 'center1' : oldCenter31, 'cluster2' : cluster32, 'center2' : oldCenter32, 'cluster3' : cluster33, 'center3' : oldCenter33, 'cluster4' : cluster34, 'center4' : oldCenter34}
                if ((count != 0) & (oldCenter31.x == center31.x) & (oldCenter31.y == center31.y) & (oldCenter32.x == center32.x) & (oldCenter32.y == center32.y) & (oldCenter33.x == center33.x) & (oldCenter33.y == center33.y) & (oldCenter34.x == center34.x) & (oldCenter34.y == center34.y)):
                    for k in range(len(cluster31)):
                        cluster31[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster32)):
                        cluster32[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster33)):
                        cluster33[k].newNumber = index + 1
                        index += 1
                    index = 0

                    for k in range(len(cluster34)):
                        cluster34[k].newNumber = index + 1
                        index += 1
                    index = 0

                    clusterDict4 = {'cluster1' : cluster31, 'center1' : oldCenter31, 'cluster2' : cluster32, 'center2' : oldCenter32, 'cluster3' : cluster33, 'center3' : oldCenter33, 'cluster4' : cluster34, 'center4' : oldCenter34}
                    break
                distToCenter31.clear()
                distToCenter32.clear()
                distToCenter33.clear()
                distToCenter34.clear()
                oldCenter31 = center31
                oldCenter32 = center32
                oldCenter33 = center33
                oldCenter34 = center34
                center31 = newCenter(cluster31)
                center32 = newCenter(cluster32)
                center33 = newCenter(cluster33)
                center34 = newCenter(cluster34)
                c31x = center31.x
                c31y = center31.y
                c32x = center32.x
                c32y = center32.y
                c33x = center33.x
                c33y = center33.y
                c34x = center34.x
                c34y = center34.y
                cluster31.clear()
                cluster32.clear()
                cluster33.clear()
                cluster34.clear()
                count += 1
    finalDict = {'dict1' : clusterDict1, 'dict2' : clusterDict2, 'dict3' : clusterDict3, 'dict4' : clusterDict4}
    return finalDict

                

                

    

                

                

    