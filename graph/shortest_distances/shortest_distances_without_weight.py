# -*- encoding: utf-8 -*-


def shortest_distances_without_weight(start_node_name):
    # 计算无权重节点的最短距离
    s_without_weight = Graph()
    s_without_weight.add_edge(node_name="V1", son_node_names=["V2", "V4"])
    s_without_weight.add_edge(node_name="V2", son_node_names=["V4", "V5"])
    s_without_weight.add_edge(node_name="V3", son_node_names=["V1", "V6"])
    s_without_weight.add_edge(node_name="V4", son_node_names=["V3", "V6", "V7", "V5"])
    s_without_weight.add_edge(node_name="V5", son_node_names=["V7"])
    s_without_weight.add_edge(node_name="V7", son_node_names=["V6"])
    distances_without_weight = s_without_weight.all_distances_without_weight(start_node_name=start_node_name)
    node_names = sorted(list(distances_without_weight.keys()))
    for node_name in node_names:
        if distances_without_weight[node_name]["known"] == 0:
            print("%s 到 %s 的距离不存在" % (start_node_name, node_name))
        else:
            father_node_name = distances_without_weight[node_name]["father_name"]
            distance = distances_without_weight[node_name]["distance"]
            print("%s 到 %s 的最短距离是 %f, 父节点名为 %s" % (start_node_name, node_name, distance, father_node_name))


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.getcwd()))
    from graph import Graph
    shortest_distances_without_weight(start_node_name="V1")
