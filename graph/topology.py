# -*- encoding: utf-8 -*-
from graph import Graph


def topology():
    s_topology = Graph()
    s_topology.add_edge(node_name="V1", son_node_names=["V2", "V3", "V4"])
    s_topology.add_edge(node_name="V2", son_node_names=["V4", "V5"])
    s_topology.add_edge(node_name="V3", son_node_names=["V6"])
    s_topology.add_edge(node_name="V4", son_node_names=["V3", "V6", "V7"])
    s_topology.add_edge(node_name="V5", son_node_names=["V4", "V7"])
    s_topology.add_edge(node_name="V7", son_node_names=["V6"])
    topology_list = s_topology.topology()
    print(topology_list)


if __name__ == "__main__":
    topology()
