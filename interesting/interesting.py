# -*- encoding: utf-8 -*-


def over_and_nearest_2_pow(n):
    """
    思路：通过位运算将最高位的1 覆盖到后面的所有位 上， 然后 加1
    寻找大于 n 的最近的 2的幂次方
    :param n: 基准数
    :return: 大于且最近的2的幂次方
    """
    # 跟位运算有关  python的int 动态存储范围可以超过int32
    assert n >= 0 and isinstance(n, int), "不是正整数"
    assert n >> 32 == 0, "超出int32 范围"
    n |= (n >> 16)
    n |= (n >> 8)
    n |= (n >> 4)
    n |= (n >> 2)
    n |= (n >> 1)
    n += 1
    return n


def swap_two_num(a, b):
    """
    交换值
    :param a: 待交换的值
    :param b: 待交换的值
    :return: 交换结果
    """
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b


def sum_two_num(a, b):
    """
    实现两数的和
    :param a: 待求和的值
    :param b: 待求和的值
    :return: 和
    """
    while a:
        a, b = a & b, a ^ b
        a <<= 1
    return b


def judge_2_pow(n) -> bool:
    """
    判断是否为2 的幂次方
    :param n: 基准数
    :return: bool
    """
    res = n & (n - 1)
    return res == 0


if __name__ == "__main__":
    s = over_and_nearest_2_pow(12)
    print(s)
    a, b = swap_two_num(21, 12)
    print(a, b)
    s = sum_two_num(12, 17)
    print(s)
