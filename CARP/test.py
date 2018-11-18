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


spec, data = read_instance_file('CARP_samples/gdb10.dat')  # 读取文件
lines = data[:, 0:2]

begin_node = 6
to_node = 11

for line in lines:
    if ([begin_node, to_node] == line).all():
        print(True)
    else:
        print(False)
