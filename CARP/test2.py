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


if __name__ == '__main__':
    '''
    Main
    '''

    time_limit = 60
    file_path = 'CARP_samples/gdb10.dat'
    seed = 1

    if len(sys.argv) == 6:
        file_path = sys.argv[1]
        time_limit = int(sys.argv[3])
        seed = int(sys.argv[5])

    spec, data = read_instance_file(file_path)  # 读取文件
    lines = data[:, 0:2]

    print(data[3, 2])
