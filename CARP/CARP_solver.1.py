import time
import sys
import numpy as np


def read_instance_file(file_path):
    openfile = open(file_path, 'r')
    content = openfile.readlines()
    content = [x.strip() for x in content]
    specification = dict()
    for i in range(8):
        line = content[i].split(':')
        specification[line[0].strip()] = line[1].strip()
    data = list()
    for line in content[9:-1]:
        tmp = line.split()
        data.append([int(x.strip()) for x in tmp])
    data = np.array(data)
    openfile.close()
    return specification, data


def isNodesValid(begin_node, to_node):
    for line in lines:
        if ([begin_node, to_node] == line or [to_node, begin_node] == line).all():
            return True
        else:
            return False


def isRoutesValid(nodes):
    for i, node in enumerate(nodes):
        if i == 0:
            if isNodesValid(1, node) is False:
                return False
        elif i == nodes.size - 1:
            if isNodesValid(node, 1) is False:
                return False
        elif isNodesValid(node, nodes[i+1]) is False:
            return False
    return True


class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size

        self.pop = np.vstack([np.random.permutation(DNA_size)
                              for _ in range(pop_size)])

    def get_fitness(self, nodes):
        total_cost = 0
        for i, node in enumerate(nodes):
            if i == 0:
                total_cost += getCost([1, node])
            elif i == len(nodes) - 1:
                total_cost += getCost([node, 1])
            else:
                total_cost += getCost([node, nodes[i+1]])
        fitness = np.exp(self.DNA_size * 2 / total_cost)
        return fitness, total_cost

    def select(self, fitness):
        idx = np.random.choice(np.arange(
            self.pop_size), size=self.pop_size, replace=True)
        return self.pop[idx]

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(
                np.bool)
            keep = parent[~cross_points]
            swap = pop[i_, np.isin(
                pop[i_].ravel(), keep, invert=True)]
            parent[:] = np.concatenate((keep, swap))
        return parent

    def mutate(self, child):
        for times in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                for i in range(0, 10):
                    mutate_point = np.random.randint(0, self.DNA_size)
                    flag2 = False
                    newnode = 0
                    for node in routes[child[mutate_point-1]]:
                        if mutate_point != self.DNA_size - 1:
                            for node2 in routes[node]:
                                if node2 == child[mutate_point+1]:
                                    flag2 = True
                                    break
                            if flag2 is True:
                                newnode = node
                                break
                        else:
                            flag2 = True
                            newnode = routes[child[mutate_point-1]][np.random.randint(
                                0, len(routes[child[mutate_point-1]]))]
                            break
                    if flag2 is True:
                        child[mutate_point] = newnode
                        break
        return child

    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop


class CARP(object):
    def __init__(self, n_nodes):
        nodes = []
        lastnode = 1
        for i in range(0, n_nodes):
            newnode = routes[lastnode][np.random.randint(
                0, len(routes[lastnode]))]
            nodes.append(newnode)
            lastnode = newnode
        self.nodes = nodes


if __name__ == '__main__':
    '''
    Main
    '''
    start_time = time.time()

    time_limit = 60
    file_path = 'CARP_samples/gdb10.dat'
    seed = 1

    if len(sys.argv) == 6:
        file_path = sys.argv[1]
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])

    spec, data = read_instance_file(file_path)  # 读取文件
    lines = data[:, 0:2]

    N_NODES = (int)(spec.get("VERTICES")) - 1  # DNA size
    CROSS_RATE = 0.1
    MUTATE_RATE = 0.02
    POP_SIZE = 500
    N_GENERATIONS = 500

    def getCost(component):
        for i, line in enumerate(lines):
            if (component == line).all():
                if data[i, 2]:
                    return data[i, 2]
        tmp = component[0]
        component[0] = component[1]
        component[1] = tmp
        for i, line in enumerate(lines):
            if (component == line).all():
                return data[i, 2]

    ga = GA(DNA_size=N_NODES, cross_rate=CROSS_RATE,
            mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)

    routes = []
    for i in range(0, N_NODES + 2):
        routes.append([])
    for line in lines:
        routes[int(line[0])].append(int(line[1]))

    for line in lines:
        flag = False
        for node in routes[int(line[1])]:
            if node == line[0]:
                flag = True
        if flag is False:
            routes[int(line[1])].append(line[0])

    env = CARP(N_NODES)
    for generation in range(N_GENERATIONS):
        nodes = env.nodes
        fitness, total_cost = ga.get_fitness(nodes)
        ga.evolve(fitness)
        best_idx = np.argmax(fitness)
        print('Gen:', generation, '| best fit: %.2f' % fitness,)
