
from GBT import *
from time import time
from sci_kmeans import *
from sci_kdtree import *

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



partition_sizes = [0.01, 0.25, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
time_array = {}
time_array["q1"] = {}
time_array["q2"] = {}
time_array["q3"] = {}
time_array["q4"] = {}
time_array["q1"]["KD"] = []
time_array["q1"]["KM"] = []
time_array["q2"]["KD"] = []
time_array["q2"]["KM"] = []
time_array["q3"]["KD"] = []
time_array["q3"]["KM"] = []
time_array["q4"]["KD"] = []
time_array["q4"]["KM"] = []
time_array["p_sizes"] = partition_sizes
time_array["k_sizes"] = []
time_array["partitioning_KD"] = []
time_array["partitioning_KM"] = []
time_array["loading"] = []
for p in partition_sizes:
    print("**** Running p: ", p)
    start_time = time()


    csv_header = None
    dataset = []
    with open("../30Percent.csv".format(p), 'r') as read_obj:
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
    time_array["loading"].append(time() - start_time)
    start_time = time()
    kd_tree = KD_tree(p)
    gr, cen, ncl = kd_tree.Partitioning(dataset)
    time_array["partitioning_KD"].append(time() - start_time)



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

    q1 = query1_GBT(csv_header,gr,cen,ncl,Ps.copy())
    q2 = query2_GBT(csv_header,gr,cen,ncl,Ps.copy())
    q3 = query3_GBT(csv_header,gr,cen,ncl,Ps.copy())
    q4 = query4_GBT(csv_header,gr,cen,ncl,Ps.copy())
    time_array["q1"]["KD"].append(q1)
    time_array["q2"]["KD"].append(q2)
    time_array["q3"]["KD"].append(q3)
    time_array["q4"]["KD"].append(q4)

    start_time = time()
    k_means = K_means(ncl)
    gr, cen, ncl = k_means.Partitioning(dataset)
    time_array["partitioning_KM"].append(time() - start_time)
    time_array["k_sizes"].append(ncl)

    q1 = query1_GBT(csv_header, gr, cen, ncl, Ps.copy())
    q2 = query2_GBT(csv_header, gr, cen, ncl, Ps.copy())
    q3 = query3_GBT(csv_header, gr, cen, ncl, Ps.copy())
    q4 = query4_GBT(csv_header, gr, cen, ncl, Ps.copy())
    time_array["q1"]["KM"].append(q1)
    time_array["q2"]["KM"].append(q2)
    time_array["q3"]["KM"].append(q3)
    time_array["q4"]["KM"].append(q4)

    with open("PartitionSize_output.json", 'w') as writer:
        json.dump(time_array, writer)




