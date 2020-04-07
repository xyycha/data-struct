# -*- encoding: utf-8 -*-
import math

"""
基数排序思路
1. 确定基数排序的次数
2. 初始化 基数桶的信息
2. 根据 基数 将每个 数 放到对应的桶内
3. 直到 基数排序的次数 最大值

s = [5, 24, 16, 7, 100]
基数选择10  最大基数排序次数 ceil(log(100, 10))  2
time = 0  base = 10 ** 0 = 1
buckets = [[], [], [], [], [], [], [], [], [], []]
buckets = [[100], [], [], [], [24], [5], [16], [7], [], []]
s = [100, 24, 5, 16, 7]

time = 1  base = 10 ** 1 = 10
buckets = [[], [], [], [], [], [], [], [], [], []]
buckets = [[5, 7, 100], [16], [24], [], [], [], [], [], [], []]
s = [5, 7, 100, 16, 24]

time = 2  base = 10 ** 2 = 100
buckets = [[], [], [], [], [], [], [], [], [], []]
buckets = [[5, 7, 16, 24], [100], [], [], [], [], [], [], [], []]
s = [5, 7, 16, 24, 100]
"""


def radix_num(n, radix):
    k = math.ceil(math.log(max(n), radix))
    return k


def radix_sort(n, radix=10, reverse=False):
    k = radix_num(n, radix=radix)
    for i in range(0, k+1, 1):
        buckets = [[] for _ in range(radix)]
        base = radix ** i
        for num in n:
            index = num // base % radix if not reverse else radix - num // base % radix - 1
            buckets[index].append(num)
        n = []
        for bucket in buckets:
            n.extend(bucket)
    return n


if __name__ == "__main__":
    import random

    info = []
    for i in range(20):
        info.append(random.randint(0, 1000))
    res = radix_sort(n=info, radix=8)
    print(res)
    res = radix_sort(n=info, radix=8, reverse=True)
    print(res)
