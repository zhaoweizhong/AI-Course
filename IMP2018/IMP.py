import numpy as np
import os
import heapq
import sys
import multiprocessing


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


def happen_with_prop(rate):
    rand = np.random.ranf()
    if rand <= rate:
        return True
    else:
        return False


def print_seeds(seeds):
    for seed in seeds:
        print(seed)


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


class CELFQueue:
    nodes = None
    q = None
    nodes_gain = None

    def __init__(self):
        self.q = []
        self.nodes_gain = {}

    def put(self, node, marginalgain):
        self.nodes_gain[node] = marginalgain
        heapq.heappush(self.q, (-marginalgain, node))

    def update(self, node, marginalgain):
        self.remove(node)
        self.put(node, marginalgain)

    def remove(self, node):
        self.q.remove((-self.nodes_gain[node], node))
        self.nodes_gain[node] = None
        heapq.heapify(self.q)

    def topn(self, n):
        top = heapq.nsmallest(n, self.q)
        top_ = list()
        for t in top:
            top_.append(t[1])
        return top_

    def get_gain(self, node):
        return self.nodes_gain[node]


def get_sample_graph(graph):
    nodes = graph.nodes
    edges = {}
    children = {}
    parents = {}
    node_num = graph.node_num

    for edge in graph.edges:
        if happen_with_prop(graph.edges[edge]):
            edges[edge] = graph.edges[edge]
            src = edge[0]
            des = edge[1]

            if children.get(src) is None:
                children[src] = []
            if parents.get(des) is None:
                parents[des] = []

            children[src].append(des)
            parents[des].append(src)
    return Graph((nodes, edges, children, parents, node_num, len(edges)))


def BFS(graph, nodes, get_checked_array=False):
    node_list = list()
    node_list.extend(nodes)
    result_list = list()
    checked = np.zeros(graph.node_num)
    for node in node_list:
        checked[node - 1] = 1
    while len(node_list) != 0:
        current_node = node_list.pop(0)
        result_list.append(current_node)
        children = graph.get_child(current_node)
        for child in children:
            if checked[child - 1] == 0:
                checked[child - 1] = 1
                node_list.append(child)
    if get_checked_array:
        return result_list, checked
    return result_list


def isc_IC(graph, seeds, sample_num=10000):
    influence = 0
    for i in range(sample_num):
        node_list = list()
        node_list.extend(seeds)
        checked = np.zeros(graph.node_num)
        for node in node_list:
            checked[node - 1] = 1
        while len(node_list) != 0:
            current_node = node_list.pop(0)
            influence = influence + 1
            children = graph.get_child(current_node)
            for child in children:
                if checked[child - 1] == 0:
                    if happen_with_prop(graph.get_weight(current_node, child)):
                        checked[child - 1] = 1
                        node_list.append(child)
    return influence


def isc_IC_m(graph, seeds, n=4):
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


def greedy_IC(graph, k, R=10000):
    seeds = set()
    for i in range(k):
        sv = np.zeros(graph.node_num)
        afficted_nodes, is_afficted = BFS(graph, list(seeds), True)
        for i in range(R):
            sample_graph = get_sample_graph(graph)
            for v in range(graph.node_num):
                if is_afficted[v] == 0:
                    sv[v] = sv[v] + len(BFS(sample_graph, [v + 1]))
        for i in range(graph.node_num):
            sv[i] = sv[i] / R
        seeds.add(sv.argmax() + 1)
    return list(seeds)


def sample_IC(graph, is_afficted, seed, R):
    sv = np.zeros(graph.node_num)
    for i in range(R):
        sample_graph = get_sample_graph(graph)
        for v in range(graph.node_num):
            if is_afficted[v] == 0:
                sv[v] = sv[v] + len(BFS(sample_graph, [v + 1]))
    return sv


def greedy_IC_m(graph, k, R=10000, n=8):
    sub = int(R / n)
    seeds = set()
    for i in range(k):
        sv = np.zeros(graph.node_num)
        afficted_nodes, is_afficted = BFS(graph, list(seeds), True)
        pool = multiprocessing.Pool(processes=8)
        results = []
        for i in range(n):
            result = pool.apply_async(sample_IC, args=(graph, is_afficted, seeds, sub))
            results.append(result)
        pool.close()
        pool.join()
        for result in results:
            for i in range(len(sv)):
                sv[i] = sv[i] + result.get()[i]
        for i in range(len(sv)):
            sv[i] = sv[i] / R
        seeds.add(sv.argmax() + 1)
    return list(seeds)


