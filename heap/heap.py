# -*- encoding: utf-8 -*-
import random

from graphviz import Digraph


class HeapNode(object):
    def __init__(self, value, info):
        self.value = value
        self.info = info


class Heap(object):
    def __init__(self, cap):
        self.cap = cap
        self.size = 0
        self.heap = []

    def show(self, file_name=None):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        node_name = []
        for node in self.heap:
            name = str(id(node))
            d.node(name=name, label=str(node.value))
            node_name.append(name)
        max_father_index = self.size // 2 + 1
        for father_index in range(1, max_father_index):
            left_son_index = father_index * 2 - 1
            right_son_index = father_index * 2
            if left_son_index < self.size:
                d.edge(head_name=node_name[left_son_index], tail_name=node_name[father_index - 1])
            if right_son_index < self.size:
                d.edge(head_name=node_name[right_son_index], tail_name=node_name[father_index - 1])
        d.view()

    def insert(self, node: HeapNode):
        if not self.heap:
            self.heap.append(node)
            self.size += 1
            return 1
        index = self.size + 1
        if index > self.cap:
            return -1
        self.heap.append(None)
        while index >= 1:
            father_index = index // 2
            if index != 1 and node.value < self.heap[father_index - 1].value:
                self.heap[index - 1] = self.heap[father_index - 1]
            else:
                self.heap[index - 1] = node
                break
            index = father_index
        self.size += 1
        return 1

    def pop(self):
        assert self.size > 0, "空堆"
        index = 1
        top = self.heap[0]
        self.size -= 1
        while index * 2 <= self.size:
            child = index * 2
            if child != self.size and self.heap[child - 1].value > self.heap[child].value:
                child += 1
            if self.heap[child - 1].value < self.heap[self.size].value:
                self.heap[index - 1] = self.heap[child - 1]
            else:
                break
            index = child
        self.heap[index - 1] = self.heap.pop()
        return top

    def swap_two_node(self, index1, index2):
        # ??? self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
        temp_value = self.heap[index1].value
        temp_info = self.heap[index2].info
        self.heap[index1].value = self.heap[index2].value
        self.heap[index1].info = self.heap[index2].info
        self.heap[index2].value = temp_value
        self.heap[index2].info = temp_info

    def keep_father_lt_son(self, father_index):
        max_father_index = self.size // 2
        if father_index > max_father_index:
            return
        left_index = father_index * 2 - 1
        right_index = father_index * 2
        if right_index < self.size and self.heap[right_index].value < self.heap[father_index - 1].value and self.heap[right_index].value < self.heap[left_index].value:
            self.swap_two_node(right_index, father_index - 1)
            return self.keep_father_lt_son(father_index=right_index + 1)
        if self.heap[left_index].value < self.heap[father_index - 1].value:
            self.swap_two_node(left_index, father_index - 1)
            return self.keep_father_lt_son(father_index=left_index + 1)

    def build_heap(self, n: list):
        assert len(n) <= self.cap, "堆超限"
        self.heap = n
        self.size = len(self.heap)
        father_index = self.size // 2
        for index in range(father_index, 0, -1):
            self.keep_father_lt_son(father_index=index)


def test1():
    h = Heap(cap=20)
    for i in range(20):
        value = random.randint(0, 100)
        info = {"value": value, "key": str(value)}
        node = HeapNode(value=value, info=info)
        h.insert(node=node)
    h.show(file_name="初始堆")
    h.pop()
    h.show(file_name="第一次pop")
    h.pop()
    h.show(file_name="第二次pop")
    h.pop()
    h.show(file_name="第三次pop")


def test2():
    node_list = []
    pre_res = []
    for i in range(20):
        value = random.randint(0, 100)
        pre_res.append(value)
        info = {"value": value, "key": str(value)}
        node = HeapNode(value=value, info=info)
        node_list.append(node)
    h = Heap(cap=20)
    h.build_heap(node_list)
    h.show(file_name="建立堆")
    print("end")


if __name__ == "__main__":
    test1()
