# -*- encoding: utf-8 -*-


class AVLTreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0
        # 计数器
        self.flag = 1

    def refresh_height(self):
        if self is None:
            self.height = -1
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
        if self.root is None:
            self.root = AVLTreeNode(key=key)
            return 1
        insert_path = []
        index_node = self.root
        while index_node is not None:
            insert_path.append(index_node)
            if key < index_node.key:
                index_node = index_node.left
            elif key > index_node.key:
                index_node = index_node.right
            else:
                return 0
        if key > insert_path[-1].key:
            insert_path[-1].right = AVLTreeNode(key=key)
        else:
            insert_path[-1].left = AVLTreeNode(key=key)
        for node in insert_path[:-1:-1]:
            pass
