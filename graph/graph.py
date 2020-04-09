# -*- encoding: utf-8 -*-
from collections import deque
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
        1. pass
    3. 针对含有负权重的图
        1. pass
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
            node.son_weight[son_node] = weights[son_index] if weights else 1

    def check_node_exist(self, node_name):
        """
        检查 节点是否存在
        :param node_name: 节点名
        :return: bool
        """
        if self._node_index.get(node_name, -1) == -1:
            return False
        return True

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

    def distance(self, start_node_name):
        pass


if __name__ == "__main__":
    s = Graph()
    s.add_edge(node_name="V1", son_node_names=["V2", "V3", "V4"])
    s.add_edge(node_name="V2", son_node_names=["V4", "V5"])
    s.add_edge(node_name="V3", son_node_names=["V6"])
    s.add_edge(node_name="V4", son_node_names=["V3", "V6", "V7"])
    s.add_edge(node_name="V5", son_node_names=["V4", "V7"])
    s.add_edge(node_name="V7", son_node_names=["V6"])
    res = s.topology()
    print(res)
