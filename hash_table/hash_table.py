# -*- encoding: utf-8 -*-
import hashlib
import math


class Node(object):
    def __init__(self, key, value, hash_key):
        """

        :param key: 键名
        :param value: 值
        :param hash_key: 哈希值 便于做桶分裂
        """
        self.key = key
        self.value = value
        self.hash_key = hash_key


class Bucket(object):
    def __init__(self, max_node=113):
        # 初始化 桶的节点个数
        self.node_num = 0
        # 桶的节点最大个数 和 填充因子 直接影响桶的分类速率
        # 初始化 桶的节点最大个数
        self._max_node = max_node
        # 填充因子
        self._full_percent = 0.5
        # 初始化 节点列表
        self._node_list = [None] * max_node

    def get_node_index(self, hash_key):
        """
        获取 节点列表的 下标   位运算加速
        :param hash_key: 哈希值
        :return: 节点列表的 下标
        """
        index = max((hash_key & self._max_node) - 1, 0)
        # index = hash_key % self._max_node     simple but calculate slow
        return index

    def check_status(self):
        """
        检查 桶是否可以插入
        :return: bool
        """
        if self.node_num < math.floor(self._max_node * self._full_percent):
            return True
        return False

    def insert_node(self, key, value, hash_key):
        """
        桶 插入 节点
        :param key: 键名
        :param value: 值
        :param hash_key: 哈希值
        :return: None
        """
        index = self.get_node_index(hash_key=hash_key)
        node = Node(key=key, value=value, hash_key=hash_key)
        index = self.get_index(index=index, key=key)
        self._node_list[index] = node
        self.node_num += 1

    def find_node(self, hash_key, key):
        """
        查询节点
        :param hash_key: 哈希值
        :param key: 键名
        :return: Node or None
        """
        index = self.get_node_index(hash_key=hash_key)
        index = self.get_index(index=index, key=key)
        node = self._node_list[index]
        if node:
            return node
        return None

    def delete_node(self, hash_key, key):
        """
        删除节点
        :param hash_key: 哈希值
        :param key: 键名
        :return: None
        """
        index = self.get_node_index(hash_key=hash_key)
        index = self.get_index(index=index, key=key)
        self._node_list[index] = None
        self.node_num -= 1

    def get_index(self, index, key):
        """
        将 下标值 转化为 可以插入的下标值 或者 相同节点的下表
        :param index: 下标值
        :param key: 键名
        :return: 可使用的下标值
        """
        collision_time = 0
        new_index = index
        while self._node_list[new_index] and self._node_list[new_index].key != key:
            collision_time += 1
            new_index = (index + self.collision(collision_time=collision_time)) % self._max_node
        return new_index

    def collision(self, collision_time):
        """
        哈希冲撞的 解决函数  平方探测
        :param collision_time: 冲撞次数
        :return: 偏移值
        """
        return collision_time ** 2

    def split_node(self, table):
        """
        节点分裂
        :param table: 哈希表
        :return: 桶下标列表  桶列表
        """
        # 桶下表列表
        index = []
        # 桶列表
        bucket = []
        for node in self._node_list:
            if not node:
                continue
            # 根据 哈希值 计算 桶的下标值
            bucket_index = (node.hash_key & table.bucket_index_base) >> table.step
            if bucket_index not in index:
                new_bucket = Bucket()
                new_bucket.insert_node(key=node.key, value=node.value, hash_key=node.hash_key)
                index.append(bucket_index)
                bucket.append(new_bucket)
            else:
                bucket_num = index.index(bucket_index)
                bucket[bucket_num].insert_node(key=node.key, value=node.value, hash_key=node.hash_key)
        return index, bucket


