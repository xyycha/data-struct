# -*- encoding: utf-8 -*-
"""
分治排序 思路：递归 将两个排序完成的 数组进行合并
1. 递归到数组长度 为1 此时数组排序完成(长度为1 的数组是有序的)
2. 开始合并 排好序的左右两个数组
3. 返回排序好的结果
"""


def merge_sort(nums):
    length = len(nums)
    if length == 1:
        return nums
    mid = length // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    new_nums = []
    left_index, right_index = 0, 0
    while left_index < mid and right_index < length - mid:
        if left[left_index] <= right[right_index]:
            new_nums.append(left[left_index])
            left_index += 1
        else:
            new_nums.append(right[right_index])
            right_index += 1
    new_nums.extend(left[left_index:])
    new_nums.extend(right[right_index:])
    return new_nums


if __name__ == "__main__":
    import random

    s = []
    for i in range(20):
        s.append(random.randint(0, 100))
    print(s)
    res = merge_sort(s)
    print(res)
