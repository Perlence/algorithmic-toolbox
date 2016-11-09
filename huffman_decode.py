import io
from itertools import islice
import sys

import pytest


def main():
    cli(iter(sys.stdin), sys.stdout)


def cli(it, writable):
    ks, _ = next(it).split()
    k = int(ks)
    codes = {}
    for line in islice(it, k):
        char, code = line.strip().split(': ')
        codes[code] = char
    encoded = next(it)
    print(decode(encoded, codes), file=writable)


def decode(s, codes):
    result = ''
    acc = ''
    for c in s:
        acc += c
        char = codes.get(acc)
        if char is not None:
            result += char
            acc = ''
    return result


@pytest.mark.timeout(5)
@pytest.mark.parametrize('s, codes, expected', [
    ('0', {'0': 'a'}, 'a'),
    ('01001100100111', {'0': 'a', '10': 'b', '110': 'c', '111': 'd'}, 'abacabad'),
    ('10110001', {'10': 'a', '11': 'b', '00': 'c', '01': 'd'}, 'abcd')
])
def test_decode(s, codes, expected):
    assert decode(s, codes) == expected


@pytest.mark.timeout(5)
@pytest.mark.parametrize('inp, expected', [
    ([
        '1 1',
        'a: 0',
        '0',
    ], 'a'),
    ([
        '4 14',
        'a: 0',
        'b: 10',
        'c: 110',
        'd: 111',
        '01001100100111',
    ], 'abacabad'),
])
def test_cli(inp, expected):
    sio = io.StringIO()
    cli(iter(inp), sio)
    out = sio.getvalue().strip()
    assert out == expected

if __name__ == '__main__':
    main()
