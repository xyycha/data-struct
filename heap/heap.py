# -*- encoding: utf-8 -*-


class HeapNode(object):
    def __init__(self, value, info):
        self.value = value
        self.info = info


class Heap(object):
    def __init__(self, cap):
        self.cap = cap
        self.size = 0
        self._heap = []

    def show(self):
        print(self._heap)

    def insert(self, node: HeapNode):
        if not self._heap:
            self._heap.append(node)
            self.size += 1
            return 1
        index = self.size + 1
        if index > self.cap:
            return -1
        self._heap.append(None)
        while index > 1:
            father_index = index // 2
            if node.value < self._heap[father_index - 1].value:
                self._heap[index - 1] = self._heap[father_index - 1]
                if father_index == 1:
                    self._heap[0] = node
            else:
                self._heap[index - 1] = node
                break
            index = father_index
        self.size += 1
        return 1

    def pop(self):
        assert self.size > 0, "空堆"
        index = 1
        top = self._heap[0]
        self.size -= 1
        while index * 2 <= self.size:
            child = index * 2
            if child != self.size and self._heap[child - 1].value > self._heap[child].value:
                child += 1
            if self._heap[child - 1].value < self._heap[self.size].value:
                self._heap[index - 1] = self._heap[child - 1]
            else:
                break
            index = child
        self._heap[index - 1] = self._heap.pop()
        return top


if __name__ == "__main__":
    h = Heap(cap=10)
    h.insert(HeapNode(value=8, info=8))
    h.insert(HeapNode(value=3, info=3))
    h.insert(HeapNode(value=4, info=4))
    h.insert(HeapNode(value=2, info=2))
    h.insert(HeapNode(value=7, info=7))
    h.insert(HeapNode(value=6, info=6))
    h.pop()
    h.pop()
    h.pop()
