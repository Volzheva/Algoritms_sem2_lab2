import time
import os, psutil


class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


def in_order_traversal(node):
    global res
    if node is None:
        return
    in_order_traversal(node.left)
    res.append(node.data)
    in_order_traversal(node.right)


def pre_order_traversal(node):
    global res
    if node is None:
        return
    res.append(node.data)
    pre_order_traversal(node.left)
    pre_order_traversal(node.right)


def post_order_traversal(node):
    global res
    if node is None:
        return
    post_order_traversal(node.left)
    post_order_traversal(node.right)
    res.append(node.data)


t_start = time.perf_counter()
process = psutil.Process(os.getpid())
with open('input.txt') as m:
    a = m.readlines()[1:]
arr = []
for i in a:
    arr.append(list(map(int, i.split())))
tree = {}
root = arr[0][0]
for leaf in arr:
    k = Node(leaf[0])
    tree[leaf[0]] = k

for l in arr:
    if l[1] != -1:
        tree[l[0]].left = tree[arr[l[1]][0]]
    else:
        tree[l[0]].left = None
    if l[2] != -1:
        tree[l[0]].right = tree[arr[l[2]][0]]
    else:
        tree[l[0]].right = None

f = open('output.txt', 'w')
res = []
in_order_traversal(tree[root])
for i in range(len(res)):
    f.write(str(res[i]) + " ")
f.write("\n")
res = []
pre_order_traversal(tree[root])
for i in range(len(res)):
    f.write(str(res[i]) + " ")
f.write("\n")
res = []
post_order_traversal(tree[root])
for i in range(len(res)):
    f.write(str(res[i]) + " ")
f.write("\n")

f.close()
m.close()
print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")