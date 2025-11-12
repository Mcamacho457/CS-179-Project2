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
        outFileName = finalPathToFile(filename, array, collectionOfDistance)
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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test1_2000.txt")

        self.assertEqual(num_pts, 2000, "The one cluster does not have all points, when it should.")
    # test for k = 1 when half the data points are in the bottom left corner and the other half are in the top right corner
    # all data points should be assigned to one big cluster
    def test_1K_2Clusters_KMeans(self):
        filename = "test_cases/1cluster_test2_2000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        landing1_center1 = [dictionary['dict1']['center1']]
        landing1_cluster1 = [dictionary['dict1']['cluster1']]

        num_pts = len(landing1_cluster1[0])

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test2_2000.txt")

        self.assertEqual(num_pts, 2000, "The one cluster does not have all points, when it should.")
    # test for k = 1 when we have 3 clusters. all data points should be assigned to one big cluster with the center being
    # slightly in the top right corner
    def test_1K_3Clusters_KMeans(self):
        filename = "test_cases/3cluster_test3_3000.txt"
        listOfPoints = FileRead(filename)
        dictionary = KM(listOfPoints)

        landing1_center1 = [dictionary['dict1']['center1']]
        landing1_cluster1 = [dictionary['dict1']['cluster1']]

        num_pts = len(landing1_cluster1[0])

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, landing1_cluster1, landing1_center1, clusterPaths, "1cluster_test3_3000.txt")

        self.assertEqual(num_pts, 3000, "The one cluster does not have all points, when it should.")
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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "2cluster_test1_2000.txt")

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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "2cluster_test2_2000.txt")

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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "2cluster_test3_3000.txt")

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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "3cluster_test1_2000.txt")

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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "3cluster_test2_2000.txt")

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

        clusterPaths = []

        # use saveClusterRoutesImg to visualize the results
        saveClusterRoutesImg(listOfPoints, clusters, cluster_centers, clusterPaths, "3cluster_test3_3000.txt")

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
if __name__ == "__main__":
    unittest.main()