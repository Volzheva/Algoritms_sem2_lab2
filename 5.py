import time
import os, psutil

t_start = time.perf_counter()
process = psutil.Process(os.getpid())

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_node = self._find_min(node.right)
                node.value = min_node.value
                node.right = self._delete(node.right, min_node.value)
        return node

    def exists(self, value):
        return self._exists(self.root, value)

    def _exists(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._exists(node.left, value)
        else:
            return self._exists(node.right, value)

    def next(self, value):
        node = self.root
        result = None
        while node is not None:
            if node.value > value:
                if result is None or node.value < result.value:
                    result = node
                node = node.left
            else:
                node = node.right
        if result is None:
            return "none"
        else:
            return str(result.value)

    def prev(self, value):
        node = self.root
        result = None
        while node is not None:
            if node.value < value:
                if result is None or node.value > result.value:
                    result = node
                node = node.right
            else:
                node = node.left
        if result is None:
            return "none"
        else:
            return str(result.value)


with open("input.txt") as f_in, open("output.txt", "w") as f_out:
    tree = BinarySearchTree()
    for line in f_in:
        operation, value = line.strip().split()
        value = int(value)
        if operation == "insert":
            tree.insert(value)
        elif operation == "delete":
            tree.delete(value)
        elif operation == "exists":
            f_out.write(str(tree.exists(value)).lower() + "\n")
        elif operation == "next":
            f_out.write(tree.next(value) + "\n")
        elif operation == "prev":
            f_out.write(tree.prev(value) + "\n")

print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")
