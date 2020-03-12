# -*- encoding: utf-8 -*-
import math

from tree_to_pdf.print_tree import Node


class BTreeNode(Node):
    def __init__(self, keys: list, nodes: list):
        super(BTreeNode, self).__init__(keys=keys, nodes=nodes)

    def get_next_node(self, key):
        if not self.next_nodes:
            return None
        for index, value in enumerate(self.key_list):
            if key < value:
                return self.next_nodes[index]
            elif key == value:
                return self
        return self.next_nodes[-1]

    def insert(self, key, node=None):
        index = -1
        for value in self.key_list:
            if key > value:
                index += 1
            else:
                break
        index += 1
        self.key_list = self.key_list[:index] + [key] + self.key_list[index:]
        if node is not None:
            self.next_nodes = self.next_nodes[:index+1] + [node] + self.next_nodes[index+1:]

    def check_status(self, m):
        if len(self.key_list) == m:
            return False
        return True

    def split_keys(self):
        index = math.ceil(len(self.key_list) / 2) - 1
        mid_key = self.key_list[index]
        new_key_list = self.key_list[index + 1:]
        new_next_nodes = self.next_nodes[index + 1:]
        self.key_list = self.key_list[:index]
        self.next_nodes = self.next_nodes[:index+1]
        new_node = BTreeNode(keys=new_key_list, nodes=new_next_nodes)
        return mid_key, new_node


class BTree(object):
    def __init__(self, m: int):
        self.M = m
        self.root = None

    def insert(self, key):
        index_node = self.root
        index_path = []
        if self.root is None:
            new_root = BTreeNode(keys=[key], nodes=[])
            self.root = new_root
            return 1
        # 先找到叶子节点   叶子节点的next_nodes 为空列表
        while index_node.next_nodes:
            index_path.append(index_node)
            next_node = index_node.get_next_node(key=key)
            # 该值已在 节点 中
            if next_node == index_node:
                return 0
            index_node = next_node
        index_node.insert(key=key)
        while not index_node.check_status(m=self.M):
            key, node = index_node.split_keys()
            if index_path:
                father_node = index_path.pop()
                father_node.insert(key=key, node=node)
                index_node = father_node
            else:
                new_root = BTreeNode(keys=[key], nodes=[index_node, node])
                self.root = new_root
                break
        return 1


if __name__ == "__main__":
    b = BTree(m=5)
    for i in range(100):
        b.insert(key=i)
    b.root.show_m_nodes(file_name="B-树")

