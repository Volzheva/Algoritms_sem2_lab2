import time
import os, psutil


class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def __find(self, node, parent, value):
        if node is None:
            return None, parent, False

        if value == node.data:
            return node, parent, True

        if value < node.data:
            if node.left:
                return self.__find(node.left, node, value)

        if value > node.data:
            if node.right:
                return self.__find(node.right, node, value)

        return node, parent, False

    def append(self, obj):
        if self.root is None:
            self.root = obj
            return obj

        s, p, fl_find = self.__find(self.root, None, obj.data)

        if not fl_find and s:
            if obj.data < s.data:
                s.left = obj
            else:
                s.right = obj

        return obj

    def find_k_element(self, node, result, k, flag, file):
        if len(result) == k:
            flag = True
            file.write(str(result[k - 1]) + "\n")
        if node is None:
            return
        if not flag:
            self.find_k_element(node.left, result, k, flag, file)
            result.append(node.data)
            self.find_k_element(node.right, result, k, flag, file)


t_start = time.perf_counter()
process = psutil.Process(os.getpid())
f = open("input.txt")
m = open("output.txt", "w")
t = Tree()
for each in f.readlines():
    operation, number = each.split()
    if operation == "+":
        t.append(Node(int(number)))
    if operation == "?":
        t.find_k_element(t.root, [], int(number), False, m)

f.close()
m.close()
print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")