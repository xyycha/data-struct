# -*- encoding: utf-8 -*-


"""
实现二叉树的 前序 中序 后序 遍历
"""


class BinaryTreeNode(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right


class BinaryTree(object):
    def __init__(self, root):
        self._root = root

    def pre_order(self):
        print("前序遍历为")
        self._pre_order(node=self._root)
        print("\n")

    def _pre_order(self, node):
        if node is not None:
            print(node.key, end=" ")
            self._pre_order(node.left)
            self._pre_order(node.right)

    def in_order(self):
        print("中序遍历为")
        self._in_order(node=self._root)
        print("\n")

    def _in_order(self, node):
        if node is not None:
            self._in_order(node.left)
            print(node.key, end=" ")
            self._in_order(node.right)

    def post_order(self):
        print("后序遍历为")
        self._post_order(node=self._root)
        print("\n")

    def _post_order(self, node):
        if node is not None:
            self._post_order(node.left)
            self._post_order(node.right)
            print(node.key, end=" ")


if __name__ == "__main__":
    nodes = [BinaryTreeNode(key=i) for i in range(1, 11, 1)]
    for i in range(1, 6, 1):
        nodes[i - 1].left = nodes[2 * i - 1] if 2 * i <= len(nodes) else None
        nodes[i - 1].right = nodes[2 * i] if 2 * i <= len(nodes) - 1 else None
    root = nodes[0]
    binary_tree = BinaryTree(root=root)
    binary_tree.pre_order()
    binary_tree.in_order()
    binary_tree.post_order()
    print("\n")
