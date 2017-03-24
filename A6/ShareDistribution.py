import random


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


def computePolynomial(t1, K1, a1, x):
    result = 0
    for itr in range(t1):
        result += (a1[itr + 1] * x ** (itr + 1))
    result += K1
    return result


inputFileName = input("Enter the name of the file containing t,n and K: ")
inputFile = open(inputFileName, "r")
t = int(inputFile.readline().rstrip())
n = int(inputFile.readline().rstrip())
K_String = inputFile.readline().rstrip()
inputFile.close()

K_Int = int(K_String, 2)
L = K_Int.bit_length()

if (1 <= t and t <= n - 1):

    if (2 ** L) > n:

        Ldash = random.randint(L + 1, 2 * L)
        itrP = True
        p = 0
        while (itrP):
            randomNum = random.randint(2 ** (Ldash - 1), 2 ** Ldash)
            if (randomNum % 2 == 0):
                itrP = True
            else:
                prime = primegenerator(randomNum)
                if (prime != -1):
                    p = randomNum
                    itrP = False

        a = []
        for i in range(t + 1):
            a.append(0)

        for i in range(t):
            num = random.randint(1, p)
            while (num in a):
                num = random.randint(1, p)
            a[i + 1] = num

        Sh = []
        for i in range(n + 1):
            Sh.append(0)

        for i in range(n):
            Sh[i + 1] = computePolynomial(t, K_Int, a, (i + 1)) % p

        fo = open("reconstructionInputs.txt", "w")
        fo.write(str(t))
        fo.write("\n")
        fo.write(str(p))
        fo.write("\n")
        fo.close()

        outputFileName = input("Enter the name of the output file (with extension .txt): ")
        f = open(outputFileName, "w")
        for i in range(n):
            writeString = str(i + 1) + "," + str(Sh[i + 1])
            f.write(writeString)
            f.write("\n")
        f.close()
        print("Done!")

    else:
        print("The number L does not satisfy the condition 2^L > n")
else:
    print("The numbers t,n do not satisfy the condition 1<=t<=n-1")
