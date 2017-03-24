import random
import math
import hashlib


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
    return s % b


def hash_file(filename):
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            sha1.update(chunk)

    return sha1.hexdigest()


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


VerKeyFile = open("VerKey.txt", "r")
p = int(VerKeyFile.readline().rstrip())
q = int(VerKeyFile.readline().rstrip())
g = int(VerKeyFile.readline().rstrip())
h = int(VerKeyFile.readline().rstrip())

SignKeyFile = open("SignKey.txt", "r")
a = int(SignKeyFile.readline().rstrip())

itr = True
c1 = 0
c2 = 0

fileName = input("Enter the name of the file you want to sign (along with extension): ")
signatureFileName = input("Enter the name of the signature (output) file (do not mention any extension): ") + ".txt"

while (itr):
    r = random.randint(1, q)
    c1 = squareNMultiply(g, r, p)
    c1 = c1 % q

    hashMessage = hash_file(fileName)
    hex = "0x" + hashMessage

    rInv = findmultiplicativeinverse(r, q)

    c2 = (int(hex, 0) + (a * c1)) * rInv
    c2 = c2 % q

    if (c1 == 0 or c2 == 0):
        itr = True
    else:
        itr = False

signatureFile = open(signatureFileName, 'w')
signatureFile.write(str(c1))
signatureFile.write("\n")
signatureFile.write(str(c2))
signatureFile.close()

print("Signed!")
