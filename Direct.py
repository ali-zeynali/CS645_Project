from pulp import *
from csv import reader
from time import *
import multiprocessing
from datetime import datetime

class Direct:

    def __init__(self):
        self.datasets = {}
        self.headers = {}

    def time_process(self):
        # To manage the termination of the ILP if it takes too much time
        while True:
            sleep(30 * 60)
            print("Process terminated because it took more than enough")


    def load_data(self, path, name):
        # load data from the file
        csv_header = None
        dataset = []
        with open(path, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            h = True
            for row in csv_reader:
                if h:
                    csv_header = row
                    h = False
                else:
                    # row variable is a list that represents a row in csv
                    dataset.append(row)
        self.datasets[name] = dataset
        self.headers[name] = csv_header

    def set_data(self, dataset, name):
        # set data from the input of the function
        self.datasets[name] = dataset

    def get_att_index(self, table_name, att_name):
        # find attribute index by its name
        header = self.headers[table_name]
        for i in range(len(header)):
            if header[i] == att_name:
                return i
        return None

    def direct_algorithm(self, name, isMax, A0, boundaries_list, objective_bound):
        # Implementation of Direct

        if name not in self.datasets:
            print("Table name is not available")
            return
        a0_index = self.get_att_index(name, A0)
        if A0 is not None and a0_index == None:
            print("Attribute name {0} is not available".format(A0))
            return
        data = self.datasets[name]
        if isMax:
            # print("max problem")
            prob = LpProblem("Direct Maximization", LpMaximize)
        else:
            # print("min problem")
            prob = LpProblem("Direct Minimization", LpMinimize)

        prob_vars = []
        for i in range(len(data)):
            # prob_vars.append(LpVariable(("x_{0}".format(i), 0, 1, LpInteger)))
            prob_vars.append(LpVariable(name="x_{0}".format(i), lowBound=0, upBound=1, cat='Integer'))

        for d in range(len(data[0])):
            L = boundaries_list[d][0]
            U = boundaries_list[d][1]
            if L is not None:
                # print(d, " ) low applied" )
                prob += lpSum([float(data[j][d]) * prob_vars[j] for j in range(len(data))]) >= L, "C_L_{0}".format(d)
            if U is not None:
                # print(d, " ) up applied")
                prob += lpSum([float(data[j][d]) * prob_vars[j] for j in range(len(data))]) <= U, "C_U_{0}".format(d)

        if objective_bound[0] is not None:
            # print("low constraint applied")
            prob += lpSum([prob_vars[j] for j in range(len(data))]) >= objective_bound[0], "total_sum_min"
        if objective_bound[1] is not None:
            # print("up constraint applied")
            prob += lpSum([prob_vars[j] for j in range(len(data))]) <= objective_bound[1], "total_sum_max"

        if A0 is not None:
            prob += lpSum([prob_vars[j] * float(data[j][a0_index]) for j in range(len(data))])
        else:
            prob += lpSum([prob_vars[j] for j in range(len(data))])


        # process = multiprocessing.Process(target=self.time_process)
        prob.solve()
        # process.terminate()
        output = []
        one_hot_output = []
        for val in prob.variables():
            if val.varValue != None:
                ind = int(val.name[2:])
                if val.varValue > 0:
                    output.append(data[ind])
                    one_hot_output.append(1)
                one_hot_output.append(0)
                # print(val.name, "=", val.varValue)
                # for n in range(int(val.varValue)):
                #     output.append(data[ind])

        return output, one_hot_output

    def get_dataset(self):
        return self.datasets