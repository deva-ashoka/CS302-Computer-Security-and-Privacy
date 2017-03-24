import math
import hashlib


def hash_file(filename):
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            sha1.update(chunk)

    return sha1.hexdigest()


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

fileName = input("Enter the name of the file that you want to verify (along with extension): ")
signFileName = input("Enter the name of the signature file (do not mention extension): ") + ".txt"

signFile = open(signFileName, "r")
c1 = int(signFile.readline().rstrip())
c2 = int(signFile.readline().rstrip())

VerKeyFile = open("VerKey.txt", "r")
p = int(VerKeyFile.readline().rstrip())
q = int(VerKeyFile.readline().rstrip())
g = int(VerKeyFile.readline().rstrip())
h = int(VerKeyFile.readline().rstrip())

c2Inv = findmultiplicativeinverse(c2, q)
hashMessage = hash_file(fileName)
hex = "0x" + hashMessage

t1 = int(hex, 0) * c2Inv
t2 = c1*c2Inv
t2 = squareNMultiply(t2, 1, q)

x = squareNMultiply(g, t1, p)
y = squareNMultiply(h, t2, p)
z = (x * y) % p
final = z % q

if(final == c1):
    print("Valid Signature")
else:
    print("Invalid Signature")