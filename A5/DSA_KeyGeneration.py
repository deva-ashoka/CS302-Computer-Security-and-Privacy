#Deva

import random
import math


def numberOfBits(n):
    return int(math.log(n, 2)) + 1


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
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(20):
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

    if (n < 2):
        return -1

    smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                   103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                   211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                   331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                   449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                   587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                   709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                   853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                   991, 997]

    if n in smallPrimes:
        return n

    for prime in smallPrimes:
        if (n % prime == 0):
            return -1

    x = rabinMiller(n)
    if (x == True):
        return n
    else:
        return -1


# ---------------------------------- choosing the prime p  ----------------------


bitLengthLow = 512
bitLengthHigh = 1024
primeFactorBitLength = 160

itr = True
p = 0
q = 0
r = 0

while (itr):

    itr1 = True
    itr2 = True

    while (itr1):
        randomNum = random.randint(2 ** (primeFactorBitLength - 1), 2 ** primeFactorBitLength)
        if (randomNum % 2 == 0):
            itr1 = True
        else:
            prime = primegenerator(randomNum)
            if (prime != -1):
                q = randomNum
                itr1 = False

    r = random.randint(2 ** (bitLengthLow - primeFactorBitLength), 2 ** (bitLengthHigh - primeFactorBitLength))

    bigPrime = 2 * q * r + 1

    L = bigPrime.bit_length()

    if L >= 512 and L <= 1024:
        if L % 64 == 0:
            # print(L)
            if (bigPrime % 2 == 0):
                itr = True
            else:
                isNumPrime = primegenerator(bigPrime)
                if (isNumPrime != -1):
                    p = bigPrime
                    itr = False


# ---------------------------------- choosing the generator g  ----------------------
t = random.randint(1, p - 1)
g = squareNMultiply(t, 2 * r, p)


# ---------------------------------- key  ----------------------

a = random.randint(2, q)
h = squareNMultiply(g, a, p)

# ----------------------------- Writing sign key and verification key ---------------------------------------
f = open("VerKey.txt", "w")
f.write(str(p))
f.write("\n")
f.write(str(q))
f.write("\n")
f.write(str(g))
f.write("\n")
f.write(str(h))
f.close()

fo = open("SignKey.txt", "w")
fo.write(str(a))
fo.close()

print("Done!")
