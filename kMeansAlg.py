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
     # if there is only one point in the cluster then we assign the center to that data points coordinates
     # to minimize the distance from the center for that cluster
     else:
         return Location(cluster[0].number, 0, cluster[0].x, cluster[0].y)

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
            # stores the locations that are in cluster 1
            cluster01 = []
            k1 = copy.deepcopy(listOfPoints) # creates a deep copy so we don't change the original array
            center01 = random.choice(listOfPoints) # randomly selects a point to be the center of the cluster

            # iterate through the list of points to create the cluster
            for i in range(len(listOfPoints)):
                cluster01.append(k1[i])

            # Make a new center for 1 cluster this can only be done one time 
            # no distance calculations needed to figure out which cluster to put in   
            center01 = newCenter(cluster01)
            # We clear the the cluster
            cluster01.clear()

            cluster01.append(center01)
            cluster01[0].newNumber = 1

            # for the length of list of points since it is one cluster
            for i in range(len(listOfPoints)):
                    # if i is 0 we need to add the new center found to the front of the cluster
                    # also need to make its newnumber one for iteration purposes
                    # The way our classic nn and modified nn are implemented we need to reindex the cluster to iterate through it
                    k1[i].newNumber = i + 2
                    # We add to the cluster
                    cluster01.append(k1[i])

            cluster01.append(center01)

            # Return a dictionary that contains the cluster and the center
            # The cluster so we can iterate through it
            # The center so that we can display the point
            clusterDict1 = {'cluster1' : cluster01, 'center1' : center01}

        # For two clusters
        if (j == 1):
            # stores the locations that are in cluster 1
            cluster11 = []
            # stores the locations that are in cluster 2
            cluster12 = []
            k2 = copy.deepcopy(listOfPoints) #we use deepcopy so we manipulate the elements without messing with original array
            center11 = random.choice(listOfPoints) # randomly selects a point to be the center of cluster 1
            c11x = center11.x
            c11y = center11.y
            center12 = random.choice(listOfPoints) # randomly selects a point to be the center of cluster 2
            # checks if the point selected to be the center for cluster 2 is the same point selected for the center of cluster 1
            # if the two centers are the same, keep randomly selecting a new center until they are different
            while ((center11.x == center12.x) & (center11.y == center12.y)):
                center12 = random.choice(listOfPoints)
            c12x = center12.x
            c12y = center12.y
            count = 0
            oldCenter11 = Location(0, 0, 0, 0)
            oldCenter12 = Location(0, 0, 0, 0)

            # loop for finding new centers
            while True:

                # loop for assigning to cluster
                for i in range(len(listOfPoints)): 
                    # we need to calculate the distance of a point from center 1 and center 2 
                    d1 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c11x, c11y)
                    d2 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c12x, c12y)
                    # if closer to center 1 it belongs to cluster 1
                    if (d1 <= d2):
                        cluster11.append(k2[i])
                    # if closer to center 2 it belongs to cluster 2
                    elif (d2 < d1):
                        cluster12.append(k2[i])

                # If it is no longer the first iteration and we can not find new centers then we must stop trying to assign to clusters
                if ((count != 0) & (oldCenter11.x == center11.x) & (oldCenter11.y == center11.y) & (oldCenter12.x == center12.x) & (oldCenter12.y == center12.y)):
                    
                    # We want to incorporate the center into the path so we can iterate the shortest path from it 
                    # If a center is something already in the cluster we need to remove it and insert to the front
                    cluster11.insert(0, center11)
                    # after we need to reassign new numbers so that we can iterate correctly in cnn/mnn
                    for k in range(len(cluster11)):
                        cluster11[k].newNumber = k + 1
                    # finally need to add the center to the back so we stop at it 
                    cluster11.append(center11)

                    # this process above is done for the second cluster as well
                    cluster12.insert(0, center12)
                    for k in range(len(cluster12)):
                        cluster12[k].newNumber = k + 1
                    cluster12.append(center12)           

                    # we return a dictionary so that it is easy to access the clusters and centers later
                    clusterDict2 = {'cluster1' : cluster11, 'center1' : center11, 'cluster2' : cluster12, 'center2' : center12}
                    # we break since there is no new centers/cluster assignments needed
                    break

                # here we keep track of the old center for comparison to stop 
                oldCenter11 = center11
                oldCenter12 = center12
                # gets new centers
                center11 = newCenter(cluster11)
                center12 = newCenter(cluster12)
                # for some reason after using rand.choice i could get the x and y using center.x so i had to use this 
                # but it works here for some reason
                c11x = center11.x
                c11y = center11.y
                c12x = center12.x
                c12y = center12.y
                count += 1
                 # clearing here prevents us from adding to an old cluster
                # also noticed if placed at the bottom results would change
                cluster11.clear()
                cluster12.clear()
        
        # The bottomm portion for 3 clusters and 4 clusters are not commented much
        # This is because if you follow the algorithm for part 2
        # It is exactly the same logic wise and code wise you just add another cluster
        # This is for 3 clusters

        if (len(listOfPoints) > 2):
            if (j == 2):
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
                oldCenter21 = Location(0, 0, 0, 0)
                oldCenter22 = Location(0, 0, 0, 0)
                oldCenter23 = Location(0, 0, 0, 0)

                while True:

                    for i in range(len(listOfPoints)):
                        d1 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c21x, c21y)
                        d2 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c22x, c22y)
                        d3 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c23x, c23y)
                        if ((d1 <= d2) & (d1 <= d3)):
                            cluster21.append(k3[i])
                        elif ((d2 < d1) & (d2 < d3)):
                            cluster22.append(k3[i])
                        elif ((d3 < d1) & (d3 < d2)):
                            cluster23.append(k3[i])

                    if ((count != 0) & (oldCenter21.x == center21.x) & (oldCenter21.y == center21.y) & (oldCenter22.x == center22.x) & (oldCenter22.y == center22.y) & (oldCenter23.x == center23.x) & (oldCenter23.y == center23.y)):
                    
                        cluster21.insert(0, center21)
                        for k in range(len(cluster21)):
                            cluster21[k].newNumber = k + 1
                        cluster21.append(center21)

                        cluster22.insert(0, center22)
                        for k in range(len(cluster22)):
                            cluster22[k].newNumber = k + 1 
                        cluster22.append(center22)
                    
                        cluster23.insert(0, center23)
                        for k in range(len(cluster23)):
                            cluster23[k].newNumber = k + 1  
                        cluster23.append(center23)

                        clusterDict3 = {'cluster1' : cluster21, 'center1' : center21, 'cluster2' : cluster22, 'center2' : center22, 'cluster3' : cluster23, 'center3' : center23}
                        break

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
                    count += 1
                    cluster21.clear()
                    cluster22.clear()
                    cluster23.clear()
        
        # This is for cluster 4
        if (len(listOfPoints) > 3):
            if (j == 3):
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
                oldCenter31 = Location(0, 0, 0, 0)
                oldCenter32 = Location(0, 0, 0, 0)
                oldCenter33 = Location(0, 0, 0, 0)
                oldCenter34 = Location(0, 0, 0, 0)

                while True:

                    for i in range(len(listOfPoints)):
                        d1 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c31x, c31y)
                        d2 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c32x, c32y)
                        d3 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c33x, c33y)
                        d4 = Euclidean(listOfPoints[i].x, listOfPoints[i].y, c34x, c34y)
                        if ((d1 <= d2) & (d1 <= d3) & (d1 <= d4)):
                            cluster31.append(k4[i])
                        elif((d2 < d1) & (d2 < d3) & (d2 < d4)):
                            cluster32.append(k4[i])
                        elif((d3 < d1) & (d3 < d2) & (d3 < d4)):
                            cluster33.append(k4[i])
                        elif((d4 < d1) & (d4 < d2) & (d4 < d3)):
                            cluster34.append(k4[i])
  
                    if ((count != 0) & (oldCenter31.x == center31.x) & (oldCenter31.y == center31.y) & (oldCenter32.x == center32.x) & (oldCenter32.y == center32.y) & (oldCenter33.x == center33.x) & (oldCenter33.y == center33.y) & (oldCenter34.x == center34.x) & (oldCenter34.y == center34.y)):
                   
                        cluster31.insert(0, center31)
                        for k in range(len(cluster31)):
                            cluster31[k].newNumber = k + 1
                        cluster31.append(center31)

                        cluster32.insert(0, center32)
                        for k in range(len(cluster32)):
                            cluster32[k].newNumber = k + 1 
                        cluster32.append(center32)
                    
                        cluster33.insert(0, center33)
                        for k in range(len(cluster33)):
                            cluster33[k].newNumber = k + 1  
                        cluster33.append(center33)

                        cluster34.insert(0, center34)
                        for k in range(len(cluster34)):
                            cluster34[k].newNumber = k + 1  
                        cluster34.append(center34)

                        clusterDict4 = {'cluster1' : cluster31, 'center1' : center31, 'cluster2' : cluster32, 'center2' : center32, 'cluster3' : cluster33, 'center3' : center33, 'cluster4' : cluster34, 'center4' : center34}
                        break
            
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
                    count += 1
                    cluster31.clear()
                    cluster32.clear()
                    cluster33.clear()
                    cluster34.clear()

    finalDict = {'dict1' : clusterDict1, 'dict2' : clusterDict2, 'dict3' : clusterDict3, 'dict4' : clusterDict4}
    return finalDict


                

                

    

                

                

    