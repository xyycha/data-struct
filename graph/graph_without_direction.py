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

    def sub_edge(self, edge):
        assert edge in self.edges, "节点没有该边"
        self.edges = self.edges - {edge}

    def get_edge(self, node):
        for edge in self.edges:
            if edge.nodes == {self, node}:
                return edge
        assert False, "与该节点没有边"


class EdgeWithoutDirection(object):
    def __init__(self, node1: NodeWithoutDirection, node2: NodeWithoutDirection, weight):
        self.nodes = {node1, node2}
        self.weight = weight

    def get_another_node(self, node: NodeWithoutDirection):
        assert node in self.nodes, "节点不属于边"
        # (self.nodes - {node}).pop()
        node1, node2 = self.nodes
        if node == node1:
            return node2
        return node1


def pre_order(start_node: NodeWithoutDirection, node_status: dict, pre_order_list: list):
    """
    先序遍历
    :param start_node: 开始节点
    :param node_status: 所有节点的状态
    :param pre_order_list: 先序遍历节点的顺序
    :return: None
    """
    pre_order_list.append(start_node)
    for edge in start_node.edges:
        another_node = edge.get_another_node(node=start_node)
        if not node_status[another_node]["num"]:
            node_status[start_node]["direction_nodes"].append(another_node)
            node_status[another_node]["num"] = len(pre_order_list) + 1
            node_status[another_node]["father"] = start_node
            pre_order(start_node=another_node, node_status=node_status, pre_order_list=pre_order_list)
        elif start_node not in node_status[another_node]["direction_nodes"] and \
                node_status[another_node]["num"] < node_status[start_node]["num"]:
            node_status[start_node]["anti_direction_nodes"].append(another_node)


