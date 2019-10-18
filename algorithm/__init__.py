class Heap(object):
    def __init__(self, heap_size=None):
        self.queue = list()
        self.heap_size = heap_size

    @staticmethod
    def parent(i):
        return i / 2

    @staticmethod
    def left(i):
        return 2 * i

    @staticmethod
    def right(i):
        return 2 * i + 1

    def max_heapify(self, i):
        """
        把i节点变成当前三角(i, i's left children, i's right children)的最大值
        :param i:
        :return:
        """
        l = self.left(i)
        r = self.right(i)

        if l < self.heap_size and self.queue[l] > self.queue[i]:
            largest = l
        else:
            largest = i

        if r <= self.heap_size and self.queue[r] > self.queue[largest]:
            largest = r

        if largest != i:
            self.queue[i], self.queue[largest] = self.queue[largest], self.queue[i]
            self.max_heapify(largest)

    def build_max_heap(self, array):
        """
        O(n)
        :param array:
        :return:
        """
        length = len(array)
        self.queue = array
        self.heap_size = self.heap_size or length
        for i in range(length // 2 - 1, -1, -1):  # 遍历所有的非叶节点
            self.max_heapify(i)

    def heap_sort(self):
        self.build_max_heap(self.queue)
        for i in range(len(self.queue) - 1, 0, -1):
            self.queue[i], self.queue[0] = self.queue[0], self.queue[i]
            self.heap_size = self.heap_size - 1
            self.max_heapify(0)

    def __repr__(self):
        return str(self.queue)


heap = Heap()
array = [1, 2, 4, 3, 2, 5, 7, 21, 12, 9]
heap.queue = array
heap.heap_sort()

# heap.build_max_heap(array)

print(heap)

# prop --> taobao
# 必须
# 异步商户
# 建中
# we -> json
# 返显