import time
import os, psutil


class Node:

    def __init__(self):
        self.key_t = None
        self.key = None
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0


class BinTree:

    def __init__(self):
        self.root = None
        self.nodes = {}

    def set_height(self, node):
        node.height = 1
        while node.parent:
            parent = node.parent
            if parent.height <= node.height:
                parent.height = node.height + 1
            node = parent


t_start = time.perf_counter()
process = psutil.Process(os.getpid())

with open('input.txt') as f:
    n = int(f.readline())
    if n == 0:
        with open('output.txt', 'w') as f:
            f.write('0')
            exit()
    tree = BinTree()
    data = []
    leaves = []
    nodes = {}
    for i in range(1, n+1):
        data.append(list(map(int, f.readline().split())))
        tree.nodes[i] = Node()
        tree.nodes[i].key = data[i-1][0]
        if data[i-1][1] == 0 and data[i-1][2] == 0:
            leaves.append(i)

for i in range(1, n+1):
    if data[i-1][1] != 0:
        tree.nodes[i].left = tree.nodes[data[i-1][1]]
        tree.nodes[data[i-1][1]].parent = tree.nodes[i]
    if data[i - 1][2] != 0:
        tree.nodes[i].right = tree.nodes[data[i - 1][2]]
        tree.nodes[data[i - 1][2]].parent = tree.nodes[i]
        if i == 1:
            tree.root = tree.nodes[i]

for i in leaves:
    tree.set_height(tree.nodes[i])
with open('output.txt', 'w') as f:
    f.write(str(tree.root.height))


print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")