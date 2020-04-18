# -*- encoding: utf-8 -*-
from collections import deque
from heap import heap
from graphviz import Digraph
"""
拓扑排序是对 有向 无圈图 的顶点的一种排序
思路:
    1. 寻找 没有边的节点
    2. 删除 该节点以及 它的边
    3. 重复 1 2
    4. 在遍历完节点前 找不到迭代的节点时  有圈
    
最短路径的寻找
思路1:
    1. 针对无权重的图
        1. 类似拓扑思路
    2. 针对非负权重的图
        1. Dijkstra 算法
            - 每次将最小权重值的节点 pop
    3. 针对含有负权重的图
        1. 
"""


class Node(object):
    def __init__(self, name):
        """
        初始化 节点 信息 包括：
        1. 节点 名字
        2. 节点 入边的个数
        3. 节点 子节点和权重的 对应关系
        :param name: 节点名字
        """
        self.name = name
        self.in_degree = 0
        self.son_weight = {}


class Graph(object):
    def __init__(self):
        """
        初始化 图的信息  包括：
        1. 图中 节点的个数
        2. 图中 所有节点的列表
        3. 图中 节点名字和节点列表下标的对应关系
        """
        self._length = 0
        self._node_index = {}
        self._nodes = []
        self._max_weight = 1

    def add_edge(self, node_name, son_node_names: list, weights: list = None):
        """
        添加 边 和 权重
        :param node_name: 起始 节点名
        :param son_node_names: 尾部 节点名
        :param weights: 权重 默认 1
        :return: None
        """
        if not self.check_node_exist(node_name):
            self.add_new_node(node_name=node_name)
        node_index = self._node_index[node_name]
        node = self._nodes[node_index]
        for son_index, son_node_name in enumerate(son_node_names):
            if self.check_node_exist(node_name=son_node_name):
                index = self._node_index[son_node_name]
                son_node = self._nodes[index]
            else:
                son_node = self.add_new_node(node_name=son_node_name)
            son_node.in_degree += 1
            if weights:
                node.son_weight[son_node] = weights[son_index]
                self._max_weight = max(self._max_weight, weights[son_index])
            else:
                node.son_weight[son_node] = 1

    def check_node_exist(self, node_name):
        """
        检查 节点是否存在
        :param node_name: 节点名
        :return: bool
        """
        if self._node_index.get(node_name, -1) == -1:
            return False
        return True

    def node_name_2_node(self, node_name):
        """
        根据节点名 得到 节点
        :param node_name: 节点名
        :return: 节点
        """
        node_index = self._node_index.get(node_name, -1)
        if node_index == -1:
            return None
        return self._nodes[node_index]

    def add_new_node(self, node_name):
        """
        创建新的节点
        :param node_name: 新的节点名
        :return: 新的节点
        """
        node = Node(name=node_name)
        self._nodes.append(node)
        self._node_index[node_name] = self._length
        self._length += 1
        return node

    def topology(self):
        """
        拓扑顺序 遍历图的节点
        :return: 拓扑顺序 节点名字列表
        """
        node_queue = deque()
        topology_sort_list = []
        for node in self._nodes:
            if node.in_degree == 0:
                node_queue.append(node)
        for step in range(self._length):
            assert node_queue, "有环"
            node = node_queue.popleft()
            topology_sort_list.append(node.name)
            for node in node.son_weight.keys():
                node.in_degree -= 1
                if node.in_degree == 0:
                    node_queue.append(node)
        return topology_sort_list

    def all_distances_without_weight(self, start_node_name):
        """
        计算 初始节点  到 所有节点的最短路径
        :param start_node_name: 初始节点名
        :return: 初始节点 到 所有节点的最短路径的 信息
        """
        if not self.check_node_exist(node_name=start_node_name):
            assert False, "起始节点名字不在图中"
        status = self.init_distance_status()
        node_know_queue = deque()
        node = self.node_name_2_node(node_name=start_node_name)
        node_know_queue.append(node)
        status[start_node_name]["distance"] = 0
        status[start_node_name]["known"] = 1
        distance_known_nums = 1
        while distance_known_nums < self._length:
            # 无法继续进行拓扑 将计算结果提前返回
            if not node_know_queue:
                return status
            father_node = node_know_queue.popleft()
            father_node_name = father_node.name
            last_distance = status[father_node_name]["distance"]
            for son_node in father_node.son_weight.keys():
                son_node_name = son_node.name
                if status[son_node_name]["known"] == 1:
                    continue
                status[son_node_name]["known"] = 1
                status[son_node_name]["distance"] = last_distance + 1
                status[son_node_name]["father_name"] = father_node_name
                node_know_queue.append(son_node)
                distance_known_nums += 1
        return status

    def all_distances_with_weight(self, start_node_name):
        """
        计算 初始节点  到 所有节点的最短路径
        :param start_node_name: 初始节点名
        :return: 初始节点 到 所有节点的最短路径的 信息
        """
        if not self.check_node_exist(node_name=start_node_name):
            assert False, "起始节点名字不在图中"
        status = self.init_distance_status()
        node_heap = self.init_node_heap(start_node_name=start_node_name)
        while node_heap.size:
            father_node_heap = node_heap.pop()
            father_node_name = father_node_heap.info
            father_node = self.node_name_2_node(node_name=father_node_name)
            father_node_distance = father_node_heap.value
            status[father_node_name]["distance"] = father_node_distance
            status[father_node_name]["known"] = 1
            for son_node, weight in father_node.son_weight.items():
                son_node_name = son_node.name
                if status[son_node_name]["known"] == 1:
                    continue
                new_distance = father_node_distance + weight
                sub_distance = node_heap.get_value(key=son_node_name) - new_distance
                if sub_distance > 0:
                    status[son_node_name]["father_name"] = father_node_name
                    node_heap.decrease_value(key=son_node_name, value=sub_distance)
        return status

    def all_distances_with_negative_weight(self, start_node_name):
        """
        计算 含有负权值边 的 初始节点  到 所有节点的最短路径
        :param start_node_name: 初始节点名
        :return: 初始节点 到 所有节点的最短路径的 信息
        """
        if not self.check_node_exist(node_name=start_node_name):
            assert False, "起始节点名字不在图中"
        status = self.init_distance_status_with_negative_weight()
        node_queue = deque()
        node = self.node_name_2_node(node_name=start_node_name)
        node_queue.append(node)
        status[start_node_name]["queue"] = 1
        status[start_node_name]["distance"] = 0
        while node_queue:
            next_node = node_queue.popleft()
            next_node_name = next_node.name
            status[next_node_name]["pop"] += 1
            status[next_node_name]["queue"] = 0
            if status[next_node_name]["pop"] == self._length + 1:
                self.mark_negative_status(negative_node=next_node, status=status)
                continue
            for son_node, weight in next_node.son_weight.items():
                son_node_name = son_node.name
                if status[son_node_name]["negative"]:
                    continue
                new_distance = status[next_node_name]["distance"] + weight
                if status[son_node_name]["distance"] is None:
                    status[son_node_name]["distance"] = new_distance
                    status[son_node_name]["father_name"] = next_node_name
                    node_queue.append(son_node)
                    status[son_node_name]["queue"] = 1
                elif status[son_node_name]["distance"] > new_distance and status[son_node_name]["queue"]:
                    status[son_node_name]["distance"] = new_distance
                    status[son_node_name]["father_name"] = next_node_name
                elif status[son_node_name]["distance"] > new_distance:
                    status[son_node_name]["distance"] = new_distance
                    status[son_node_name]["father_name"] = next_node_name
                    node_queue.append(son_node)
                    status[son_node_name]["queue"] = 1
        return status

    def mark_negative_status(self, negative_node, status):
        """
        标记 因负值圈无法计算的 所有节点
        :param status: 节点的最短路径信息
        :param negative_node: 起始节点
        :return: None
        """
        node_name = negative_node.name
        status[node_name]["negative"] = 1
        for next_node in negative_node.son_weight.keys():
            if not status[next_node.name]["negative"]:
                self.mark_negative_status(negative_node=next_node, status=status)

    def init_distance_status_with_negative_weight(self):
        """
        初始化 带有负权重 的 最短路径信息
        :return: 初始化的最短路径信息
        """
        status = {}
        for node_name in self._node_index.keys():
            status[node_name] = {"pop": 0, "queue": 0, "distance": None, "father_name": "", "negative": 0}
        return status

    def init_distance_status(self):
        """
        初始化 最短路径信息
        :return: 初始化的最短路径信息
        """
        status = {}
        for node_name in self._node_index.keys():
            status[node_name] = {"known": 0, "distance": None, "father_name": ""}
        return status

    def init_node_heap(self, start_node_name):
        """
        初始化 节点的 堆信息
        :param start_node_name: 堆顶点名
        :return: 节点的 堆
        """
        node_heap = heap.Heap(cap=self._length)
        node_heap_list = []
        for node in self._nodes:
            name = node.name
            value = self._max_weight + 1 if start_node_name != name else 0
            heap_node = heap.HeapNode(value=value, info=name)
            node_heap_list.append(heap_node)
        node_heap.build_heap(node_heap_list)
        return node_heap

    def show(self, file_name):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        # 将所有节点 画出
        for node in self._nodes:
            d.node(name=node.name, label=node.name)
        for node in self._nodes:
            father_name = node.name
            for son, weight in node.son_weight.items():
                son_name = son.name
                d.edge(tail_name=father_name, head_name=son_name, label=str(weight))
        d.view()
