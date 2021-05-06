from Direct import *
from csv import reader


class Sketch:
    def __init__(self, partitioner):
        self.direct = Direct()
        self.partitioner = partitioner

    def load_dataset(self, path):
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
        return dataset, csv_header

    @staticmethod
    def sketch_numbers(headers, centroids, partition_sizes, isMax, A0, boundaries_list, objective_bound):
        # find number of representative items for each group, solving ILP
        partition_sizes_aggregated = [0 for i in range(len(partition_sizes))]
        partition_sizes_aggregated[0] = partition_sizes[0]
        for i in range(1, len(partition_sizes)):
            partition_sizes_aggregated[i] = partition_sizes_aggregated[i - 1] + partition_sizes[i]
        a0_index = None
        for i in range(len(headers)):
            if headers[i] == A0:
                a0_index = i
        if a0_index == None:
            print("Attribute name {0} is not available".format(A0))
            return

        data = []
        for i in range(len(centroids)):
            for _ in range(partition_sizes[i]):
                data.append(centroids[i])
        if isMax:
            # print("max problem")
            prob = LpProblem("Direct Maximization", LpMaximize)
        else:
            # print("min problem")
            prob = LpProblem("Direct Minimization", LpMinimize)

        prob_vars = []
        for i in range(len(data)):
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

        for g_index in range(len(centroids)):
            prob += lpSum([prob_vars[j] for j in range(partition_sizes_aggregated[g_index] - partition_sizes[g_index],
                                                       partition_sizes_aggregated[g_index])]) <= partition_sizes[
                        g_index], "group_size_{0}".format(g_index)

        if a0_index is not None:
            prob += lpSum([prob_vars[j] * float(data[j][a0_index]) for j in range(len(data))])

        prob.solve()

        group_sketches_sizes = [0 for _ in range(len(centroids))]
        current_group = 0
        passed_group_data = 0
        for val in prob.variables():
            if val.varValue != None:
                ind = int(val.name[2:])
                if ind < passed_group_data + partition_sizes[current_group]:
                    if val.varValue > 0:
                        group_sketches_sizes[current_group] += 1
                elif ind == passed_group_data + partition_sizes[current_group]:
                    passed_group_data += partition_sizes[current_group]
                    current_group += 1
                    if val.varValue > 0:
                        group_sketches_sizes[current_group] += 1
                else:
                    print("error in group counting!")

        return group_sketches_sizes

    def sketch_data(self, data_path, table_name, isMax, A0, boundaries_list, objective_bound):
        # Sketching

        dataset, header = self.load_dataset(data_path)

        self.partitioner.fit(dataset)
        partitioned_data = self.partitioner.get_partitioned_data()
        centroids = self.partitioner.get_centroids()
        n_groups = self.partitioner.NGroups
        group_sizes = self.partitioner.get_group_sizes()

        sketch_initial_numbers = self.sketch_numbers(header, centroids, group_sizes, isMax, A0, boundaries_list,
                                                     objective_bound)

        previous_direct_results = [[] for _ in range(n_groups)]
        new_ordered_data = []
        new_one_hot_output = []
        for i in range(n_groups):
            direct_data = []

            # previous groups
            for j in range(i):
                for d in previous_direct_results[j]:
                    direct_data.append(d)
            first_index = len(direct_data)

            #current group
            for d in partitioned_data[i]:
                direct_data.append(d)
                new_ordered_data.append(d)
            last_index = len(direct_data)

            # future groups
            for j in range(i + 1, n_groups):
                for t in range(sketch_initial_numbers[j]):
                    direct_data.append(centroids[j])

            self.direct.set_data(direct_data, table_name, header)
            output, one_hot_output = self.direct.direct_algorithm(table_name, isMax, A0, boundaries_list,
                                                                  objective_bound)
            for j in range(first_index, last_index):
                if one_hot_output[j] > 0:
                    previous_direct_results[i].append(direct_data[j])
                    new_one_hot_output.append(1)
                else:
                    new_one_hot_output.append(0)

        return previous_direct_results, new_one_hot_output, new_ordered_data
