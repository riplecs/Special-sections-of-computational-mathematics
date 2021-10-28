# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:50:51 2021

@author: RIPLECS
"""

from CFRAC import factorization_small_n, sum_vectors
import pandas as pd
import numpy as np
import itertools 
import gmpy2
import math 


PRIMES = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 43]


def q(x, m, n):
    return (x + m)**2 - n
  
    
def combination(List):
    result = []
    for l in range(1, len(List)+1):
        for comb in itertools.combinations(List, l):
            result.append(list(comb))
    return result


def square_modulo_root(a, p):
    if (p - 3)%4 == 0:
        x = a**((p - 3)//4 + 1)%p
        return x, p - x
    elif (p - 5)%8 == 0:
        k = (p - 5)//8
        if a**(2*k + 1)%p == 1:
            x = a**(k + 1)%p
            return x, p - x
        else:
            x = a**(k + 1)*2**(2*k + 1)%p
            return x, p - x
    else:
        k = (p - 1)//8
        d, s = gmpy2.remove(p - 1, 2)
        for num in PRIMES:
            if gmpy2.legendre(num, p) == -1:
                b = num
                break
        ta, tb = (p - 1)//2, 0
        for r in range(s - 1):
            ta //= 2
            tb //= 2
            if a**ta*b**tb%p == p - 1:
                tb += (p - 1)//2
        x = a**((d + 1)//2)*b**(tb//2)%p
        return x, p - x
    
        
# solving congruences kind of (x + m)**2 - n == 0 mod p       
def congruence(m, n, p):
    b = 2*m%p
    c = (m**2 - n)%p
    if b == c == 0:
        return 0, 0
    if b == 0 and abs(c) == 1 and p == 2:
        return 1, -1
    if b == 0:
        return square_modulo_root(-c, p)
    if c == 0:
        return 0, -b
    inv2 = gmpy2.invert(2, p)
    inv4 = gmpy2.invert(4, p)
    x1, x2 = square_modulo_root(inv4*b**2 - c, p)
    return x1 - inv2*b, x2 - inv2*b
    

def find_x(sign, mas, x, p, lim):
    while abs(x) <= lim:
        if x not in mas:
            mas.append(x)
        if sign == '+':
            x += p
        else:
            x -= p
    return mas


def eratosthenes(n, lim, Beta = [-1, 2]):
    for num in PRIMES[1:]:
        if gmpy2.legendre(n, num) == 1:
            Beta.append(num)
            if len(Beta) == lim + 1:
                break
    m = int(math.sqrt(n))
    df = pd.DataFrame({'x': -lim, 'x + m': 0, 'b': q(-lim, m, n)}, index = [0])
    for x in range(-lim + 1, lim + 1):
        df = df.append({'x': x, 'x + m': x + m, 'b': q(x, m, n)}, 
                       ignore_index = True)
    df['lgb'] = [math.log(abs(b), 10) for b in df['b']]
    for p in Beta[1:]:
        X = []
        for x in congruence(m, n, p):
            X = find_x('+', X, x, p, lim)
            X = find_x('-', X, x, p, lim)
        if X == []:
            Beta.remove(p)
        else:
            df[f'lg{p}'] = [(1 if df['x'][i] in X else 0) 
                            for i in range(len(df))]
    diff = []
    for i in range(len(df)):
        ans = df['lgb'][i]
        for p in Beta[1:]:
            ans -= math.log(p, 10)*df[f'lg{p}'][i]
        diff.append(ans)
    df['Q(x)'] = diff
    potential_Beta_numbers = df['b'][df['Q(x)'] < 
                                     np.mean(df['Q(x)'])].values.tolist()
    vectors, Beta_numbers  = [], []
    for num in potential_Beta_numbers:
        factorization = factorization_small_n(num)
        if np.in1d(factorization, Beta).all():
            Beta_numbers.append(num)
            vectors.append([factorization.count(j) for j in Beta])
    df['v'] = [(vectors[Beta_numbers.index(num)] 
                if num in Beta_numbers else 'Not Beta') 
               for num in df['b']]
    for comb in combination(vectors):
        if sum_vectors(comb) == len(Beta)*[0]:
            X, Y = 1, 1
            for v in comb:
                X *= int(df['x + m'][df['b'] == Beta_numbers[vectors.index(v)]])
                Y *= int(abs(Beta_numbers[vectors.index(v)]))
            Y = int(math.sqrt(Y))
            d = np.gcd(X + Y, n)
            if 1 < d < n:
                return d, df
            d = np.gcd(X - Y, n)
            if 1 < d < n:
                return d, df
    return 0
            

def factorization(n, lim = 5):
    d = eratosthenes(n, lim)
    while d == 0:
        lim  = lim**2
        d = eratosthenes(n, lim)
    print(d[1])
    return d[0]


print('\nd = ', factorization(91))
print('\nd = ', factorization(8931721))
