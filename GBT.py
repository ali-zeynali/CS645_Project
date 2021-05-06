from Direct import *
import numpy as np




######################################################
#####                                               ##
#####                                               ##
#####           Greedy Backtracking Algorithm       ##
#####                                               ##
######################################################


class GBT:
    def __init__(self,table_name, att_names, all_groups, centroids, isMax, A0, boundaries_list, objective_bound):

        self.all_groups = all_groups
        self.centroids = centroids
        self.att_names = att_names
        self.isMax = isMax
        self.A0 = A0
        self.boundaries_list = boundaries_list
        self.objective_bound = objective_bound
        self.table_name = table_name
        self.direct = Direct()
        self.groups_sizes_aggregated = [0 for _ in range(len(centroids))]

        for i in range(1,len(self.groups_sizes_aggregated)):
            self.groups_sizes_aggregated[i] = self.groups_sizes_aggregated[i-1] + len(all_groups[i-1])
        self.n = self.groups_sizes_aggregated[-1] + len(all_groups[-1])

    def get_group_index(self, i):
        for j in range(len(self.centroids)):
            if i < self.groups_sizes_aggregated[j] + len(self.all_groups[j]):
                return j

    def get_data_from_Ps(self, Ps):
        input_data = []
        for i in range(len(Ps)):
            if Ps[i] == 1:
                if i < self.n:
                    g_index = self.get_group_index(i)
                    input_data.append(self.all_groups[g_index][i - self.groups_sizes_aggregated[g_index]])
                else:
                    g_index = i - self.n
                    input_data.append(self.centroids[g_index])
        return input_data

    def Refine(self, P, S, Ps):
        """

        :param Q:
        :param P:
        :param S: set of group indexes (not includes ti)
        :param Ps: Array of size n + | G |, one hot array!
        :return:
        """

        F = []
        if len(S) == 0:
            return Ps, F
        queue = S.copy()
        while len(queue) > 0:
            Gi = queue.pop()
            if Ps[Gi + self.n] == 0:
                continue
            input_data = self.get_data_from_Ps(Ps)
            self.direct.set_data(input_data, self.table_name, self.att_names)
            output, one_hot_output = self.direct.direct_algorithm(self.table_name, self.isMax, self.A0, self.boundaries_list, self.objective_bound)
            feasible = True if np.sum(one_hot_output[self.groups_sizes_aggregated[Gi] : len(self.all_groups[Gi]) + self.groups_sizes_aggregated[Gi]]) > 0 else False
            if feasible:
                Ps_prime = Ps.copy()
                Ps_prime[Gi + self.n] = 0
                for j  in range(self.groups_sizes_aggregated[Gi], len(self.all_groups[Gi]) + self.groups_sizes_aggregated[Gi]):
                    Ps_prime[j] = one_hot_output[j]

                S_prime = S.copy()
                if Gi in S_prime:
                    S_prime.remove(Gi)
                p, F_prime = self.Refine( P,S_prime , Ps_prime)
                if len(F_prime) > 0:
                    F = np.union1d(F, F_prime)
                    for f_item in F:
                        if f_item in queue:
                            queue.remove(f_item)
                            queue.append(f_item)
                else:
                    return p, F
            else:
                if sorted(S) != sorted(P):
                    F = np.union1d(F, Gi)
                    return [0 for _ in range(self.n + len(self.centroids))], F
        return [0 for _ in range(self.n + len(self.centroids))], F


