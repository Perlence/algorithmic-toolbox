import sys

import pytest


def dots(starts, ends):
    so = sorted(zip(starts, ends), key=lambda se: se[1])
    result = set()
    while so:
        _, d = so.pop(0)
        result.add(d)
        for s, e in so[:]:
            if s <= d <= e:
                so.remove((s, e))
            else:
                break
    return result


@pytest.mark.timeout(5)
@pytest.mark.parametrize('starts, ends, expected', [
    ([1, 2, 3], [3, 5, 6], {3}),
    ([4, 1, 2, 5], [7, 3, 5, 6], {3, 6}),
])
def test_dots(starts, ends, expected):
    assert dots(starts, ends) == expected

if __name__ == '__main__':
    nums = list(map(int, sys.stdin.read().split()))
    n = nums[0]
    starts = nums[1:(2*n + 2):2]
    ends = nums[2:(2*n + 2):2]
    ds = dots(starts, ends)
    print(len(ds), ' '.join(map(str, ds)), sep='\n')
