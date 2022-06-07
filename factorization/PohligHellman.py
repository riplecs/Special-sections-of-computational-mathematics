# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:00:29 2021

@author: RIPLECS
"""

from CFRAC import factorization_small_n
import numpy as np
import gmpy2

def oiler(n):
    if gmpy2.is_prime(n):
        return n - 1
    count = 0
    for i in range(1, n):
        if gmpy2.gcd(i, n) == 1:
            count += 1
    return count


def CRT(congruences):
    M = np.prod([cong[1] for cong in congruences])
    M_i = [M//cong[1] for cong in congruences]
    invM_i = [gmpy2.invert(int(M_i[i]), int(congruences[i][1])) 
              for i in range(len(M_i))]
    return sum(M_i[i]*invM_i[i]*congruences[i][0] for i in range(len(M_i)))%M


def PohligHellman(alpha, beta, n, order = None):
    if order is None:
        order = oiler(n)
    factor_ord = factorization_small_n(order)
    p =list(set(factor_ord))
    l = [factor_ord.count(i) for i in p]
    congruences = []
    for p_i in p:
        r, x = [], []
        for j in range(p_i):
            r.append(int(gmpy2.powmod(alpha, order*j//p_i, n)))
        comb = 1
        for l_i in range(l[p.index(p_i)]):
            x.append(r.index(int(gmpy2.powmod(comb*beta, 
                                                  order//(p_i**(l_i+1)), n))))
            comb *= gmpy2.invert(alpha**(x[-1]*p_i**l_i), n)%n
        congruences.append((sum([x[j]*p_i**j for j in range(l[p.index(p_i)])]), 
                                                        p_i**l[p.index(p_i)]))
    return CRT(congruences)


print('x = ', PohligHellman(5, 11, 97))
print('x = ', PohligHellman(3, 148, 181))
print('x = ', PohligHellman(9704, 13896, 17389, 1242))
