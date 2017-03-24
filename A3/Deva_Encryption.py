# Name: Deva


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


# ----------------Main-----------------------

publicKeyFile = open("publicKey.txt", "r")
e = int(publicKeyFile.readline().rstrip())
n = int(publicKeyFile.readline().rstrip())

publicKeyFile.close()

fileName = input("Enter the file to be encrypted: ")
messageFile = open(fileName, "r")
k = int(messageFile.readline().rstrip())

encryptedMessage = squareNMultiply(k, e, n)

f = open("encryptedMessage.txt", "w")
f.write(str(encryptedMessage))

print("Encryption done!")
