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
    next(it)  # count
    seq = list(map(int, next(it).split()))
    print(inversions(seq), file=w)


def inversions_naive(seq):
    result = 0
    for i, a in enumerate(seq):
        for b in seq[i+1:]:
            print(a, b, file=sys.stderr)
            if a > b:
                result += 1
    return result


def inversions_divide(seq):
    print(seq, file=sys.stderr)
    if len(seq) < 2:
        print(seq, 0, file=sys.stderr)
        return 0
    elif len(seq) == 2:
        a, b = seq
        print(seq, int(a > b), file=sys.stderr)
        return int(a > b)
    else:
        mid = int(len(seq) / 2)
        return inversions_divide(seq[:mid+1]) + inversions_divide(seq[mid:])


def inversions_merge_sort(seq):
    _, invs = merge_sort(seq)
    return invs


@profile
def merge_sort(seq):
    if len(seq) < 2:
        return seq, 0

    mid = int(len(seq) / 2)
    so1, invs1 = merge_sort(seq[:mid])
    so2, invs2 = merge_sort(seq[mid:])
    merged, invs3 = merge(so1, so2)
    return merged, invs1 + invs2 + invs3


@profile
def merge(xs, ys):
    result = []
    invs = 0
    diff = 1
    while True:
        if not xs:
            return list(result + ys), invs
        if not ys:
            return list(result + xs), invs

        x = xs[0]
        difftmp = diff
        for y in ys[:]:
            if x <= y:
                xs = xs[1:]
                result.append(x)
                break
            else:
                ys = ys[1:]
                invs += diff
                result.append(y)
            diff = 1
            difftmp += 1
        diff = difftmp


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
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


def stress():
    import random
    while True:
        # n = random.randint(1, 1e5)
        n = int(1e5)
        yield [random.randint(0, 1e9) for _ in range(n)]


# @pytest.mark.skip
@pytest.mark.parametrize('seq', islice(stress(), 1))
def test_stress(seq):
    # assert inversions_naive(seq) == inversions_merge_sort(seq)
    inversions_merge_sort(seq)

if __name__ == '__main__':
    try:
        line_profiler
    except NameError:
        main()
    else:
        pytest.main(sys.argv)
