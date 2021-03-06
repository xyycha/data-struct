from graphviz import Digraph


class Node(object):
    def __init__(self, key=None, keys=None, nodes=None):
        self.key = key
        self.left = None
        self.right = None
        self.key_list = keys
        self.next_nodes = nodes

    def print_node(self, father_name, d=None):
        node_name = str(id(self))
        d.node(name=node_name, label=str(self.key))
        if father_name is not None:
            d.edge(father_name, node_name)
        if self.left is not None:
            self.left.print_node(node_name, d)
        if self.right is not None:
            self.right.print_node(node_name, d)

    def print_m_nodes(self, father_name, d=None):
        node_name = str(id(self))
        label = " ".join([str(key) for key in self.key_list])
        d.node(name=node_name, label=label)
        if father_name is not None:
            d.edge(father_name, node_name)
        for node in self.next_nodes:
            node.print_m_nodes(node_name, d)

    def show(self, file_name):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        self.print_node(father_name=None, d=d)
        d.view()

    def show_m_nodes(self, file_name):
        d = Digraph(filename=file_name, directory="./pdf_data")
        d.clear()
        self.print_m_nodes(father_name=None, d=d)
        d.view()
