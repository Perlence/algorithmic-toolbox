import random
import io
from itertools import islice
import sys

import pytest

M = 11


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    next(it)  # count
    seq = list(map(int, next(it).split()))
    print(' '.join(map(str, countsort(seq))), file=w)


def countsort(seq):
    counts = [0] * M
    for x in seq:
        counts[x] += 1
    return sum(([i] * c for i, c in enumerate(counts)), [])


def stress(full=False):
    if not full:
        n = int(6)
    else:
        n = int(1e4)
    while True:
        seq = [random.randint(0, M - 1) for _ in range(n)]
        yield seq


@pytest.mark.parametrize('seq', islice(stress(), 100))
def test_countsort(seq):
    assert countsort(seq) == sorted(seq)


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '5',
        '2 3 9 2 9'
    ], [
        '2 2 3 9 9',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


@pytest.mark.timeout(3)
@pytest.mark.parametrize('seq', islice(stress(full=True), 1))
def test_bench(seq):
    list(countsort(seq))

if __name__ == '__main__':
    main()