class ExtendableHashTable(object):
    # 最大 桶 个数
    max_bucket = 3
    # associate with hash function as we use sha256. The result's most length is 256
    max_step = 256

    def __init__(self):
        # 使用了几个二进制
        self.bucket = 1
        # 桶的个数
        self.bucket_num = 1 << 1
        # 初始化桶的状态
        self.bucket_list = [None] * self.bucket_num
        # 初始化 最高n位 为1的 基准数 与 hash key 求 & 运算 计算 桶的下标
        self.bucket_index_base = None
        # 到 最大步长的 距离
        self.step = 0
        # 刷新 步长
        self.refresh_step()
        # 刷新
        self.refresh_bucket_index_base()

    def refresh_step(self):
        self.step = self.__class__.max_step - self.bucket

    def refresh_bucket_index_base(self):
        index = 1
        start = self.bucket
        while start > 1:
            index = (index << 1) ^ 1
            start -= 1
        self.bucket_index_base = index << self.step

    def extend_bucket(self):
        """
        桶的个数 翻倍操作
        :return:
        """
        # 桶的个数翻倍
        self.bucket += 1
        assert self.bucket <= self.__class__.max_bucket, "超过桶子上限"
        self.bucket_num = self.bucket_num << 1
        # 构造新的 桶列表
        new_bucket_list = []
        for bucket in self.bucket_list:
            new_bucket_list += [bucket]
            new_bucket_list += [bucket]
        self.bucket_list = new_bucket_list
        # 刷新 步长
        self.refresh_step()
        # 刷新 基准数
        self.refresh_bucket_index_base()

    def hash(self, key: str):
        """
        生成 哈希 值
        :param key:  真实的 键名
        :return: 哈希值
        """
        key = key.encode()
        res = hashlib.sha256(key).hexdigest()
        return int(res, 16)

    def get_index(self, hash_key):
        """
        根据 哈希值 找到 目标桶的下标    使用位运算 加速运算
        :param hash_key: 哈希值
        :return: 桶的下标
        """
        bucket_index = (hash_key & self.bucket_index_base) >> self.step
        return bucket_index

    def insert(self, key, value):
        """
        插入操作
        :param key: 键名
        :param value: 值
        :return: None
        """

        hash_key = self.hash(key=key)
        while True:
            bucket_index = self.get_index(hash_key=hash_key)
            # 目标桶 为空
            if not self.bucket_list[bucket_index]:
                self.bucket_list[bucket_index] = Bucket()
                break
            # 目标桶 元素达到上限 需要进行 桶数翻倍操作
            if not self.bucket_list[bucket_index].check_status():
                # 将目标桶的信息 暂存
                old_bucket = self.bucket_list[bucket_index]
                # 将目标桶 清空
                self.bucket_list[bucket_index] = None
                # 将与目标桶相同的 桶 清空
                # 二分法会更好
                left_index = bucket_index - 1
                right_index = bucket_index + 1
                while left_index >= 0:
                    if old_bucket == self.bucket_list[left_index]:
                        self.bucket_list[left_index] = None
                        left_index -= 1
                    else:
                        break
                while right_index < self.bucket_num:
                    if old_bucket == self.bucket_list[right_index]:
                        self.bucket_list[right_index] = None
                        right_index += 1
                    else:
                        break
                # 进行 桶的个数 翻倍操作
                self.extend_bucket()
                # 进行 目标桶的 分裂 操作
                bucket_index, bucket = old_bucket.split_node(table=self)
                # 将 分裂 结果 插入到 新的桶列表中
                for i, index in enumerate(bucket_index):
                    self.bucket_list[index] = bucket[i]
            # 桶可以 插入元素
            else:
                break
        # 目标桶可以 进行插入  插入操作
        self.bucket_list[bucket_index].insert_node(key=key, value=value, hash_key=hash_key)

    def delete(self, key):
        """
        删除操作
        :param key: 键名
        :return: None
        """
        hash_key = self.hash(key=key)
        bucket_index = self.get_index(hash_key=hash_key)
        if not self.bucket_list[bucket_index]:
            return
        self.bucket_list[bucket_index].delete_node(hash_key=hash_key, key=key)

    def find(self, key):
        """
        查找操作
        :param key: 键名
        :return: None or Node
        """
        hash_key = self.hash(key=key)
        bucket_index = self.get_index(hash_key=hash_key)
        if not self.bucket_list[bucket_index]:
            return None
        node = self.bucket_list[bucket_index].find_node(hash_key=hash_key, key=key)
        return node


if __name__ == "__main__":
    hash_table = ExtendableHashTable()
    for i in range(1, 127):
        key = chr(i)
        hash_table.insert(key=key, value=i)
    for i in range(1, 127):
        key = chr(i)
        node = hash_table.find(key=key)
        if node is None:
            print(key)
        else:
            assert node.value == i, "find 操作不一致"
    print("end")
