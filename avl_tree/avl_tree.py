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
        insert_path = insert_path[::-1]
        for index, node in enumerate(insert_path):
            node.refresh_height()
            if index == 0:
                continue
            if node.height < 2:
                continue
            elif node.left is not None and node.right is not None and abs(node.left.height - node.right.height) <= 1:
                continue
            if node.left == insert_path[index - 1] and key < insert_path[index - 1].key:
                node.left_rotate()
            elif node.left == insert_path[index - 1]:
                insert_path[index - 1].right_rotate()
                node.left_rotate()
            elif key > insert_path[index - 1].key:
                node.right_rotate()
            else:
                insert_path[index - 1].left_rotate()
                node.right_rotate()
        return 1


avl = AVLTree(root=None)
elements = [5, 2, 12, 1, 4, 7, 3, 6, 10]
for element in elements:
    avl.insert(key=element)

