import math
from random import randint
import random


def computeInverse(in1, in2):
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0
    q = math.floor((aL[0] / bL[0]))
    r = (aL[0] - (q * bL[0]))

    while r > 0:
        temp = (tL[0] - (q * bL[0]))
        tL[0] = t
        t = temp
        temp = (sL[0] - (q * s))
        sL[0] = s
        s = temp
        aL[0] = bL[0]
        bL[0] = r
        q = math.floor(aL[0] / bL[0])
        r = (aL[0] - (q * bL[0]))

    r = bL[0]

    inverse = s % in2
    return inverse


def squareNMultiply(x, c, n):
    c1 = bin(c).lstrip('0b')
    c2 = []

    for bit in c1:
        c2.append(int(bit))

    c2.reverse()

    l = len(str(bin(c).lstrip('0b')))
    z = 1

    for i in range(l - 1, -1, -1):
        z = (z ** 2) % n
        if (c2[i] == 1):
            z = (z * x) % n

    return z


def rabinMiller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5):  # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def isPrime(num):
    # Return True if num is a prime number.
    # Using other methods to check primes before using Rabin-Miller for faster results.

    if (num < 2):
        return False

    smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                   103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                   211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                   331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                   449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                   587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                   709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                   853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                   991, 997]

    if num in smallPrimes:
        return True

    # Checking if any of the low prime numbers can divide num
    for prime in smallPrimes:
        if (num % prime == 0):
            return False

    # Calling Rabin-Miller
    return rabinMiller(num)


def generateLargePrime(keysize):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if isPrime(num):
            return num

def getGenerator(n, B):
    a = 2
    for j in range(2, B):
        a = squareNMultiply(a, j, n)
    d = gcd(a - 1, n)
    if 1 < d < n:
        return d
    else:
        return "failure"


def getpandg():
    flag = True
    while (flag):
        p1 = generateLargePrime(150)
        p2 = generateLargePrime(150)
        p = (2 * p1 * p2) + 1
        a = randint(1, p - 1)
        if (isPrime(p)):
            flag2 = True
            while (flag2):
                t1 = squareNMultiply(a, p1 * p2, p) - 1
                # print (t1)
                # print(squareNMultiply(a,p1*p2,p))
                if (t1 % p != 0):
                    t2 = squareNMultiply(a, 2 * p1, p) - 1
                    if (t2 % p != 0):
                        t3 = squareNMultiply(a, 2 * p2, p) - 1
                        if (t3 % p != 0):
                            flag = flag2 = False
                            return p, a

def gcd(a, b):
    r = [a, b]
    q = [0]
    m = 1

    # print(r[1])
    while r[m] != 0:
        q.append(math.floor((r[m - 1]) / r[m]))
        r.append(r[m - 1] - (q[m] * r[m]))
        m = m + 1

    m = m - 1

    return r[m]

def getPrime ():
    while(True):
        q = generateLargePrime(160)
        r = randint(2**(512-160),2**(1024-160))
        p = (2 * q * r) + 1
        L = p.bit_length()
        if (isPrime(p)):
            if (L % 64 == 0):
                if (512 <= L <=1024):
                    return p,q,r
                    break

p, q, r = getPrime()
t = randint(1,p-1)
g = squareNMultiply(t,2*r,p)

a = randint(2,q-1)

h = squareNMultiply(g,a,p)

#print(p)
#print(q)
verKeyFile = open("VerKey", 'w')
verKeyFile.write(str((p)))
verKeyFile.write("\n")
verKeyFile.write(str(q))
verKeyFile.write("\n")
verKeyFile.write(str(g))
verKeyFile.write("\n")
verKeyFile.write(str(h))
verKeyFile.close()

signKeyFile = open("SignKey", 'w')
signKeyFile.write(str(a))
signKeyFile.close()

print("VerKey and SignKey files have been created.")
