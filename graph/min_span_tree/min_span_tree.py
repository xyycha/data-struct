# -*- encoding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from graph_without_direction import GraphWithoutDirection


def min_span_tree_by_prim():
    graph_without_direction.min_span_tree_by_prim()


def min_span_tree_by_kruskal():
    graph_without_direction.min_span_tree_by_kruskal()


if __name__ == "__main__":
    graph_without_direction = GraphWithoutDirection()
    # 生成测试用例
    graph_without_direction.add_node(node_name="V1", near_node_names=["V2", "V4", "V3"], weights=[2, 1, 4])
    graph_without_direction.add_node(node_name="V2", near_node_names=["V1", "V4", "V5"], weights=[2, 3, 10])
    graph_without_direction.add_node(node_name="V3", near_node_names=["V1", "V4", "V6"], weights=[4, 2, 5])
    graph_without_direction.add_node(node_name="V4", near_node_names=["V1", "V3", "V6", "V7", "V5", "V2"],
                                     weights=[1, 2, 8, 4, 7, 3])
    graph_without_direction.add_node(node_name="V5", near_node_names=["V2", "V4", "V7"], weights=[10, 7, 6])
    graph_without_direction.add_node(node_name="V6", near_node_names=["V3", "V4", "V7"], weights=[5, 8, 1])
    graph_without_direction.add_node(node_name="V7", near_node_names=["V6", "V4", "V5"], weights=[1, 4, 6])
    graph_without_direction.show(file_name="初始无向图")
    min_span_tree_by_prim()
