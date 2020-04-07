# -*- encoding: utf-8 -*-
"""
快速排序 思路：
1. 选中基数  小于等于基数的放到 左边  大于基数的放到右边
2. 迭代第一步 直到数组长度为1
3. 返回 排好序的数组
"""


def find_core(nums):
    """
    优化 枢纽元的 选取
    两个元素  选取 最后一个
    三个元素及以上  选取 首 尾 中间 三个元素的中间值 作为 枢纽元
    :param nums: 数组
    :return: 枢纽元的 下标
    """
    length = len(nums)
    if length == 2:
        return length - 1
    first_num = nums[0]
    last_num = nums[-1]
    mid_num = nums[length // 2]
    res = (first_num >= mid_num) + 2 * (mid_num >= last_num) + 4 * (first_num >= last_num)
    if res == 1 or res == 6:
        return 0
    if res == 2 or res == 5:
        return length - 1
    return length // 2


def split_nums(nums, core):
    """
    优化 数组的分割策略:
        1. 将枢纽元与尾部元素互换位置
        2. 左侧下标 从第一个元素开始与 枢纽元进行比较
        3. 如果小于 枢纽元  左侧下标 + 1
        4. 如果大于 枢纽元 右侧下标在倒数第二个元素开始寻找 小于枢纽元的元素 满足 进行交换左右下标对应的元素。不管满足不满足 右侧下标 - 1
        5. 直到左侧下标大于右侧下标
        6. 交换左侧下标的元素 和 尾部元素
        7. 左侧下标 之前的元素 为 左子集  左侧下标对应的元素 记为 枢纽元  左侧下标 之后的元素为 右子集
    根据枢纽元的下标拆分 数组
    :param nums: 数组
    :param core: 枢纽元下标
    :return: 左右两个数组
    """
    nums[core], nums[-1] = nums[-1], nums[core]
    left_index = 0
    right_index = len(nums) - 2
    while left_index <= right_index:
        if nums[left_index] <= nums[-1]:
            left_index += 1
        elif nums[right_index] <= nums[-1]:
            nums[left_index], nums[right_index] = nums[right_index], nums[left_index]
            left_index += 1
            right_index -= 1
        else:
            right_index -= 1
    nums[left_index], nums[-1] = nums[-1], nums[left_index]
    return nums[:left_index], nums[left_index + 1:]


def quick_sort(nums):
    length = len(nums)
    if length == 1 or length == 0:
        return nums
    core = find_core(nums=nums)
    mid_nums = nums[core]
    left, right = split_nums(nums=nums, core=core)
    new_left = quick_sort(left)
    new_right = quick_sort(right)
    new_nums = new_left + [mid_nums] + new_right
    return new_nums


if __name__ == "__main__":
    import random

    s = []
    for i in range(20):
        s.append(random.randint(0, 100))
    print(s)
    res = quick_sort(s)
    print(res)
