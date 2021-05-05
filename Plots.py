import matplotlib.pyplot as plt

x = [10, 20, 30, 40, 50, 60]
q1 = []
q2 = [56.2, 116.2, 184.3, 244.4, 315.2, 381.9]
q3 = [75.4, 282.1, 718.6, 1518.4, 2785, 4434.2]
q4 = [150.5, 722.5, 1780.9, 3739.6, 6305.7, 9828.9]


# plt.plot(x, q1, label="Q1")
plt.plot(x, q2, label="Q2")
plt.plot(x, q3, label="Q3")
plt.plot(x, q4, label="Q4")
plt.yscale('log')
plt.xlabel("Dataset size (in percentage)")
plt.ylabel("Time(s)")
plt.title("Direct algorithm")
plt.xticks(x)
plt.legend()
plt.savefig("direct_log.png", dpi=600)
