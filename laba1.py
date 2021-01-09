import math
import datetime

def parcer(obj, n):
    args = [iter(obj)] * n
    return zip(*args)

def from_hex(hexnum):
    n = math.ceil(len(hexnum) / 8)
    hexs = []
    decs = []
    if len(hexnum) % 8 == 0:
        hexs = [''.join(i) for i in parcer(hexnum, 8)]
    else:
        zeros = 8 * n - len(hexnum)
        strzeros = zeros * '0'
        finalhex = strzeros + hexnum
        hexs = [''.join(i) for i in parcer(finalhex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs

def to_hex(num):
    num.reverse()
    hexnum = ''
    for i in range(len(num)):
        hex_el = hex(num[i])[2:]
        if len(hex_el) != 8:
            zeros = (8 - len(hex_el)) * '0'
            hex_str = zeros + hex_el
            hexnum += hex_str
        else:
            hexnum += hex_el
        hexnum = hexnum.lstrip('0')
    num.reverse()
    return hexnum.swapcase()

A=from_hex('170076B15F9575D21DE39D5C429799BBCDDB867016DE2248E3CFDE73A4D70C8636A9E41ABE671E7B9FB4739A5FF64DF9D0D3A64E0C9B20BFE58F1C62B28477EE9FD202010BAC440ADF3CA016A32DB844F23DEC2AB93AE869A6262FC23C5CE419807CDBA930A5433884E3B34B22477289BD3A7712CDD4B4110BD9887E7428FDF7')
B=from_hex('9D1C2D6E1591932F73C2F499C4E0A2E252DE828CDA7842CE0972C4101FE772B56C45C475EDDEDAEC2DBD13E375E02D2C149B69AB51FF3F94533CA34A815484EC86DACE936BDC62B5F3F9EB6F5BE6BD253E256181D35D7D63EE24459824D462C53676E3DFF98700415ADA65FDA7CBD3B3F359C817F52BEDA70C9DD85F68473C6')


def LongAdd(a, b):
    maxlen=max(len(a), len(b))
    shift = 0
    c= []
    for i in range(maxlen):
            tempA = int(a[i]) if i<len(a) else 0
            tempB = int(b[i]) if i<len(b) else 0
            temp = tempA + tempB + shift
            c.append(temp & (2**32 - 1))
            shift = temp >> 32
    if shift >0:
        c.append(shift)
    return c


print('A + B = ' + to_hex(LongAdd(A, B)))

def LongSub(a, b):
    borrow=0
    d= []
    maxlen=max(len(a), len(b))
    for i in range(maxlen):
            tempA = int(a[i]) if i<len(a) else 0
            tempB = int(b[i]) if i<len(b) else 0
            temp=tempA-tempB-borrow
            if temp>=0:
                d.append(temp)
                borrow=0
            else:
                d.append((2**32 + temp))
                borrow=1
    if borrow !=0:
        return None
    elif a==b:
        return 0
    else:
        return d

C=LongSub(A, B)
if C is None:
    print('A - B = Negative number')
elif C == 0:
    print('A - B = ' + '0')
else:
    print('A - B = ' + to_hex(C))


def LongCmp(a, b):
    if len(a)==len(b):
        i=len(a)-1
        while a[i]==b[i]:
            i=i-1
        if i==-1:
            return 0
        else:
            if a[i]>b[i]:
                return 1
            else:
                return -1
    elif len(a)>len(b):
            return 1
    else:
        return -1
    
    

def LongMulOneDigit(a, k):
    shift=0
    e=[]
    for i in range (len(a)):
        temp=int(a[i])*k+shift
        e.append(temp&(2**32 - 1))
        shift = temp >> 32
    e.append(shift)
    return e



def LongShiftDigitsToHigh(n, amount): 
    for i in range(amount):
        n.insert(0, 0)
    return n

 
def LongMul(a, b):
    f=[]
    for i in range (len(b)):
        temp= LongMulOneDigit(a, int(b[i]))
        LongShiftDigitsToHigh(temp, i)
        f=LongAdd(f, temp)
    return f
    
F=to_hex(LongMul(A, B))
print('A * B = ' + F)          

def LongSquare(a):
    res=LongMul(a, a)
    return res

print('A^2 = ' + to_hex(LongSquare(A)))


#в сторону старших битов, влево
def LongShiftBitsToHigh(n, amount):  
    k = amount // 32
    k1 = amount % 32
    if k1 == 0: return LongShiftDigitsToHigh(n, k)
    k2 = n[len(n) - 1] >> 32-k1
    k3 = 1 if k2 != 0 else 0
    res = [0] * (len(n) + k + k3)
    i = len(res) - 1
    if k2 != 0:
        res[i] = k2
        i = i - 1
    j = len(n) - 1
    while j > 0:
        x = n[j] << k1
        j = j - 1
        res[i] = x | n[j] >> 32-k1
        i = i - 1
    res[i] = n[j] << k1
    return res



def BitLength(a):
    res = (len(a) - 1) * 32 + a[len(a)-1].bit_length()
    return res


def LongDivMod(a, b):
    k=BitLength(b)
    r=a
    q=[]
    while LongCmp(r, b) == 1 or  0:
        t=BitLength(r)
        c=LongShiftBitsToHigh(b, t-k)
        if LongCmp(r, c) is -1:
            t=t-1
            c=LongShiftBitsToHigh(b, t-k)
        r=LongSub(r, c)
        q=LongAdd(q, LongShiftBitsToHigh([1], t-k))
    return [q, r]

Q=LongDivMod(A, B)
if Q[0] == []:
    print('A/B = ' + '0' + '; A mod B = ' + to_hex(Q[1]))
else:
    print('A/B = ' + to_hex(Q[0]) + '; A mod B = ' + to_hex(Q[1]))
    

def BitCheck(a, i):
    c = i % 32
    j = i // 32
    return (a[j] >> c) & 1

def LongPower(a, b):
    c=[1]
    for i in range(BitLength(b)):
        if  BitCheck(b, i) == 1:
            c=LongMul(c, a)
        a=LongMul(a, a)
    return c
#print('A^B = ' +  to_hex(LongPower(A, B)))
###ПРОВЕРКА###
#C=from_hex('38CDD88155E5E68A2B66FC28861FB57657E27A1D41D3E61730FAB712FB0E55728443D1A18C27DE41A5C3CAAFE43DE9484F48D282F29F8505F4BDF734D492B484')
#F1=LongAdd(A, B)
#F2=LongMul (A, C)
#F3=LongMul(C, B)
#print(' (A + B)*C = ' + to_hex(LongMul(F1, C)))
#print(' C*(A + B) = ' + to_hex(LongMul(C, F1)))
#print('C*A + C*B = ' + to_hex(LongAdd(F2, F3)))
M=from_hex('9C2794E6FB944C4183A1282039')
n=1000
print('M*n = ' + to_hex(LongMul(M, [n])))
def LongAdd2(a,n):
    a1=a
    while n>1:
        a1=LongAdd(a1, a) 
        n-=1
    return a1

print ('M+M+...+M n times = ' + to_hex(LongAdd2(M, n)))