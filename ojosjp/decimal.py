# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals


def encode(n, l=10, chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ'):
    s = ''
    while n != 0:
        s = chars[int(n % len(chars))] + s
        n = n - n % len(chars)
        n = n / len(chars)
    return (chars[0] * (l - len(s))) + s


def decode(s, chars='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJELMNOPQRSTUVWXYZ'):
    s = s.lstrip(chars[0])
    n = 0
    for c in s:
        n = n * len(chars)
        n = n + chars.index(c)
    return n
