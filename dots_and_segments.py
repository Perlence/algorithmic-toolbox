from collections import MutableSequence
import random
import io
from itertools import islice, chain
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


def inclusions_recursive(dots, segments, result=None):
    # print('dots, segments, result', dots, len(segments), result, file=sys.stderr)

    if result is None:
        dots = list(enumerate(dots))
        result = [0] * len(dots)

    if not dots:
        return result

    i, pivot = random.choice(dots)
    count = sum(1 for start, end in segments if start <= pivot <= end)
    # print('pivot', pivot, file=sys.stderr)
    # print('count', count, file=sys.stderr)
    result[i] = count
    inclusions_recursive([(i, dot) for (i, dot) in dots if dot < pivot], segments, result)
    inclusions_recursive([(i, dot) for (i, dot) in dots if dot > pivot], segments, result)
    return result


def inclusions_sorted(dots, segments):
    so = quicksort(chain(((i, v, '1dot') for (i, v) in enumerate(dots)),
                         ((None, start, '0start') for (start, _) in segments),
                         ((None, end, '2end') for (_, end) in segments)),
                   key=lambda seq: (seq[1], seq[2]))
    count = 0
    counts = [0 for _ in dots]
    for index, value, kind in so:
        if kind.endswith('start'):
            count += 1
        elif kind.endswith('end'):
            count -= 1
        elif kind.endswith('dot'):
            counts[index] = count
    return counts


def quicksort(iterable, key=None, lo=0, hi=None):
    if not isinstance(iterable, MutableSequence):
        seq = list(iterable)
    else:
        seq = iterable
    if key is None:
        def key(x): return x
    if hi is None:
        hi = len(seq)

    while lo < hi - 1:
        # Swap random element with last
        j = random.randint(lo, hi - 1)
        seq[hi - 1], seq[j] = seq[j], seq[hi - 1]

        m = partition(seq, key, lo, hi)
        quicksort(seq, key, lo, m)
        lo = m + 1

    return seq


def partition(seq, key, lo, hi):
    lo -= 1
    hi -= 1
    pivot = seq[hi]
    keyed = key(pivot)
    while True:
        while True:
            lo += 1
            if lo == hi:
                seq[hi] = pivot
                return hi
            if key(seq[lo]) > keyed:
                seq[hi] = seq[lo]
                break
        while True:
            hi -= 1
            if hi == lo:
                seq[hi] = pivot
                return hi
            if key(seq[hi]) < keyed:
                seq[lo] = seq[hi]
                break


# inclusions = inclusions_recursive
# inclusions = inclusions_quick
inclusions = inclusions_sorted


def stress(full=False):
    if not full:
        n = int(3)
        m = int(3)
        maxi = 10
    else:
        n = int(5e4)
        m = int(5e4)
        maxi = 1e8
    while True:
        dots = set()
        while len(dots) < m:
            dots.add(random.randint(-maxi, maxi))

        segments = []
        for _ in range(n):
            start = random.randint(-maxi, maxi - 1)
            end = random.randint(start + 1, maxi)
            segments.append((start, end))
        yield list(dots), segments


@pytest.mark.skip
@pytest.mark.parametrize('seq, m, n, expected', [
    ([3, 0, 1, 1, 1], 1, 3, [0, 1, 1, 1, 3]),
    ([3, 1, 1, 1, 0], 0, 0, [0, 1, 1, 1, 3]),
    ([3, 10, 4, 9, 4], 1, 2, [3, 4, 4, 9, 10]),
    ([-3, -10, -4, -9, -4], 2, 3, [-10, -9, -4, -4, -3]),
])
def test_partition(seq, m, n, expected):
    j, k = partition(seq)
    assert (j, k) == (m, n)
    assert seq == expected


@pytest.mark.parametrize('seq, _', islice(stress(), 100))
def test_quicksort(seq, _):
    assert quicksort(seq[:]) == sorted(seq)


@pytest.mark.parametrize('dots, segments, expected', [
    ([3], [(0, 3), (3, 6)], [2]),
    ([-1, 2, 5], [(1, 9), (-5, 2), (0, 7)], [1, 3, 2]),
    ([7, -5, 5], [(-7, 6), (1, 9), (2, 10)], [2, 1, 3]),
    ([0, 8, -9], [(-8, 7), (-6, 7), (4, 6)], [2, 0, 0]),
    ([10, -4, -10], [(-4, 3), (-9, 8), (-4, 9)], [0, 3, 0]),
])
def test_inclusions(dots, segments, expected):
    assert inclusions(dots, segments) == expected


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


@pytest.mark.parametrize('dots, segments', islice(stress(), 100))
def test_stress(dots, segments):
    assert inclusions(dots, segments) == list(inclusions_naive(dots, segments))


@pytest.mark.timeout(3)
@pytest.mark.parametrize('dots, segments', islice(stress(full=True), 1))
def test_bench(dots, segments):
    list(inclusions(dots, segments))

if __name__ == '__main__':
    main()
