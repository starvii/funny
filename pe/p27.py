# -*- coding: utf8 -*-

# https://projecteuler.net/problem=27

import math

all_primes = set()

def is_prime(n):
    if n in all_primes:
        return 1
    if 2 == n:
        all_primes.add(n)
        return 1
    m = int(math.floor(math.sqrt(n))) + 1
    for i in xrange(2, m):
        if 0 == n % i:
            return 0
    all_primes.add(n)
    return 1

def prime_count(a, b):
    n = 0
    primes = set()
    while 1:
        p = n * n + a * n + b
        if p < 2:
            return 0
        if is_prime(p):
            primes.add(p)
            n = n + 1
        else:
            return len(primes)

def main():
    t = (0, 0, 0)
    for a in xrange(-999, 1000):
        for b in xrange(-999, 1000):
            c = prime_count(a, b)
            if c > t[0]:
                t = (c, a, b)
    print 'max_prime = {max_prime}, a = {a}, b = {b}, a * b = {ab}'.format(max_prime = t[0], a = t[1], b = t[2], ab = t[1] * t[2])

if '__main__' == __name__:
    main()

