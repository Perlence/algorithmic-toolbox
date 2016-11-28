import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, w):
    a = next(it).strip()
    b = next(it).strip()
    print(levenshtein_distance(a, b), file=w)


def levenshtein_distance(a, b):
    la1 = len(a) + 1
    lb1 = len(b) + 1
    d = [[None] * lb1 for i in range(la1)]
    for i in range(la1):
        d[i][0] = i
    for j in range(lb1):
        d[0][j] = j

    for i in range(1, la1):
        for j in range(1, lb1):
            c = int(a[i-1] != b[j-1])
            d[i][j] = min(d[i-1][j] + 1,
                          d[i][j-1] + 1,
                          d[i-1][j-1] + c)

    return d[-1][-1]


def stress(full=False):
    import random
    import string

    if not full:
        n = int(6)
        m = random.randint(2, 6)
    else:
        n = int(1e2)
        m = random.randint(0, 1e2)
    while True:
        def randstr(n):
            return ''.join([random.choice(string.ascii_lowercase)
                            for _ in range(n)])
        yield randstr(n), randstr(m)


@pytest.mark.timeout(2)
@pytest.mark.parametrize('inp, expected', [
    ([
        'ab',
        '',
    ], [
        '2',
    ]),
    ([
        'ab',
        'ab',
    ], [
        '0',
    ]),
    ([
        'short',
        'ports',
    ], [
        '3',
    ]),
    ([
        'google',
        'schmugle',
    ], [
        '5',
    ]),
    ([
        'levenshtein distance',
        'edit distance',
    ], [
        '9',
    ]),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().splitlines()
    assert out == expected


def test_stress():
    import editdistance
    for a, b in islice(stress(full=True), 100):
        assert levenshtein_distance(a, b) == editdistance.eval(a, b)


@pytest.mark.timeout(2)
@pytest.mark.parametrize('a, b', islice(stress(full=True), 3))
def test_bench(a, b):
    levenshtein_distance(a, b)

if __name__ == '__main__':
    main()
