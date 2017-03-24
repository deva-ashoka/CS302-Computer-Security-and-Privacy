# Name: Deva


import random
import math


def rabinMiller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def primegenerator(n):
    count = 0;
    for i in range(0, 20):
        x = rabinMiller(n);
        if (x == True):
            count = count + 1;
    if (count == 20):
        return n;
    else:
        return -1;


def gcd(a, b):
    if b > a:
        if b % a == 0:
            return a
        else:
            return gcd(b % a, a)
    else:
        if a % b == 0:
            return b
        else:
            return gcd(b, a % b)


def findmultiplicativeinverse(a, b):
    a0 = a
    b0 = b
    t0 = 0
    t = 1
    s0 = 1
    s = 0
    q = math.floor(a0 / b0)
    r = a0 - (q * b0)
    while (r > 0):
        temp = t0 - (q * t)
        t0 = t
        t = temp
        temp = s0 - (q * s)
        s0 = s
        s = temp
        a0 = b0
        b0 = r
        q = math.floor(a0 / b0)
        r = a0 - (q * b0)

    r = b0
    ans = [r, s, t]
    return s % b


# ---------------------Main------------------------------

positiveInteger = int(input("Enter a positive number: "))
bitLength = math.floor(positiveInteger / 2)

itr1 = True;
itr2 = True;
prime1 = 0
prime2 = 0

while (itr1):
    randomNum = random.randint(2 ** (bitLength - 1), 2 ** bitLength);
    if (randomNum % 2 == 0):
        itr1 = True
    else:
        prime = primegenerator(randomNum)
        if (prime != -1):
            prime1 = randomNum
            itr1 = False
while (itr2):
    randomNum = random.randint(2 ** (bitLength - 1), 2 ** bitLength);
    if (randomNum % 2 == 0):
        itr2 = True;
    else:
        prime = primegenerator(randomNum);
        if (prime != -1):
            prime2 = randomNum;
            itr2 = False;

print("Value of Prime 1: %d" % prime1)
print("Value of Prime 2: %d" % prime2)

n = prime1 * prime2
print("Value of n: %d" % n)

phin = (prime1 - 1) * (prime2 - 1)
print("Value of Phi(n): %d" % phin)

c = True
e = 0
while (c):
    e0 = random.randint(1, phin)
    if (gcd(e0, phin) == 1):
        e = (e0)
        c = False

print("Value of e: %d" % e)

eInverse = findmultiplicativeinverse(e, phin)
d = (eInverse) % phin

print("Value of d: %d" % d)

print(" (e*d)%d: ")
print((e * d) % phin)


f = open("publickey.txt", "w")
f.write(str(e))
f.write("\n")
f.write(str(n))
f.close()

fo = open("secretKey.txt", "w")
fo.write(str(d))
fo.write("\n")
fo.write(str(n))
fo.close()
