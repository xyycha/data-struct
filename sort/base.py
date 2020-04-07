# -*- encoding: utf-8 -*-
from copy import deepcopy


class Sort(object):
    def __init__(self, info, copy: bool = False):
        """
        初始化参数
        :param info: 待排序的对象
        :param copy: 是否深拷贝(是否原地排序)
        """
        self._info = info if not copy else deepcopy(info)
        self._length = self.length()

    def length(self) -> int:
        """
        返回长度
        :return: 长度
        """
        pass

    def less(self, info_i, info_j) -> bool:
        """
        返回比较结果
        :param info_i: 第 i 个元素
        :param info_j: 第 j 个元素
        :return: 比较结果
        """
        pass

    def swap(self, i, j) -> None:
        """
        交换操作
        :param i: 第 i 个元素
        :param j: 第 j 个元素
        :return: None
        """
        pass

    def sort(self) -> None:
        """
        进行排序
        :return: None
        """
        pass

    def show(self) -> object:
        """
        返回排序结果
        :return: 排序结果
        """
        return self._info
