# -*- coding: utf8 -*-

last_num_dict = {1 : 1}

def interval(n_spiral):
    return (n_spiral - 2) * 2 + 1

def last_num(n_spiral):
    if last_num_dict.has_key(n_spiral):
        return last_num_dict[n_spiral]
    if 1 == n_spiral:
        ret = 1
    else:
        ret = last_num(n_spiral - 1) + interval(n_spiral) * 4 + 4
    last_num_dict[n_spiral] = ret
    return ret

def main():
    summ = 1
    i = 1
    while 1:
        i += 1
        a = last_num(i - 1)
        v = interval(i)
        b = last_num(i)
        s = (a + v + 1 + b) * 2
        summ += s
        if v + 2 == 1001:
            break
        #print 'n = {i}, a = {a}, v = {v}, b = {b}, s = {s}, sum = {summ}'.format(a = a, v = v, b = b, s = s, summ = summ, i = i)
    print summ

if __name__ == '__main__':
    main()
