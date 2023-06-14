import time
import os, psutil


def high(h, n):
    left = 0
    right = h[0]
    while (right - left > 0.0000000001):
        h[1] = (left + right) / 2
        Up = True
        for i in range(2,n):
            h[i] = 2 * h[i - 1] - h[i - 2] + 2
            if h[i] < 0:
                Up = False
                break
        if Up:
            right = h[1]
        else:
            left = h[1]
    return h[n - 1]


t_start = time.perf_counter()
process = psutil.Process(os.getpid())

with open('input.txt') as m:
    a = list(map(float, m.readline().split()))
    n = int(a[0])
    A = a[1]

h = []
for i in range(n):
    h.append(0)
h[0]=float(A)
res = high(h, n)

f = open('output.txt', 'w')
f.write(str(res))

f.close()
m.close()
print("Time of working: %s second" % (time.perf_counter() - t_start))
print("Memory", process.memory_info().rss/(1024*1024), "mb")