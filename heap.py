import heapq
import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    count = int(next(it))
    heap = BuiltinMaxHeap()
    for line in islice(it, 0, count):
        words = line.split()
        if words[0] == 'Insert':
            heap.insert(int(words[1]))
        elif words[0] == 'ExtractMax':
            val = heap.extract_max()
            print(val, file=w)


class BuiltinMaxHeap:
    def __init__(self, iterable=None):
        if iterable is None:
            self._list = []
        else:
            self._list = list(iterable)

    def insert(self, x):
        heapq.heappush(self._list, invert_comparison(x))

    def extract_max(self):
        return heapq.heappop(self._list).orig()


class invert_comparison:
    def __init__(self, obj):
        self._obj = obj

    def __lt__(self, other):
        if isinstance(other, invert_comparison):
            return self._obj >= other._obj
        else:
            return self._obj >= other

    def orig(self):
        return self._obj


class MaxHeap:
    def __init__(self, iterable=None):
        if iterable is None:
            self._list = []
        else:
            self._list = list(iterable)

    def insert(self, x):
        raise NotImplemented

    def extract_max(self):
        raise NotImplemented


@pytest.mark.timeout(5)
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

if __name__ == '__main__':
    main()
