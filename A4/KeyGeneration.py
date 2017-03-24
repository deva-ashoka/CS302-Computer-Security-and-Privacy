import random
import math


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


# ---------------------------------- choosing the prime p  ----------------------

bitLength = 150;

itr = True;
p = 0
prime1 = 0
prime2 = 0

while (itr):

    itr1 = True;
    itr2 = True;

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
            itr2 = True
        else:
            prime = primegenerator(randomNum)
            if (prime != -1):
                prime2 = randomNum
                itr2 = False

    bigPrime = (2 * prime1 * prime2) + 1

    if (bigPrime % 2 == 0):
        itr = True;
    else:
        isNumPrime = primegenerator(bigPrime)
        if (isNumPrime != -1):
            p = bigPrime
            itr = False

# ----------------------------- Generator - g ---------------------------------------

genItr = True
g = 0
while (genItr):
    gen = random.randint(1, p);
    if (((squareNMultiply(gen, prime1 * prime2, p)) - 1) % p) != 0:
        if (((squareNMultiply(gen, 2 * prime1, p)) - 1) % p) != 0:
            if (((squareNMultiply(gen, 2 * prime2, p)) - 1) % p) != 0:
                g = gen
                genItr = False
            else:
                genItr = True
        else:
            genItr = True
    else:
        genItr = True

# ----------------------------- h ---------------------------------------

a = random.randint(2, p - 1)
h = squareNMultiply(g, a, p)

# ----------------------------- Writing public key and secret key ---------------------------------------
f = open("publickey.txt", "w")
f.write(str(p))
f.write("\n")
f.write(str(g))
f.write("\n")
f.write(str(h))
f.close()

fo = open("secretKey.txt", "w")
fo.write(str(a))
fo.close()

print("Done!")
