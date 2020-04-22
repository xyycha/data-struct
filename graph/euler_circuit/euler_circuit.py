# -*- encoding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from graph_without_direction import GraphWithoutDirection


def test1():
    # 所有顶点的度都为 偶数
    graph_without_direction = GraphWithoutDirection()
    graph_without_direction.add_node(node_name="1", near_node_names=["3", "4"])
    graph_without_direction.add_node(node_name="2", near_node_names=["3", "8"])
    graph_without_direction.add_node(node_name="3", near_node_names=["1", "2", "6", "9", "7", "4"])
    graph_without_direction.add_node(node_name="4", near_node_names=["1", "3", "7", "10", "11", "5"])
    graph_without_direction.add_node(node_name="5", near_node_names=["4", "10"])
    graph_without_direction.add_node(node_name="6", near_node_names=["3", "9"])
    graph_without_direction.add_node(node_name="7", near_node_names=["3", "4", "9", "10"])
    graph_without_direction.add_node(node_name="8", near_node_names=["2", "9"])
    graph_without_direction.add_node(node_name="9", near_node_names=["8", "6", "3", "7", "10", "12"])
    graph_without_direction.add_node(node_name="10", near_node_names=["9", "7", "4", "5", "11", "12"])
    graph_without_direction.add_node(node_name="11", near_node_names=["4", "10"])
    graph_without_direction.add_node(node_name="12", near_node_names=["9", "10"])

    graph_without_direction.show(file_name="初始无向图")
    euler_circuit_node_list = graph_without_direction.find_euler_circuit()
    euler_circuit_node_name_list = [node.name for node in euler_circuit_node_list]
    print(euler_circuit_node_name_list)


def test2():
    # 仅有两个 顶点的 度 为 奇数    路径应该为 开始和结束必须为 这两个顶点
    graph_without_direction = GraphWithoutDirection()
    graph_without_direction.add_node(node_name="1", near_node_names=["2", "3"])
    graph_without_direction.add_node(node_name="2", near_node_names=["1", "3", "6", "4"])
    graph_without_direction.add_node(node_name="3", near_node_names=["1", "2", "6", "5"])
    graph_without_direction.add_node(node_name="4", near_node_names=["2", "6", "5"])
    graph_without_direction.add_node(node_name="5", near_node_names=["3", "6", "4"])
    graph_without_direction.add_node(node_name="6", near_node_names=["2", "3", "4", "5"])

    graph_without_direction.show(file_name="初始无向图")
    euler_circuit_node_list = graph_without_direction.find_euler_circuit()
    euler_circuit_node_name_list = [node.name for node in euler_circuit_node_list]
    print(euler_circuit_node_name_list)


if __name__ == "__main__":
    test2()
