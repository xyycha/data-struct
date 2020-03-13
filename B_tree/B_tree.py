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
        if len(self.key_list) >= m:
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
        # 判断是否在叶子节点
        if key in index_node.key_list:
            return 0
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

    def new_insert(self, key):
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
        # 判断是否在叶子节点
        if key in index_node.key_list:
            return 0
        index_node.insert(key=key)
        while not index_node.check_status(m=self.M):
            # 存在父节点
            if index_path:
                father_node = index_path.pop()
                # 找到父节点到本节点的路径
                index = father_node.next_nodes.index(index_node)
                # 检查兄弟节点是否可以 插入
                brother_nodes_status = [node.check_status(m=self.M - 1)for node in father_node.next_nodes]
                # 兄弟节点 可以 插入
                if any(brother_nodes_status):
                    # 寻找 到本节点 最近的 可插入兄弟节点
                    left_index = right_index = index
                    for i in range(1, max(index + 1, len(father_node.next_nodes) - index)):
                        left_index = max(index - i, 0)
                        right_index = min(index + i, len(father_node.next_nodes) - 1)
                        if brother_nodes_status[left_index] or brother_nodes_status[right_index]:
                            break
                    # 是 本节点的 左边的兄弟节点
                    if brother_nodes_status[left_index]:
                        # 从本节点开始 与 父节点 交换关键字  父节点与 本节点的兄弟节点交换关键字
                        # 本节点的 子节点的 第一个节点  添加到  其兄弟节点的 子节点的最后
                        for step in range(index - left_index):
                            node = father_node.next_nodes[index - step]
                            move_key = node.key_list.pop(0)
                            move_node = None
                            if node.next_nodes:
                                move_node = node.next_nodes.pop(0)
                            father_old_key = father_node.key_list[index - step - 1]
                            father_node.key_list[index - step - 1] = move_key
                            front_node = father_node.next_nodes[index - step - 1]
                            front_node.key_list.append(father_old_key)
                            if move_node:
                                front_node.next_nodes.append(move_node)
                    # 是本节点 右边的兄弟节点
                    # 具体类似 左边的兄弟节点
                    else:
                        for step in range(right_index - index):
                            node = father_node.next_nodes[index + step]
                            move_key = node.key_list.pop()
                            move_node = None
                            if node.next_nodes:
                                move_node = node.next_nodes.pop()
                            father_old_key = father_node.key_list[index + step]
                            father_node.key_list[index + step] = move_key
                            post_node = father_node.next_nodes[index + step + 1]
                            post_node.key_list.insert(0, father_old_key)
                            if move_node:
                                post_node.next_nodes.insert(0, move_node)
                    return 1
                # 兄弟节点 都不在允许插入
                # 需要分解 该节点
                key, node = index_node.split_keys()
                father_node.insert(key=key, node=node)
                index_node = father_node
            # 没有父节点 创建新的根节点
            else:
                key, node = index_node.split_keys()
                new_root = BTreeNode(keys=[key], nodes=[index_node, node])
                self.root = new_root
                break
        return 1


if __name__ == "__main__":
    b = BTree(m=5)
    for i in range(20):
        b.insert(key=i)
    b.root.show_m_nodes(file_name="B-树 初始版")
    b = BTree(m=5)
    for i in range(20):
        b.new_insert(key=i)
    b.root.show_m_nodes(file_name="B-树 修改版")

