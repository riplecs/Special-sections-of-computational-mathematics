# -*- coding: utf-8 -*-
"""
Created on Tue May 25 11:12:13 2021

@author: RIPLECS
"""


import random
import numpy as np


def MakeGen(m, b, c, d, k):
    res = [0]*(m+1)
    res[m] = res[b] = res[c] = res[d] = res[k] = 1
    return res[::-1]


def MakeX(poly):
    x = []
    for i in range(m - 1):
        if poly[i] == 1:
            t = f'x^{m - 1 - i}'
            x.append(t)
    if poly[-1] == 1: 
        x.append('1')
    if x == []: 
        x == [0]*m
    return x
       
def PrintX(poly):
    pol = MakeX(poly)
    res = []
    res.append(' + '.join(pol))
    return res


def AddPoly(a, b):
    c = [0]
    for i in range(m):
        c.append(((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0))%2)
    return (c if len(c) <= m else c[(len(c) - m):])


def PolyMod(a, g):
    final = np.polydiv(a, g)[1]
    for i in range (0, len(final) + 1):
        final[i] = final[i]%2
    return np.array(final)


def MulPoly(a, b):
    p1 = np.poly1d(a)
    p2 = np.poly1d(b)
    res = p1*p2 
    for i in range (0, len(res) + 1):
        res[i] %= 2
    return PolyMod(res, GEN)


def SquarePoly(a):
    res = a
    i = 1
    while i < len(res):
        if i%2 == 1:
            res.insert(i, 0)
        i += 1
    return PolyMod(np.poly1d(res), GEN)


def Trace(a):
    res = 0
    deg = 0
    while deg < m:
        res += int(Convert(PowPoly(a, ((2**deg)%(2**m - 1)))), 2)
        deg += 1
        print(deg)
    return res%2


