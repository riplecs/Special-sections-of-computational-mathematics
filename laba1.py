import math


def parcer(obj, n):
    args = [iter(obj)]*n
    return zip(*args)


def from_hex(hexnum):
    n = math.ceil(len(hexnum)/8)
    hexs = []
    decs = []
    if len(hexnum)%8 == 0:
        hexs = [''.join(i) for i in parcer(hexnum, 8)]
    else:
        zeros = 8*n - len(hexnum)
        strzeros = zeros*'0'
        finalhex = strzeros + hexnum
        hexs = [''.join(i) for i in parcer(finalhex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs


def to_hex(num):
    if num == [0]: 
        return '0'
    i = len(num) - 1
    while num[i] == 0:
        i -= 1
        if i == -1:
            return '0'
    num.reverse()
    hexnum = ''
    for i in range(len(num)):
        hex_el = hex(num[i])[2:]
        if len(hex_el) != 8:
            zeros = (8 - len(hex_el))*'0'
            hex_str = zeros + hex_el
            hexnum += hex_str
        else:
            hexnum += hex_el
        hexnum = hexnum.lstrip('0')
    num.reverse()
    return hexnum.swapcase()

A=from_hex('94EDE1A444B9738ADF06CDB40DCAFA87B25A8BECA2D2262A53D8431A119405F0CBEFB83D2AD547CCE3AE74A8EC74A313C8BED20D4349D9EFBA356FE6E8AD89E2')
B=from_hex('5BCC0B222EE17877C9EB60FA91632BC7A6E29D80F02CD3FE16B5C2A2231B43DB2B2D12F21B293AAF49FE1165CB7A21D12D6ACEC225285544B36BABD3F8B4DD8D')
N=from_hex('269D7722EA018F2AC35C5A3517AA06EAA1949059AE8240428BBFD0A8BE6E2EBF91223991F80D7413D6B2EB213E7122710EDEC617460FA0191F39016046199720')
C=from_hex('791EDB102DA183759979CEF70E1405AF14B98CD44357EADF6A8E35E49F99BB56CBD3F68897D6E05502ED1DE14EC46D04F96992C2D129737987E84E62371648B3')


def LongAdd(a, b):
    maxlen = max(len(a), len(b))
    shift = 0
    c = []
    for i in range(maxlen):
            tempA = int(a[i]) if i<len(a) else 0
            tempB = int(b[i]) if i<len(b) else 0
            temp = tempA + tempB + shift
            c.append(temp & (2**32 - 1))
            shift = temp >> 32
    if shift > 0:
        c.append(shift)
    return c


print('A + B = ' + to_hex(LongAdd(A, B)))


def LongSub(a, b):
    borrow = 0
    d = []
    maxlen = max(len(a), len(b))
    for i in range(maxlen):
            tempA = int(a[i]) if i < len(a) else 0
            tempB = int(b[i]) if i < len(b) else 0
            temp = tempA - tempB - borrow
            if temp >= 0:
                d.append(temp)
                borrow = 0
            else:
                d.append((2**32 + temp))
                borrow = 1
    if borrow != 0:
        return None
    else:
        return d
 

print('A - B = ' + to_hex(LongSub(A, B)))
    
    
def LongMulOneDigit(a, k):
    shift = 0
    e = []
    for i in range (len(a)):
        temp = int(a[i])*k + shift
        e.append(temp&(2**32 - 1))
        shift = temp >> 32
    e.append(shift)
    return e


def LongCmp(a, b):
    if a != [0]: 
        while a[len(a)-1] == 0: 
            del a[len(a)-1]
    if b != [0]: 
        while b[len(b)-1] == 0: 
            del b[len(b)-1]
    if len(a) == len(b):
        i = max(len(a), len(b)) - 1
        while a[i] == b[i]:
            i -= 1
            if i == -1:
                return 0
        else:
            if a[i] > b[i]:
                return 1
            else:
                return -1
    elif len(a) > len(b):
            return 1
    else:
        return -1

    
 print('Comparison of results:\n')
 cmp = LongCmp(A, B)
 if cmp == 1: 
    print('A>B')
 elif cmp == 0: 
    print('A=B')
 else: 
    print('A<B')
    
    
 def LongShiftDigitsToHigh(n, l):
    for i in range(l):
        n.insert(0, 0)
    return n
 
def LongMul(a, b):
    if LongCmp(a , b) == -1: 
        return LongMul(b, a)
    f = []
    for i in range (max(len(a), len(b))):
        temp = LongMulOneDigit(a, int(b[i]))
        LongShiftDigitsToHigh(temp, i)
        f = LongAdd(f, temp)
    while f[len(f)-1] == 0 : 
        del f[len(f)-1]
        if f == []: 
            f = [0]
            break
    return f
 


print('A*B = ' + to_hex(LongMul(A, B)))

def LongSquare(a):
    res = LongMul(a, a)
    return res



print('A^2 = ' + to_hex(LongSquare(A)))


def LongShiftDigitsToLow(n, amount): 
    if len(n) - amount <= 0: 
        return [0]
    i = amount - 1
    while i > -1:
        del n[i]
        i -= 1
    return n


def LongShiftBitsToHigh(n, amount):  
    if amount%32 == 0: 
        return LongShiftDigitsToHigh(n, amount//32)
    b = 32 - amount%32
    k = 1 if n[len(n) - 1] >> b !=0 else 0
    res = [0]*(len(n) + k + amount//32)
    if k == 1:
        res[len(n) - 1] = n[len(n) - 1] >> b
        i = len(res) - 2
    else: 
        i = len(res) - 1
    for j in reversed(range(1, len(n))):
        res[i] = (n[j]<<32 - b)&(2**32 - 1)|n[j - 1] >> b
        i -= 1
    res[i] = (n[0] << 32 - b)&(2**32 - 1)       
    return res
  
    
def LongShiftBitsToLow(n, amount):
    if amount//32 >= len(n):
        return from_hex('0')
    if amount%32 == 0: 
        return LongShiftDigitsToLow(n, amount//32)
    b = 32 - amount%32
    k= 0 if n[len(n) - 1] >> 32 - b != 0 else 1
    res = [0]*(len(n) - k - amount//32)
    if k == 0:
        res[len(n) - 1] = n[len(n) - 1] >> 32 - b
        i = len(res) - 2
    else: 
        i = len(res) - 1
    for j in reversed(range(amount//32 + 1, len(n))):
        res[i] = (n[j] << b)&(2**32 - 1)| n[j - 1] >> 32 - b
        i -= 1
    return res


def BitLength(a):
    res = (len(a) - 1)*32 + a[len(a) - 1].bit_length()
    return res

def LongDivMod(a, b):
        k = BitLength(b)
        r = a
        q = []
        while LongCmp(r, b) != -1:
            t = BitLength(r)
            c = LongShiftBitsToHigh(b, t-k)
            if LongCmp(r, c) is -1:
                t -= 1
                while b[0] == 0: 
                    b = b[1:] 
                c = LongShiftBitsToHigh(b, t - k)
            r = LongSub(r, c)
            q = LongAdd(q, LongShiftBitsToHigh([1], t - k))
            while b[0] == 0: 
                b = b[1:] 
        return [q, r]



Div=LongDivMod(A, B)
print('A/B = ' + (to_hex(Div[0]) if Div[0] != [] else '0') + '; A mod B = ' + to_hex(Div[1]))
  
    
def BitCheck(a, i):
    c = i%32
    j = i//32
    return (a[j] >> c)&1

def LongPower(a, b):
    c = [1]
    for i in range(BitLength(b)):
        if  BitCheck(b, i) == 1:
            c = LongMul(c, a)
        a = LongMul(a, a)
    return c


A2 = 'EDF'
B2 = 'FB5'


print('A^B = ' + to_hex(LongPower(from_hex(A2), from_hex(B2))))


def GCD(a, b):
    d = [1]
    s = 0
    t = 0
    while a[0]%2 == 0 and b[0]%2 == 0:
        a = LongShiftBitsToLow(a, 1)
        b = LongShiftBitsToLow(b, 1)
        d = LongShiftBitsToHigh(d, 1)
    while a[0]%2 == 0:
        a = LongShiftBitsToLow(a, 1)
    while LongCmp(b, from_hex('0')) != 0:
        s += 1
        while b[0]%2 == 0:
            b = LongShiftBitsToLow(b, 1)
        comp = LongCmp(a, b)
        s += 1
        if comp == 1:
            min_ab = b
            sub = LongSub(a, b)
            t += 1
        elif comp == -1:
            min_ab = a
            sub = LongSub(b, a)
        else:
            min_ab = b
            sub = [0]
        a =  min_ab
        b = sub
    d = LongMul(d, a)
    return d, s, t


print('НСД(A, B) = ' + to_hex(GCD(A, B)[0]) + '; кількість порівнянь = ' + str(GCD(A, B)[1]) + '; кількість віднімань = ' + str(GCD(A, B)[2]))

def EvklidGCD(a, b):
    s = 0
    t = 0
    while LongCmp(a, [0]) != 0 and LongCmp(b, [0]) != 0:
        s += 2
        comp = LongCmp(a, b)
        if comp == 1:
            a = LongDivMod(a, b)[1]
        elif comp == -1:
            b = LongDivMod(b, a)[1]
         else:
            b = [0]
    return LongAdd(a, b), s, t

%timeit EvklidGCD(A, B)
print('НСД(A, B) за алгоритмом Евкліда = ' + to_hex(EvklidGCD(A, B)[0]) + '; кількість порівнянь = ' + 
      str(EvklidGCD(A, B)[1]) + '; кількість ділень = ' + str(EvklidGCD(A, B)[2]))


def LCM(a, b):
    mul = LongMul(a, b)
    gcd = GCD(a, b)[0]
    res = LongDivMod(mul, from_hex(to_hex(gcd)))[0]
    return res


print('НСК(A, B) = ', to_hex(LCM(A, B)))


def BarrettReduction(x, n, nu):
    if nu is None:
        beta = LongShiftDigitsToHigh([1], len(n)*2)
        nu = LongDivMod(beta, n)[0]
    while n[0] == 0: 
        del n[0]
    q = LongShiftDigitsToLow(x, len(n) - 1)
    q = LongMul(q, nu)
    q = LongShiftDigitsToLow(q, len(n) + 1)
    r = LongSub(x, LongMul(q, n))
    while r[len(r) - 1] == 0: 
        del r[len(r) - 1]
    while LongCmp(r, n) != -1:
        r = LongSub(r, n)
    return r

def LongAddMod(a, b, n):
    sum = LongAdd(a, b)
    return BarrettReduction(sum, n, None)



print('The answer is correct. (A+B)mod N = ' + to_hex(LongAddMod(A, B, N)))


def LongSubMod(a, b, n):
    sub = LongSub(a, b)
    return BarrettReduction(sub, n, None)


print('(A-B)mod N = ' + to_hex(LongSubMod(A, B, N)))


def LongMulMod(a, b, n):
    mul = LongMul(a, b)
    return BarrettReduction(mul, n, None)


print('(A*B)mod N = ' + to_hex(LongMulMod(A, B, N)))

def LongSquareMod(a, n):
    sq = LongSquare(a)
    return BarrettReduction(sq, n, None)


print('A^2 = ' + to_hex(LongSquareMod(A, N)))


def LongModPowerBarrett(a, b, n):
    c = [1]
    nu = LongDivMod(LongShiftDigitsToHigh([1], 2*len(n)), n)[0]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            c = BarrettReduction(LongMul(c, a), n, nu)
        a = BarrettReduction(LongMul(a, a), n, nu)
    return c


print('A^Bmod N = ' + to_hex(LongModPowerBarrett(A, B, N)) )


###ПРОВЕРКА###

F1 = from_hex(to_hex(LongAdd(A, B)))
F2 = LongMul(C, A)
F3 = LongMul(C, B)
if to_hex(LongMul(F1, C)) == to_hex(LongMul(C, F1)) == to_hex(LongAdd(F2, F3)):
    print(' (A + B)*C = C*(A + B) = C*A + C*B = ' + to_hex(LongMul(F1, C)))
else: print('ERROR')

n = 1000
def LongAdd2(a,n):
    a1 = a
    while n > 1:
        a1 = LongAdd(a1, a) 
        n -= 1
    return a1

if to_hex(LongMul(C, [n]))==to_hex(LongAdd2(C, n)):
    print ('С*1000 = С+С+...+С 1000 times = ' + to_hex(LongAdd2(C, n)))
else: print('ERROR')
    

print('B*(A/B) = ' + to_hex(LongMul(B, LongDivMod(A, B)[0])) + ' =\n B = ' + to_hex(B))

S1 = to_hex(LongSquare(LongAdd(A, B)))
S2 = to_hex(LongAdd(LongAdd(LongSquare(A), LongSquare(B)), LongMulOneDigit(LongMul(A, B), 2)))
if S1 == S2:
    print('(A + B)^2 = A^2 + 2*A*B + B^2 = ' + S1)
else: print('ERROR')

if to_hex(LongMulMod(F1, C, N))==to_hex(LongMulMod(C, F1, N))==to_hex(LongAddMod(F2, F3, N)):
    print(' (A + B)*C mod N = C*(A + B) mod N = C*A + C*B mod N =' + to_hex(LongMul(F1, C)))
else: print('ERROR')

k=1000
def LongAddMod2(a, k, n):
    a1 = a
    while k > 1:
        a1 = LongAddMod(a1, a, n) 
        k -= 1
    return a1

if to_hex(LongMulMod(C, [k], N))==to_hex(LongAddMod2(C, k, N)):
    print ('С*1000 mod N= С+С+...+С 1000 times mod N = ' + to_hex(LongAddMod2(C, k, N)))
else: print('ERROR')

S1 = to_hex(LongSquareMod(LongAdd(A, B), N))
S2 = to_hex(LongAddMod(LongAdd(LongSquare(A), LongSquare(B)), LongMulOneDigit(LongMul(A, B), 2), N))
if S1 == S2:
    print('(A + B)^2 mod N + (A^2 + 2*A*B + B^2) mod N= ' + S2)
else: print('ERROR')
