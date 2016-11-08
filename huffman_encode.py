from collections import Counter
import heapq
import sys

import pytest


def main():
    line = sys.stdin.readline().strip()
    btree = huffman(line)
    cs = codes(btree)
    encoded = _encode(line, cs)
    print(len(cs), len(encoded))
    for char, code in cs.items():
        print('{}: {}'.format(char, code))
    print(encoded)


def encode(s):
    btree = huffman(s)
    cs = codes(btree)
    return _encode(s, cs)


def huffman(s):
    if not s:
        return BTree()
    count = Counter(s)
    pool = list(map(BTree, count.items()))
    heapq.heapify(pool)
    while pool:
        a = heapq.heappop(pool)
        if not pool:
            if a.char() is None:
                return a
            else:
                return BTree((None, a.freq()), a)
        b = heapq.heappop(pool)
        result = BTree((None, a.freq() + b.freq()), b, a)
        heapq.heappush(pool, result)


def codes(btree, d=None, prefix=''):
    if d is None:
        d = {}

    if btree is None or btree.is_empty():
        pass
    elif not btree.has_children():
        d[btree.char()] = prefix
    elif btree.char() is None:
        codes(btree.left(), d, prefix=prefix + '0')
        codes(btree.right(), d, prefix=prefix + '1')

    return d


def _encode(s, cs):
    result = ''
    for char in s:
        result += cs[char]
    return result


class BTree:
    _value = (None, None)
    _l = None
    _r = None

    def __init__(self, value=(None, None), left=None, right=None):
        self._value = value
        self._l = left
        self._r = right

    def char(self):
        return self._value[0]

    def freq(self):
        return self._value[1]

    def left(self):
        return self._l

    def right(self):
        return self._r

    def is_empty(self):
        return self._value == (None, None) and not self.has_children()

    def has_children(self):
        return self._l is not None or self._r is not None

    def __lt__(self, other):
        if other is None:
            return False

        if self._value[1] == other._value[1]:
            if self._value[0] is None:
                return True
            if other._value[0] is None:
                return False
            return self._value[0] > other._value[0]

        return self._value[1] < other._value[1]

    def __eq__(self, other):
        if other is None:
            return False
        return self._value == other._value and self._l == other._l and self._r == other._r

    def __repr__(self):
        return 'BTree({!r}, {!r}, {!r})'.format(self._value, self._l, self._r)


def test_huffman():
    assert huffman('') == BTree()
    assert huffman('a') == BTree((None, 1), BTree(('a', 1)))
    assert huffman('aaaa') == BTree((None, 4), BTree(('a', 4)))
    assert huffman('aaaabb') == BTree((None, 6), BTree(('a', 4)), BTree(('b', 2)))
    assert huffman('abacabad') == BTree((None, 8), BTree(('a', 4)), BTree((None, 4), BTree(('b', 2)), BTree((None, 2), BTree(('c', 1)), BTree(('d', 1)))))


def test_codes():
    assert codes(huffman('')) == {}
    assert codes(huffman('a')) == {'a': '0'}
    assert codes(huffman('aaaa')) == {'a': '0'}
    assert codes(huffman('aaaabb')) == {'a': '0', 'b': '1'}
    assert codes(huffman('abacabad')) == {'a': '0', 'b': '10', 'c': '110', 'd': '111'}


@pytest.mark.timeout(5)
@pytest.mark.parametrize('s, expected', [
    ('a', '0'),
    ('abacabad', '01001100100111'),
    ('abcd', '10110001')
])
def test_encode(s, expected):
    assert encode(s) == expected

if __name__ == '__main__':
    main()
