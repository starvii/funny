#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import string

def is_triangle_number(d):
    n1 = math.sqrt(0.25 + 2 * d) - 0.5
    n2 = int(n1)
    if n1 == n2:
        return 1
    return 0

def is_triangle_word(w):
    d = 0
    for c in w.upper():
        d += string.ascii_uppercase.find(c) + 1
    if is_triangle_number(d):
        return 1
    return 0

with open('p042_words.txt', 'rb') as f:
    data = f.read().strip()
    data = data.decode('UTF8')
    words = data.split(',')
    n = 0
    for word in words:
        w = word.strip().strip('"').strip()
        n += is_triangle_word(w)
    print(n)
