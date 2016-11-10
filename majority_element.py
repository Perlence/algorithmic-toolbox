from collections import Counter, defaultdict
import io
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    next(it)  # count
    seq = list(map(int, next(it).split()))
    print(int(majority_element(seq)), file=w)


def majority_element_counter(seq):
    return max(Counter(seq).values()) > len(seq) / 2


def majority_element_custom_counter(seq):
    count = defaultdict(int)
    halflen = len(seq) / 2
    for x in seq:
        count[x] += 1
        if count[x] > halflen:
            return True
    return False


def majority_element_divide(seq):
    if len(seq) < 3:
        return False
    elif len(seq) == 3:
        return len(Counter(seq)) < 3
    else:
        mid = int(len(seq) / 2)
        return majority_element(seq[:mid]) or majority_element(seq[mid:])

# majority_element = majority_element_counter
# majority_element = majority_element_custom_counter
majority_element = majority_element_divide


@pytest.mark.timeout(3)
@pytest.mark.parametrize('inp, expected', [
    ([
        '5',
        '2 3 9 2 2',
    ], [
        '1',
    ]),
    ([
        '4',
        '1 2 3 4',
    ], [
        '0',
    ]),
    ([
        '4',
        '1 2 3 1',
    ], [
        '0',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected

if __name__ == '__main__':
    main()
