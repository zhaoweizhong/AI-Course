import os
import sys
import multiprocessing as mp
from multiprocessing import Pool
import time
import numpy as np
import random
import argparse

start_time = time.time()
print("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))

global_graph = None
global_seeds = None


class Worker(mp.Process):
    def __init__(self):
        super(Worker, self).__init__(target=self.start)
        self.inQ = mp.Queue()
        self.outQ = mp.Queue()

    def run(self):
        while True:
            model, graph, seeds = self.inQ.get()
            if model == 'IC':
                self.outQ.put(solve_IC(graph, seeds))
            elif model == 'LT':
                self.outQ.put(solve_LT(graph, seeds))


def create_worker(num):
    '''
    创建子进程备用
    :param num: 多线程数量
    '''
    for i in range(num):
        worker.append(Worker(mp.Queue(), mp.Queue(), np.random.randint(0, 10 ** 9)))
        worker[i].start()


def finish_worker():
    '''
    关闭所有子线程
    '''
    for w in worker:
        w.terminate()


class Graph:
    '''
    Graph Class
    '''
    nodes_num = None
    weight = None
    parents_map = None
    children_map = None

    def __init__(self, nodes_num, weight, parents_map, children_map):
        self.nodes_num = nodes_num
        self.weight = weight
        self.parents_map = parents_map
        self.children_map = children_map

    def get_weight(self, src_node, dst_node):
        return self.weight[src_node][dst_node]

    def get_children(self, node):
        return self.children_map[node]

    def get_parents(self, node):
        return self.parents_map[node]


def load_graph(file_name):
    '''
    Load Graph data
    '''
    graph_file = open(file_name, 'r')
    lines = graph_file.readlines()
    graph_file.close()
    nodes_num = int(str.split(lines[0])[0])
    weight = np.zeros((nodes_num + 1, nodes_num + 1), dtype=np.float)
    parents_map = [[] for i in range(nodes_num + 1)]
    children_map = [[] for i in range(nodes_num + 1)]

    for line in lines[1:]:
        data = str.split(line)
        src_node = int(data[0])
        dst_node = int(data[1])
        weight[src_node][dst_node] = float(data[2])
        parents_map[dst_node].append(src_node)
        children_map[src_node].append(dst_node)

    return Graph(nodes_num, weight, parents_map, children_map)


def load_seeds(file_name):
    '''
    Load Seeds data
    '''
    seeds_file = open(file_name, 'r')
    lines = seeds_file.readlines()
    seeds_file.close()
    seeds = []

    for line in lines:
        seeds.append(int(line))

    return seeds


def solve_IC(time_budget):
    model_start_time = time.time()

    graph = global_graph
    seeds = global_seeds

    result, count = 0, 0
    while time.time() - model_start_time < time_budget - 3:
        activity_set = seeds
        res_count = len(activity_set)
        activited = [False] * (graph.nodes_num + 1)
        for node in activity_set:
            activited[node] = True
        while len(activity_set) != 0:
            new_activity_set = []
            for seed in activity_set:
                children = graph.get_children(seed)
                for child in children:
                    if child not in activity_set and child not in new_activity_set and not activited[child]:
                        random.seed(int(os.getpid() + time.time() * 1e5))
                        rand = random.random()
                        if rand <= graph.get_weight(seed, child):
                            new_activity_set.append(child)
                            activited[child] = True
            res_count += len(new_activity_set)
            activity_set = new_activity_set
        result += res_count
        count += 1
    return result, count


def solve_LT(time_budget):
    model_start_time = time.time()

    graph = global_graph
    seeds = global_seeds

    result, count = 0, 0
    while time.time() - model_start_time < time_budget - 3:
        activity_set = seeds
        threshold = np.zeros(graph.nodes_num + 1, dtype=np.float)
        activited = [False] * (graph.nodes_num + 1)
        for i in range(1, graph.nodes_num + 1):
            random.seed(int(os.getpid() + time.time() * 1e5))
            threshold[i] = random.random()
            if threshold[i] == 0.0:
                activity_set.append(i)
        res_count = len(activity_set)
        while activity_set:
            new_activity_set = []
            for seed in activity_set:
                activited[seed] = True
                children = graph.get_children(seed)
                for child in children:
                    threshold[child] -= graph.get_weight(seed, child)
            for seed in activity_set:
                children = graph.get_children(seed)
                for child in children:
                    if not activited[child]:
                        if threshold[child] < 0:
                            new_activity_set.append(child)
                            activited[child] = True
            res_count += len(new_activity_set)
            activity_set = new_activity_set
        result += res_count
        count += 1
    return result, count


if __name__ == '__main__':
    '''
    从命令行读参数
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name  # Network File
    seed = args.seed  # Seeds File
    model = args.model  # Model: LT or IC
    time_limit = args.time_limit  # Time Limit, default 60s

    graph = load_graph(file_name)  # Load Graph
    seeds = load_seeds(seed)

    global_graph = graph
    global_seeds = seeds

    worker = []
    worker_num = 8
    n = 500

    random.seed(int(os.getpid() + time.time() * 1e5))

    with Pool(worker_num) as p:
        if model == 'IC':
            res = p.map(solve_IC, [(time_limit - (time.time() - start_time)) for i in range(worker_num)])
        elif model == 'LT':
            res = p.map(solve_LT, [(time_limit - (time.time() - start_time)) for i in range(worker_num)])
        result_sum = 0
        count_sum = 0
        for result, count in res:
            result_sum += result
            count_sum += count
        print(result_sum / count_sum)

    end_time = time.time()
    print("End Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    total_time = end_time - start_time
    print("Total Time: " + str(total_time))
    '''
    程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
    '''
    sys.stdout.flush()
