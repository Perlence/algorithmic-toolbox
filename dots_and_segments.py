import random
import io
from itertools import islice
import sys

import pytest

try:
    profile
except NameError:
    def profile(fn):
        return fn


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
        result = [0 for _ in dots]

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


@profile
def inclusions_quick(dots, segments, lo=0, hi=None, result=None):
    # print('dots, segments, result', dots, len(segments), result, file=sys.stderr)
    if hi is None:
        hi = len(dots)

    if result is None:
        dots = list(enumerate(dots))
        result = [0 for _ in dots]

    if lo >= hi or not segments:
        return result

    j = random.randint(lo, hi - 1)
    dots[hi - 1], dots[j] = dots[j], dots[hi - 1]
    m, pivot = partition(dots, lo, hi)

    count = 0
    seg_lo = []
    seg_hi = []
    for start, end in segments:
        if start <= pivot:
            seg_lo.append((start, end))
        if pivot <= end:
            seg_hi.append((start, end))
        if start <= pivot <= end:
            count += 1

    # print('m, pivot, left, right', m, pivot, dots[lo:m], dots[m + 1:hi], file=sys.stderr)
    # print('count', count, file=sys.stderr)
    result[dots[m][0]] = count
    inclusions_quick(dots, seg_lo, lo, m, result)
    inclusions_quick(dots, seg_hi, m + 1, hi, result)
    return result


def partition(seq, lo=0, hi=None):
    if hi is None:
        hi = len(seq)

    hi -= 1
    _, pivot = seq[hi]
    i = lo
    for j in range(lo, hi):
        _, val = seq[j]
        if val <= pivot:
            seq[i], seq[j] = seq[j], seq[i]
            i += 1
    seq[hi], seq[i] = seq[i], seq[hi]
    return i, seq[i][1]


# inclusions = inclusions_recursive
inclusions = inclusions_quick


def stress(full=False):
    if not full:
        n = int(3)
        m = int(3)
        maxi = 10
    else:
        # n = int(5e4)
        # m = int(5e4)
        n = int(5e2)
        m = int(5e2)
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


@pytest.mark.parametrize('seq, _', islice(stress(), 100))
def test_partition(seq, _):
    seq = list(enumerate(seq))
    j, pivot = partition(seq)
    assert all([x <= pivot for (_, x) in seq[:j]]) and all([x > pivot for (_, x) in seq[j+1:]])


def test_inclusions():
    # assert inclusions([-4, -4, -4], [(8, 10), (-5, 4), (3, 10)]) == [1, 1, 1]
    assert inclusions([-1, 2, 5], [(1, 9), (-5, 2), (0, 7)]) == [1, 3, 2]
    assert inclusions([7, -5, 5], [(-7, 6), (1, 9), (2, 10)]) == [2, 1, 3]


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


# @pytest.mark.skip
# @pytest.mark.timeout(3)
@pytest.mark.parametrize('dots, segments', islice(stress(full=True), 1))
def test_bench(dots, segments):
    list(inclusions(dots, segments))

if __name__ == '__main__':
    try:
        line_profiler
    except NameError:
        main()
    else:
        pytest.main(sys.argv)
