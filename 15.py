import time
import os, psutil
import sys
from collections import deque


res = []
class Node:
    def __init__(self, data):
        self.data = data
        self.par = None
        self.left = None
        self.right = None
        self.height = -1
        self.id = 0
        self.next = None


def dfs(root):
    if root.left is not None:
        dfs(root.left)
    if root.right is not None:
        dfs(root.right)
    fix_height(root)


def height_right(root):
    if root.right is None:
        return 0
    return root.right.height


def height_left(root):
    if root.left is None:
        return 0
    return root.left.height


def fix_height(root):
    root.height = max(height_left(root), height_right(root)) + 1


def blc(root):
    r = 0
    l = 0
    if root.right is not None:
        r = root.right.height
    if root.left is not None:
        l = root.left.height
    return r - l


def Rotate(node, side):
    if side == 'left':
        if node is None or node.right is None:
            return node
        parent = node.par
        right = node.right
        right_left = right.left
        if parent:
            if parent.right == node:
                parent.right = right
            else:
                parent.left = right
        right.par = parent
        right.left = node
        node.par = right
        node.right = right_left
        if right_left:
            right_left.par = node
        fix_height(node)
        fix_height(right)
        return right
    else:
        if node is None or node.left is None:
            return node
        parent = node.par
        left = node.left
        left_right = left.right
        if parent:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
        left.par = parent
        left.right = node
        node.par = left
        node.left = left_right
        if left_right:
            left_right.par = node
        fix_height(node)
        fix_height(left)
        return left


def getMax(root):
    if root is None:
        return root
    while root.right is not None:
        root = root.right
    return root


def Balance(root):
    fix_height(root)
    balance = blc(root)
    if balance > 1:
        if blc(root.right) < 0:
            root.right = Rotate(root.right, 'right')
        return Rotate(root, 'left')
    elif balance < -1:
        if blc(root.left) > 0:
            root.left = Rotate(root.left, 'left')
        return Rotate(root, 'right')
    return root


def delete(root, key):
    if root is None:
        return root
    elif key < root.data:
        root.left = delete(root.left, key)
    elif key > root.data:
        root.right = delete(root.right, key)
    else:
        if root.left is None and root.right is None:
            return None
        if root.left is None:
            root = root.right
            return Balance(root)
        temp = getMax(root.left)
        root.data = temp.data
        root.left = delete(root.left, temp.data)
    return Balance(root)


def printBST(root, n):
    global res
    queue = deque()
    queue.append((root, (-1, -1)))
    while queue:
        u, v = queue.popleft()
        if v[0] >= 0 and v[1] >= 0:
            res[v[0]][v[1]] = len(res) + 1
        if u is None:
            continue
        tmp = [0, 0, 0]
        tmp[0] = u.data
        res.append(tmp)
        cur = len(res)
        if u.left is not None:
            queue.append((u.left, (cur - 1, 1)))
        if u.right is not None:
            queue.append((u.right, (cur - 1, 2)))


t_start = time.perf_counter()
process = psutil.Process(os.getpid())
sys.stdin = open("input.txt", "r")
sys.stdout = open("output.txt", "w")
n = int(sys.stdin.readline())
nodes = []
for i in range(n + 10):
    nodes.append(Node(0))
for i in range(n):
    k, l, r = map(int, sys.stdin.readline().split())
    nodes[i + 1].data = k
    if l:
        nodes[i + 1].left = nodes[l]
        nodes[l].par = nodes[i + 1]
    if r:
        nodes[i + 1].right = nodes[r]
        nodes[r].par = nodes[i + 1]

val = int(sys.stdin.readline())
dfs(nodes[1])
nodes[1] = delete(nodes[1], val)
printBST(nodes[1], n)
sys.stdout.write(str(len(res)) + "\n")
n = len(res)
for i, j, k in res:
    sys.stdout.write(str(i) + ' ' + str(j) + ' ' + str(k) + '\n')
print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")