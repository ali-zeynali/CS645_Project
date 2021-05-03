
import numpy as np




######################################################
#####                                               ##
#####                                               ##
#####           Greedy Backtracking Algorithm       ##
#####                                               ##
######################################################


class GBT:
    def __init__(self, all_groups, centroids):
        #TODO complete this
        self.all_groups = all_groups
        self.centroids = centroids

    def Refine(self, Q, P, S, Ps):
        """

        :param Q:
        :param P:
        :param S: set of group indexes (not includes ti)
        :param Ps:
        :return:
        """

        F = []
        if len(S) == 0:
            return Ps, F
        queue = S
        while len(queue) > 0:
            Gi = queue.pop()
            ti = self.centroids[Gi]
            if ti not in Ps:
                continue
            pi = None #TODO
            feasibility = True # TODO
            if feasibility:
                Ps_prime = #TODO
                if Gi in S:
                    S.remove(Gi)
                p, F_prime = self.Refine(Q, P, Ps_prime)
                if len(F_prime) > 0:
                    F = np.union1d(F, F_prime)
                    for f_item in F:
                        if f_item in queue:
                            queue.remove(f_item)
                            queue.append(f_item)
                else:
                    return p, F
            else:
                if S != P: #TODO complete this line to works
                    F = np.union1d(F, Gi)
                    return None, F
        return None, F


