import matplotlib.pyplot as plt
import numpy as np
import json
import mpltex

with open('direct_output.json') as reader:
    direct_output = json.load(reader)
with open('direct_output_GBT.json') as reader:
    GBT_output = json.load(reader)

with open('Skrefine_kmeans.json') as reader:
    skrefine_output = json.load(reader)

with open('PartitionSize_output.json') as reader:
    partition_size = json.load(reader)

# print(data)
# x = [10, 20, 30, 40, 50, 60]
# q1 = []
# q2 = [56.2, 116.2, 184.3, 244.4, 315.2, 381.9]
# q3 = [75.4, 282.1, 718.6, 1518.4, 2785, 4434.2]
# q4 = [150.5, 722.5, 1780.9, 3739.6, 6305.7, 9828.9]

#
# # plt.plot(x, q1, label="Q1")
# plt.plot(x, q2, label="Q2")
# plt.plot(x, q3, label="Q3")
# plt.plot(x, q4, label="Q4")
# plt.yscale('log')
# plt.xlabel("Dataset size (in percentage)")
# plt.ylabel("Time(s)")
# plt.title("Direct algorithm")
# plt.xticks(x)
# plt.legend()
# plt.savefig("direct_log.png", dpi=600)

m_size = 5
line_w = 1.5
queries = ["q1", "q2", "q3", "q4"]
x = direct_output["percentages"]
partitioning = GBT_output["partitioning"]
i = 0
for q in queries:
    linestyles = mpltex.linestyle_generator()
    plt.figure(i)
    i += 1
    dirc = direct_output[q]
    gbt = GBT_output[q]
    plt.rcParams.update({'font.size': 16})
    plt.plot(x[:len(dirc)], dirc, label="Direct", **next(linestyles), markersize=m_size, linewidth=line_w)
    plt.plot(x[:len(gbt)], np.array(gbt) + partitioning, label="SketchRefine", **next(linestyles), markersize=m_size,
             linewidth=line_w)

    plt.yscale('log')
    plt.xlabel("% of Dataset size")
    plt.ylabel("Time (s)")
    plt.xticks(x)
    plt.title(q.upper())
    plt.rcParams.update({'font.size': 13})
    plt.legend()
    plt.savefig("pics/{0}_vs_time.png".format(q), dpi=600, bbox_inches='tight')

plt.figure(i)
linestyles = mpltex.linestyle_generator()
plt.plot(x[:len(partitioning)], partitioning, **next(linestyles), markersize=m_size, linewidth=line_w)
plt.xlabel("% of Dataset size")
plt.ylabel("Time (s)")
plt.title("KD-Tree Partitioning")
plt.xticks(x)
plt.savefig("pics/partitioning_time_KDTree.png", dpi=600, bbox_inches='tight')



i+= 1
partitioning = skrefine_output["partitioning"]
partitioning_kd = GBT_output["partitioning"]
for q in queries:
    linestyles = mpltex.linestyle_generator()
    plt.figure(i)
    i += 1
    dirc = direct_output[q]
    gbt = skrefine_output[q]
    gbt_kd = GBT_output[q]
    plt.rcParams.update({'font.size': 16})
    plt.plot(x[:len(gbt_kd)], np.array(gbt_kd) + partitioning_kd, label="KD-Tree", **next(linestyles), markersize=m_size, linewidth=line_w)
    plt.plot(x[:len(gbt)], np.array(gbt) + partitioning, label="K-Means", **next(linestyles), markersize=m_size,
             linewidth=line_w)

    plt.yscale('log')
    plt.xlabel("% of Dataset size")
    plt.ylabel("Time (s)")
    plt.xticks(x)
    plt.title(q.upper())
    plt.rcParams.update({'font.size': 13})
    plt.legend()
    plt.savefig("pics/{0}_vs_time_KM.png".format(q), dpi=600, bbox_inches='tight')

plt.figure(i)
linestyles = mpltex.linestyle_generator()
plt.plot(x[:len(partitioning)], partitioning, **next(linestyles), markersize=m_size, linewidth=line_w)
plt.xlabel("Numbef of clusters")
plt.ylabel("Time (s)")
plt.title("K-Means Partitioning")
plt.xticks(x[:len(partitioning)])
plt.savefig("pics/partitioning_time_KMeans.png", dpi=600, bbox_inches='tight')


i += 1
partitioning_KD = partition_size["partitioning_KD"]
partitioning_Km = partition_size["partitioning_KM"]
loading_time = partition_size["loading"]
p_sizes = partition_size["p_sizes"]
k_sizes = partition_size["k_sizes"]
for q in queries:
    linestyles = mpltex.linestyle_generator()
    plt.figure(i)
    i += 1
    p_kd = np.array(partition_size[q]["KD"]) + np.array(loading_time) + np.array(partitioning_KD)
    plt.rcParams.update({'font.size': 16})
    plt.plot(p_sizes[:len(p_kd)],[direct_output[q][3] for _ in range(len(p_kd))],**next(linestyles), label="Direct", markersize=m_size, linewidth=line_w)
    plt.plot(p_sizes[:len(p_kd)], p_kd,label="SketchRefine-KD",**next(linestyles), markersize=m_size, linewidth=line_w)

    plt.yscale('log')
    plt.xlabel("Partition size threshold")
    plt.ylabel("Time (s)")
    # plt.xticks(p_sizes[:len(direct_output[q])])
    plt.title("{0} using KD-Tree".format(q.upper()))
    plt.rcParams.update({'font.size': 13})
    plt.legend()
    plt.savefig("pics/{0}_partition_size_KD.png".format(q), dpi=600, bbox_inches='tight')

    linestyles = mpltex.linestyle_generator()
    plt.figure(i)
    i += 1
    p_km = partition_size[q]["KM"] + np.array(loading_time) + np.array(partitioning_KD)
    plt.rcParams.update({'font.size': 16})
    plt.plot(k_sizes[:len(p_km)][1:], [direct_output[q][3] for _ in range(len(k_sizes[:len(p_km)][1:]))],**next(linestyles), label="Direct", markersize=m_size, linewidth=line_w)
    plt.plot(k_sizes[:len(p_km)][1:], p_km[1:], label="SketchRefine-KMeans",**next(linestyles), markersize=m_size, linewidth=line_w)

    plt.yscale('log')
    plt.xlabel("Number of of clusters")
    plt.ylabel("Time (s)")
    # plt.xticks(k_sizes)
    plt.title("{0} using K-Means".format(q.upper()))
    plt.rcParams.update({'font.size': 13})
    plt.legend()
    plt.savefig("pics/{0}_partition_size_KM.png".format(q), dpi=600, bbox_inches='tight')

