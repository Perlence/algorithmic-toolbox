import sys

import pytest


def largest_number(numbers):
    result = ''
    numbers = numbers[:]
    while numbers:
        max_number = ''
        for number in numbers:
            if is_greater_or_equal(number, max_number):
                max_number = number
        result += str(max_number)
        numbers.remove(max_number)
    return int(result)


def is_greater_or_equal(a, b):
    ab = int(str(a) + str(b))
    ba = int(str(b) + str(a))
    if ab >= ba:
        return True
    else:
        return False


@pytest.mark.parametrize('a, b, expected', [
    (2, 21, True),
    (2, 23, False),
    (93, 2, True),
])
def test_is_greater_or_equal(a, b, expected):
    assert is_greater_or_equal(a, b) == expected


@pytest.mark.parametrize('numbers, expected', [
    ([21, 2], 221),
    ([9, 4, 6, 1, 9], 99641),
    ([23, 39, 92], 923923),
])
def test_largest_number(numbers, expected):
    assert largest_number(numbers) == expected

if __name__ == '__main__':
    data = map(int, sys.stdin.read().split())
    a = data[1:]
    print(largest_number(a))
