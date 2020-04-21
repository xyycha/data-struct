# -*- encoding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from graph_without_direction import graph_without_direction


def min_span_tree_by_prim():
    graph_without_direction.min_span_tree_by_prim()


def min_span_tree_by_kruskal():
    graph_without_direction.min_span_tree_by_kruskal()


if __name__ == "__main__":
    min_span_tree_by_prim()
