# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 17:51:36 2021

@author: RIPLECS
"""

import numpy as np
import pandas as pd
import itertools
import math


pd.set_option('display.max_columns', 30)


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
    
    
def update_factor_base(base, n, num, vectors, table, limit):
    base_new = base.copy()
    factorize = factorization_small_n(num)
    for f in set(factorize):
        if f not in base_new and f < limit:
            if (n%f)**int(((f - 1)/2))%f == 1:
                    base_new.append(f)
    base_new = sorted(base_new)
    if len(base_new) != len(base):
        for i in range(len(vectors)):
            factorize_i = factorization_small_n(table[f'{i}'][2])
            vectors[i] = [factorize_i.count(k) for k in base_new]
    if np.in1d(factorize, base_new).all():
        vectors.append([factorize.count(j) for j in base_new])
    else:
        vectors.append(None)
    return base_new, vectors
  
  
def combination(List):
    result = []
    for l in range(1, len(List)+1):
        for i in itertools.combinations(List, l):
            if List[-1] in comb and None not in comb:
                    result.append(list(i))
    return result

  
def sum_vectors(vectors):
    result = []
    for i in range(len(vectors[0])):
        result.append(sum(vectors[j][i] for j in range(len(vectors)))%2)
    return result
  
  
def CFRAC_Brillhart_Morrison(n, lim, v = 1, Beta = [-1, 2], d = 0):
    TABLE = pd.DataFrame({'S': ['a', 'bmodn', 'b^2modn'], 
                         '-1' : ['-', 1, 0]}).set_index('S')
    alpha = math.sqrt(n)
    a = int(alpha)
    u = a
    b = counting_b2(a, n)
    TABLE['0'] = [a, a, b]
    Beta, w = update_factor_base(Beta, n, b, [], TABLE, lim)
    it = 1
    while True:
        v1 = (n - u**2)/v
        alpha1 = (alpha + u)/v1
        a1 = int(alpha1)
        u1 = v1*a1 - u
        b = (a1*TABLE[f'{it-1}'][1] + TABLE[f'{it-2}'][1])%n
        b2= counting_b2(b, n)
        TABLE[f'{it}'] = [a1, b, b2]
        Beta, w = update_factor_base(Beta, n, b2, w, TABLE, lim)
        for comb in combination(w):
            if sum_vectors(comb) == (len(Beta))*[0]:
                X, Y = 1, 1   
                for vec in comb[:-1]:
                    X = float(X*TABLE[f'{w.index(vec)}'][1]%n)
                    Y = float(Y*TABLE[f'{w.index(vec)}'][2])
                X = X*TABLE[f'{it}'][1]%n
                Y = math.sqrt(Y*TABLE[f'{it}'][2])
                d1 = np.gcd(int(X + Y), n)
                if 1 < d1 < n:
                    d = d1
                    break
                else:
                    d2 = np.gcd(int(X - Y), n)
                    if 1 < d2 < n:
                        d = d2
                        break
        if d == 0:
            it+=1
            if it > 21:
                return 0
            u = u1
            v = v1
            a = a1
        else:
            print(TABLE)
            print('\nФактор-база: ', Beta)
            for vec in comb[:-1]:
                print(f'\nν_{w.index(vec)} = {w[w.index(vec)]}')
            print(f'\nν_{it} = {w[it]}')
            return d
    
    
def factorization(n, lim = 50):
    result = CFRAC_Brillhart_Morrison(n, lim)
    while result == 0:
        lim += 50
        result = CFRAC_Brillhart_Morrison(n, lim)
    return result    


print('\nd = ', factorization(21299881))

