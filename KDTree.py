import numpy as np


class KDTree:
    """
    K-Dimensional Tree Partitioning
    """
    def __init__(self, max_size, max_distance):
        self.max_size = max_size
        self.max_distance = max_distance
        self.dataset = []
        self.groups = []
        self.NGroups = 0
        self.k = 0

    def get_distance(self, d1, d2):
        """

        :param d1:
        :param d2:
        :return: euclidean distance between d1 and d2
        """
        return np.linalg.norm(np.array(d1) - np.array(d2))

    def get_max_distance(self, dataset):
        """

        :param dataset:
        :return: maximum distance between two pairs in the dataset
        """
        max_d = 0
        range_of_atts = [[float('inf'), -float('inf')] for _ in range(len(dataset[0]))]
        for i in range(len(dataset)):
            for k in range(len(dataset[i])):
                if dataset[i][k] < range_of_atts[k][0]:
                    range_of_atts[k][0] = dataset[i][k]
                if dataset[i][k] > range_of_atts[k][1]:
                    range_of_atts[k][1] = dataset[i][k]
            for j in range(i):
                d = self.get_distance(dataset[i], dataset[j])
                if d > max_d:
                    max_d = d
        return max_d, range_of_atts

    def max_same_group(self, groups):
        grps = {}
        for val in groups:
            if val in grps:
                grps[val] += 1
            else:
                grps[val] = 1
        max_gr = 0
        for k in grps:
            if grps[k] > max_gr:
                max_gr = grps[k]
        return max_gr

    def recursive_split(self, data_groups, indexes, range_of_atts, from_att):
        #Recursively split the dataset into 2^^k sub groups
        if from_att == self.k:
            return data_groups, indexes
        else:
            new_data_groups = []
            new_indexes = []
            for i in range(len(data_groups)):
                group = data_groups[i]
                index = indexes[i]
                group1 = []
                group2 = []
                index1 = []
                index2 = []
                mid_point = (range_of_atts[from_att][1] + range_of_atts[from_att][0]) / 2
                for j in range(len(group)):
                    if group[j][from_att] < mid_point:
                        group1.append(group[j])
                        index1.append(index[j])
                    else:
                        group2.append(group[j])
                        index2.append(index[j])
                if len(group1) > 0:
                    new_data_groups.append(group1)
                    new_indexes.append(index1)
                if len(group2) > 0:
                    new_data_groups.append(group2)
                    new_indexes.append(index2)
            return self.recursive_split(new_data_groups, new_indexes, range_of_atts, from_att + 1)

    def split_dataset(self, data, range_of_atts):
        # split the dataset into 2^^k sub groups
        return self.recursive_split([data], [[i for i in range(len(data))]], range_of_atts, 0)

    def partition_group(self, data):
        # Check whether the splitting is required then returns the group index for each tuple
        max_d, range_of_atts = self.get_max_distance(data)
        if len(data) > self.max_size or max_d > self.max_distance:
            group_of_data, indexes = self.split_dataset(data, range_of_atts)
            groups = []
            for i in range(len(group_of_data)):
                groups.append(self.partition_group(group_of_data[i]))
            g = 0
            final_groups = [0 for _ in range(len(data))]
            for i in range(len(groups)):
                n_groups = 0
                for j in range(len(indexes[i])):
                    idx = indexes[i][j]
                    final_groups[idx] = g + groups[i][j]
                    n_groups = max(n_groups, groups[i][j])
                g += 1 + n_groups
            return final_groups
        else:
            return [0 for _ in range(len(data))]

    def fit(self, dataset):
        # Fit the model to the input dataset
        self.dataset = dataset
        self.k = len(dataset[0])

        self.groups = self.partition_group(dataset)
        self.NGroups = np.max(self.groups) + 1

    def get_classes(self):
        """

        :return: group index for each vector
        """
        return self.groups

    def get_partitioned_data(self):
        """

        :return: groups of vectors
        """
        partitioned = [[] for _ in range(self.NGroups)]
        for i in range(len(self.dataset)):
            g = self.groups[i]
            partitioned[g - 1].append(self.dataset[i])
        return partitioned

    def get_group_sizes(self):
        """

        :return: size of each group after partitioning
        """
        partitioned = self.get_partitioned_data()
        return [len(partitioned[i]) for i in range(self.NGroups)]


    def get_centroids(self):
        """

        :return: center of each group after partitioning
        """
        partitioned = self.get_partitioned_data()
        centroids = [None for _ in range(self.NGroups)]
        for i in range(self.NGroups):
            group = partitioned[i]
            center = (np.sum(group, axis=0)) / len(group)
            centroids[i] = center
        return centroids
