from itertools import count

import pytest


def fibonacci_partial_sum_naive(from_, to):
    if to <= 1:
        return to
    previous = 0
    current = 1
    for _ in range(from_ - 1):
        previous, current = current, previous + current
    result = current
    for _ in range(to - from_):
        previous, current = current, previous + current
        result += current
    return result % 10


def fibonacci_partial_sum_smart(n, k, m=10):
    period = pisano_period(m)
    return (fibmod((k + 2) % period, m) - fibmod((n + 1) % period, m)) % m


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

# fibonacci_partial_sum = fibonacci_partial_sum_naive
fibonacci_partial_sum = fibonacci_partial_sum_smart


@pytest.mark.timeout(5)
@pytest.mark.parametrize('n, k, expected', [
    (3, 7, 1),
    (10, 200, 2),
    (int(6e17), int(1e18), 5),
])
def test_fibonacci_partial_sum(n, k, expected):
    assert fibonacci_partial_sum(n, k) == expected
