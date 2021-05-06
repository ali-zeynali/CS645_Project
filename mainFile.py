from Direct import *
from KDTree import *
from Sketch import *
from GBT import *
from time import time
import json
import numpy as np

def query1(percent):
    initial_time = time()
    direct = Direct()
    direct.load_data("../{0}Percent.csv".format(percent), "name")
    # print("data loaded")
    q1 = direct.direct_algorithm("name", True, "count_order",
                                 [[None, None], [None, 15469853.7043], [None, 45279795.0584], [None, 95250227.7918],
                                  [None, 50.353948653], [None, 68677.5852459], [None, 0.110243522496],
                                  [None, 77782.028739], [None, None], [None, None], [None, None], [None, None],
                                  [None, None], [None, None]],
                                 [1, None])

    end_time = time()

    return end_time - initial_time

def query2(percent):
    initial_time = time()
    direct = Direct()
    direct.load_data("../{0}Percent.csv".format(percent), "name")
    q2 = direct.direct_algorithm("name", False, "ps_min_supplycost",
                                 [[None, None], [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, 8], [None, None], [None, None],
                                  [None, None], [None, None]],
                                 [1, None])

    end_time = time()
    return end_time - initial_time

def query3(percent):
    initial_time = time()
    direct = Direct()
    direct.load_data("../{0}Percent.csv".format(percent), "name")
    q3 = direct.direct_algorithm("name", False, None,
                                 [[None, None], [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None], [None, None], [413930.849506, None],
                                  [None, None], [None, None]],
                                 [1, None])

    end_time = time()
    return end_time - initial_time

def query4(percent):
    initial_time = time()
    direct = Direct()
    direct.load_data("../{0}Percent.csv".format(percent), "name")
    q3 = direct.direct_algorithm("name", False, None,
                                 [[None, None], [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None], [None, None], [None, None],
                                  [None, 453998.242103], [3, None]],
                                 [1, None])

    end_time = time()
    return end_time - initial_time



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

# sketch = Sketch(None)
# data = [[1,1], [2,2], [1,2], [2,1]]
#
# sketch_ns = sketch.sketch_numbers(["b", "a"],data, [1,2,3,1], True, "a", [[2, 5], [3,6]], [2,7])
# print(sketch_ns)

# percentages = [10, 20, 30]
# time_array = {}
# time_array["q1"] = []
# time_array["q2"] = []
# time_array["q3"] = []
# time_array["q4"] = []
# time_array["percentages"] = percentages
# for p in percentages:
#     q2 = query2(p)
#     q3 = query3(p)
#     q4 = query4(p)
#     time_array["q2"].append(q2)
#     time_array["q3"].append(q3)
#     time_array["q4"].append(q4)
#
#
# with open("direct_output.json", 'w') as writer:
#     json.dump(time_array, writer)

all_groups = [
    [[1,2], [0,2], [1,0]],
    [[3,2], [3,2], [3,1], [3,0]],
    [[1, 3], [ 0, 4]],
    [[4, 4], [3,4], [4,3]]
]
centroids = [[1,1], [3,1], [1,3], [3,3]]

gbt = GBT("name", ["a", "b"], all_groups, centroids, True, "a", [[1, None], [1, None]], [1,None])

p, f = gbt.Refine([0,1,2,3], [0,1,2,3], [0,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1])
print(p)
