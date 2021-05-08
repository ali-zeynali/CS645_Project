
from GBT import *
from time import time

from sci_kdtree import *

def query1(percent):
    initial_time = time()
    direct = Direct()
    direct.load_data("../{0}Percent.csv".format(percent), "name")
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


    return time() - starting


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

            Ps[i] = len(gr[i - len(dataset)])

    q1 = query1_GBT(csv_header,gr,cen,ncl,Ps)
    q2 = query2_GBT(csv_header,gr,cen,ncl,Ps.copy())

    q3 = query3_GBT(csv_header,gr,cen,ncl,Ps)
    q4 = query4_GBT(csv_header,gr,cen,ncl,Ps)
    time_array["q1"].append(q1)
    time_array["q2"].append(q2)
    time_array["q3"].append(q3)
    time_array["q4"].append(q4)
    with open("direct_output_GBT.json", 'w') as writer:
        json.dump(time_array, writer)


