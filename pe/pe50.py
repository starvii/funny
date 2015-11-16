#!/usr/bin/python3
# -*- coding: utf-8 -*-

N = 1000000
PrimeList = []


def IsPrime(n):
    if n < 2:
        return 0
    elif n == 2:
        return 1
    if n in PrimeList:
        return 1
    for p in PrimeList:
        if p ** 2 >= n + 1:
            return 1
        if n % p == 0:
            return 0

def NextPrime():
    global PrimeList
    if len(PrimeList) == 0:
        PrimeList = []
        n = 2
    else:
        n = PrimeList[-1]
        while 1:
            n = n + 2 if n % 2 == 1 else n + 1
            if IsPrime(n):
                break
    PrimeList.append(n)
    return n

# 在 primelist 中，获取一个从 start_idx 开始，之和不超过 N 的子列表
def GetALessNList(start_idx):
    s, i = 0, start_idx
    while s < N:
        while i >= len(PrimeList):
            NextPrime()
        s += PrimeList[i]
        i += 1
    sl = PrimeList[start_idx : i - 1]
    return sl

# 列表 sublist 由后向前计算每个子列表和，判断是否为素数
# 第一个出现的素数，即为此 sublist 中最多连续数之和的素数
def GetAMostSumPrimeFromSubList(sublist):
    pl = sublist
    while len(pl) > 1:
        p = sum(pl)
        if IsPrime(p):
            return p, len(pl)
        pl.pop()

# 计算 N 以内，由最多连续素数之和组成的素数。
def CalcTheMostSumPrime():
    idx = 0
    maxsubprime = None
    maxprime = None
    while 1:
        sublist = GetALessNList(idx)
        if maxsubprime: # 如果子序列长度小于连续素数长度，即可退出循环
            if len(sublist) <= maxsubprime:
                break
        p, lp = GetAMostSumPrimeFromSubList(sublist)
        if not maxsubprime or lp > maxsubprime:
            maxprime, maxsubprime = p, lp
        idx += 1
    print(maxprime, maxsubprime)



def main():
    CalcTheMostSumPrime()

if __name__ == '__main__':
    main()
