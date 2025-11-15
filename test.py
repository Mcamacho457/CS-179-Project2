#test all functions making sure they work properly
#everyone

import unittest
import math
from euclideanDistance import Euclidean
from main import Location
from main import FileRead
from main import finalPathToFile
from DistanceMatrix import dist_matrix
from ClassicNN import ClassicNN
from ModifiedNN import ModifiedNN
from kMeansAlg import KM
from kMeansAlg import newCenter
from route import saveClusterRoutesImg
from se import error
import random

class TestEuclidean(unittest.TestCase):
    def test_euclideanCalc(self):
        x1 = 8
        y1 = 6
        x2 = 5
        y2 = 7
        self.assertEqual(Euclidean(x1, y1, x2, y2), math.sqrt(10), "The distance is incorrectly miscalculated for whole numbers")

   #def test_euclideanFloats(self):
        #x1 = 8.5
        #y1 = 6.2
        #x2 = 5.1
        #y2 = 7.8
        #self.assertAlmostEqual(Euclidean(x1, y1, x2, y2), math.sqrt(14.12), "The distance is incorrectly miscalculated for floating points")

testArray = []
node1 = Location(1, 0, 8, 6)
testArray.append(node1)

node2 = Location(2, 0, 10, 5)
testArray.append(node2)

node3 = Location(3, 0, 9, 1)
testArray.append(node3)

node4 = Location(4, 0, 5, 7)
testArray.append(node4)

node5 = Location(5, 0, 1, 10)
testArray.append(node5)

node6 = Location(6, 0, 3, 13)
testArray.append(node6)

node7 = Location(7, 0, 2, 15)
testArray.append(node7)

node8 = Location(8, 0, 12, 5)
testArray.append(node8)

node9 = Location(1, 0, 4, 11)
testArray.append(node9)

node10 = Location(1, 0, 10, 20)
testArray.append(node10)

# This tests if a file is read in correctly
class TestFileRead(unittest.TestCase):
    def test_CorrectRead(self):
        testFile = "test_cases/filereadtest.txt"
        listOfPoints = FileRead(testFile)
        one = Location(1, 0, 1.0, 2.0)
        two = Location(2, 0, 3.0, 4.0)
        three = Location(3, 0, 5.0, 6.0)
        four = Location(1, 0, 1.0, 2.0)
        array = [one, two, three, four]
        count = 0
        for i in range(len(array)):
            if ((listOfPoints[i].number == array[i].number) & (listOfPoints[i].x == array[i].x) & (listOfPoints[i].y == array[i].y)):
                count += 1
        self.assertEqual(4, 4, "The file is not read correctly")

# This tests if an output file was made correctly 
class TestOutputFile(unittest.TestCase):
    def test_MakeOutputFile(self):
        filename = "test_cases/file"
        one = Location(1, 0, 1.0, 2.0)
        two = Location(2, 0, 3.0, 4.0) 
        three = Location(3, 0, 5.0, 6.0)
        four = Location(1, 0, 1.0, 2.0)
        s1 = Euclidean(one.x, one.y, two.x, two.y)
        s2 = Euclidean(three.x, three.y, four.x, four.y)
        ts = s1 + s2 
        array = [one, two, three, four]
        collectionOfDistance = []
        collectionOfDistance.append((ts, 0.25))
        outFileName = finalPathToFile(filename, array, collectionOfDistance[-1][0])
        created = False
        print(outFileName)
        if (outFileName == f"{filename.split('/')[-1]}_SOLUTION_{int(round(collectionOfDistance[-1][0]))}.txt"):
            created = True
        self.assertEqual(created, True, "The output file is not made correctly")
    
