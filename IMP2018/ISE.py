import numpy as np
import os
import sys
import multiprocessing

spd = None


def read_seed(path):
    if os.path.exists(path):
        f = open(path, 'r')
        txt = f.readlines()
        seeds = list()
        for line in txt:
            seeds.append(int(line))
        return seeds


def read_graph(path):
    if os.path.exists(path):
        parents = {}
        children = {}
        edges = {}
        nodes = set()

        f = open(path, 'r')
        txt = f.readlines()
        header = str.split(txt[0])
        node_num = int(header[0])
        edge_num = int(header[1])
        for line in txt[1:]:
            row = str.split(line)

            src = int(row[0])
            des = int(row[1])
            nodes.add(src)
            nodes.add(des)

            if children.get(src) is None:
                children[src] = []
            if parents.get(des) is None:
                parents[des] = []

            weight = float(row[2])
            edges[(src, des)] = weight
            children[src].append(des)
            parents[des].append(src)
        return list(nodes), edges, children, parents, node_num, edge_num


def with_property(rate):
    rand = np.random.ranf()
    if rand <= rate:
        return True
    else:
        return False


class Graph:
    nodes = None
    edges = None
    children = None
    parents = None
    node_num = None
    edge_num = None

    def __init__(self, lists):
        self.nodes = lists[0]
        self.edges = lists[1]
        self.children = lists[2]
        self.parents = lists[3]
        self.node_num = lists[4]
        self.edge_num = lists[5]

    def get_child(self, node):
        ch = self.children.get(node)
        if ch is None:
            self.children[node] = []
        return self.children[node]

    def get_parents(self, node):
        pa = self.parents.get(node)
        if pa is None:
            self.parents[node] = []
        return self.parents[node]

    def get_weight(self, src, dest):
        weight = self.edges.get((src, dest))
        if weight is None:
            return 0
        else:
            return weight

    def is_parent_of(self, node1, node2):
        if self.get_weight(node1, node2) != 0:
            return True
        else:
            return False

    def is_child_of(self, node1, node2):
        return self.is_parent_of(node2, node1)

    def get_out_degree(self, node):
        return len(self.get_child(node))

    def get_in_degree(self, node):
        return len(self.get_parents(node))


def isc_IC(graph, seeds, sample_num=10000):
    influence = 0
    for i in range(sample_num):
        node_list = list()
        node_list.extend(seeds)
        checked = np.zeros(graph.node_num)
        for node in node_list:
            checked[node - 1] = 1
        while len(node_list) != 0:
            curr_node = node_list.pop(0)
            influence = influence + 1
            children = graph.get_child(curr_node)
            for child in children:
                if checked[child - 1] == 0:
                    if with_property(graph.get_weight(curr_node, child)):
                        checked[child - 1] = 1
                        node_list.append(child)
    return influence


def isc_IC_m(graph, seeds, n=8):
    pool = multiprocessing.Pool(processes=8)
    results = []
    sub = int(10000 / n)
    for i in range(n):
        result = pool.apply_async(isc_IC, args=(graph, seeds, sub))
        results.append(result)
    pool.close()
    pool.join()
    influence = 0
    for result in results:
        influence = influence + result.get()
    return influence / 10000


def forward(Q, D, spd, pp, r, W, U, spdW_u, graph):
    x = Q[-1]
    if U is None:
        U = []
    children = graph.get_child(x)
    count = 0
    while True:

        for child in range(count, len(children)):
            if (children[child] in W) and (children[child] not in Q) and (children[child] not in D[x]):
                y = children[child]
                break
            count = count + 1

        if count == len(children):
            return Q, D, spd, pp

        if pp * graph.get_weight(x, y) < r:
            D[x].append(y)
        else:
            Q.append(y)
            pp = pp * graph.get_weight(x, y)
            spd = spd + pp
            D[x].append(y)
            x = Q[-1]
            for v in U:
                if v not in Q:
                    spdW_u[v] = spdW_u[v] + pp
            children = graph.get_child(x)
            count = 0


def trackback(u, r, W, U, spdW_, graph):
    Q = [u]
    spd = 1
    pp = 1
    D = init_D(graph)

    while len(Q) != 0:
        Q, D, spd, pp = forward(Q, D, spd, pp, r, W, U, spdW_, graph)
        u = Q.pop()
        D[u] = []
        if len(Q) != 0:
            v = Q[-1]
            pp = pp / graph.get_weight(v, u)
    return spd


def simpath_spread(S, r, U, graph, spdW_=None):
    spread = 0
    W = set(graph.nodes).difference(S)
    if U is None or spdW_ is None:
        spdW_ = np.zeros(graph.node_num + 1)
    for u in S:
        W.add(u)
        spread = spread + trackback(u, r, W, U, spdW_[u], graph)
        W.remove(u)
    return spread


def isc_LT(graph, seeds, r=0.01):
    return simpath_spread(seeds, r, None, graph)


def init_D(graph):
    D = list()
    for i in range(graph.node_num + 1):
        D.append([])
    return D


if __name__ == '__main__':
    graph_path = str(sys.argv[2])
    seed_path = str(sys.argv[4])
    model = str(sys.argv[6])
    timeout = int(sys.argv[8])

    graph = Graph(read_graph(graph_path))
    seeds = read_seed(seed_path)
    if model == 'IC':
        print(isc_IC_m(seeds=seeds, graph=graph))
    elif model == 'LT':
        print(isc_LT(graph=graph, seeds=seeds, r=0.001))    