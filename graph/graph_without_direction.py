# -*- encoding: utf-8 -*-
from graphviz import Digraph
from heap import heap


class NodeWithoutDirection(object):
    def __init__(self, node_name: str):
        self.name = node_name
        self.edges = set()

    def add_edge(self, edge):
        assert edge not in self.edges, "边已经存在"
        self.edges.add(edge)


class EdgeWithoutDirection(object):
    def __init__(self, node1: NodeWithoutDirection, node2: NodeWithoutDirection, weight):
        self.nodes = {node1, node2}
        self.weight = weight

    def get_another_node(self, node: NodeWithoutDirection):
        node1, node2 = self.nodes
        if node == node1:
            return node2
        return node1


def pre_order(start_node: NodeWithoutDirection, node_status: dict, pre_order_list: list):
    pre_order_list.append(start_node)
    for edge in start_node.edges:
        another_node = edge.get_another_node(node=start_node)
        if not node_status[another_node]["num"]:
            node_status[start_node]["direction_nodes"].append(another_node)
            node_status[another_node]["num"] = node_status[start_node]["num"] + 1
            pre_order(start_node=another_node, node_status=node_status, pre_order_list=pre_order_list)
        elif start_node not in node_status[another_node]["direction_nodes"]:
            node_status[start_node]["anti_direction_nodes"].append(another_node)


