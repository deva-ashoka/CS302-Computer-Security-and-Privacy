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

secretKeyFile = open("secretKey.txt", "r")
d = int(secretKeyFile.readline().rstrip())
n = int(secretKeyFile.readline().rstrip())

secretKeyFile.close()

fileName = input("Enter the file to be decrypted: ")
encryptedMessageFile = open(fileName, "r")
c = int(encryptedMessageFile.readline().rstrip())

decryptedMessage = squareNMultiply(c, d, n)

f = open("decryptedMessage.txt", "w")
f.write(str(decryptedMessage))

print("Message Decrypted!")
