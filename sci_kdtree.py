from Direct import *
import numpy as np
from sklearn.neighbors import KDTree
import math


 

class KD_tree:
	def __init__(self, threshold):
        
		self.threshold = threshold
		

	def Partitioning(self, data):

		threshold = math.floor(self.threshold * len(data))
		n_clusters = math.ceil(len(data)/threshold)
		data = np.asarray(data)
		
		tree = KDTree(data, leaf_size=2)
		
		groups = []
		centroids = []	
		for i in range(n_clusters):
			# print(str(i) + " from " + str(n_clusters))
			sub_groups = []
			if(i != n_clusters - 1):
				dist, ind = tree.query(data[:1], k=threshold)
				for ind_temp in ind[0]:
					sub_groups.append(data[ind_temp])
				new_data = np.delete(data, ind[0], 0)
			else:
				dist, ind = tree.query(data[:1], k=len(data))
				for ind_temp in ind[0]:
					sub_groups.append(data[ind_temp])
				new_data = np.delete(data, ind[0], 0)
			# coumpute centroids by averaging			
			sub_groups = np.asarray(sub_groups)
			centroids.append(np.mean(sub_groups, axis=0))			

			data = new_data
			if(i != n_clusters - 1):
				tree = KDTree(data, leaf_size=2)
			groups.append(sub_groups)
		groups = np.asarray(groups)
		centroids = np.asarray(centroids)
		return groups, centroids, n_clusters
			





