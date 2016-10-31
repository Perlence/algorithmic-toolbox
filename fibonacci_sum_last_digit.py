from itertools import count

import pytest


def fibonacci_sum_naive(n, m=10):
    if n <= 1:
        return n
    prev, cur = 0, 1
    result = 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
        result += cur
    return result % m


def fibonacci_sum_smart(n, m=10):
    period = pisano_period(m)
    return (fibmod((n + 2) % period, m) - 1) % m


def pisano_period(m):
    if m == 1:
        return 1
    prev, cur = 0, 1
    for n in count(2):
        prev, cur = cur, fibmod(n, m)
        if (prev, cur) == (0, 1):
            return n - 1


def fibmod(n, m):
    if n <= 1:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur % m, (prev + cur) % m
    return cur

fibonacci_sum = fibonacci_sum_smart


@pytest.mark.timeout(5)
@pytest.mark.parametrize('n, expected', [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 4),
    (100, 5),
    (int(1e14), 5),
])
def test_fibonacci_sum(n, expected):
    assert fibonacci_sum(n) == expected
