import heapq
import io
from itertools import islice
import math
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    count = int(next(it))
    # heap = BuiltinMaxHeap()
    heap = MaxHeap()
    for line in islice(it, count):
        words = line.split()
        if words[0] == 'Insert':
            heap.insert(int(words[1]))
        elif words[0] == 'ExtractMax':
            val = heap.extract_max()
            print(val, file=w)


class BuiltinMaxHeap:
    def __init__(self, iterable=None):
        self._list = []
        if iterable is not None:
            for x in iterable:
                self.insert(x)

    def insert(self, x):
        heapq.heappush(self._list, invert_comparison(x))

    def extract_max(self):
        return heapq.heappop(self._list).orig()

    def __repr__(self):
        return 'BuiltinMaxHeap({!r})'.format(self._list)


class invert_comparison:
    def __init__(self, obj):
        self._obj = obj

    def __lt__(self, other):
        if isinstance(other, invert_comparison):
            return self._obj >= other._obj
        else:
            return self._obj >= other

    def __eq__(self, other):
        if isinstance(other, invert_comparison):
            return self._obj == other._obj
        else:
            return self._obj == other

    def orig(self):
        return self._obj

    def __repr__(self):
        return repr(self._obj)


class MaxHeap:
    def __init__(self, iterable=None):
        self._list = []
        if iterable is not None:
            for x in iterable:
                self.insert(x)

    def insert(self, x):
        self._list.append(x)
        if len(self._list) == 1:
            return
        last_id = len(self._list) - 1
        self._sift_up(last_id)

    def extract_max(self):
        if not self._list:
            return
        result = self._list.pop(0)
        if len(self._list) < 2:
            return result
        last = self._list.pop()
        self._list.insert(0, last)
        self._sift_down(0)
        return result

    def _sift_up(self, i):
        while True:
            parent_id = self._parent_of(i)
            if parent_id < 0 or self._list[parent_id] >= self._list[i]:
                break
            self._list[parent_id], self._list[i] = self._list[i], self._list[parent_id]
            i = parent_id

    @profile
    def _sift_down(self, i):
        l = self._list
        while True:
            child_ids = self._children_of(i)
            nhood = [(i, l[i])] + [(child_id, l[child_id]) for child_id in child_ids if child_id < len(l)]
            max_id, max_value = max(nhood, key=lambda t: t[1])
            if max_id == i:
                break
            l[max_id], l[i] = l[i], l[max_id]
            i = max_id

    def _parent_of(self, i):
        return math.ceil(i / 2) - 1

    def _children_of(self, i):
        first = 2*i + 1
        return (first, first + 1)

    def __repr__(self):
        return 'MaxHeap({!r})'.format(self._list)


def test_extract_max():
    h = MaxHeap([66, 57, 42, 11, 52, 29, 29])
    assert h.extract_max() == 66
    assert h.extract_max() == 57
    assert h.extract_max() == 52
    assert h.extract_max() == 42
    assert h.extract_max() == 29
    assert h.extract_max() == 29
    assert h.extract_max() == 11


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '6',
        'Insert 200',
        'Insert 10',
        'ExtractMax',
        'Insert 5',
        'Insert 500',
        'ExtractMax',
    ], [
        '200',
        '500',
    ])
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


def stress():
    import random
    while True:
        n = random.randint(1, 1e4)
        yield (random.randint(0, 1e9) for _ in range(n))


@pytest.mark.stress
@pytest.mark.parametrize('iterable', islice(stress(), 4))
def test_stress(iterable):
    h1 = BuiltinMaxHeap()
    h2 = MaxHeap()
    for x in iterable:
        h1.insert(x)
        h2.insert(x)
    assert h1._list == h2._list
    for _ in h1._list:
        x1 = h1.extract_max()
        x2 = h2.extract_max()
        assert x1 == x2

if __name__ == '__main__':
    # main()
    pytest.main([__file__])
