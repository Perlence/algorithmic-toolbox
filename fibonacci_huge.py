from itertools import count
import sys

import pytest


def fibmod(n, m=None):
    if n <= 1:
        return n
    prev, cur = 0, 1
    if m is None:
        for _ in range(n - 1):
            prev, cur = cur, prev + cur
    else:
        for _ in range(n - 1):
            prev, cur = cur % m, (prev + cur) % m
    return cur


def fibonacci_huge_smart(n, m):
    return fibmod(n % pisano_period(m), m)


def pisano_period(m):
    if m == 1:
        return 1
    prev, cur = 0, 1
    for n in count(2):
        prev, cur = cur, fibmod(n) % m
        if (prev, cur) == (0, 1):
            return n - 1

fibonacci_huge = fibonacci_huge_smart


@pytest.mark.parametrize('n, expected', [
    (1, 1),
    (2, 3),
    (3, 8),
    (4, 6),
    (5, 20),
    (6, 24),
    (7, 16),
    (8, 12),
    (9, 24),
    (10, 60),
])
def test_pisano_period(n, expected):
    assert pisano_period(n) == expected


@pytest.mark.timeout(5)
@pytest.mark.parametrize('n, m, expected', [
    (1, 239, 1),
    (239, 1000, 161),
    (2816213588, 30524, 10249),
])
def test_fibonacci_huge(n, m, expected):
    assert fibonacci_huge(n, m) == expected


if __name__ == '__main__':
    inp = sys.stdin.read()
    n = int(inp)
    print(fibonacci_huge(n))