class GraphWithoutDirection(object):
    def __init__(self):
        self.nodes = []
        self.node_names = set()
        self.node_name_2_node_index = {}
        self.edges = []

    def add_node(self, node_name: str, near_node_names: list, weights: list = None):
        """
        添加节点
        :param node_name: 新节点名
        :param near_node_names: 新节点相邻的节点名列表
        :param weights: 对应的权重值
        :return: None
        """
        if weights is None:
            weights = [1 for _ in near_node_names]
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

    def show(self, file_name):
        """
        将无向图转化为pdf 好检查结果
        :param file_name: pdf名字
        :return: None
        """
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
        """
        最少生成树
        所有已知点 和 未知点的最小权重边加到图中，直到所有的节点都加到图中为止
        :return: None
        """
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
        最小生成树  寻找最小权重的边加到图中
        条件就是 不能形成环，直到所有节点都被连接停止
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

    def depth_first_search(self, start_node: NodeWithoutDirection = None, connect_check: bool = True):
        """
        先序遍历和后续遍历 所有节点 计算 Num值和Low值
        :param start_node: 开始节点
        :param connect_check: 是否检查图的连通性(默认是检查的，但是寻找欧拉路径是可以不连通的)
        :return: 返回所有节点的信息 和 截点的列表
        """
        status = {}
        pre_order_node_list = []
        cut_vertex_list = []
        if start_node is None:
            start_node = self.nodes[0]
        for node in self.nodes:
            status[node] = {"num": 0 if node != start_node else 1,
                            "low": len(self.nodes) if node != start_node else 1,
                            "direction_nodes": [],
                            "anti_direction_nodes": [],
                            "father": None
                            }
        pre_order(start_node=start_node, node_status=status, pre_order_list=pre_order_node_list)
        if connect_check:
            assert len(pre_order_node_list) == len(self.nodes), "图不连通"
        for node in pre_order_node_list[::-1]:
            anti_direction_nodes = status[node].get("anti_direction_nodes")
            direction_nodes = status[node].get("direction_nodes")
            if anti_direction_nodes:
                for anti_direction_node in anti_direction_nodes:
                    if status[anti_direction_node].get("num") < status[node]["low"]:
                        status[node]["low"] = status[anti_direction_node].get("num")
            elif not direction_nodes:
                status[node]["low"] = status[node]["num"]
                continue
            if direction_nodes:
                for direction_node in direction_nodes:
                    if status[direction_node]["low"] < status[node]["low"]:
                        status[node]["low"] = status[direction_node]["low"]
            if node == pre_order_node_list[0]:
                cut_vertex_list += [node.name] if len(status[node]["direction_nodes"]) > 1 else []
                continue
            for direction_node in direction_nodes:
                if status[direction_node]["low"] >= status[node]["num"]:
                    cut_vertex_list.append(node.name)
                    break
        return status, cut_vertex_list

    def find_cut_vertex(self):
        """
        借助 深度优先搜索 查询 割点
        :return: 割点列表
        """
        _, cut_vertex_list = self.depth_first_search()
        return cut_vertex_list

    def check_euler_circuit(self):
        """
        检验 欧拉回路是否存在 三种情况
        1. 节点的度 全部为偶数 True
        2. 节点的度 为 奇数的个数 大于 2 False
        3. 节点的度 为 奇数的个数 等于 2 Half True（严格意义上不是欧拉回路但是可以经过所有的边，但是回不到初始的节点）
        :return: bool, None or List
        """
        edges_num = [len(node.edges) % 2 for node in self.nodes]
        odd_edges_nodes = []
        for index, edge_num in enumerate(edges_num):
            if edge_num == 1:
                odd_edges_nodes.append(self.nodes[index])
            if len(odd_edges_nodes) > 2:
                return False, None
        if not odd_edges_nodes:
            return True, None
        if len(odd_edges_nodes) == 2:
            return True, odd_edges_nodes

    def find_euler_circuit(self):
        """
        寻找欧拉回路
        :return: 欧拉回路的节点名
        """
        status, nodes = self.check_euler_circuit()
        if not status:
            return []
        if not nodes:
            start_node = self.nodes[0]
            return self._find_euler_circuit(start=start_node)
        base_path = self._find_path_by_topology(start=nodes[0], end=nodes[1])
        return self._find_euler_circuit(start=nodes[0], euler_circuit=base_path)

    def _find_euler_circuit(self, start: NodeWithoutDirection, euler_circuit: list = None):
        """
        :param start: 从哪个节点开始 寻找欧拉路径。
        如果所有节点的度都是 偶数 那么 开始的节点随意
        但是 仅有两个节点的度是 奇数 那么 开始的节点必须是这两个节点的其中一个
        :param euler_circuit: 基础的欧拉回路
        如果所有节点的度都是 偶数 那么 开始的欧拉回路的列表是空
        但是 仅有两个节点的度是 奇数 那么 开始的欧拉回路是这两个节点的通路路径
        :return: 欧拉回路
        """
        if euler_circuit is None:
            euler_circuit = []
        index = 0
        while index >= 0:
            circle = self._find_path_by_topology(start=start)
            euler_circuit = euler_circuit[:index] + circle + euler_circuit[index + 1:]
            for i in range(index, len(euler_circuit) + 1):
                if i == len(euler_circuit):
                    index = -1
                elif len(euler_circuit[i].edges) >= 2:
                    index = i
                    start = euler_circuit[index]
                    break
        return euler_circuit

    def _find_path_by_topology(self, start: NodeWithoutDirection, end: NodeWithoutDirection = None):
        """
        寻找从开始节点到结束节点的路径
        当结束节点为空时 寻找开始节点到本身的闭环路径
        并将路径所经过的边 在图中删除 防止重复使用
        :param start: 开始节点
        :param end: 结束节点
        :return: 路径
        """
        status, _ = self.depth_first_search(start_node=start, connect_check=False)
        target_node, target_num = None, 1
        for node, info in status.items():
            node_num = info.get("num")
            node_low = info.get("low")
            if end and node == end:
                target_node = node
                break
            if node_num > target_num and node_low == 1:
                target_node = node
                target_num = node_num
        path = []
        last_node = target_node
        while target_node != start:
            path.append(target_node)
            father_node = status[target_node].get("father")
            edge = target_node.get_edge(node=father_node)
            target_node.sub_edge(edge=edge)
            edge = father_node.get_edge(node=target_node)
            father_node.sub_edge(edge=edge)
            target_node = father_node
        path.append(start)
        path = list(reversed(path))
        if end is None:
            path.append(start)
            edge = last_node.get_edge(node=start)
            last_node.sub_edge(edge=edge)
            edge = start.get_edge(node=last_node)
            start.sub_edge(edge=edge)
        return path
