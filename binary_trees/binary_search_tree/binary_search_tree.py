# -*- encoding: utf-8 -*-
from tree_to_pdf.print_tree import Node


class BinarySearchTree(object):
    def __init__(self, root: Node = None):
        """
        初始化 二叉搜索树
        :param root: 根节点 默认为None
        """
        self.root = root

    def insert(self, key):
        """
        插入 新节点
        :param key: 节点值
        :return: 插入成功：1   已存在：0
        """
        # 根节点为空
        if self.root is None:
            new_node = Node(key=key)
            self.root = new_node
            return 1
        # 遍历 二叉搜索树
        index_node = self.root
        while True:
            # 位于 右子树
            if key > index_node.key:
                # 右子树 为空
                if index_node.right is None:
                    index_node.right = Node(key=key)
                    return 1
                # 右子树 不为空  迭代
                index_node = index_node.right
            # 左子树 判断同右子树
            elif key < index_node.key:
                if index_node.left is None:
                    index_node.left = Node(key=key)
                    return 1
                index_node = index_node.left
            # 节点即为 插入节点
            else:
                return 0

    def find(self, key):
        """
        查询节点
        :param key: 节点值
        :return: 节点
        """
        node = self._find(key=key, pre=False)
        return node

    def _find(self, key, pre: bool):
        """
        查询 节点
        :param key: 节点值
        :param pre: 是否需要父节点
        :return: 查询成功: 节点   不存在：None
        """
        pre_node = None
        index_node = self.root
        while index_node is not None:
            if key > index_node.key:
                pre_node = index_node
                index_node = index_node.right
            elif key < index_node.key:
                pre_node = index_node
                index_node = index_node.left
            else:
                return pre_node, index_node if pre else index_node
        return pre_node, None if pre else None

    def delete(self, key):
        """
        删除节点
        :param key: 节点值
        :return: 删除成功：1   不存在 0
        """
        pre_node, target_node = self._find(key=key, pre=True)
        if target_node is None:
            # 未找到节点
            return 0
        if target_node.left is None and target_node.right is not None:
            # 单子树节点  使用子节点代替 父节点 即可
            if pre_node is None:
                self.root = target_node.right
            elif pre_node.left == target_node:
                pre_node.left = target_node.right
            else:
                pre_node.right = target_node.right
            # or
            # temp = target_node.right
            # target_node.key = temp.key
            # target_node.left = temp.left
            # target_node.right = temp.right

            # or
            # target_node.left = target_node.right
            # target_node.key = target_node.right.key
            # target_node.right = target_node.right.right
            # target_node.left = target_node.left.left
        elif target_node.right is None and target_node.left is not None:
            # 单子树节点  使用子节点代替 父节点 即可
            if pre_node is None:
                self.root = target_node.left
            elif pre_node.left == target_node:
                pre_node.left = target_node.left
            else:
                pre_node.right = target_node.left
        elif target_node.right is not None and target_node.left is not None:
            # 存在 左右 子树时  寻找右子树的最左节点
            pre_replace_node, replace_node = self.right_son_most_left_node(target_node)
            target_node.key = replace_node.key
            if pre_replace_node.left == replace_node:
                pre_replace_node.left = replace_node.right
            else:
                pre_replace_node.right = replace_node.right
        else:
            # 删除叶子节点  需要设置父节点的子节点为None
            if pre_node.left == target_node:
                pre_node.left = None
            else:
                pre_node.right = None
        return 1

    def right_son_most_left_node(self, node: Node) -> (Node, Node):
        """
        返回该节点的 右子树上面的最左节点 及其 父节点
        :param node: 寻找 右子树的最左节点 的 节点
        :return: 右子树的最左节点及其 父节点
        """
        pre_node = node
        index_node = node.right
        while index_node.left is not None:
            pre_node = index_node
            index_node = index_node.left
        return pre_node, index_node


def test1():
    s = BinarySearchTree()
    s.insert(5)
    s.insert(3)
    s.insert(1)
    s.insert(4)
    s.insert(7)
    s.insert(6)
    s.insert(9)
    s.insert(8)
    s.insert(2)
    s.root.show("初始")

    s.delete(5)
    s.root.show("删除节点 5")

    s.delete(7)
    s.root.show("删除节点 7")

    s.insert(7)
    s.root.show("插入节点 7")

    s.insert(5)
    s.root.show("插入节点 5")


def test2():
    s = BinarySearchTree()
    s.insert(5)
    s.insert(4)
    s.insert(3)
    s.insert(2)
    s.insert(1)

    s.delete(5)
    s.root.show("单左树测试")


if __name__ == "__main__":
    test1()
    test2()
