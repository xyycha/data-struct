# -*- encoding: utf-8 -*-
import hashlib
import math


class Node(object):
    def __init__(self, key, value, hash_key):
        self.key = key
        self.value = value
        self.hash_key = hash_key


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

    def split_node(self, bucket_index_base, step):
        index = []
        bucket = []
        for node in self._node_list:
            if not node:
                continue
            bucket_index = (node.hash_key & bucket_index_base) >> step
            node_index = node.hash_key & self._max_node - 1
            if bucket_index not in index:
                new_bucket = Bucket(max_node=self._max_node)
                new_bucket.insert_node(index=node_index, key=node.key, value=node.value, hash_key=node.hash_key)
                index.append(bucket_index)
                bucket.append(new_bucket)
            else:
                bucket_num = index.index(bucket_index)
                bucket[bucket_num].insert_node(index=node_index, key=node.key, value=node.value, hash_key=node.hash_key)
        return index, bucket


class ExtendableHashTable(object):
    max_bucket = 5

    def __init__(self, max_node=7):
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
        self.bucket_num = self.bucket_num << 1
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
        node_index = max((hash_key & self.max_node) - 1, 0)
        return bucket_index, node_index

    def insert(self, key, value):
        hash_key = self.hash(key=key)
        while True:
            bucket_index, node_index = self.get_index(hash_key=hash_key)
            if not self.bucket_list[bucket_index]:
                self.bucket_list[bucket_index] = Bucket(max_node=self.max_node)
            if not self.bucket_list[bucket_index].check_status():
                left_index = bucket_index - 1
                right_index = bucket_index + 1
                old_bucket = self.bucket_list[bucket_index]
                self.bucket_list[bucket_index] = None
                while left_index >= 0 or right_index < self.bucket_num:
                    if left_index >= 0 and old_bucket == self.bucket_list[left_index]:
                        self.bucket_list[left_index] = None
                        left_index -= 1
                    else:
                        left_index = -1
                    if right_index < self.bucket_num and old_bucket == self.bucket_list[right_index]:
                        self.bucket_list[right_index] = None
                        right_index += 1
                    else:
                        right_index = self.bucket_num
                self.extend_bucket()
                bucket_index, bucket = old_bucket.split_node(bucket_index_base=self.bucket_index_base,
                                                             step=self.step)
                for i, index in enumerate(bucket_index):
                    self.bucket_list[index] = bucket[i]
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
        return node


if __name__ == "__main__":
    hash_table = ExtendableHashTable()
    for i in range(65, 80):
        key = chr(i)
        hash_table.insert(key=key, value=i)
    for i in range(65, 80):
        key = chr(i)
        node = hash_table.find(key=key)
        if node is None:
            print(key)
        else:
            assert node.value == i, "find 操作不一致"
    print("end")
