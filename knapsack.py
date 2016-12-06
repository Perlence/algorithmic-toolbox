import io
from itertools import islice
from functools import lru_cache
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    capacity, _ = map(int, next(it).split())
    weights = tuple(map(int, next(it).split()))
    print(knapsack(capacity, weights), file=w)


@lru_cache()
def knapsack(capacity, weights):
    if capacity < 0:
        return float('-inf')
    if not weights:
        return 0
    w = weights[-1]
    return max(knapsack(capacity - w, weights[:-1]) + w,
               knapsack(capacity, weights[:-1]))


def stress(full=False):
    import random

    if not full:
        capacity = 100
        n = 6
        w = 10
    else:
        capacity = int(1e4)
        n = 300
        w = 1e5
    while True:
        yield capacity, tuple(random.randint(0, w) for _ in range(n))


@pytest.mark.timeout(2)
@pytest.mark.parametrize('inp, expected', [
    ([
        '10 3',
        '1 4 8',
    ], [
        '9',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


# def test_stress():
#     for capacity, weights in islice(stress(full=True), 100):
#         assert levenshtein_distance(capacity, weights) == editdistance.eval(capacity, weights)


@pytest.mark.timeout(5)
@pytest.mark.parametrize('capacity, weights', islice(stress(full=True), 3))
def test_bench(capacity, weights):
    knapsack(capacity, weights)

if __name__ == '__main__':
    main()
