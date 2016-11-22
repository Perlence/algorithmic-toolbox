import random
import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    next(it)  # count
    seq = list(map(int, next(it).split()))
    print(greatest_subsequence(seq), file=w)


def greatest_subsequence(seq):
    table = [1] * len(seq)
    for i, x in enumerate(seq):
        table[i] = 1 + max((d for j, d in enumerate(table[:i]) if x % seq[j] == 0), default=0)
    return max(table)


def stress(full=False):
    if not full:
        n = int(6)
        m = 10
    else:
        n = int(1e3)
        m = 2e9
    while True:
        yield [random.randint(0, m - 1) for _ in range(n)]


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '4',
        '3 6 7 12',
    ], [
        '3',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


@pytest.mark.timeout(5)
@pytest.mark.parametrize('seq', islice(stress(full=True), 1))
def test_bench(seq):
    greatest_subsequence(seq)

if __name__ == '__main__':
    main()
