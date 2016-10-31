import sys

import pytest


def lcm_naive(a, b):
    for l in range(1, a * b + 1):
        if l % a == 0 and l % b == 0:
            return l
    return a * b


def lcm_smart(a, b):
    if a == b == 0:
        return 0
    return a * (b / gcd(a, b))


def gcd(a, b):
    if b > a:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a

lcm = lcm_smart


@pytest.mark.parametrize('a, b, expected', [
    (0, 10, 10),
    (1, 10, 1),
    (2, 10, 2),
    (3, 10, 1),
    (4, 10, 2),
    (5, 10, 5),
])
def test_gcd(a, b, expected):
    assert gcd(a, b) == expected


@pytest.mark.timeout(5)
@pytest.mark.parametrize('a, b, expected', [
    (6, 8, 24),
    (28851538, 1183019, 1933053046),
])
def test_lcm(a, b, expected):
    assert lcm(a, b) == expected


if __name__ == '__main__':
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(lcm(a, b))
