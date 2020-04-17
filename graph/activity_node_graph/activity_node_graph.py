# -*- encoding: utf-8 -*-
from collections import deque

from graphviz import Digraph


class ActivityNode(object):
    def __init__(self, activity_name, time_cost, father_activity_nodes: list):
        self.name = activity_name
        self.cost = time_cost
        self.fathers = father_activity_nodes
        self.input = len(father_activity_nodes)
        self.sons = []
        self.output = 0
        self.min_time = 0
        self.max_time = 0
        self.init_son()

    def refresh_min_time(self):
        times = [father.min_time for father in self.fathers] if self.fathers else [0]
        self.min_time = max(times) + self.cost

    def refresh_max_time(self):
        times = [son.max_time - son.cost for son in self.sons] if self.sons else [self.min_time]
        self.max_time = min(times)

    def init_son(self):
        for father in self.fathers:
            father.sons.append(self)
            father.output += 1

    def check_split(self):
        if len(self.fathers) > 1:
            return True
        return False

    def split_node(self):
        new_node = ActivityNode(activity_name=self.name, time_cost=self.cost,
                                father_activity_nodes=[self])
        self.name = self.name + "_start"
        self.cost = 0
        return new_node

    def print_node(self, father_nodes, d=None):
        node_name = self.name
        label = self.name + "/" + str(self.min_time) + "/" + str(self.max_time)
        d.node(name=node_name, label=label)
        for father in father_nodes:
            d.edge(father.name, node_name)


class ActivityNodeGraph(object):
    def __init__(self):
        self.root = ActivityNode(activity_name="start", time_cost=0, father_activity_nodes=[])
        self.leaf = None
        self.activity_name_2_activity_node = {}
        self.topology_node_list = []

    def add_activity(self, activity_name, time_cost, father_activity_names: list = None):
        if father_activity_names is None:
            father_activity_nodes = [self.root]
        else:
            father_activity_nodes = [self.activity_name_2_activity_node[father_activity_name] for father_activity_name in father_activity_names]
        new_node = ActivityNode(activity_name=activity_name,
                                time_cost=time_cost,
                                father_activity_nodes=father_activity_nodes)
        self.activity_name_2_activity_node[activity_name] = new_node
        if new_node.check_split():
            self.activity_name_2_activity_node[activity_name] = new_node.split_node()

    def topology(self):
        node_queue = deque()
        node_queue.append(self.root)
        while node_queue:
            father_node = node_queue.popleft()
            self.topology_node_list.append(father_node)
            father_node.refresh_min_time()
            son_nodes = father_node.sons
            for son_node in son_nodes:
                son_node.input -= 1
                if son_node.input == 0:
                    node_queue.append(son_node)
        node_queue = deque()
        node_queue.append(self.topology_node_list[-1])
        while node_queue:
            son_node = node_queue.popleft()
            son_node.refresh_max_time()
            father_nodes = son_node.fathers
            for father_node in father_nodes:
                father_node.output -= 1
                if father_node.output == 0:
                    node_queue.append(father_node)

    def show(self, file_name):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        for node in self.topology_node_list:
            node.print_node(father_nodes=node.fathers, d=d)
        d.view()


if __name__ == "__main__":
    activity_node_graph = ActivityNodeGraph()
    activity_node_graph.add_activity(activity_name="A", time_cost=3)
    activity_node_graph.add_activity(activity_name="B", time_cost=2)
    activity_node_graph.add_activity(activity_name="C", time_cost=3,
                                     father_activity_names=["A"])
    activity_node_graph.add_activity(activity_name="D", time_cost=2,
                                     father_activity_names=["A", "B"])
    activity_node_graph.add_activity(activity_name="E", time_cost=1,
                                     father_activity_names=["B"])
    activity_node_graph.add_activity(activity_name="F", time_cost=3,
                                     father_activity_names=["C", "D"])
    activity_node_graph.add_activity(activity_name="G", time_cost=2,
                                     father_activity_names=["D", "E"])
    activity_node_graph.add_activity(activity_name="K", time_cost=4,
                                     father_activity_names=["E"])
    activity_node_graph.add_activity(activity_name="H", time_cost=1,
                                     father_activity_names=["F", "G", "K"])
    activity_node_graph.topology()
    activity_node_graph.show(file_name="动作节点图")
