from graphviz import Digraph


def accumulator():
    i = [0]

    def accumulate():
        i[0] += 1
        return str(i[0])
    return accumulate


s = accumulator()


class Node(object):
    def __init__(self, key):
        self.name = s()
        self.key = key
        self.left = None
        self.right = None


def print_node(d, father: str or None, node: Node):
    if node is None:
        return
    d.node(name=node.name, label=str(node.key))
    if father is not None:
        d.edge(father, node.name)
    print_node(d, node.name, node.left)
    print_node(d, node.name, node.right)


def show(d):
    d.view()


def reset(d):
    d.clear()


def show_binary_tree(file_name: str, root: Node):
    d = Digraph(filename=file_name, directory="./pdf_data")
    print_node(d=d, father=None, node=root)
    d.view()
