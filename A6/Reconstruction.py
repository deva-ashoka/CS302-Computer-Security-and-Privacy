import math


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


def calculateLambda(pickedShareNums, num, prime):
    productNumerator = 1
    productDenominator = 1
    for itr in range(len(pickedShareNums)):
        if num != pickedShareNums[itr]:
            productNumerator *= -(pickedShareNums[itr])
            productDenominator *= (num - pickedShareNums[itr])
    productDenominatorInverse = findmultiplicativeinverse(productDenominator, prime)
    product = (productNumerator * productDenominatorInverse) % prime
    return product


inputFile = open("reconstructionInputs.txt", "r")
t = int(inputFile.readline().rstrip())
p = int(inputFile.readline().rstrip())
inputFile.close()


sharesFileName = input("Enter the name of the file containing (t+1) shares: ")

with open(sharesFileName) as sharesFile:
    shares = sharesFile.read().splitlines()

if (len(shares) == t + 1):

    pickedSh = []
    pickedNum = []
    lambdaOfX = []
    for i in range(t + 1):
        pickedSh.append(0)
        pickedNum.append(0)
        lambdaOfX.append(0)

    for i in range(t + 1):
        shareSplit = shares[i].split(',')
        pickedNum[i] = int(shareSplit[0])
        pickedSh[i] = int(shareSplit[1])


    for i in range(t + 1):
        lambdaOfX[i] = calculateLambda(pickedNum, pickedNum[i], p)

    Kdash = 0
    for i in range(t + 1):
        Kdash += (lambdaOfX[i] * pickedSh[i]) % p
    Kdash = Kdash % p

    secret = "{0:b}".format(Kdash)

    secretFile = open("secret.txt", "w")
    secretFile.write(secret)
    secretFile.close()

    print("Done!")
else:
    print("The number of shares is not equal to (t + 1)")
