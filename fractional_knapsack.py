import sys

import pytest


def get_optimal_value_recursive(capacity, values, weights):
    if capacity == 0 or not weights or not values:
        return 0
    so = sorted(zip(values, weights), key=lambda vw: vw[0] / vw[1], reverse=True)
    return _get_optimal_value(capacity, so)


def _get_optimal_value(capacity, vws, outvalue=0):
    if capacity == 0 or not vws:
        return outvalue
    value, weight = vws[0]
    if weight <= capacity:
        return _get_optimal_value(capacity - weight, vws[1:], outvalue + value)
    else:
        return _get_optimal_value(0, [], outvalue + value*capacity/weight)


def get_optimal_value_loop(capacity, values, weights):
    result = 0
    vws = sorted(zip(values, weights), key=lambda vw: vw[0] / vw[1], reverse=True)
    while capacity > 0 and vws:
        value, weight = vws.pop(0)
        if weight <= capacity:
            result += value
            capacity -= weight
        else:
            result += value*capacity/weight
            capacity = 0
    return result

# get_optimal_value = get_optimal_value_recursive
get_optimal_value = get_optimal_value_loop


@pytest.mark.timeout(5)
@pytest.mark.parametrize('capacity, weights, values, expected', [
    (50, [60, 100, 120], [20, 50, 30], 180),
    (10, [500], [30], 166.66666666666666),
])
def test_get_optimal_value(capacity, weights, values, expected):
    assert get_optimal_value(capacity, weights, values) == expected


def stress():
    from random import randint

    n = randint(1, 1e3)
    capacity = randint(0, 2e6)
    values = [randint(0, 2e6) for _ in range(n)]
    weights = [randint(0, 2e6) for _ in range(n)]
    return capacity, values, weights

if __name__ == '__main__':
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = get_optimal_value(capacity, values, weights)
    print("{:.3f}".format(opt_value))
