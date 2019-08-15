import collections


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = collections.OrderedDict()

    def get(self, key):
        if key not in self.queue:
            return -1  # 要找的数据不在缓存中则返回 -1
        value = self.queue.pop(key)  # 将命中缓存的数据移除
        self.queue[key] = value  # 将命中缓存的数据重新添加到头部
        return self.queue[key]

    def put(self, key, value):
        if key in self.queue:  # 如果已经存在缓存中，则先移除老的数据
            self.queue.pop(key)
        elif len(self.queue.items()) == self.capacity:
            self.queue.popitem(last=False)  # 如果不存在缓存并且达到最大容量 则把最后的数据淘汰
        self.queue[key] = value  # 将新数据添加到头部


def test_LRUCache():
    lru = LRUCache(10)

    for i in range(20):
        lru.put(i, i * 2)

    for i in range(20):
        ret = lru.get(i)
    print(lru.queue)


test_LRUCache()
