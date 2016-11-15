import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    n, _ = map(int, next(it).split())
    segments = [tuple(map(int, line.split())) for line in islice(it, n)]
    dots = list(map(int, next(it).split()))
    print(' '.join(map(str, inclusions(dots, segments))), file=w)


def inclusions_naive(dots, segments):
    for i, dot in enumerate(dots):
        count = 0
        for start, end in segments:
            if start <= dot <= end:
                count += 1
        yield count


inclusions = inclusions_naive


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '2 3',
        '0 5',
        '7 10',
        '1 6 11',
    ], [
        '1 0 0',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


def stress(full=False):
    import random
    if not full:
        n = int(6)
        m = int(6)
        maxi = 10
    else:
        n = int(5e4)
        m = int(5e4)
        maxi = 1e8
    while True:
        dots = [random.randint(-maxi, maxi) for _ in range(m)]
        segments = []
        for _ in range(n):
            start = random.randint(-maxi, maxi - 1)
            end = random.randint(start + 1, maxi)
            segments.append((start, end))
        yield dots, segments


@pytest.mark.timeout(3)
@pytest.mark.parametrize('dots, segments', islice(stress(full=True), 1))
def test_bench(dots, segments):
    list(inclusions(dots, segments))

if __name__ == '__main__':
    main()
