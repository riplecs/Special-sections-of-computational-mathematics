import random
from numpy.polynomial import Polynomial as P
import numpy as np
items = [1, 0]
Poly_one = random.choices(items, k=283)
Poly_two = random.choices(items, k=283)
print(Poly_one,'\n', Poly_two)

def MakeX(poly):
    x=[]
    for i in range(282):
        if poly[i]==1:
            t = f'x^{282-i}'
            x.append(t)
    if poly[-1]==1: x.append('1')
    return x
    
    
def PrintX(poly):
    pol=MakeX(poly)
    res=[]
    res.append(' + '.join(pol))
    return res

print('P1 = ', PrintX(Poly_one))

print('P2 = ', PrintX(Poly_two))

def AddPoly(a, b):
    c=[0]
    for i in range(283):
        #print(a[i], b[i])
        if a[i]==1 and b[i]==1:
            c.append(0)
        elif a[i]==0 and b[i]==0:
            c.append(0)
        else: c.append(1)
    return c[1:]

print(PrintX(AddPoly(Poly_one, Poly_two)))

p1 = np.poly1d(Poly_one)
p2 = np.poly1d(Poly_two)
res=p1*p2
for i in range (len(res)):
    res[i]=res[i]%2
gen=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

res2=np.polydiv(res, gen)[1]
for i in range (0, len(res2)+1):
    res2[i]=res2[i]%2
print(res2)