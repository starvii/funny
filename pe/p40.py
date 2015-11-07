#!/usr/bin/python3
# -*- coding: utf-8 -*-

d = {}
i = 1
n = 0
p = 0
dp = 10 ** p

while 1:
    si = str(i)
    n_bf = n
    n_af = n + len(si)
    n = n_af
    if n_bf < dp and n_af >= dp:
        print(n_bf, n_af, si)
        delta = dp - n_bf - 1
        d[dp] = int(si[delta])
        p += 1
        dp = 10 ** p
    i += 1
    if p > 6:
        break
print(d)
v = 1
for k in d:
    v *= d[k]
print(v)
