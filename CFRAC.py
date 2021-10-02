# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 17:51:36 2021

@author: RIPLECS
"""

import numpy as np
import pandas as pd


TABLE = pd.DataFrame({'S': ['a', 'bmodn', 'b^2modn'], 
                      '-1' : ['-', 1, 0]}).set_index('S')

def factorization_small_n(n):
    numbers = []
    if n < 0:
        numbers.append(-1)
        n = -n
    for i in range(2, int(np.sqrt(n)) + 1):
        while n%i == 0:
            numbers.append(i)
            n /= i 
    if n > 1:
        numbers.append(int(n))
    return numbers

    
def counting_b2(m, n):
    mod = (m**2)%n
    if mod < n/2:
        return mod
    else:
        return mod - n
    
    
def update_factor_base(base, n, num, vectors):
    base_new = base.copy()
    factorize = factorization_small_n(num)
    for f in set(factorize):
        if f not in base_new and f < 100:
            if (n%f)**int(((f-1)/2))%f == 1:
                    base_new.append(f)
    if base_new != base:
        for i in range(len(vectors)):
            factorize_i = factorization_small_n(TABLE[f'{i}'][2])
            vectors[i] = [factorize_i.count(k) for k in base_new]
    vectors.append([factorize.count(i) for i in base_new])
    return sorted(base_new), vectors
  
    
def CFRAC_Brillhart_Morrison(n, v = 1, Beta = [-1, 2], d = 0):
    alpha = np.sqrt(n)
    a = int(alpha)
    u = a
    b = counting_b2(a, n)
    TABLE['0'] = [a, a, b]
    Beta, w = update_factor_base(Beta, n, b, [])
    it = 1
    while True:
        v1 = (n - u**2)/v
        alpha1 = (alpha + u)/v1
        a1 = int(alpha1)
        u1 = v1*a1 - u
        b = (a1*TABLE[f'{it-1}'][1] + TABLE[f'{it-2}'][1])%n
        b2= counting_b2(b, n)
        TABLE[f'{it}'] = [a1, b, b2]
        Beta, w = update_factor_base(Beta, n, b2, w)
        for i in range(len(w)):
            for j in range(i):
                if [(x + y)%2 for x, y in zip(w[i], w[j])] == len(w[i])*[0]:
                    X = TABLE[f'{i}'][1]*TABLE[f'{j}'][1]%n
                    Y = np.sqrt(TABLE[f'{i}'][2]*TABLE[f'{j}'][2])
                    d1 = np.gcd(int(X + Y), n)
                    if 1 < d1 < n:
                        d = d1
                    else:
                        d2 = np.gcd(int(X - Y), n)
                        if 1 < d2 < n:
                            d = d2
        if d == 0:
            it+=1
            u = u1
            v = v1
            a = a1
            continue
        else:
            print(TABLE)
            print('\nФактор-база: ', Beta)
            return d
            break
    
    
print('\nd = ', CFRAC_Brillhart_Morrison(25511))