def degree_discount_ic(k, graph):
    seeds = []
    ddv = np.zeros(graph.node_num)
    tv = np.zeros(graph.node_num)
    for i in range(graph.node_num):
        ddv[i] = graph.get_out_degree(i + 1)
    for i in range(k):
        u = ddv.argmax() + 1
        ddv[u - 1] = -1
        seeds.append(u)
        children = graph.get_child(u)
        for child in children:
            if child not in seeds:
                tv[child - 1] = tv[child - 1] + 1
                ddv[child - 1] = ddv[child - 1] - 2 * tv[child - 1] - (graph.get_out_degree(child) - tv[
                    child - 1]) * tv[child - 1] * graph.get_weight(u, child)
    return seeds


def degree_discount(k, graph):
    seeds = []
    ddv = np.zeros(graph.node_num)

    for i in range(graph.node_num):
        ddv[i] = graph.get_out_degree(i + 1)
    for i in range(k):
        u = ddv.argmax() + 1
        ddv[u - 1] = -1
        seeds.append(u)
        children = graph.get_child(u)
        for child in children:
            if child not in seeds:
                ddv[child - 1] = ddv[child - 1] - 1
    return seeds


def init_D(graph):
    D = list()
    for i in range(graph.node_num + 1):
        D.append([])
    return D


def get_vertex_cover(graph):
    dv = np.zeros(graph.node_num)
    check_array = np.zeros((graph.node_num, graph.node_num))
    checked = 0

    for i in range(graph.node_num):
        dv[i] = graph.get_out_degree(i + 1) + graph.get_in_degree(i + 1)
    V = set()
    while checked < graph.edge_num:
        s = dv.argmax() + 1
        V.add(s)
        children = graph.get_child(s)
        parents = graph.get_parents(s)
        for child in children:
            if check_array[s - 1][child - 1] == 0:
                check_array[s - 1][child - 1] = 1
                checked = checked + 1
        for parent in parents:
            if check_array[parent - 1][s - 1] == 0:
                check_array[parent - 1][s - 1] = 1
                checked = checked + 1
        dv[s - 1] = -1
    return list(V)


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


def simpath(graph, k, r, l):
    C = set(get_vertex_cover(graph))
    V = set(graph.nodes)

    V_C = V.difference(C)
    spread = np.zeros(graph.node_num + 1)
    spdV_ = np.ones((graph.node_num + 1, graph.node_num + 1))
    for u in C:
        U = V_C.intersection(set(graph.get_parents(u)))
        spread[u] = simpath_spread(set([u]), r, U, graph, spdV_)
    for v in V_C:
        v_children = graph.get_child(v)
        for child in v_children:
            spread[v] = spread[v] + spdV_[child][v] * graph.get_weight(v, child)
        spread[v] = spread[v] + 1
    celf = CELFQueue()
    for node in range(1, graph.node_num + 1):
        celf.put(node, spread[node])
    S = set()
    W = V
    spd = 0
    checked = np.zeros(graph.node_num + 1)

    while len(S) < k:
        U = celf.topn(l)
        spdW_ = np.ones((graph.node_num + 1, graph.node_num + 1))
        spdV_x = np.zeros(graph.node_num + 1)
        simpath_spread(S, r, U, graph, spdW_=spdW_)
        for x in U:
            for s in S:
                spdV_x[x] = spdV_x[x] + spdW_[s][x]
        for x in U:
            if checked[x] != 0:
                S.add(x)
                W = W.difference(set([x]))
                spd = spread[x]
                checked = np.zeros(graph.node_num + 1)
                celf.remove(x)
                break
            else:
                spread[x] = trackback(x, r, W, None, None, graph) + spdV_x[x]
                checked[x] = 1
                celf.update(x, spread[x] - spd)
    return S


def main(args, q):
    graph_path = args.graph_path
    seed_size = args.seed_size
    model = args.model
    random_seed = args.random_seed
    np.random.seed(random_seed)
    graph = Graph(read_graph(graph_path))

    if model == 'IC':
        seeds = degree_discount_ic(k=seed_size, graph=graph)
        q.put(seeds)
        seeds = greedy_IC(graph, k=seed_size, R=10000)
        q.put(seeds)

    elif model == 'LT':
        seeds = degree_discount(seed_size, graph)
        q.put(seeds)
        seeds = simpath(graph, seed_size, 0.001, 7)
        q.put(seeds)
    else:
        raise ValueError('Model type err')


if __name__ == '__main__':
    graph_path = str(sys.argv[2])
    seed_size = int(sys.argv[4])
    model = str(sys.argv[6])
    timeout = int(sys.argv[8])

    graph = Graph(read_graph(graph_path))
    if model == 'IC':
        if graph.node_num <= 300:
            seeds = greedy_IC_m(graph, k=seed_size, R=10000)
            print_seeds(seeds)
        else:
            seeds = degree_discount_ic(k=seed_size, graph=graph)
            print_seeds(seeds)
    elif model == 'LT':
        seeds = simpath(graph, seed_size, 0.001, 7)
        print_seeds(seeds)