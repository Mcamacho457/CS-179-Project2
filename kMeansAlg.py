import random
from euclideanDistance import Euclidean
from Location import Location

# kmeans algorithm implemented form scratch
# returns a finalPathDict where {1: points in cluster 1, 2: points in cluster 2, ...}
class KMeans:
    def __init__(self, num_clusters, num_random_seeds, random_state):
        self.num_clusters = num_clusters
        self.num_random_seeds = num_random_seeds
        self.random_state = random_state
    def fit(self, pts_array):
        solution = {}
        if (self.num_clusters == 1):
            solution = self.fit1(pts_array)
        elif (self.num_clusters == 2):
            solution = self.fit2(pts_array)
        elif (self.num_clusters == 3):
            solution = self.fit3(pts_array)
        elif (self.num_clusters == 4):
            solution = self.fit4(pts_array)
        return solution
    
    def fit1(self, pts_array):
        solution = {}
        sum_x = 0.0
        sum_y = 0.0
        for i in range(0, len(pts_array)):
            sum_x += pts_array[i].x
            sum_y += pts_array[i].y
        mean_x = sum_x / float(len(pts_array))
        mean_y = sum_y / float(len(pts_array))

        clust_center = Location(len(pts_array) + 1, mean_x, mean_y)
        pts_array.insert(0, clust_center)
        solution["cluster1"] = pts_array
        return solution
    def fit2(self, pts_array):
        best_solution = {}
        cluster1 = []
        cluster2 = []
        pts_array2 = pts_array
        rand_clust_ind = random.randint(0, len(pts_array2))
        clust_center1 = pts_array2[rand_clust_ind]
        clust_center1.number = -1

        pts_array2.pop(rand_clust_ind)
        rand_clust_ind2 = random.randint(0, len(pts_array2))
        clust_center2 = pts_array2[rand_clust_ind2]
        clust_center2.number = -2

        nodes_have_changed = True
        orig_cluster1_nodes = set()
        orig_cluster2_nodes = set()
        while nodes_have_changed:
            new_cluster1_nodes = set()
            new_cluster2_nodes = set()
            # determines which cluster center the given point is closest to and assigns it to that cluster
            for j in range(0, len(pts_array)):
                dist_frm_center1 = Euclidean(clust_center1.x, clust_center1.y, pts_array[j].x, pts_array[j].y)
                dist_frm_center2 = Euclidean(clust_center2.x, clust_center2.y, pts_array[j].x, pts_array[j].y)
                if (dist_frm_center1 < dist_frm_center2):
                    cluster1.append(pts_array[j])
                    new_cluster1_nodes.add(pts_array[j].number)
                else:
                    cluster2.append(pts_array[j])
                    new_cluster2_nodes.add(pts_array[j].number)
            # check if the new cluster is different from the old cluster
            # but how do we check this?
            # if the new clusters are not different from the old clusters, then return the clusters as a solution
            if ((orig_cluster1_nodes == new_cluster1_nodes) and (orig_cluster2_nodes == new_cluster2_nodes)):
                cluster1.insert(0, clust_center1)
                best_solution["cluster1"] = cluster1
                
                cluster2.insert(0, clust_center2)
                best_solution["cluster2"] = cluster2
                nodes_have_changed = False
                return best_solution

            # scenario 1: when it is the first iteration, no nodes will have changed from one set to another so we just
            # assign the new center of each cluster to the mean of the points in each cluster
            # scenario 2: if the new clusters are different from the old clusters, then move centeroid and keep iterating
            else:
                # now get the mean and set as new center center
                num_pts1 = len(cluster1)
                sum_x1 = 0.0
                sum_y1 = 0.0
                for z in range(0, num_pts1):
                    sum_x1 += cluster1[z].x
                    sum_y1 += cluster1[z].y
                mean_x1 = sum_x1 / float(num_pts1)
                mean_y1 = sum_y1 / float(num_pts1)

                clust_center1.x = mean_x1
                clust_center1.y = mean_y1

                num_pts2 = len(cluster2)
                sum_x2 = 0.0
                sum_y2 = 0.0
                for z in range(0, num_pts2):
                    sum_x2 += cluster2[z].x
                    sum_y2 += cluster2[z].y
                mean_x2 = sum_x2 / float(num_pts2)
                mean_y2 = sum_y2 / float(num_pts2)

                clust_center2.x = mean_x2
                clust_center2.y = mean_y2
                
                orig_cluster1_nodes.clear()
                orig_cluster2_nodes.clear()
                orig_cluster1_nodes = new_cluster1_nodes
                orig_cluster2_nodes = new_cluster2_nodes

                new_cluster1_nodes.clear()
                cluster1.clear()

                new_cluster2_nodes.clear()
                cluster2.clear()