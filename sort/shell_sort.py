# -*- encoding: utf-8 -*-
from sort.base import Sort
"""
希尔排序的问题：相邻的希尔增量可能会存在公因子，导致不能进一步排序
当数组的个数为2 ** n，奇数列和偶数列的两个递增序列 且 奇数列的值小于偶数列的值
例子： 1, 5, 2, 6, 3, 7, 4, 8

step = 4
1 3 
5 7
2 4
6 8
无变化
 
step = 2
1 2 3 4
5 6 7 8
无变化

step = 1
退化为  插入排序

改进 Hibbard 增量  2 ** k - 1  (1, 3, 7 ... )
"""


class ShellSort(Sort):
    def __init__(self, info, copy):
        super(ShellSort, self).__init__(info=info, copy=copy)

    def length(self) -> int:
        return len(self._info)

    def less(self, info_i, info_j) -> bool:
        if info_i <= info_j:
            return True
        return False

    def swap(self, i, j):
        self._info[i], self._info[j] = self._info[j], self._info[i]

    def sort(self):
        step = self._length // 2
        while step > 0:
            for i in range(step, self._length):
                temp = self._info[i]
                j = i
                while j >= step:
                    if self.less(temp, self._info[j - step]):
                        self.swap(j, j - step)
                        j -= step
                    else:
                        break
                self._info[j] = temp
            step //= 2


class DictListShellSort(ShellSort):
    def __init__(self, info, copy, key):
        super(DictListShellSort, self).__init__(info=info, copy=copy)
        self._sort_key = key

    def less(self, info_i, info_j) -> bool:
        if info_i.get(self._sort_key) <= info_j.get(self._sort_key):
            return True
        return False


if __name__ == "__main__":
    import random

    print("*******测试1*******")
    s = []
    for nums in range(20):
        s.append(random.randint(0, 100))
    shell_sort = ShellSort(info=s, copy=True)
    shell_sort.sort()
    res = shell_sort.show()
    print(s)
    print(res)
    if sorted(s) == res:
        print("Success")
    else:
        print("Fail")

    print("*******测试2*******")
    s = []
    for nums in range(20):
        s.append(dict(test=random.randint(0, 100)))
    dict_list_shell_sort = DictListShellSort(info=s, copy=True, key="test")
    dict_list_shell_sort.sort()
    res = dict_list_shell_sort.show()
    print(s)
    print(res)
