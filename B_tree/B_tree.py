# -*- encoding: utf-8 -*-
import math

from tree_to_pdf.print_tree import Node


def move_element_between_brother(father_node, src_index, des_index):
    if des_index < src_index:
        # 从本节点开始 与 父节点 交换关键字  父节点与 本节点的兄弟节点交换关键字
        # 本节点的 子节点的 第一个节点  添加到  其兄弟节点的 子节点的最后
        for step in range(src_index - des_index):
            node = father_node.next_nodes[src_index - step]
            move_key = node.key_list.pop(0)
            move_node = None
            if node.next_nodes:
                move_node = node.next_nodes.pop(0)
            father_old_key = father_node.key_list[src_index - step - 1]
            father_node.key_list[src_index - step - 1] = move_key
            front_node = father_node.next_nodes[src_index - step - 1]
            front_node.key_list.append(father_old_key)
            if move_node:
                front_node.next_nodes.append(move_node)
    # 是本节点 右边的兄弟节点
    # 具体类似 左边的兄弟节点
    else:
        for step in range(des_index - src_index):
            node = father_node.next_nodes[src_index + step]
            move_key = node.key_list.pop()
            move_node = None
            if node.next_nodes:
                move_node = node.next_nodes.pop()
            father_old_key = father_node.key_list[src_index + step]
            father_node.key_list[src_index + step] = move_key
            post_node = father_node.next_nodes[src_index + step + 1]
            post_node.key_list.insert(0, father_old_key)
            if move_node:
                post_node.next_nodes.insert(0, move_node)


def find_nearest_true(status_list, index):
    target_index = index
    for distance in range(1, max(index + 1, len(status_list) - index)):
        left_index = max(index - distance, 0)
        right_index = min(index + distance, len(status_list) - 1)
        if status_list[left_index]:
            target_index = left_index
            break
        elif status_list[right_index]:
            target_index = right_index
            break
    return target_index


def merge_node(father_node, index, m, root):
    left_son = father_node.next_nodes.pop(index)
    right_son = father_node.next_nodes.pop(index)
    keys = left_son.key_list + right_son.key_list
    nodes = left_son.next_nodes + right_son.next_nodes
    new_node = BTreeNode(keys=keys, nodes=nodes)
    father_node.next_nodes.insert(index, new_node)
    if new_node.next_nodes:
        second_index = len(left_son.key_list)
        merge_node(father_node=new_node, index=second_index, m=m, root=root)
    if not new_node.check_top_status(m=m):
        new_key, new_right_node = new_node.split_keys()
        father_node.key_list.insert(index, new_key)
        father_node.next_nodes.insert(index + 1, new_right_node)
        print("1")
    elif father_node == root and len(father_node.key_list) == 0:
        root.key_list = new_node.key_list
        root.next_nodes = new_node.next_nodes


class BTreeNode(Node):
    def __init__(self, keys: list, nodes: list):
        super(BTreeNode, self).__init__(keys=keys, nodes=nodes)

    def get_next_node(self, key):
        if key in self.key_list:
            return self
        if not self.next_nodes:
            return None
        for index, value in enumerate(self.key_list):
            if key < value:
                return self.next_nodes[index]
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

    def check_top_status(self, m):
        if len(self.key_list) >= m:
            return False
        return True

    def check_floor_status(self, m):
        if len(self.key_list) <= math.ceil(m / 2) - 2:
            return False
        return True

    def check_floor_status_for_root(self):
        if len(self.key_list) < 1:
            return False
        return True

    def check_insert(self, m):
        if len(self.key_list) < m - 1:
            return True
        return False

    def check_delete(self, m):
        if len(self.key_list) > math.ceil(m / 2) - 1:
            return True
        return False

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
        while not index_node.check_top_status(m=self.M):
            # 存在父节点
            if index_path:
                father_node = index_path.pop()
                # 找到父节点到本节点的路径
                index = father_node.next_nodes.index(index_node)
                # 检查兄弟节点是否可以 插入
                brother_nodes_status = [node.check_insert(m=self.M)for node in father_node.next_nodes]
                # 兄弟节点 可以 插入
                if any(brother_nodes_status):
                    # 寻找 到本节点 最近的 可插入兄弟节点
                    target_index = find_nearest_true(status_list=brother_nodes_status, index=index)
                    move_element_between_brother(father_node=father_node, src_index=index, des_index=target_index)
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

    def delete(self, key):
        index_node = self.root
        if index_node is None:
            return -1
        index_path = []
        while index_node:
            next_node = index_node.get_next_node(key=key)
            # 该值在 节点 中
            if next_node == index_node:
                break
            elif not next_node:
                return 0
            else:
                index_path.append(index_node)
                index_node = next_node
        # 删除 关键字
        delete_index = index_node.key_list.index(key)
        index_node.key_list.pop(delete_index)
        # 删除非叶子节点 关键字
        if index_node.next_nodes:
            merge_node(father_node=index_node, index=delete_index, m=self.M, root=self.root)

        while not index_node.check_floor_status(m=self.M):
            if (not index_path) and not index_node.check_floor_status_for_root():
                assert len(self.root.next_nodes) == 1, "迭代有问题，根节点的子节点树不是1"
                self.root = self.root.next_nodes[0]
                break
            if not index_path:
                break
            father_node = index_path.pop()
            index = father_node.next_nodes.index(index_node)
            brother_nodes_status = [node.check_delete(m=self.M) for node in father_node.next_nodes]
            if any(brother_nodes_status):
                # 存在 兄弟节点可以 提供一个 关键字
                target_index = find_nearest_true(status_list=brother_nodes_status, index=index)
                move_element_between_brother(father_node=father_node, src_index=target_index, des_index=index)
                break
            else:
                # 合并 临近的 兄弟节点
                length = len(brother_nodes_status)
                new_key = father_node.key_list.pop(index) if index != length - 1 else father_node.key_list.pop()
                old_left_node = father_node.next_nodes.pop(index) if index != length - 1 else father_node.next_nodes.pop()
                old_right_node = father_node.next_nodes.pop(index) if index != length - 1 else father_node.next_nodes.pop()
                keys = old_left_node.key_list + [new_key] + old_right_node.key_list
                new_node = BTreeNode(keys=keys, nodes=[])
                father_node.next_nodes[index] = new_node
                index_node = father_node
        return 1


if __name__ == "__main__":
    b = BTree(m=5)
    for i in range(50):
        b.insert(key=i)
    b.root.show_m_nodes(file_name="B-树")
    b.delete(24)
    b.root.show_m_nodes(file_name="删除24")
    b.delete(39)
    b.root.show_m_nodes(file_name="删除39")
    b.delete(14)
    b.root.show_m_nodes(file_name="删除14")
    b.delete(34)
    b.root.show_m_nodes(file_name="删除34")
