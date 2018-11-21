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


def newNode(lastnode, nodes):
    while True:
        newnode = routes[lastnode][np.random.randint(
            0, len(routes[lastnode]))]
        if nodes.count(newnode) <= 1:
            break
    return newnode


class CARP(object):

    def __init__(self, n_nodes):
        nodes = []
        lastnode = 1
        for i in range(0, n_nodes):
            if i % 2 != 0:
                while True:
                    newnode = newNode(lastnode, nodes)
                    if newnode != 1:
                        nodes.append(newnode)
                        lastnode = newnode
                        break
            else:
                if (i == int(n_nodes / 2)):
                    if 1 in routes[lastnode]:
                        newnode = 1
                        nodes.append(newnode)
                        lastnode = newnode
                    else:
                        newnode = newNode(lastnode, nodes)
                        nodes.append(newnode)
                        lastnode = newnode
                else:
                    newnode = newNode(lastnode, nodes)
                    nodes.append(newnode)
                    lastnode = newnode
        self.nodes = nodes


if __name__ == '__main__':
    '''
    Main
    '''
    start_time = time.time()

    time_limit = 60
    file_path = 'CARP_samples/val7A.dat'
    seed = 1

    if len(sys.argv) == 6:
        file_path = sys.argv[1]
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])

    spec, data = read_instance_file(file_path)  # 读取文件
    lines = data[:, 0:2]

    N_NODES = (int)(spec.get("VERTICES"))  # size
    CAPACITY = (int)(spec.get("CAPACITY"))

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

    def getDemand(component):
        for i, line in enumerate(lines):
            if (component == line).all():
                if data[i, 3]:
                    return data[i, 3]
        tmp = component[0]
        component[0] = component[1]
        component[1] = tmp
        for i, line in enumerate(lines):
            if (component == line).all():
                return data[i, 3]

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

    carp = CARP(N_NODES)

    def checkCapacity(carp):
        last_node_demand = 0
        total_demand = 0
        for node in carp.nodes:
            if last_node_demand != 0:
                if node == 1:
                    total_demand = 0
                    last_node_demand = node
                else:
                    total_demand = total_demand + \
                        getDemand([last_node_demand, node])
                    last_node_demand = node
                    if total_demand > CAPACITY:
                        carp = CARP(N_NODES)
                        checkCapacity(carp)
            else:
                last_node_demand = node

    # checkCapacity(carp)

    total_cost = 0
    last_node = 0
    for node in carp.nodes:
        if last_node != 0:
            total_cost = total_cost + getCost([last_node, node])
            last_node = node
        else:
            last_node = node

    run_time = (time.time() - start_time)
    print("s 0,(1,", end='')
    for i, node in enumerate(carp.nodes):
        if node == 1:
            print(str(node) + "),0,0,", end='')
        else:
            if i % 2 != 0:
                print("(" + str(node) + ",", end='')
            else:
                print(str(node) + "),", end='')
    print("1),0")
    # print("nodes: " + str(carp.nodes))
    print("q " + str(total_cost))
    exit(0)