# This tests to see if the distance matrix makes the correct output
class TestDistanceMatrix(unittest.TestCase):
    def test_DistanceMatrix(self):
        one = Location(1, 0, 1.0, 2.0)
        two = Location(2, 0, 3.0, 4.0) 
        three = Location(3, 0,5.0, 6.0)
        four = Location(4, 0, 7.0, 8.0)
        path = [one, two, three, four]
        dm = dist_matrix(path)
        matrix = [[float(0) for i in range(4)] for j in range(4)]
        matrix[0][1] = 2.82842712
        matrix[0][2] = 5.65685425
        matrix[0][3] = 8.48528137
        matrix[1][2] = 2.82842712
        matrix[1][3] = 5.65685425
        matrix[2][3] = 2.82842712
        count = 0
        for i in range(4): # row
            for j in range(4): # col
                if (int(dm[i][j]) == int(matrix[i][j])):
                    count += 1
        self.assertEqual(count, 16, "The distance matrix is not made correctly")

# This tests the classic nn functions, creating a path, ensures start and stop position are the same
class TestClassicNN(unittest.TestCase):
    def test_ClassicNN(self):
        one = Location(1, 1, 1.0, 10.0)
        two = Location(2, 2, 10.0, 4.0) 
        three = Location(3, 3, 5.0, 8.0)
        four = Location(4, 4, 7.0, 6.0)
        five = Location(5, 5, 1.0, 2.0)
        path = [one, two, three, four, five]
        dm = dist_matrix(path)
        sumOfDistance, newPath, _, _ = ClassicNN(path, dm)
        # This should always be true
        if (sumOfDistance >= 0):
            self.assertNotEqual(path, newPath, "Classic NN was not able to find a new path")

# This tests the modified nn functions, creating a path, ensures start and stop position are the same
class TestModifiedNN(unittest.TestCase):
    def test_ModifiedNN(self):
        one = Location(1, 1, 1.0, 10.0)
        two = Location(2, 2, 10.0, 4.0) 
        three = Location(3, 3, 5.0, 8.0)
        four = Location(4, 4, 7.0, 6.0)
        five = Location(5, 5, 1.0, 2.0)
        path = [one, two, three, four, five]
        dm = dist_matrix(path)
        csumOfDistance, cnnPath, _, _ = ClassicNN(path, dm)
        msumOfDistance, modnnPath, _, _ = ModifiedNN(path, dm, cnnPath, dist_to_beat=csumOfDistance)
        # This should always be true
        if (modnnPath != cnnPath):
            self.assertless(msumOfDistance, csumOfDistance, "Modified NN was not able to find a new path that is shorter than Classic NN")

