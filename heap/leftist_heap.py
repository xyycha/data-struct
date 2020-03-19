# -*- encoding: utf-8 -*-
import random

from tree_to_pdf.print_tree import Node


def swap_leftist_heap_node(node1, node2):
    temp_key = node1.key
    temp_left = node1.left
    temp_right = node1.right
    temp_npl = node1.npl
    node1.key = node2.key
    node1.left = node2.left
    node1.right = node2.right
    node1.npl = node2.npl
    node2.key = temp_key
    node2.left = temp_left
    node2.right = temp_right
    node2.npl = temp_npl


def merge(node1, heap_root):
    if heap_root is None:
        node1.refresh_npl()
        return
    if node1.key > heap_root.key:
        swap_leftist_heap_node(node1=node1, node2=heap_root)
    if node1.right is not None:
        merge(node1=node1.right, heap_root=heap_root)
    else:
        node1.right = heap_root
    node1.refresh_npl()


class LeftistHeapNode(Node):
    def __init__(self, key):
        super(LeftistHeapNode, self).__init__(key=key)
        self.key = key
        self.left = None
        self.right = None
        self.npl = 0

    def refresh_npl(self):
        if self.left is None or self.right is None:
            self.npl = 0
        else:
            self.npl = min(self.left.npl, self.right.npl) + 1


class LeftistHeap(object):
    def __init__(self):
        self.root = None

    def merge(self, heap_root):
        if self.root is None:
            self.root = heap_root
            return
        merge(node1=self.root, heap_root=heap_root)

    def insert(self, key):
        node = LeftistHeapNode(key=key)
        if self.root is None:
            self.root = node
        else:
            merge(node1=self.root, heap_root=node)
        if self.root.left is None or self.root.right is None:
            old_right = self.root.right
            self.root.right = None
            self.root.left = old_right if old_right is not None else self.root.left
        elif self.root.left.npl < self.root.right.npl:
            old_right = self.root.right
            self.root.right = self.root.left
            self.root.left = old_right

    def pop(self):
        if self.root is None:
            return None
        root = self.root
        if self.root.left is None:
            self.root = self.root.right
        elif self.root.right is None:
            self.root = self.root.left
        else:
            right_tree = self.root.right
            self.root = self.root.left
            merge(node1=self.root, heap_root=right_tree)
            if self.root.left.npl < self.root.right.npl:
                old_right = self.root.right
                self.root.right = self.root.left
                self.root.left = old_right
        return root


if __name__ == "__main__":
    leftist_heap = LeftistHeap()
    for i in range(10):
        key = random.randint(0, 100)
        print(key, end=" ")
        leftist_heap.insert(key=key)
    root = leftist_heap.root
    if root is not None:
        root.show(file_name="初始左式堆")
    print("end")
