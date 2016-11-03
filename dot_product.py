import sys

import pytest


def max_dot_product(perclick, clicks):
    perclick_so = sorted(perclick, reverse=True)
    clicks_so = sorted(clicks, reverse=True)
    return sum(a * b for a, b in zip(perclick_so, clicks_so))


@pytest.mark.timeout(5)
@pytest.mark.parametrize('perclick, clicks, expected', [
    ([23], [39], 897),
    ([1, 3, -5], [-2, 4, 1], 23),
])
def test_max_dot_product(perclick, clicks, expected):
    assert max_dot_product(perclick, clicks) == expected

if __name__ == '__main__':
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1:(n + 1)]
    b = data[(n + 1):]
    print(max_dot_product(a, b))
