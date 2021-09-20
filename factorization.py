# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:33:15 2021

@author: RIPLECS
"""


import numpy as np


def classicPollard(x0, n, func):
    x = [x0]
    triger = False
    while True:
        x.append(func(x[-1], n))
        print(f'x{len(x) - 1} = {x[-1]}: ')
        for el in x[:-1]:
            gcd = np.gcd(x[-1] - el, n)
            print(5*' ' + f'НСД(x{len(x) - 1} - x{x.index(el)}, {n}) = {gcd}')
            if gcd!=1:
                print(f'Відповідь: d = {gcd}')
                triger = True
                break
        if triger == True:
            break
        
        
        
def FloydModification(x0, n, func):
    x = [x0, func(x0, n)]
    j = 2
    while True:
        x.append(func(x[-1], n))
        h = 1
        while j < 2**h or j >= 2**(h + 1):
            h+=1
        k = 2**h - 1
        gcd = np.gcd(x[j] - x[k], n)
        print(f'j = {j}, k = {k}:')
        print(5*' ' + f'(x{k}, x{j}) = ({x[k]}, {x[j]})')
        print(5*' ' + f'НСД(x{j} - x{k}, {n}) = ', gcd)
        if gcd!=1:
            print(f'Відповідь: d = {gcd}')
            break
        j+=1
        
        
        
def twoKmodification(x0, n, func):
    x = [x0, func(x0, n)]
    triger = False
    while True:
        x.append(func(x[-1], n))
        if len(x)%2 == 1:
            for j in range(1, len(x)//2):
                gcd = np.gcd(x[2*j] - x[j], n)
                print(f'x{j} = {x[j]}, x{2*j} = {x[2*j]}:')
                print(5*' ' + f'НСД(x{2*j} - x{j}, {n}) = ', gcd)
                if  gcd != 1:
                    print(f'Відповідь: d = {gcd}')
                    triger = True
                    break
        if triger == True:
            break
        
        
def f(x, n):
    return (x**2 + 1)%n

def Ferma(n):
    x = int(np.sqrt(n))
    y = 0
    r = x**2 - y**2 - n
    it = 1
    while r != 0:
        if r>0:
            y+=1
            print(f'{it}) r = ', r, f'> 0 => x = {x}, y = {y}')
        else:
            x+=1
            print(f'{it}) r = ', r, f' < 0 => x = {x}, y = {y}')
        r = x**2 - y**2 - n
        it+=1
    print(f'{it}) r = ', r, f' => p = x + y = {x + y}, q = x - y = {x - y}')
Ferma(200819)

print('Examples: ')
print("\nPollard's Ro-method of factorization: ")
classicPollard(1, 8051, f)
print("\nFloyd's modification: ")
FloydModification(1, 8051, f)
print("\n2k modification: ")
twoKmodification(1, 8051, f)
print('Ferma method: ')
Ferma(8051)
