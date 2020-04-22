# -*- encoding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from graph_without_direction import GraphWithoutDirection


def test1():
    graph_without_direction = GraphWithoutDirection()
    graph_without_direction.add_node(node_name="A", near_node_names=["B", "D"], weights=[1, 1])
    graph_without_direction.add_node(node_name="B", near_node_names=["A", "C"], weights=[1, 1])
    graph_without_direction.add_node(node_name="C", near_node_names=["B", "D", "G"], weights=[1, 1, 1])
    graph_without_direction.add_node(node_name="D", near_node_names=["A", "C", "E", "F"], weights=[1, 1, 1, 1])
    graph_without_direction.add_node(node_name="E", near_node_names=["D", "F"], weights=[1, 1])
    graph_without_direction.add_node(node_name="F", near_node_names=["D", "E"], weights=[1, 1])
    graph_without_direction.add_node(node_name="G", near_node_names=["C"], weights=[1])
    graph_without_direction.show(file_name="初始无向图")

    cut_vertex = graph_without_direction.find_cut_vertex()
    print(cut_vertex)


def test2():
    graph_without_direction1 = GraphWithoutDirection()
    graph_without_direction1.add_node(node_name="A", near_node_names=["B"], weights=[1])
    graph_without_direction1.add_node(node_name="B", near_node_names=["C"], weights=[1])
    graph_without_direction1.add_node(node_name="C", near_node_names=["D"], weights=[1])
    graph_without_direction1.add_node(node_name="D", near_node_names=["E"], weights=[1])
    graph_without_direction1.add_node(node_name="E", near_node_names=["F"], weights=[1])
    graph_without_direction1.add_node(node_name="F", near_node_names=["G"], weights=[1])
    graph_without_direction1.add_node(node_name="G", near_node_names=["E"], weights=[1])
    graph_without_direction1.show(file_name="初始无向图")

    cut_vertex = graph_without_direction1.find_cut_vertex()
    print(cut_vertex)


if __name__ == "__main__":
    test2()
