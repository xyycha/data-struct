# -*- encoding: utf-8 -*-


"""
根据二叉树遍历结果 构建二叉树
前序表达式 pop 第一个作为 父节点 左节点在前所以先 建立左子树   父左右
后序表达式 pop 最后一个作为父节点 右节点在前所以先 建立右子树  左右父
"""
from binary_trees.binary_tree.binary_tree_traversal import BinaryTree


class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def pre_in_order_to_binary_tree(pre_order: list, in_order: list):
    key = pre_order.pop(0)
    if len(in_order) == 1:
        return Node(key=in_order[0])
    node = Node(key=key)
    index = in_order.index(key)
    left_son_in_order = in_order[:index]
    right_son_in_order = in_order[index + 1:]
    if left_son_in_order:
        left_son = pre_in_order_to_binary_tree(pre_order=pre_order, in_order=left_son_in_order)
        node.left = left_son
    if right_son_in_order:
        right_son = pre_in_order_to_binary_tree(pre_order=pre_order, in_order=right_son_in_order)
        node.right = right_son
    return node


def post_in_order_to_binary_tree(post_order: list, in_order: list):
    key = post_order.pop()
    if len(in_order) == 1:
        return Node(key=in_order[0])
    node = Node(key=key)
    index = in_order.index(key)
    left_son_in_order = in_order[:index]
    right_son_in_order = in_order[index + 1:]
    if right_son_in_order:
        right_son = post_in_order_to_binary_tree(post_order=post_order, in_order=right_son_in_order)
        node.right = right_son
    if left_son_in_order:
        left_son = post_in_order_to_binary_tree(post_order=post_order, in_order=left_son_in_order)
        node.left = left_son
    return node


if __name__ == "__main__":
    pre_order = "1 2 4 8 9 5 10 3 6 7".split(" ")
    in_order = "8 4 9 2 10 5 1 6 3 7".split(" ")
    post_order = "8 9 4 10 5 2 6 7 3 1".split(" ")
    root = pre_in_order_to_binary_tree(pre_order=pre_order, in_order=in_order)
    binary_tree = BinaryTree(root=root)
    binary_tree.pre_order()
    binary_tree.in_order()
    binary_tree.post_order()
    root = post_in_order_to_binary_tree(post_order=post_order, in_order=in_order)
    binary_tree = BinaryTree(root=root)
    binary_tree.pre_order()
    binary_tree.in_order()
    binary_tree.post_order()
