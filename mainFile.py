from Direct import *
from KDTree import *
from Sketch import *
from GBT import *
from time import time
import json
import numpy as np
from sci_kdtree import *

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



def query1_GBT(csv_header, gr, cen,ncl, Ps):
    starting = time()
    gbt = GBT("name", csv_header, gr, cen, True, "count_order",
                                 [[None, 15469853.7043], [None, 45279795.0584], [None, 95250227.7918],
                                  [None, 50.353948653], [None, 68677.5852459], [None, 0.110243522496],
                                  [None, 77782.028739], [None, None], [None, None], [None, None], [None, None],
                                  [None, None], [None, None]],
                                 [1, None])
    p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
    # q1 = direct.direct_algorithm("name", True, "count_order",
    #                              [[None, None], [None, 15469853.7043], [None, 45279795.0584], [None, 95250227.7918],
    #                               [None, 50.353948653], [None, 68677.5852459], [None, 0.110243522496],
    #                               [None, 77782.028739], [None, None], [None, None], [None, None], [None, None],
    #                               [None, None], [None, None]],
    #                              [1, None])


    return time() - starting

def query2_GBT(csv_header, gr, cen,ncl, Ps):
    starting = time()
    gbt = GBT("name", csv_header, gr, cen, False, "ps_min_supplycost",
                                 [[None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, 8], [None, None], [None, None],
                                  [None, None], [None, None]],
                                 [1, None])
    p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
    # q2 = direct.direct_algorithm("name", False, "ps_min_supplycost",
    #                              [[None, None], [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, 8], [None, None], [None, None],
    #                               [None, None], [None, None]],
    #                              [1, None])

    return time() - starting

def query2_changed(csv_header, gr, cen,ncl, Ps):
    starting = time()
    gbt = GBT("name", csv_header, gr, cen, False, None,
                                 [[None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, 8], [None, None], [None, None],
                                  [None, None], [None, None]],
                                 [1, None])
    p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
    # q2 = direct.direct_algorithm("name", False, "ps_min_supplycost",
    #                              [[None, None], [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, 8], [None, None], [None, None],
    #                               [None, None], [None, None]],
    #                              [1, None])

    return time() - starting

def query3_GBT(csv_header, gr, cen,ncl, Ps):
    starting = time()
    gbt = GBT("name", csv_header, gr, cen, False, None,
                                 [[None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None], [None, None], [413930.849506, None],
                                  [None, None], [None, None]],
                                 [1, None])
    p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
    # q3 = direct.direct_algorithm("name", False, None,
    #                              [[None, None], [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None], [None, None], [413930.849506, None],
    #                               [None, None], [None, None]],
    #                              [1, None])


    return time() - starting

def query4_GBT(csv_header, gr, cen,ncl, Ps):
    starting =time()
    gbt = GBT("name", csv_header, gr, cen, False, None,
                                 [[None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None],
                                  [None, None], [None, None], [None, None], [None, None], [None, None],
                                  [None, 453998.242103], [3, None]],
                                 [1, None])

    p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
    # q3 = direct.direct_algorithm("name", False, None,
    #                              [[None, None], [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None],
    #                               [None, None], [None, None], [None, None], [None, None], [None, None],
    #                               [None, 453998.242103], [3, None]],
    #                              [1, None])

    return time() - starting

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