class GraphWithoutDirection(object):
    def __init__(self):
        self.nodes = []
        self.node_names = set()
        self.node_name_2_node_index = {}
        self.edges = []

    def add_node(self, node_name: str, near_node_names: list, weights: list):
        assert len(near_node_names) == len(weights), "参数个数不一致"
        node_names = [node_name] + near_node_names
        weights = [0] + weights
        for index, name in enumerate(node_names):
            if name not in self.node_names:
                new_node = NodeWithoutDirection(node_name=name)
                self.node_names.add(name)
                self.nodes.append(new_node)
                self.node_name_2_node_index[name] = len(self.nodes) - 1
            if name != node_name:
                node1 = self.nodes[self.node_name_2_node_index[node_name]]
                node2 = self.nodes[self.node_name_2_node_index[name]]
                new_edge = EdgeWithoutDirection(node1=node1, node2=node2, weight=weights[index])
                self.edges.append(new_edge)
                node1.add_edge(edge=new_edge)
                node2.add_edge(edge=new_edge)

    def get_min_node_name(self):
        return min(self.node_names)

    def show(self, file_name):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        edges_known = []
        # 将所有节点 画出
        for name in self.node_names:
            d.node(name=name, label=name)
        for node in self.nodes:
            for edge in node.edges:
                node1, node2 = edge.nodes
                if edge.nodes not in edges_known:
                    edges_known.append(edge.nodes)
                    d.edge(tail_name=node1.name, head_name=node2.name, label=str(edge.weight))
        d.view()

    def min_span_tree_by_prim(self):
        new_graph = GraphWithoutDirection()
        node_names_known = {min(self.node_names)}
        while len(node_names_known) != len(self.node_names):
            all_min_weight_edge = None
            for node_name_known in node_names_known:
                node_known = self.nodes[self.node_name_2_node_index[node_name_known]]
                min_weight_edge = None
                for edge in node_known.edges:
                    another_node = (edge.nodes - {node_known}).pop()
                    if another_node.name not in node_names_known and (min_weight_edge is None or min_weight_edge.weight > edge.weight):
                        min_weight_edge = edge
                if min_weight_edge is None:
                    continue
                if all_min_weight_edge is None or all_min_weight_edge.weight > min_weight_edge.weight:
                    all_min_weight_edge = min_weight_edge
            all_min_weight_edge_node_names = {node.name for node in all_min_weight_edge.nodes}
            node_names_known = node_names_known.union(all_min_weight_edge_node_names)
            node_name_1 = all_min_weight_edge_node_names.pop()
            node_name_2 = all_min_weight_edge_node_names.pop()
            weight = all_min_weight_edge.weight
            new_graph.add_node(node_name=node_name_1, near_node_names=[node_name_2], weights=[weight])
            new_graph.add_node(node_name=node_name_2, near_node_names=[node_name_1], weights=[weight])
        new_graph.show(file_name="Prim最小生成树")

    def min_span_tree_by_kruskal(self):
        """
        未使用 Find/Join 模型
        :return: None
        """
        new_graph = GraphWithoutDirection()
        edge_heap = heap.Heap(len(self.edges))
        edge_heap_list = []
        for edge in self.edges:
            value = edge.weight
            heap_node = heap.HeapNode(value=value, info=edge)
            edge_heap_list.append(heap_node)
        edge_heap.build_heap(edge_heap_list)
        node_names_known = [i for i in range(len(self.node_names))]
        step = 0
        while edge_heap and step < len(self.node_names) - 1:
            edge = edge_heap.pop().info
            node_1, node_2 = edge.nodes
            index_1 = self.node_name_2_node_index[node_1.name]
            index_2 = self.node_name_2_node_index[node_2.name]
            group_id_1, group_id_2 = node_names_known[index_1], node_names_known[index_2]
            if group_id_1 != group_id_2:
                step += 1
                node_name_1 = node_1.name
                node_name_2 = node_2.name
                weight = edge.weight
                new_graph.add_node(node_name=node_name_1, near_node_names=[node_name_2], weights=[weight])
                new_graph.add_node(node_name=node_name_2, near_node_names=[node_name_1], weights=[weight])
                all_index = sorted([group_id_1, group_id_2])
                for index, group_id in enumerate(node_names_known):
                    if group_id == all_index[1]:
                        node_names_known[index] = all_index[0]
        new_graph.show(file_name="Kruskal最小生成树")

    def find_cut_vertex(self):
        status = {}
        pre_order_node_list = []
        cut_vertex_list = []
        start_node = self.nodes[0]
        for node in self.nodes:
            status[node] = {"num": 0 if node != start_node else 1,
                            "low": 0 if node != start_node else 1,
                            "direction_nodes": [],
                            "anti_direction_nodes": []
                            }
        pre_order(start_node=start_node, node_status=status, pre_order_list=pre_order_node_list)
        assert len(pre_order_node_list) == len(self.nodes), "图不连通"
        for node in pre_order_node_list[::-1]:
            anti_direction_nodes = status[node].get("anti_direction_nodes")
            direction_nodes = status[node].get("direction_nodes")
            if anti_direction_nodes:
                min_num = len(self.nodes) + 1
                for anti_direction_node in anti_direction_nodes:
                    if status[anti_direction_node].get("num") < min_num:
                        min_num = status[anti_direction_node].get("num")
                status[node]["low"] = min_num
            elif not direction_nodes:
                status[node]["low"] = status[node]["num"]
                continue
            else:
                min_num = status[node]["num"]
                for direction_node in direction_nodes:
                    if status[direction_node]["low"] < min_num:
                        min_num = status[direction_node]["low"]
                status[node]["low"] = min_num
            if node == pre_order_node_list[0]:
                cut_vertex_list += node.name if len(status[node]["direction_nodes"]) > 1 else []
                continue
            for direction_node in direction_nodes:
                if status[direction_node]["low"] >= status[node]["num"]:
                    cut_vertex_list.append(node.name)
                    break
        return cut_vertex_list


graph_without_direction = GraphWithoutDirection()
# 生成测试用例
graph_without_direction.add_node(node_name="V1", near_node_names=["V2", "V4", "V3"], weights=[2, 1, 4])
graph_without_direction.add_node(node_name="V2", near_node_names=["V1", "V4", "V5"], weights=[2, 3, 10])
graph_without_direction.add_node(node_name="V3", near_node_names=["V1", "V4", "V6"], weights=[4, 2, 5])
graph_without_direction.add_node(node_name="V4", near_node_names=["V1", "V3", "V6", "V7", "V5", "V2"], weights=[1, 2, 8, 4, 7, 3])
graph_without_direction.add_node(node_name="V5", near_node_names=["V2", "V4", "V7"], weights=[10, 7, 6])
graph_without_direction.add_node(node_name="V6", near_node_names=["V3", "V4", "V7"], weights=[5, 8, 1])
graph_without_direction.add_node(node_name="V7", near_node_names=["V6", "V4", "V5"], weights=[1, 4, 6])
graph_without_direction.show(file_name="初始无向图")

