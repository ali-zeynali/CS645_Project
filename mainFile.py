from Direct import *
from KDTree import *
from Sketch import *


import numpy as np
#
# direct = Direct()
# direct.load_data("../test.csv", "test")
#
#
# solution = direct.direct_algorithm("test", True, "sum_disc_price", [[None, None], [None, None], [None, None], [None, None],[200,600],[None, None],[0.2, 12],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None]],
#                                    [12, 18])
#
# print("n: {0}".format(len(solution)))
# # for i in range(len(solution)):
# #     print(i, ") :", solution[i])



# data = []

# k = 5
# for i in range(50):
#     d = []
#     for ki in range(k):
#         d.append(np.random.random()*4+1)
#     data.append(d)
#
# data = [[2,0], [3,2], [2,2]]
# # kdTree = KDTree(5, 2)
# # kdTree.fit(data)
# # groups = kdTree.groups
# # print(groups)
# # print(kdTree.NGroups)
# # group_of_data = [[] for _ in range(kdTree.NGroups)]
# # for i in range(len(data)):
# #     g = groups[i]
# #     group_of_data[g-1].append(data[i])
# # #
# # # for g in range(kdTree.NGroups):
# #     print(g, ") ", group_of_data[g])
#
#
# print(np.sum(data, axis=0))

sketch = Sketch(None)
data = [[1,1], [2,2], [1,2], [2,1]]

sketch_ns = sketch.sketch_numbers(["b", "a"],data, [1,2,3,1], True, "a", [[2, 5], [3,6]], [2,7])
print(sketch_ns)
