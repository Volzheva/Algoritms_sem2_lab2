import time
import psutil
import sys

t_start = time.perf_counter()


class Node:
    def __init__(self, v=int()): #значение (value
        self.value = v
        self.left = None #ссылки на левого и правого потомков (left и right)
        self.right = None
        self.count_left = 0 #количество узлов в поддеревьях слева и справа
        self.count_right = 0
        self.height_left = 0 #высоту левого и правого поддеревьев
        self.height_right = 0
        self.parent = None #ссылка на родительский узел


class AVLTree:
    root = None

    def __init__(self):  #дерево в данный момент не содержит ни одного узла и является пустым
        self.root = None

    def insert(self, value): #вставляет новый узел со значением value в дерево, сохраняя его самобалансировку.
        if not self.find(value):
            time = Node(value)
            if self.root is None:
                self.root = time
            else:
                index = self.root
                flag = True
                while flag:
                    if time.value > index.value and index.right is not None:
                        index = index.right
                    elif time.value < index.value and index.left is not None:
                        index = index.left
                    else:
                        flag = False
                if time.value > index.value:
                    time.parent = index
                    index.right = time
                else:
                    time.parent = index
                    index.left = time
                self.balance_number(index)
                while index is not None:
                    self.balance_number(index)
                    index = self.balance(index)
                    self.root = index
                    index = index.parent
            return time

    def delete(self, value): #удаляет узел с заданным значением value из дерева, сохраняя его самобалансировку.
        self.delete_vertex(self.find(value))

    def delete_vertex(self, time): #удаление узла time из АВЛ-дерева.
        if time:
            if max(time.height_right, time.height_left) == 0:
                if time.parent is None:
                    self.root = None
                else:
                    index = time.parent
                    if time.parent.left == time:
                        time.parent.left = None
                    else:
                        time.parent.right = None
                    while index is not None:
                        self.balance_number(index)
                        index = self.balance(index)
                        self.root = index
                        index = index.parent
            else:
                if time.height_right > time.height_left:
                    time.value = time.right.value
                    self.delete_vertex(time.right)
                else:
                    time.value = time.left.value
                    self.delete_vertex(time.left)

    def find(self, value): #выполняет поиск узла с заданным значением value в дереве и возвращает его. Если узел не найден, возвращается None.
        index = self.root
        flag = True
        while flag and index is not None:
            if value > index.value:
                index = index.right
            elif value < index.value:
                index = index.left
            else:
                flag = False
        if index is None:
            return None
        else:
            return index

    # log(n)
    def exists(self, value): #проверяет, существует ли узел с заданным значением value в дереве. Возвращает строку 'true', если узел существует, и 'false' в противном случае.
        if self.find(value):
            return 'true'
        return 'false'

    def next(self, value): #находит минимальное значение, большее заданного value в дереве, и возвращает его. Если такого значения нет, возвращается строка 'none'.
        time = self.next_time(value, self.root)
        if time == 10 ** 10:
            return 'none'
        else:
            return time

    def next_time(self, value, link): #рекурсивно находит минимальное значение, которое больше заданного значения value в дереве, начиная с узла link.
        if link is not None:
            min_l = self.next_time(value, link.left)
            if min_l <= value:
                min_l = 10 ** 10
            min_r = self.next_time(value, link.right)
            if min_r <= value:
                min_r = 10 ** 10
            return min(min_l, min_r, link.value if link.value > value else 10 ** 10)
        else:
            return 10 ** 10

    def prev(self, value): #использует prev_time(value, link) для поиска максимального значения, меньшего заданного значения value в дереве.
        time = self.prev_time(value, self.root) #Функция prev возвращает найденное значение или строку 'none', если такого значения нет.
        if time == -10 ** 11:
            return 'none'
        else:
            return time

    def prev_time(self, value, link): #рекурсивно находит максимальное значение, которое меньше заданного значения value в дереве, начиная с узла link.
        if link is not None:
            min_l = self.prev_time(value, link.left)
            if min_l >= value:
                min_l = -10 ** 11
            min_r = self.prev_time(value, link.right)
            if min_r >= value:
                min_r = -10 ** 11
            return max(min_l, min_r, link.value if link.value < value else -10 ** 11)
        else:
            return -10 ** 11

    def balance_number(self, vertex): #пересчитывает значения высоты и количества узлов в поддеревьях для указанного узла vertex.
        if vertex:
            vertex.height_left = 0
            vertex.height_right = 0
            if vertex.left:
                vertex.height_left = 1 + max(vertex.left.height_right, vertex.left.height_left)
            if vertex.right:
                vertex.height_right = 1 + max(vertex.right.height_right, vertex.right.height_left)
            self.balance_sum(vertex)

    def balance_sum(self, vertex): # пересчитывает суммарное количество узлов в поддеревьях для указанного узла vertex.
        if vertex:
            vertex.count_left = 0
            vertex.count_right = 0
            if vertex.left:
                vertex.count_left = 1 + vertex.left.height_right + vertex.left.height_left
            if vertex.right:
                vertex.count_right = 1 + vertex.right.height_right + vertex.right.height_left

    def balance(self, vertex): #выполняет балансировку дерева для указанного узла vertex в случае несоответствия баланса.
        if vertex:
            dif = vertex.height_right - vertex.height_left
            if dif > 1:
                if vertex.right.height_right < vertex.right.height_left:
                    vertex = self.blt(vertex)
                else:
                    vertex = self.slt(vertex)
            elif dif < -1:
                if vertex.left.height_right > vertex.left.height_left:
                    vertex = self.brt(vertex)
                else:
                    vertex = self.srt(vertex)
        return vertex

    def slt(self, vertex): #операцию малого левого поворота (single left rotation) для балансировки АВЛ-дерева.
        if vertex is not None and vertex.height_right - vertex.height_left > 0 and vertex.right.height_left <= vertex.right.height_right:
            time_par = vertex.parent
            time_left = vertex.right.left
            vertex.right.left = vertex
            vertex.parent = vertex.right
            vertex.right = time_left
            vertex.parent.parent = time_par
            if time_par is not None:
                if time_par.left == vertex:
                    time_par.left = vertex.parent
                else:
                    time_par.right = vertex.parent
            self.balance_number(vertex)
            vertex = vertex.parent
            self.balance_number(vertex)
        return vertex

    def srt(self, vertex):
        if vertex is not None and vertex.height_left - vertex.height_right > 0 and vertex.left.height_right <= vertex.left.height_left:
            time_par = vertex.parent
            time_right = vertex.left.right
            vertex.left.right = vertex
            vertex.parent = vertex.left
            vertex.left = time_right
            vertex.parent.parent = time_par
            if time_par is not None:
                if time_par.left == vertex:
                    time_par.left = vertex.parent
                else:
                    time_par.right = vertex.parent
            self.balance_number(vertex)
            vertex = vertex.parent
            self.balance_number(vertex)
        return vertex

    def blt(self, vertex):
        if vertex is not None and vertex.height_right - vertex.height_left >= 2 and vertex.right.height_left > vertex.right.height_right:
            vertex.right = self.srt(vertex.right)
            vertex = self.slt(vertex)
        return vertex

    def brt(self, vertex):
        if vertex is not None and vertex.height_left - vertex.height_right >= 2 and vertex.left.height_right <= vertex.left.height_left:
            vertex.left = self.slt(vertex.left)
            vertex = self.srt(vertex)
        return vertex

    def find_max(self, n, vertex=None): #находит n-ое по величине значение в дереве и возвращает его.
        if not vertex:
            vertex = self.root
        if vertex.count_right + 1 == n:
            return vertex.value
        elif vertex.count_right >= n:
            return self.find_max(n, vertex.right)
        else:
            return self.find_max(n - vertex.count_right - 1, vertex.left)


sys.stdin = open("input.txt", "r")
sys.stdout = open("output.txt", "w")

tree = AVLTree()
n = int(sys.stdin.readline())
for i in range(n):
    s = sys.stdin.readline().split()
    if s[0] == '+1' or s[0] == '1':
        tree.insert(int(s[1]))
    elif s[0] == '-1':
        tree.delete(int(s[1]))
    elif s[0] == '0':
        print(tree.find_max(int(s[1])))

print("Время работы: %s секунд " % (time.perf_counter() - t_start))
print(str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total) + " MB")