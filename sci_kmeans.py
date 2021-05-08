import numpy as np
from sklearn.cluster import KMeans


class K_means:
    def __init__(self, n_clusters):

        self.n_clusters = n_clusters

    def Partitioning(self, data):

        data = np.asarray(data)
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=0).fit(data)

        labels = kmeans.labels_
        unique, counts = np.unique(labels, return_counts=True)
        n_clusters = len(unique)
        groups = []

        dic_temp = {}

        ind_d = 0
        for d_ in data:
            if (labels[ind_d] in dic_temp):
                dic_temp[labels[ind_d]].append(d_)
            else:
                dic_temp[labels[ind_d]] = [d_]
            ind_d = ind_d + 1

        for i in range(n_clusters):
            groups.append(np.asarray(dic_temp[i]))

        centroids = kmeans.cluster_centers_
        groups = np.asarray(groups)

        return groups, centroids, n_clusters