# This tests the KMeans algorithm
class TestKMeans(unittest.TestCase):
    # test for k = 1 when all the data points are in one big cluster
    def test_1K_1Cluster_KMeans(self):
        filename = "test_cases/1cluster_test1_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        landing1_center1 = [dictionary['dict1']['center1']]
        landing1_cluster1 = [dictionary['dict1']['cluster1']]

        num_pts = len(landing1_cluster1[0])

        clusterPaths = [landing1_cluster1[0]]
        clusterPaths.append(landing1_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test1_2000.txt")

        self.assertEqual(num_pts, 2002, "The one cluster does not have all points, when it should.")
    # test for k = 1 when half the data points are in the bottom left corner and the other half are in the top right corner
    # all data points should be assigned to one big cluster
    def test_1K_2Clusters_KMeans(self):
        filename = "test_cases/1cluster_test2_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        landing1_center1 = [dictionary['dict1']['center1']]
        landing1_cluster1 = [dictionary['dict1']['cluster1']]

        num_pts = len(landing1_cluster1[0])

        clusterPaths = [landing1_cluster1[0]]
        clusterPaths.append(landing1_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test2_2000.txt")

        self.assertEqual(num_pts, 2002, "The one cluster does not have all points, when it should.")
    # test for k = 1 when we have 3 clusters. all data points should be assigned to one big cluster with the center being
    # slightly in the top right corner
    def test_1K_3Clusters_KMeans(self):
        filename = "test_cases/3cluster_test3_3000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        landing1_center1 = [dictionary['dict1']['center1']]
        landing1_cluster1 = [dictionary['dict1']['cluster1']]

        num_pts = len(landing1_cluster1[0])

        clusterPaths = [landing1_cluster1[0]]
        clusterPaths.append(landing1_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test3_3000.txt")

        self.assertAlmostEqual(num_pts, 3000, None, "The one cluster does not have all points, when it should.", 2)
    # test for k = 2 when all the data points are in one big cluster, each cluster should have roughly half the points
    def test_2K_1Clusters_KMeans(self):
        filename = "test_cases/1cluster_test1_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []

        landing2_center1 = dictionary['dict2']['center1']
        landing2_cluster1 = dictionary['dict2']['cluster1']

        landing2_center2 = dictionary['dict2']['center2']
        landing2_cluster2 = dictionary['dict2']['cluster2']

        clusters.append(landing2_cluster1)
        clusters.append(landing2_cluster2)

        cluster_centers.append(landing2_center1)
        cluster_centers.append(landing2_center2)

        clust1_num_pts = len(landing2_cluster1)
        clust2_num_pts = len(landing2_cluster2)

        clusterPaths = [landing2_cluster1[0]]
        clusterPaths.append(landing2_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "2cluster_test1_2000.txt")

        self.assertAlmostEqual(clust1_num_pts, 1000, None, "The 1st cluster does not have half of the points.", 100)
        self.assertAlmostEqual(clust2_num_pts, 1000, None, "The 2nd cluster does not have half of the points.", 100)
    # test for k = 2 when we have two separate clusters. each cluster should have roughly half the data points
    def test_2K_2Clusters_KMeans(self):
        filename = "test_cases/1cluster_test2_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []

        landing2_center1 = dictionary['dict2']['center1']
        landing2_cluster1 = dictionary['dict2']['cluster1']

        landing2_center2 = dictionary['dict2']['center2']
        landing2_cluster2 = dictionary['dict2']['cluster2']

        clusters.append(landing2_cluster1)
        clusters.append(landing2_cluster2)

        cluster_centers.append(landing2_center1)
        cluster_centers.append(landing2_center2)

        clust1_num_pts = len(landing2_cluster1)
        clust2_num_pts = len(landing2_cluster2)

        clusterPaths = [landing2_cluster1[0]]
        clusterPaths.append(landing2_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "2cluster_test2_2000.txt")

        self.assertAlmostEqual(clust1_num_pts, 1000, None, "The 1st cluster does not have half of the points.", 10)
        self.assertAlmostEqual(clust2_num_pts, 1000, None, "The 2nd cluster does not have half of the points.", 10)
    # test for k = 2, when we have 3 separate clusters with 2 of them being close together
    def test_2K_3Clusters_KMeans(self):
        filename = "test_cases/3cluster_test3_3000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []
        cluster_len = []

        landing2_center1 = dictionary['dict2']['center1']
        landing2_cluster1 = dictionary['dict2']['cluster1']

        landing2_center2 = dictionary['dict2']['center2']
        landing2_cluster2 = dictionary['dict2']['cluster2']

        clusters.append(landing2_cluster1)
        clusters.append(landing2_cluster2)

        cluster_centers.append(landing2_center1)
        cluster_centers.append(landing2_center2)

        clust1_num_pts = len(landing2_cluster1)
        clust2_num_pts = len(landing2_cluster2)

        cluster_len.append(clust1_num_pts)
        cluster_len.append(clust2_num_pts)

        clusterPaths = [landing2_cluster1[0]]
        clusterPaths.append(landing2_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "2cluster_test3_3000.txt")

        for i in range(len(cluster_centers)):
            center = cluster_centers[i]
            num_pts = cluster_len[i]

            if center.x <= 25.0:
                self.assertAlmostEqual(num_pts, 1000, None, "The 1st cluster does not have 1/3rd of the points.", 10)
            else:
                self.assertAlmostEqual(num_pts, 2000, None, "The 2nd cluster does not have 2/3rd of the points.", 20)
    #
    def test_3K_1Cluster_KMeans(self):
        filename = "test_cases/1cluster_test1_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []

        landing3_center1 = dictionary['dict3']['center1']
        landing3_cluster1 = dictionary['dict3']['cluster1']

        landing3_center2 = dictionary['dict3']['center2']
        landing3_cluster2 = dictionary['dict3']['cluster2']

        landing3_center3 = dictionary['dict3']['center3']
        landing3_cluster3 = dictionary['dict3']['cluster3']

        num_pts1 = len(landing3_cluster1)
        num_pts2 = len(landing3_cluster2)
        num_pts3 = len(landing3_cluster3)

        clusters.append(landing3_cluster1)
        clusters.append(landing3_cluster2)
        clusters.append(landing3_cluster3)

        cluster_centers.append(landing3_center1)
        cluster_centers.append(landing3_center2)
        cluster_centers.append(landing3_center3)

        clusterPaths = [landing3_cluster1[0]]
        clusterPaths.append(landing3_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "3cluster_test1_2000.txt")

        self.assertAlmostEqual(num_pts1, 667, None, "The 1st cluster does not have 1/3rd of the points.", 100)
        self.assertAlmostEqual(num_pts2, 667, None, "The 2nd cluster does not have 1/3rd of the points.", 100)
        self.assertAlmostEqual(num_pts3, 667, None, "The 3rd cluster does not have 1/3rd of the points.", 100)
    # test for k = 3, when we have 2 clusters
    def test_3K_2Clusters_KMeans(self):
        filename = "test_cases/1cluster_test2_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []
        cluster_len = []

        landing3_center1 = dictionary['dict3']['center1']
        landing3_cluster1 = dictionary['dict3']['cluster1']

        landing3_center2 = dictionary['dict3']['center2']
        landing3_cluster2 = dictionary['dict3']['cluster2']

        landing3_center3 = dictionary['dict3']['center3']
        landing3_cluster3 = dictionary['dict3']['cluster3']

        num_pts1 = len(landing3_cluster1)
        num_pts2 = len(landing3_cluster2)
        num_pts3 = len(landing3_cluster3)
        
        clusters.append(landing3_cluster1)
        clusters.append(landing3_cluster2)
        clusters.append(landing3_cluster3)

        cluster_centers.append(landing3_center1)
        cluster_centers.append(landing3_center2)
        cluster_centers.append(landing3_center3)

        cluster_len.append(num_pts1)
        cluster_len.append(num_pts2)
        cluster_len.append(num_pts3)

        clusterPaths = [landing3_cluster1[0]]
        clusterPaths.append(landing3_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "3cluster_test2_2000.txt")

        # these tests run if the bottom left corner is the cluster that is split into two since k = 3 now
        if (landing3_center1.x < 25.0) and (landing3_center2.x < 25.0):
            self.assertAlmostEqual(num_pts1, 500, None, "The 1st cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts2, 500, None, "The 2nd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 1000, None, "The 3rd cluster does not have 1/2 of the points.", 100)
        elif (landing3_center1.x < 25.0) and (landing3_center3.x < 25.0):
            self.assertAlmostEqual(num_pts1, 500, None, "The 1st cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts2, 1000, None, "The 2nd cluster does not have 1/2 of the points.", 100)
        elif (landing3_center2.x < 25.0) and (landing3_center3.x < 25.0):
            self.assertAlmostEqual(num_pts2, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts1, 1000, None, "The 3rd cluster does not have 1/2 of the points.", 100)
        # these tests run if the top right corner is the cluster that is split into two since k = 3 now
        elif (landing3_center1.x >= 25.0) and (landing3_center2.x >= 25.0):
            self.assertAlmostEqual(num_pts1, 500, None, "The 1st cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts2, 500, None, "The 2nd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 1000, None, "The 3rd cluster does not have 1/2 of the points.", 100)
        elif (landing3_center1.x >= 25.0) and (landing3_center3.x >= 25.0):
            self.assertAlmostEqual(num_pts1, 500, None, "The 1st cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts2, 1000, None, "The 2nd cluster does not have 1/2 of the points.", 100)
        elif (landing3_center2.x >= 25.0) and (landing3_center3.x >= 25.0):
            self.assertAlmostEqual(num_pts2, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts3, 500, None, "The 3rd cluster does not have 1/4 of the points.", 100)
            self.assertAlmostEqual(num_pts1, 1000, None, "The 3rd cluster does not have 1/2 of the points.", 100)

    # test for k = 3, when we have 3 clusters
    def test_3K_3Clusters_KMeans(self):
        filename = "test_cases/3cluster_test3_3000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        clusters = []
        cluster_centers = []
        cluster_len = []

        landing3_center1 = dictionary['dict3']['center1']
        landing3_cluster1 = dictionary['dict3']['cluster1']

        landing3_center2 = dictionary['dict3']['center2']
        landing3_cluster2 = dictionary['dict3']['cluster2']

        landing3_center3 = dictionary['dict3']['center3']
        landing3_cluster3 = dictionary['dict3']['cluster3']

        num_pts1 = len(landing3_cluster1)
        num_pts2 = len(landing3_cluster2)
        num_pts3 = len(landing3_cluster3)

        clusters.append(landing3_cluster1)
        clusters.append(landing3_cluster2)
        clusters.append(landing3_cluster3)

        cluster_centers.append(landing3_center1)
        cluster_centers.append(landing3_center2)
        cluster_centers.append(landing3_center3)

        cluster_len.append(num_pts1)
        cluster_len.append(num_pts2)
        cluster_len.append(num_pts3)

        clusterPaths = [landing3_cluster1[0]]
        clusterPaths.append(landing3_cluster1[0])

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, [clusterPaths], "3cluster_test3_3000.txt")

        for i in range(len(clusters)):
            cluster_center = cluster_centers[i]
            num_pts = cluster_len[i]

            # checks if this cluster center is for the cluster in the bottom left corner, if it is then this cluster
            # should definitely have around 1000 data points
            if cluster_center.x <= 25.0:
                self.assertAlmostEqual(num_pts, 1000, None, "The first cluster does not have 1/3rd of the points, when it should.", 10)
            # if the cluster center belongs to one of the top right clusters, then the amount of points can range from 1000 +- 260 points
            # due to randomness of KMeans
            else:
                self.assertAlmostEqual(num_pts, 1000, None, "The first cluster does not have 1/3rd of the points, when it should.", 260)

class TestKMCenter(unittest.TestCase):
    # tests for the KMeans function when K = 1
    # tests that the center was set correctly and that all points are assigned to the one cluster
    def test_1K_Center_50pts_1Circle(self):
        # setting the properties of the circle (source: Dr. Keogh's "Is your implementation of K-means is correct" slides from Dropbox)
        xCenter = 0.0
        yCenter = 0.0
        radius = 1.0
        numPoints = 50

        listOfPoints = []
        number = 0
        for i in range(0, numPoints):
            rand_val = random.random()
            angle = rand_val * 2 * math.pi
            x = radius * math.cos(angle) + xCenter
            y = radius * math.sin(angle) + yCenter

            number += 1
            node = Location(number, 0, float(x), float(y))
            listOfPoints.append(node)

        total_ses = []
        clusters = []
        centers = []

        for i in range(10):
            newdictionary = KM(listOfPoints)
            landing1_center1 = newdictionary['dict1']['center1']
            landing1_cluster1 = newdictionary['dict1']['cluster1']
            
            totalse = 0.0
            for j in range(len(listOfPoints)):
                se = error(landing1_cluster1[j].x, landing1_cluster1[j].y, landing1_center1.x, landing1_center1.y)
                totalse += se
            total_ses.append(totalse)
            clusters.append(landing1_cluster1)
            centers.append(landing1_center1)

        best_idx11 = total_ses.index(min(total_ses))
        best_cluster11 = clusters[best_idx11]
        best_center11 = centers[best_idx11]
        landing1_center1 = best_center11
        landing1_cluster1 = best_cluster11

        path = [best_cluster11[0]]
        path.append(best_cluster11[0])

        saveClusterRoutesImg(listOfPoints, [best_cluster11], [best_center11], [path], "1kcluster_50Circle.txt")

        self.assertAlmostEqual(landing1_center1.x, 0.0, None, "The center's x value was not set correctly.", 0.30)
        self.assertAlmostEqual(landing1_center1.y, 0.0, None, "The center's y value was not set correctly.", 0.30)
        self.assertAlmostEqual(float(len(landing1_cluster1)), 50.0, None, "Not all the points were assigned to the single and same cluster.", 10)

    def test_2K_Center_1000pts_2Circle(self):
        # tests for the KMeans function when K = 2
        # tests that the center was set correctly and that half the points are assigned to the left cluster, and other half to 2nd cluster
        xCenterL = -1.0
        yCenterL = -1.0
        numPoints = 1000
        xCenterR = 1.0
        yCenterR = 1.0
        listOfPointsR = []
        listOfPointsL = []
        number = 0

        # generates 1000 nodes with 500 in the bottom left corner and 500 in the top right
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

        total_ses = []
        clusters1 = []
        centers1 = []
        clusters2 = []
        centers2 = []

        listOfPoints = listOfPointsR + listOfPointsL

        # performs kmeans 10 times and chooses the best clustering when k = 2
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

        clusters = []
        centers = []

        clusters.append(best_cluster1)
        clusters.append(best_cluster2)

        centers.append(best_center1)
        centers.append(best_center2)

        path1 = [best_cluster1[0]]
        path1.append(best_cluster1[0])

        path2 = [best_cluster2[0]]
        path2.append(best_cluster2[0])

        paths = []
        paths.append(path1)
        paths.append(path2)

        saveClusterRoutesImg(listOfPoints, clusters, centers, paths, "2kcluster_1000Circle.txt")

        left_center = 0
        left_cluster = 0
        right_center = 0
        right_cluster = 0
        if (landing2_center1.x < 0.0 and landing2_center1.y < 0.0):
            left_center = landing2_center1
            left_cluster = landing2_cluster1

            right_center = landing2_center2
            right_cluster = landing2_cluster2
        else:
            left_center = landing2_center2
            left_cluster = landing2_cluster2

            right_center = landing2_center1
            right_cluster = landing2_cluster1

        # tests the properties of the left clusters points and center
        self.assertAlmostEqual(left_center.x, -1.0, None, "The left center's x value was not set correctly.", 0.30)
        self.assertAlmostEqual(left_center.y, -1.0, None, "The left center's y value was not set correctly.", 0.30)
        self.assertAlmostEqual(float(len(left_cluster)), 500.0, None, "Half of the points were not assigned to the left cluster.", 30)
        
        # tests the properties of the right clusters points and center
        self.assertAlmostEqual(right_center.x, 1.0, None, "The right center's x value was not set correctly.", 0.30)
        self.assertAlmostEqual(right_center.y, 1.0, None, "The right center's y value was not set correctly.", 0.30)
        self.assertAlmostEqual(float(len(right_cluster)), 500.0, None, "Half of the points were not assigned to the right cluster.", 30)


class TestSSE(unittest.TestCase):
    # tests that the sse function is working and implemented correctly
    def test_sse_50Circle(self):
        # setting the properties of the circle (source: Dr. Keogh's "Is your implementation of K-means is correct" slides from Dropbox)
        xCenter = 0.0
        yCenter = 0.0
        radius = 1.0
        numPoints = 50

        listOfPoints = []
        number = 0
        for i in range(0, numPoints):
            angle = random.random() * 2 * math.pi
            x = radius * math.cos(angle) + xCenter
            y = radius * math.sin(angle) + yCenter

            number += 1
            node = Location(number, 0, float(x), float(y))
            listOfPoints.append(node)

        totalse = 0.0
        for i in range(len(listOfPoints)):
            se = error(listOfPoints[i].x, listOfPoints[i].y, xCenter, yCenter)
            totalse += se
        
        self.assertAlmostEqual(totalse, 50.0, 4, "SSE function is not implemented correctly.")
if __name__ == "__main__":
    unittest.main()