def PowPoly(a, n):
    if n == 0: 
        return [1]
    elif n%2 == 0:
        return PowPoly(MulPoly(a, a), n//2)
    else:
        return MulPoly(PowPoly(MulPoly(a, a), n//2), a)


def Reverse(a):
    return PowPoly(a, 2**m - 2)


def Convert(a):
    res=[0]*(len(a))
    for i in range(len(a)):
        res[i] = str(int(a[i]))
    result = ''.join(res)
    return result


def Deconvert(a):
    return list(map(int, a))


print('Enter the m - the field dimension:')
m = int(input('dimension: '))
print('Choose to what degrees the coefficients are equal to 1 (start from the biggest):')
k, k1, k2, k3 = int(input('degrees: ')), int(input()), int(input()), int(input())
GEN = np.poly1d(MakeGen(m, k, k1, k2, k3))
print(GEN, ' - field generator ')

print('Enter 1 if you wants randomly generate inputs data or enter 2 to fill in it by yourself: ')
choise = input()
if choise == '1':
    items = [1, 0]
    Poly_one = random.choices(items, k=m)
    Poly_two = random.choices(items, k=m)
    Poly_one_copy = Poly_one.copy()
    Poly_two_copy = Poly_two.copy()
    print('A = ', PrintX(Poly_one))
    print('B = ', PrintX(Poly_two))
    print('A = ', hex(int(Convert(Poly_one), 2))[2:].swapcase())
    print('B = ', hex(int(Convert(Poly_two), 2))[2:].swapcase())
    print('A + B = ', hex(int(Convert(AddPoly(Poly_one, Poly_two)), 2))[2:].swapcase())
    print('A*B = ', hex(int(Convert(MulPoly(Poly_one, Poly_two)), 2))[2:].swapcase())
    print('A^2 = ', hex(int(Convert(SquarePoly(Poly_one)), 2))[2:].swapcase())
    print('Enter the degree you want the polynom to raise in: ')
    n = int(input('n in dec = '))
    k = hex(n)[2:].swapcase()
    print('n in hex = ', k)
    print(f'A^{k} = ', hex(int(Convert(PowPoly(Poly_one_copy, n)), 2))[2:].swapcase())
    #print('Tr(A) = ', Trace(Poly_one_copy))
    #print('Tr(A) = ', hex(int(Convert(Trace(Poly_one_copy)), 2))[2:].swapcase())
    print('A^-1 = ', hex(int(Convert(Reverse(Poly_one_copy)), 2))[2:].swapcase())
    print('Сorrectness tests:')
    print(f'A^(2^{m}-1) = ', hex(int(Convert(PowPoly(Poly_one_copy, 2**m-1)), 2))[2:].swapcase())


if choise == '2':
    Poly_1 = input('Enter first polynom: A = ')
    Poly_one = Deconvert(str(bin(int(f'0x{Poly_1.swapcase()}', 16)))[2:])
    while len(Poly_one) < m: 
        Poly_one.insert(0, 0)
    Poly_2 = input('Enter second polynom: B = ')
    Poly_two = Deconvert(bin(int(f'0x{Poly_2.swapcase()}', 16))[2:])
    while len(Poly_two) < m: 
        Poly_two.insert(0, 0)
    print('A = ', PrintX(Poly_one))
    print('B = ', PrintX(Poly_two))
    print('A + B = ', hex(int(Convert(AddPoly(Poly_one, Poly_two)), 2))[2:].swapcase())
    print('A*B = ', hex(int(Convert(MulPoly(Poly_one, Poly_two)), 2))[2:].swapcase())
    print('A^2 = ', hex(int(Convert(SquarePoly(Poly_one)), 2))[2:].swapcase())
    Poly_one = Deconvert(bin(int(f'0x{Poly_1.swapcase()}', 16))[2:])
    print('Enter the degree you want the polynom to raise in: ')
    n = int(input('n in dec = '))
    k = hex(n)[2:].swapcase()
    print('n in hex = ', k)
    Poly_one = Deconvert(bin(int(f'0x{Poly_1.swapcase()}', 16))[2:])
    Poly_two = Deconvert(bin(int(f'0x{Poly_2.swapcase()}', 16))[2:])
    print(f'A^{k} = ', hex(int(Convert(PowPoly(Poly_one, n)), 2))[2:].swapcase())
    #print('Tr(A) = ', Trace(Poly_one_copy))
    print('A^-1 = ', hex(int(Convert(Reverse(Poly_one)), 2))[2:].swapcase())
    print('Сorrectness tests:')
    print(f'A^(2^{m}-1) = ', hex(int(Convert(PowPoly(Poly_one, 2**m-1)), 2))[2:].swapcase())
    
    
###########     NORMAL BASIS    ########### 
    
def MakeBasis(m):
    x = []
    for i in range(m):
        t = f'x^{2**i}'
        x.append(t)
    res = []
    res.append(', '.join(x))
    return res


def Trace(a):
    res = 0
    for i in range(len(a)):
        res += a[i]
    return res%2


def SquarePoly(a):
    return a[-1:] + a[:-1]


def MakeMatrix(m):
    p = 2*m + 1
    matrix = np.zeros((m, m))
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            if (2**i + 2**j)%p == 1 or (2**i - 2**j)%p == 1 or (-2**i + 2**j)%p == 1 or (-2**i - 2**j)%p == 1:
                matrix[:,i][j] = 1
    return matrix


def MulPoly(a, b):
    while len(a) > m: 
        del a[0]
    while len(b) > m: 
        del b[0]
    if a == [1]: 
        return b
    res = m*[0]
    M = MakeMatrix(m)
    for i in range(m):
        res[i] = np.array(np.array(a[i:] + a[:i]).dot(M))
        for j in range(len(res[i])):
            res[i][j] %= 2
        res[i] = int(res[i].dot(np.array([b[i:] + b[:i]]).transpose()))%2
    return (res)


def ItohTsujiiReverse(a):
    x = bin(m - 1)[2:]
    t = len(x) - 1
    beta = a
    k = 1
    for i in reversed(range(0, t)):
        beta = MulPoly(PowPoly(beta, 2**k), beta)
        k *= 2
        if x[::-1][i] == '1':
            beta = MulPoly(SquarePoly(beta), a)
            k += 1
    beta = SquarePoly(beta)
    return beta


def PowPoly(a, n):
    if n == 0: 
        return [1]
    elif n%2 == 0:
        return PowPoly(SquarePoly(a), n//2)
    else:
        return MulPoly(PowPoly(SquarePoly(a), n//2), a)
    
    
print('Enter the m - the field dimension:')
m = int(input('dimension: '))
print('Enter 1 if you wants randomly generate inputs data or enter 2 to fill in it by yourself: ')
choise = input()
if choise == '1':
    items = [1, 0]
    AA = random.choices(items, k = m)
    BB = random.choices(items, k = m)
    print('A = ', hex(int(Convert(AA), 2))[2:].swapcase())
    print('B = ', hex(int(Convert(BB), 2))[2:].swapcase())
    print('Λ = ', MakeMatrix(m))
    print('A + B = ', hex(int(Convert(AddPoly(AA, BB)), 2))[2:].swapcase())
    print('A^2 = ', hex(int(Convert(SquarePoly(AA)), 2))[2:].swapcase())
    print('A*B = ', hex(int(Convert(MulPoly(AA, BB)), 2))[2:].swapcase())
    print('Tr(A) = ', Trace(AA))
    n = int(input('n in dec = '))
    k = hex(n)[2:].swapcase()
    print('n in hex =', k)
    print(f'A^{k} = ', hex(int(Convert(PowPoly(AA, n)), 2))[2:].swapcase())
    print('A^-1 by Itoh Tsujii algorithm = ', hex(int(Convert(ItohTsujiiReverse(AA)), 2))[2:].swapcase())
    print('A^-1 = ', hex(int(Convert(PowPoly(AA, 2**m-2)), 2))[2:].swapcase())
    print('Сorrectness tests:')
    C = Convert(PowPoly(AA, 2**m-1))
    if ('0' in C) is False:
        print(f'A^(2^{m}-1) = ' + '1')
    else: print('ERROR')
    print('(A+B)^2 = ', hex(int(Convert(SquarePoly(AddPoly(AA, BB))), 2))[2:].swapcase())
    print('A^2 + B^2 = ', hex(int(Convert(AddPoly(SquarePoly(AA), SquarePoly(BB))), 2))[2:].swapcase())
    print('(A+B)*C = ', hex(int(Convert(MulPoly(AddPoly(AA, BB), C)), 2))[2:].swapcase())
    print('A*C + B*C = ', hex(int(Convert(AddPoly(MulPoly(AA, C), MulPoly(C, BB))), 2))[2:].swapcase())
if choise == '2':
    Poly_1 = input('Enter first polynom: A = ')
    AA = Deconvert(str(bin(int(f'0x{Poly_1.swapcase()}', 16)))[2:])
    Poly_2 = input('Enter second polynom: B = ')
    BB = Deconvert(str(bin(int(f'0x{Poly_2.swapcase()}', 16)))[2:])
    print('Λ = ', MakeMatrix(m))
    print('A + B = ', hex(int(Convert(AddPoly(AA, BB)), 2))[2:].swapcase())
    print('A^2 = ', hex(int(Convert(SquarePoly(AA)), 2))[2:].swapcase())
    print('A*B = ', hex(int(Convert(MulPoly(AA, BB)), 2))[2:].swapcase())
    print('Tr(A) = ', Trace(AA))
    n = int(input('n in dec = '))
    k = hex(n)[2:].swapcase()
    print('n in hex = ', k)
    print(f'A^{k} = ', hex(int(Convert(PowPoly(AA, n)), 2))[2:].swapcase())
    print('A^-1 by Itoh Tsujii algorithm = ', hex(int(Convert(ItohTsujiiReverse(AA)), 2))[2:].swapcase())
    print('A^-1 = ', hex(int(Convert(PowPoly(AA, 2**m-2)), 2))[2:].swapcase())
    print('Сorrectness tests:')
    C = Convert(PowPoly(AA, 2**m-1))
    if '0' not in C:
        print(f'A^(2^{m}-1) = ' + '1')
    else: 
        print('ERROR')
    print('(A+B)^2 = ', hex(int(Convert(SquarePoly(AddPoly(AA, BB))), 2))[2:].swapcase())
    print('A^2 + B^2 = ', hex(int(Convert(AddPoly(SquarePoly(AA), SquarePoly(BB))), 2))[2:].swapcase())
    print('(A+B)*C = ', hex(int(Convert(MulPoly(AddPoly(AA, BB), C)), 2))[2:].swapcase())
    print('A*C + B*C = ', hex(int(Convert(AddPoly(MulPoly(AA, C), MulPoly(C, BB))), 2))[2:].swapcase())