percentages = [10, 20, 30, 40, 50]
time_array = {}
time_array["q1"] = []
time_array["q2"] = []
time_array["q2_chg"] = []
time_array["q3"] = []
time_array["q4"] = []
time_array["percentages"] = percentages
time_array["partitioning"] = []
for p in percentages:
    print("**** Running p: ", p)
    start_time = time()
    kd_tree = KD_tree(0.1)
    csv_header = None
    dataset = []
    with open("../{0}Percent.csv".format(p), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        h = True
        for row in csv_reader:
            if h:
                csv_header = row[1:]
                h = False
            else:
                # row variable is a list that represents a row in csv
                dataset.append(np.array(row[1:]).astype(np.float))
    gr, cen, ncl = kd_tree.Partitioning(dataset)
    time_array["partitioning"].append(time() - start_time)
    Ps = [0 for _ in range(len(dataset) + ncl)]
    for i in range(len(Ps)):
        if i < len(dataset):
            if np.random.random() < 0.6:
                Ps[i] = 1
            else:
                Ps[i] = 0
        else:
            # Ps[i] = group_sketches_sizes[i - len(dataset)]
            Ps[i] = len(gr[i - len(dataset)])

    # q1 = query1_GBT(csv_header,gr,cen,ncl,Ps)
    q2 = query2_GBT(csv_header,gr,cen,ncl,Ps.copy())
    q2_ch = query2_changed(csv_header, gr, cen, ncl, Ps.copy())
    # q3 = query3_GBT(csv_header,gr,cen,ncl,Ps)
    # q4 = query4_GBT(csv_header,gr,cen,ncl,Ps)
    # time_array["q1"].append(q1)
    time_array["q2"].append(q2)
    time_array["q2_chg"].append(q2_ch)
    # time_array["q3"].append(q3)
    # time_array["q4"].append(q4)
    # with open("direct_output_GBT.json", 'w') as writer:
    with open("q2_output_GBT.json", 'w') as writer:
        json.dump(time_array, writer)




# all_groups = [
#     [[1,2], [0,2], [1,0]],
#     [[3,2], [3,2], [3,1], [3,0]],
#     [[1, 3], [ 0, 4]],
#     [[4, 4], [3,4], [4,3]]
# ]
# centroids = [[1,1], [3,1], [1,3], [3,3]]





# direct = Direct()
#
#
# print("Starting")
# inital_time = time()
# kd_tree = KD_tree(0.1)
# csv_header = None
# dataset = []
# with open("../10Percent.csv", 'r') as read_obj:
# 	# pass the file object to reader() to get the reader object
# 	csv_reader = reader(read_obj)
# 	h = True
# 	for row in csv_reader:
# 		if h:
# 			csv_header = row[1:]
# 			h = False
# 		else:
# 			# row variable is a list that represents a row in csv
# 			dataset.append(np.array(row[1:]).astype(np.float))
# print("Data loaded ", time() -inital_time)
# # direct.set_data(dataset,"name", csv_header)
# # output, one_hot_output =direct.direct_algorithm("name", False, "ps_min_supplycost",
# #                                  [[None, None], [None, None], [None, None],
# #                                   [None, None], [None, None], [None, None],
# #                                   [None, None], [None, None], [None, 8], [None, None], [None, None],
# #                                   [None, None], [None, None]],
# #                                  [1, None])
# print("Direct output is ready , ", time() - inital_time)
# gr, cen, ncl = kd_tree.Partitioning(dataset)
# print("Partitioning finished, ", time() - inital_time)
# print("number of clusters ", ncl)
#
# gbt = GBT("name", csv_header, gr, cen, False, "p_size",
#                                  [ [None, None], [None, None], [None, None],
#                                   [100, None], [None, None], [None, None],
#                                   [None, None], [None, None], [None, None], [None, None], [None, None],
#                                   [None, None], [None, None]],
#                                  [1, None])
#
#
#
#
#
# partition_sizes = [len(g) for g in gr]
# # group_sketches_sizes = Sketch.sketch_numbers(csv_header, cen, partition_sizes, True, "p_size",
# #                                  [ [None, None], [None, None], [None, None],
# #                                   [100, None], [None, None], [None, None],
# #                                   [None, None], [None, None], [None, None], [None, None], [None, None],
# #                                   [None, None], [None, None]],
# #                                  [1, None])
# # print(group_sketches_sizes)
# # print("Sketch sizes: ", time() - inital_time)
#
#
# Ps = [0 for _ in range(len(dataset) + ncl)]
# for i in range(len(Ps)):
#     if i < len(dataset):
#         if np.random.random() < 0.6:
#             Ps[i] = 1
#         else:
#             Ps[i] = 0
#     else:
#         # Ps[i] = group_sketches_sizes[i - len(dataset)]
#         Ps[i] = len(gr[i - len(dataset)])
# print("Starting Refine: ", time() - inital_time)
# p, f = gbt.Refine(list(range(ncl)), list(range(ncl)), Ps)
#
# print(p)
# print(np.sum(p))
# print("GBT refine done, ", time() - inital_time)
