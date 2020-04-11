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
        self.heap = [None]

    def show(self, file_name=None):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        node_name = []
        for node in self.heap:
            if node is None:
                node_name.append(None)
                continue
            name = str(id(node))
            d.node(name=name, label=str(node.value))
            node_name.append(name)
        max_father_index = self.size // 2
        for father_index in range(1, max_father_index + 1):
            left_son_index = father_index * 2
            right_son_index = father_index * 2 + 1
            if left_son_index <= self.size:
                d.edge(head_name=node_name[left_son_index], tail_name=node_name[father_index])
            if right_son_index <= self.size:
                d.edge(head_name=node_name[right_son_index], tail_name=node_name[father_index])
        d.view()

    def insert(self, node: HeapNode):
        self.heap.append(None)
        self.size += 1
        index = self.size
        while index > 1:
            father_index = index // 2
            if self.heap[father_index].value > node.value:
                self.heap[index] = self.heap[father_index]
                index = father_index
            else:
                break
        self.heap[index] = node
        return 1

    def pop(self):
        assert self.size > 0, "空堆"
        first_node = self.heap[1]
        last_node = self.heap.pop()
        self.size -= 1
        if first_node == last_node:
            return first_node
        index = 1
        while index <= self.size // 2:
            left_son = self.heap[index * 2]
            father_index = index
            right_son_index = index * 2 + 1
            self.heap[index] = left_son
            if left_son.value < last_node.value:
                index *= 2
            if right_son_index <= self.size and self.heap[right_son_index].value < last_node.value and self.heap[right_son_index].value < self.heap[father_index].value:
                self.heap[father_index] = self.heap[right_son_index]
                index = right_son_index
            if index == father_index:
                break
        self.heap[index] = last_node
        return first_node

    def find_node_index(self, key):
        for index in range(1, self.size + 1):
            node_key = self.heap[index].info
            if node_key == key:
                break
        return index

    def decrease_value(self, key, value):
        index = self.find_node_index(key=key)
        self.heap[index].value -= value
        father_index = index // 2
        while father_index >= 1 and self.heap[father_index].value > self.heap[index].value:
            self.swap_two_node(index1=father_index, index2=index)
            index = father_index
            father_index //= 2

    def get_value(self, key):
        index = self.find_node_index(key=key)
        return self.heap[index].value

    def swap_two_node(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def keep_father_lt_son(self, father_index):
        """
        下滤 操作
        :param father_index: 父节点下标
        :return: None
        """
        if father_index > self.size // 2:
            return
        left_index = father_index * 2
        right_index = father_index * 2 + 1
        index = father_index
        if self.heap[left_index].value < self.heap[father_index].value:
            index = left_index
        if right_index <= self.size and self.heap[right_index].value < self.heap[father_index].value and self.heap[right_index].value < self.heap[left_index].value:
            index = right_index
        if index == father_index:
            return
        self.swap_two_node(index1=index, index2=father_index)
        self.keep_father_lt_son(father_index=index)

    def build_heap(self, n: list):
        assert len(n) <= self.cap, "堆超限"
        self.heap.extend(n)
        self.size = len(n)
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
    print(pre_res)
    h = Heap(cap=20)
    h.build_heap(node_list)
    h.show(file_name="建立堆")
    print("end")


if __name__ == "__main__":
    test2()
