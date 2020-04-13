# -*- encoding: utf-8 -*-


def shortest_distances_with_negative_weight(start_node_name):
    s_with_negative_weight = Graph()
    s_with_negative_weight.add_edge(node_name="V1", son_node_names=["V2", "V4"], weights=[2, 1])
    s_with_negative_weight.add_edge(node_name="V2", son_node_names=["V5"], weights=[-3])
    s_with_negative_weight.add_edge(node_name="V3", son_node_names=["V1", "V6"], weights=[4, 2])
    s_with_negative_weight.add_edge(node_name="V4", son_node_names=["V2", "V3", "V6", "V7"], weights=[3, 5, 6, 2])
    s_with_negative_weight.add_edge(node_name="V5", son_node_names=["V4", "V7"], weights=[1, 6])
    s_with_negative_weight.add_edge(node_name="V7", son_node_names=["V6"], weights=[1])
    distances_with_negative_weight = s_with_negative_weight.all_distances_with_negative_weight(start_node_name=start_node_name)
    node_names = sorted(list(distances_with_negative_weight.keys()))
    for node_name in node_names:
        if distances_with_negative_weight[node_name]["negative"]:
            print("%s 到 %s 的距离不存在最小值" % (start_node_name, node_name))
        elif not distances_with_negative_weight[node_name]["pop"]:
            print("%s 到 %s 的路径不存在" % (start_node_name, node_name))
        else:
            father_node_name = distances_with_negative_weight[node_name]["father_name"]
            distance = distances_with_negative_weight[node_name]["distance"]
            print("%s 到 %s 的最短距离是 %f, 父节点名为 %s" % (start_node_name, node_name, distance, father_node_name))


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.getcwd())
    from graph import Graph
    shortest_distances_with_negative_weight(start_node_name="V1")
