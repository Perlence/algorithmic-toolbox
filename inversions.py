import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    next(it)  # count
    seq = list(map(int, next(it).split()))
    print(inversions(seq), file=w)


def inversions_naive(seq):
    result = 0
    for i, a in enumerate(seq):
        for b in seq[i+1:]:
            if a > b:
                result += 1
    return result


def inversions_divide(seq):
    if len(seq) < 2:
        return 0
    elif len(seq) == 2:
        a, b = seq
        return int(a > b)
    else:
        mid = int(len(seq) / 2)
        return inversions_divide(seq[:mid+1]) + inversions_divide(seq[mid:])


def inversions_merge_sort(seq):
    _, invs = merge_sort(seq)
    return invs


def merge_sort(seq):
    if len(seq) < 2:
        return seq, 0
    mid = int(len(seq) / 2)
    so1, invs1 = merge_sort(seq[:mid])
    so2, invs2 = merge_sort(seq[mid:])
    merged, invs3 = merge(so1, so2)
    return merged, invs1 + invs2 + invs3


def merge(xs, ys):
    result = []
    invs = 0
    i = j = 0
    while i < len(xs) and j < len(ys):
        if xs[i] <= ys[j]:
            result.append(xs[i])
            i += 1
        else:
            result.append(ys[j])
            invs += len(xs) - i
            j += 1
    result.extend(xs[i:])
    result.extend(ys[j:])
    return result, invs


def inversions_insort(seq):
    import bisect

    if len(seq) < 2:
        return 0

    acc = []
    result = 0
    for a in reversed(seq):
        for b in acc:
            if a > b:
                result += 1
            else:
                break
        bisect.insort(acc, a)
    return result

# inversions = inversions_naive
# inversions = inversions_divide
inversions = inversions_merge_sort
# inversions = inversions_insort


def test_merge():
    assert merge([3], [9]) == ([3, 9], 0)
    assert merge([2], [3, 9]) == ([2, 3, 9], 0)
    assert merge([4], [9]) == ([4, 9], 0)
    assert merge([2], [4, 9]) == ([2, 4, 9], 0)
    assert merge([2, 3, 9], [2, 4, 9]) == ([2, 2, 3, 4, 9, 9], 3)
    assert merge([1, 3, 5, 9], [2, 3, 7, 8]) == ([1, 2, 3, 3, 5, 7, 8, 9], 7)
    assert merge([2, 3, 5], [0, 5, 9]) == ([0, 2, 3, 5, 5, 9], 3)


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '5',
        '2 3 9 2 9',
    ], [
        '2',
    ]),
    ([
        '6',
        '2 3 9 2 4 9',
    ], [
        '3',
    ]),
    ([
        '2',
        '10 2',
    ], [
        '1',
    ]),
    ([
        '6',
        '2 3 5 9 0 5',
    ], [
        '5',
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
        maxi = 10
    else:
        n = int(1e5)
        maxi = 1e9
    while True:
        yield [random.randint(0, maxi) for _ in range(n)]


@pytest.mark.parametrize('seq', islice(stress(), 100))
def test_stress(seq):
    assert inversions(seq) == inversions_naive(seq)


@pytest.mark.timeout(3)
@pytest.mark.parametrize('seq', islice(stress(full=True), 1))
def test_bench(seq):
    inversions(seq)

if __name__ == '__main__':
    main()
