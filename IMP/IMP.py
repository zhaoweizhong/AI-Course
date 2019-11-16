# import os
import sys
# from multiprocessing import Pool
import time
import numpy as np
# import random
import argparse
import heapq

start_time = time.time()
# print("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))


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


def solve(graph, count, time_limit):
    # model_start_time = time.time()
    # graph = global_graph
    weights = np.zeros(graph.nodes_num + 1, dtype=np.float)
    for node in range(1, graph.nodes_num + 1):
        time_now = time.time()
        total_time = time_now - start_time
        if time_limit - total_time <= 3:
            break
        children = graph.get_children(node)
        for child in children:
            weights[node] = weights[node] + graph.get_weight(node, child)

    result = list(map(list(weights).index, heapq.nlargest(count, weights)))
    for i in range(count):
        print(result[i])

    # while time.time() - model_start_time < time_budget - 3:
        # result += res_count
    #     count += 1
    # return result, count


if __name__ == '__main__':
    '''
    从命令行读参数
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--count', type=int, default='5')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name  # Network File
    count = args.count  # Pre-defined size of the seed set
    model = args.model  # Model: LT or IC
    time_limit = args.time_limit  # Time Limit, default 60s

    graph = load_graph(file_name)  # Load Graph
    solve(graph, count, time_limit)

    # worker = []
    # worker_num = 8
    # n = 500

    # random.seed(int(os.getpid() + time.time() * 1e5))

    # with Pool(worker_num) as p:
    #     if model == 'IC':
    #         res = p.map(solve_IC, [(time_limit - (time.time() - start_time)) for i in range(worker_num)])
    #     elif model == 'LT':
    #         res = p.map(solve_LT, [(time_limit - (time.time() - start_time)) for i in range(worker_num)])
    #     result_sum = 0
    #     count_sum = 0
    #     for result, count in res:
    #         result_sum += result
    #         count_sum += count
    #     print(result_sum / count_sum)

    # end_time = time.time()
    # print("End Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    # total_time = end_time - start_time
    # print("Total Time: " + str(total_time))
    '''
    程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
    '''
    sys.stdout.flush()
