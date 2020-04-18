# -*- encoding: utf-8 -*-
from tree_to_pdf.print_tree import Node


class AVLTreeNode(Node):
    def __init__(self, key):
        super(AVLTreeNode, self).__init__(key=key)
        self.key = key
        self.left = None
        self.right = None
        self.height = 0
        # 计数器
        self.flag = 1

    def refresh_height(self):
        if self.left is None and self.right is None:
            self.height = 0
        elif self.left is None:
            self.height = self.right.height + 1
        elif self.right is None:
            self.height = self.left.height + 1
        else:
            self.height = max(self.left.height, self.right.height) + 1

    def left_rotate(self):
        temp_key = self.key
        temp_node = self.right

        # 左旋
        self.key = self.left.key
        self.right = self.left
        self.left = self.right.left
        self.right.key = temp_key
        self.right.left = self.right.right
        self.right.right = temp_node
        self.right.refresh_height()
        self.refresh_height()

    def right_rotate(self):
        temp_key = self.key
        temp_node = self.left

        # 右旋
        self.key = self.right.key
        self.left = self.right
        self.right = self.left.right
        self.left.key = temp_key
        self.left.right = self.left.left
        self.left.left = temp_node
        self.left.refresh_height()
        self.refresh_height()


class AVLTree(object):
    def __init__(self, root):
        self.root = root

    def insert(self, key):
        # 树为空, 新建节点，根为新建节点
        if self.root is None:
            self.root = AVLTreeNode(key=key)
            return 1
        # 记录插入的节点路径  需要校核路径上的平衡
        insert_path = []
        index_node = self.root
        while index_node is not None:
            insert_path.append(index_node)
            # 左子树寻找
            if key < index_node.key:
                index_node = index_node.left
            # 右子树寻找
            elif key > index_node.key:
                index_node = index_node.right
            # 已存在  直接返回
            else:
                return 0
        # 进行插入 操作
        if key > insert_path[-1].key:
            insert_path[-1].right = AVLTreeNode(key=key)
        else:
            insert_path[-1].left = AVLTreeNode(key=key)
        # 倒叙 校核节点的平衡性
        insert_path = insert_path[::-1]
        for index, node in enumerate(insert_path):
            # 记录原始高度
            old_height = node.height
            # 进行了插入动作，重新计算高度
            node.refresh_height()
            # 如果插入动作不再改变节点的高度 停止遍历
            if old_height == node.height:
                break
            # 高度小于2的节点 不需要校核平衡
            if node.height < 2:
                continue
            # 高度 大于等于2的节点 在 左右子树存在 且 高度差小于2 的情况下 不需要校核平衡
            elif node.left is not None and node.right is not None and abs(node.left.height - node.right.height) < 2:
                continue
            # 不满足上面条件的需要校核平衡
            # 节点的左节点的左子树进行了插入
            if node.left == insert_path[index - 1] and key < insert_path[index - 1].key:
                node.left_rotate()
            # 节点的左节点的右子树进行了插入
            elif node.left == insert_path[index - 1]:
                insert_path[index - 1].right_rotate()
                node.left_rotate()
            # 节点的右节点的右子树进行了插入
            elif key > insert_path[index - 1].key:
                node.right_rotate()
            # 节点的右节点的左子树进行了插入
            else:
                insert_path[index - 1].left_rotate()
                node.right_rotate()
            # 已找到第一个失去平衡的节点并调整完毕 停止遍历
            break
        return 1

    def delete(self, key):
        index_node = self.root
        while index_node is not None:
            if key < index_node.key:
                index_node = index_node.left
            elif key > index_node.key:
                index_node = index_node.right
            elif index_node.flag == 1:
                index_node.flag = 0
                return 1
            else:
                return 0
        return -1

    def find(self, key):
        index_node = self.root
        while index_node is not None:
            if key < index_node.key:
                index_node = index_node.left
            elif key > index_node.key:
                index_node = index_node.right
            elif index_node.flag == 1:
                return index_node
            else:
                break
        return None


if __name__ == "__main__":
    avl = AVLTree(root=None)
    elements = [5, 2, 12, 1, 4, 7, 3, 6, 10]
    for element in elements:
        avl.insert(key=element)
    root = avl.root
    if root is not None:
        root.show(file_name="AVL 插入")
