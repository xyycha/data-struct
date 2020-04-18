# -*- encoding: utf-8 -*-
from binary_trees.avl_tree.avl_tree import AVLTreeNode


"""
借助 AVL树节点的旋转操作
"""


class SplayTree(object):
    def __init__(self, root):
        self.root = root

    def insert(self, key):
        """
        插入 新节点
        :param key: 节点值
        :return: 插入成功：1   已存在：0
        """
        # 根节点为空
        if self.root is None:
            new_node = AVLTreeNode(key=key)
            self.root = new_node
            return 1
        # 遍历 二叉搜索树
        index_node = self.root
        while True:
            # 位于 右子树
            if key > index_node.key:
                # 右子树 为空
                if index_node.right is None:
                    index_node.right = AVLTreeNode(key=key)
                    return 1
                # 右子树 不为空  迭代
                index_node = index_node.right
            # 左子树 判断同右子树
            elif key < index_node.key:
                if index_node.left is None:
                    index_node.left = AVLTreeNode(key=key)
                    return 1
                index_node = index_node.left
            # 节点即为 插入节点
            else:
                return 0

    def find(self, key):
        search_path = []
        index_node = self.root
        while index_node is not None:
            search_path.append(index_node)
            if key == index_node.key:
                break
            elif key < index_node.key:
                index_node = index_node.left
            else:
                index_node = index_node.right
        # 未找到 该节点
        if index_node is None:
            return -1
        while len(search_path) > 0:
            if len(search_path) == 1:
                self.root = search_path[0]
                return search_path[0]
            elif len(search_path) == 2:
                node = search_path.pop()
                father_node = search_path.pop()
                if father_node.left == node:
                    father_node.left_rotate()
                else:
                    father_node.right_rotate()
                search_path.append(father_node)
            else:
                node = search_path.pop()
                father_node = search_path.pop()
                grand_father_node = search_path.pop()
                if grand_father_node.left == father_node and father_node.right == node:
                    father_node.right_rotate()
                    grand_father_node.left_rotate()
                elif grand_father_node.left == father_node:
                    grand_father_node.left_rotate()
                    # 父节点 祖父节点已经交换
                    grand_father_node.left_rotate()
                elif father_node.left == node:
                    father_node.left_rotate()
                    grand_father_node.right_rotate()
                else:
                    grand_father_node.right_rotate()
                    # 父节点 祖父节点已经交换
                    grand_father_node.right_rotate()
                search_path.append(grand_father_node)


if __name__ == "__main__":
    s = SplayTree(root=None)
    elements = [i for i in range(7, 0, -1)]
    for element in elements:
        s.insert(key=element)
    s.root.show(file_name="伸展树初始")
    s.find(key=1)
    s.root.show(file_name="伸展树调整")
