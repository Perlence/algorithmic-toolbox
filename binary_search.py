import io
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    nums = next(it).split()
    seq = list(map(int, nums[1:]))

    nums = next(it).split()
    needles = map(int, nums[1:])

    indices = []
    for needle in needles:
        index = bisect(seq, needle)
        indices.append(index)
    print(' '.join(map(str, indices)), file=w)


def bisect(seq, x):
    a, b = 0, len(seq) - 1
    while a <= b:
        mid = int((a + b) / 2)
        if seq[mid] == x:
            return mid + 1
        elif seq[mid] < x:
            a = mid + 1
        else:
            b = mid - 1
    return -1


@pytest.mark.timeout(5)
@pytest.mark.parametrize('inp, expected', [
    ([
        '5 1 5 8 12 13',
        '5 8 1 23 1 11',
    ], [
        '3 1 -1 1 -1',
    ])
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected

if __name__ == '__main__':
    main()
