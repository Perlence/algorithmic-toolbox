import bisect
from collections import Counter
import random
import io
from itertools import islice
import sys

import pytest

INF = float('inf')


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    next(it)  # count
    seq = list(map(int, next(it).split()))
    result = greatest_subsequence(seq)
    print(len(result), file=w)
    print(' '.join(map(str, result)), file=w)


def greatest_subsequence_quad(seq):
    table = [1] * len(seq)
    for i, x in enumerate(seq):
        table[i] = 1 + max((d for j, d in enumerate(table[:i]) if seq[j] >= x), default=0)

    result = []
    maxi = max(table)
    for i in range(len(table)-1, -1, -1):
        if maxi < 0:
            break
        if table[i] == maxi:
            result.append(i + 1)
            maxi -= 1
    return list(reversed(result))


def greatest_subsequence_nlogn(seq):
    rseq = reversed(seq)
    counter = Counter(seq)
    table = [float('inf')] * len(seq)
    table.insert(0, float('-inf'))
    # nums = [0] * len(table)
    for i, x in enumerate(rseq):
        print(i, x, file=sys.stderr)
        print(table, file=sys.stderr)
        # print(nums, file=sys.stderr)
        j = bisect.bisect(table, x)

        # if table[j-1] <= x:
        #     if table[j] == INF:
        #         table[j] = x
        #     elif table[j] < x:
        #         table.insert(j, x)
        #         table.pop()

        # if table[j-1] <= x and (table[j] == INF or x >= table[j]):
        #     table[j] = x

        print(j, table[j], counter[table[j]], counter[x], file=sys.stderr)
        if table[j-1] <= x < table[j] and counter[table[j]] <= counter[x]:
            table[j] = x
            # counter[x] -= 1
    print(table, file=sys.stderr)
    # print(nums, file=sys.stderr)

    result = []
    i = 0
    # for x, n in zip(reversed(table), reversed(nums)):
    for x in reversed(table):
        if x == float('inf') or x == float('-inf'):
            continue
        while x != seq[i]:
            i += 1
            if i >= len(seq):
                return result
        result.append(i + 1)
        # result.extend(range(i + 1, i + n + 1))
        i += 1
    return result

greatest_subsequence = greatest_subsequence_nlogn


def stress(full=False):
    if not full:
        n = int(6)
        m = 10
    else:
        n = int(1e5)
        m = 1e9
    while True:
        yield [random.randint(0, m - 1) for _ in range(n)]


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '5',
        '5 4 3 2 1',
    ], [
        '5',
        '1 2 3 4 5',
    ]),
    ([
        '6',
        '3 3 3 4 4 2',
    ], [
        '4',
        '1 2 3 6',
    ]),
    ([
        '5',
        '5 3 4 4 2',
    ], [
        '4',
        '1 3 4 5',
    ]),
    ([
        '6',
        '3 3 2 1 3 8',
    ], [
        '4',
        '1 2 3 4',
    ]),
    ([
        '4',
        '2 2 2 2',
    ], [
        '4',
        '1 2 3 4',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


@pytest.mark.parametrize('seq', islice(stress(), 100))
def test_stress(seq):
    assert greatest_subsequence(seq) == greatest_subsequence_quad(seq)


@pytest.mark.timeout(5)
@pytest.mark.parametrize('seq', islice(stress(full=True), 1))
def test_bench(seq):
    greatest_subsequence(seq)

if __name__ == '__main__':
    main()
