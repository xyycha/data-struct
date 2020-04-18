# -*- encoding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from graph import Graph, Node


class CurrentGraph(Graph):
    def __init__(self):
        super(CurrentGraph, self).__init__()

    def init_weight(self):
        """
        初始化 权重信息 为 0
        :return: None
        """
        for son, weight in self.son_weight:
            self.son_weight[son] = 0

    def decrease_weight(self, father_node_name, son_node_name, decrease_value):
        """
        残余流量图 降低 边的权重值
        残余流量图 如果权重为 0 删除 该边
        :param father_node_name: 父节点名
        :param son_node_name: 子节点名
        :param decrease_value: 下调的值
        :return: None
        """
        father_node = self.node_name_2_node(node_name=father_node_name)
        son_node = self.node_name_2_node(node_name=son_node_name)
        father_node.son_weight[son_node] -= decrease_value
        if father_node.son_weight[son_node] == 0:
            father_node.son_weight.pop(son_node)

    def add_weight(self, father_node_name, son_node_name, add_value, add=True):
        father_node = self.node_name_2_node(node_name=father_node_name)
        son_node = self.node_name_2_node(node_name=son_node_name)
        if father_node.son_weight.get(son_node, None) is not None:
            father_node.son_weight[son_node] += add_value
        elif add:
            father_node.son_weight[son_node] = add_value
        else:
            son_node.son_weight[father_node] -= add_value

    def shortest_distance_path_without_weight(self, start="s", end="t"):
        status = self.all_distances_without_weight(start_node_name=start)
        if status[end]["known"] == 0:
            return None
        path = []
        node_name = end
        while status[node_name]["father_name"] != start:
            path.append(node_name)
            node_name = status[node_name]["father_name"]
        path.extend([node_name, start])
        return list(reversed(path))

    def get_max_current(self, path: list):
        weights = []
        for index in range(len(path) - 1):
            father_name = path[index]
            son_name = path[index + 1]
            father_node = self.node_name_2_node(node_name=father_name)
            son_node = self.node_name_2_node(node_name=son_name)
            weight = father_node.son_weight[son_node]
            weights.append(weight)
        return min(weights)


class MaxCurrentGraph(CurrentGraph):
    def __init__(self):
        super(MaxCurrentGraph, self).__init__()


class RestCurrentGraph(CurrentGraph):
    def __init__(self):
        super(RestCurrentGraph, self).__init__()


if __name__ == "__main__":
    current_graph = CurrentGraph()
    max_current_graph = MaxCurrentGraph()
    rest_current_graph = RestCurrentGraph()
    edges = [
        ("s", ("a", "b"), (3, 2), (0, 0)),
        ("a", ("b", "d", "c"), (1, 4, 3), (0, 0, 0)),
        ("b", ("d",), (2,), (0,)),
        ("c", ("t",), (2,), (0,)),
        ("d", ("t",), (3,), (0,)),
    ]
    for edge in edges:
        current_graph.add_edge(node_name=edge[0], son_node_names=edge[1], weights=edge[2])
        rest_current_graph.add_edge(node_name=edge[0], son_node_names=edge[1], weights=edge[2])
        max_current_graph.add_edge(node_name=edge[0], son_node_names=edge[1], weights=edge[3])
    while True:
        node_name_path = rest_current_graph.shortest_distance_path_without_weight()
        if node_name_path is None:
            break
        max_weight = rest_current_graph.get_max_current(path=node_name_path)
        for index in range(len(node_name_path) - 1):
            father_node_name = node_name_path[index]
            son_node_name = node_name_path[index + 1]
            rest_current_graph.decrease_weight(father_node_name=father_node_name, son_node_name=son_node_name, decrease_value=max_weight)
            # 添加逆向流
            rest_current_graph.add_weight(father_node_name=son_node_name, son_node_name=father_node_name, add_value=max_weight)
            max_current_graph.add_weight(father_node_name=father_node_name, son_node_name=son_node_name, add_value=max_weight, add=False)
    current_graph.show(file_name="流量图")
    max_current_graph.show(file_name="最大流量图")
    rest_current_graph.show(file_name="残余流量图")
    print("END")
