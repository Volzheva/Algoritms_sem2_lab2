import time
import os, psutil

t_start = time.perf_counter()
process = psutil.Process(os.getpid())


class BNode:
    def __init__(self, value=0, left=0, right=0):
        self.value = value
        self.left = left
        self.right = right


def tree_input():
    with open("input.txt", "r") as f:
        n = int(f.readline())
        if n == 0:
            return True
        arr = []
        for _ in range(n):
            inp = list(map(int, f.readline().split()))
            arr.append(BNode(inp[0], inp[1] - 1, inp[2] - 1))
        result = binary_tree_check(arr, 0, -float('inf'), float('inf'))
        if result:
            return True
        return False


def binary_tree_check(inp, i, left, right):
    if i == -1:
        return True
    if inp[i].value <= left or inp[i].value >= right:
        return False
    check = binary_tree_check(inp, inp[i].left, left, inp[i].value) and binary_tree_check(inp, inp[i].right, inp[i].value, right)
    return check


if __name__ == "__main__":
    res = tree_input()
    with open("output.txt", "w") as f:
        if res:
            f.write('YES')
        else:
            f.write('NO')


print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")