# -*- encoding: utf-8 -*-
import hashlib
import math


class Node(object):
    def __init__(self, key, value, hash_key):
        self.key = key
        self.value = value
        self.hash_key = hash_key
        self.bin_bash_key = bin(self.hash_key)


class Bucket(object):
    def __init__(self, max_node):
        self.node_num = 0
        self._max_node = max_node
        self._full_percent = 0.5
        self._node_list = [None] * max_node

    def check_status(self):
        if self.node_num < math.floor(self._max_node * self._full_percent):
            return True
        return False

    def insert_node(self, index, key, value, hash_key):
        node = Node(key=key, value=value, hash_key=hash_key)
        index = self.get_index(index=index, key=key)
        self._node_list[index] = node
        self.node_num += 1

    def find_node(self, index, key):
        index = self.get_index(index=index, key=key)
        node = self._node_list[index]
        if node:
            return node
        return None

    def delete_node(self, index, key):
        index = self.get_index(index=index, key=key)
        self._node_list[index] = None
        self.node_num -= 1

    def get_index(self, index, key):
        collision_time = 0
        new_index = index
        while self._node_list[new_index] and self._node_list[new_index].key != key:
            collision_time += 1
            new_index = (index + self.collision(collision_time=collision_time)) % self._max_node
        return new_index

    def collision(self, collision_time):
        return collision_time ** 2

    def split_node(self, bucket_index_base, step, old_bucket_index):
        left = 2 * old_bucket_index
        right = left + 1
        left_bucket = Bucket(max_node=self._max_node)
        right_bucket = Bucket(max_node=self._max_node)
        for node in self._node_list:
            if not node:
                continue
            bucket_index = (node.hash_key & bucket_index_base) >> step
            node_index = node.hash_key & self._max_node - 1
            if bucket_index == left:
                left_bucket.insert_node(index=node_index, key=node.key, value=node.value, hash_key=node.hash_key)
            elif bucket_index == right:
                right_bucket.insert_node(index=node_index, key=node.key, value=node.value, hash_key=node.hash_key)
            else:
                assert False, "Bucket wrong"
        return left, left_bucket, right, right_bucket


class ExtendableHashTable(object):
    max_bucket = 8

    def __init__(self, max_node=17):
        self.bucket = 1
        self.bucket_num = 1 << 1
        self.bucket_list = [None] * self.bucket_num
        self.bucket_index_base = None
        self.max_node = max_node
        self.step = 256 - self.bucket
        self.refresh_bucket_index_base()

    def refresh_bucket_index_base(self):
        index = 1
        start = self.bucket
        while start > 1:
            index = (index << 1) ^ 1
            start -= 1
        self.bucket_index_base = index << self.step

    def extend_bucket(self):
        self.bucket += 1
        assert self.bucket <= self.__class__.max_bucket, "超过桶子上限"
        self.bucket_num = 1 << self.bucket
        new_bucket_list = []
        for bucket in self.bucket_list:
            new_bucket_list += [bucket]
            new_bucket_list += [bucket]
        self.bucket_list = new_bucket_list
        self.step = 256 - self.bucket
        self.refresh_bucket_index_base()

    def hash(self, key: str):
        key = key.encode()
        res = hashlib.sha256(key).hexdigest()
        return int(res, 16)

    def get_index(self, hash_key):
        bucket_index = (hash_key & self.bucket_index_base) >> self.step
        node_index = (hash_key & self.max_node) - 1
        return bucket_index, node_index

    def insert(self, key, value):
        hash_key = self.hash(key=key)
        while True:
            bucket_index, node_index = self.get_index(hash_key=hash_key)
            if not self.bucket_list[bucket_index]:
                self.bucket_list[bucket_index] = Bucket(max_node=self.max_node)
            if not self.bucket_list[bucket_index].check_status():
                old_bucket = self.bucket_list[bucket_index]
                self.extend_bucket()
                left, left_bucket, right, right_bucket = old_bucket.split_node(bucket_index_base=self.bucket_index_base,
                                                                               step=self.step,
                                                                               old_bucket_index=bucket_index)
                self.bucket_list[left] = left_bucket
                self.bucket_list[right] = right_bucket
            else:
                break
        self.bucket_list[bucket_index].insert_node(index=node_index, key=key, value=value, hash_key=hash_key)

    def delete(self, key):
        hash_key = self.hash(key=key)
        bucket_index, node_index = self.get_index(hash_key=hash_key)
        if not self.bucket_list[bucket_index]:
            return 0
        self.bucket_list[bucket_index].delete_node(index=node_index, key=key)

    def find(self, key):
        hash_key = self.hash(key=key)
        bucket_index, node_index = self.get_index(hash_key=hash_key)
        if not self.bucket_list[bucket_index]:
            return None
        node = self.bucket_list[bucket_index].find_node(index=node_index, key=key)
        return node.value


if __name__ == "__main__":
    hash_table = ExtendableHashTable()
    for i in range(65, 96):
        key = chr(i)
        hash_table.insert(key=key, value=i)
        assert hash_table.find(key=key) == i, "find 操作不一致"
    print("end")
