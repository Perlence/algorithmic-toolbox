import pytest


def get_change(m):
    if m >= 10:
        return 1 + get_change(m - 10)
    elif m >= 5:
        return 1 + get_change(m - 5)
    elif m > 0:
        return m
    else:
        return 0


@pytest.mark.timeout(5)
@pytest.mark.parametrize('m, expected', [
    (0, 0),
    (2, 2),
    (9, 5),
    (10, 1),
    (11, 2),
    (28, 6),
    (999, 104),
    (1000, 100),
])
def test_get_change(m, expected):
    assert get_change(m) == expected
