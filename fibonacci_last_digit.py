import sys

import pytest


def fib(n):
    if n <= 1:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur


def fib_last_digit_naive(n):
    if n <= 1:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur % 10


def fib_last_digit_smart(n):
    if n <= 1:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur % 10, (prev + cur) % 10
    return cur

fib_last_digit = fib_last_digit_smart


@pytest.mark.timeout(5)
@pytest.mark.parametrize('n, expected', [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (331, 9),
    (327305, 5),
])
def test_fib_last_digit(n, expected):
    assert fib_last_digit(n) == expected


if __name__ == '__main__':
    inp = sys.stdin.read()
    n = int(inp)
    print(fib_last_digit(n))
