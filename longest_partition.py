import sys
from itertools import count

import pytest


def longest_partition(n):
    result = []
    if n == 0:
        return result

    s = 0
    for i in count(1):
        s2 = s + i
        if s2 > n:
            result[-1] += n - s
            break
        result.append(i)
        if s2 == n:
            break
        s = s2

    return result


@pytest.mark.timeout(5)
@pytest.mark.parametrize('n, expected', [
    (0, []),
    (1, [1]),
    (2, [2]),
    (3, [1, 2]),
    (4, [1, 3]),
    (5, [1, 4]),
    (6, [1, 2, 3]),
    (7, [1, 2, 4]),
    (8, [1, 2, 5]),
    (9, [1, 2, 6]),
    (10, [1, 2, 3, 4]),
    (11, [1, 2, 3, 5]),
    (12, [1, 2, 3, 6]),
    (13, [1, 2, 3, 7]),
    (14, [1, 2, 3, 8]),
    (15, [1, 2, 3, 4, 5]),
    (16, [1, 2, 3, 4, 6]),
    (17, [1, 2, 3, 4, 7]),
    (18, [1, 2, 3, 4, 8]),
    (19, [1, 2, 3, 4, 9]),
    (20, [1, 2, 3, 4, 10]),
    (21, [1, 2, 3, 4, 5, 6]),
])
def test_longest_partition(n, expected):
    assert longest_partition(n) == expected

if __name__ == '__main__':
    nums = map(int, sys.stdin.read().split())
    n = next(nums)
    result = longest_partition(n)
    print(len(result), ' '.join(map(str, result)), sep='\n')
