# -*- encoding: utf-8 -*-
from tree_to_pdf.print_tree import Node, show_binary_tree


__author__ = "xyy"
legal_operation = ("+", "-", "*", "/")
post_order_expression = "abc*+de*f+g*+"
pre_order_expression = "++a*bc*+*defg"


def post_order_to_binary_tree(post_order: str) -> None:
    """
    将 后续表达式 转化为 二叉树 并 绘制二叉树
    :param post_order: 后续表达式
    :return: None or Raise
    """
    variables = []
    for char in post_order:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            variable_node = Node(key=char)
            variables.append(variable_node)
        elif char in legal_operation:
            operation_node = Node(key=char)
            tip = "表达式在 %s 有问题" % char
            assert len(variables) > 1, tip
            operation_node.right = variables.pop()
            operation_node.left = variables.pop()
            variables.append(operation_node)
        else:
            tip = "字符 %s 不在范围内" % char
            assert False, tip
    assert len(variables) == 1, "表达式有问题"
    show_binary_tree("后缀表达式", variables[0])


def pre_order_to_binary_tree(pre_order: str) -> None:
    """
    将 前续表达式 转化为 二叉树 并 绘制二叉树
    :param pre_order: 前序表达式
    :return: None or Raise
    """
    root = _pre_order_to_binary_tree(pre_order=pre_order)
    show_binary_tree("前缀表达式", root)


def _pre_order_to_binary_tree(pre_order: str) -> Node:
    """
    将 前续表达式 转化为 二叉树 返回根节点
    :param pre_order: 前序表达式
    :return: 树的根节点
    """
    if len(pre_order) == 1:
        assert 'a' <= pre_order <= 'z' or 'A' <= pre_order <= 'Z', "前缀表达式不对"
        return Node(key=pre_order)
    operate = pre_order[0]
    assert operate in legal_operation, "前缀表达式不对"
    father_node = Node(key=operate)
    variable_num = 0
    operate_num = 0
    for char in pre_order[1:]:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            variable_num += 1
        elif char in legal_operation:
            operate_num += 1
        else:
            assert False, "非法字符"
        if variable_num - operate_num == 1:
            break
    assert variable_num - operate_num == 1, "前缀表达式不对"
    left_pre_order = pre_order[1: variable_num + operate_num + 1]
    father_node.left = _pre_order_to_binary_tree(left_pre_order)
    right_pre_order = pre_order[variable_num + operate_num + 1:]
    father_node.right = _pre_order_to_binary_tree(right_pre_order)
    return father_node


if __name__ == "__main__":
    post_order_to_binary_tree(post_order_expression)
    pre_order_to_binary_tree(pre_order_expression)
