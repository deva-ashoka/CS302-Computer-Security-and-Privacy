import math, os, struct
from base64 import b64encode
from Crypto.Cipher import AES

AES_MODE = AES.MODE_CBC
IVEC_SIZE = 16

DEFAULT_CHUNKSIZE = 64 * 1024
FILE_LENGTH_FIELD_SIZE = struct.calcsize('Q')

OUTPUT_FILE_DEFAULT_SUFFIX = '.enc'

# Indicator for moving file pointer relative to end of file.
WHENCE_EOF = 2


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


def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infp:

        ivec = infp.read(IVEC_SIZE)
        decryptor = AES.new(key, AES_MODE, ivec)

        with open(out_filename, 'wb+') as outfp:

            # We need to read the next chunk to know how to treat this
            # first chunk.
            chunk = infp.read(chunksize)
            final_chunk = False

            while True:

                # We need to read the new chunk to know how to treat
                # the current chunk.
                new_chunk = infp.read(chunksize)

                plaintext_chunk = decryptor.decrypt(chunk)

                if len(new_chunk) == 0:
                    final_chunk = True

                outfp.write(plaintext_chunk)

                if final_chunk:
                    # Read the expected file length from the now
                    # complete reconstruction of the original file.
                    # This moves the file pointer back from the end of
                    # the file then reads the same number of bytes
                    # back in, so should leave the file pointer at the
                    # same position, but we break out of the read loop
                    # anyway.
                    outfp.seek(-FILE_LENGTH_FIELD_SIZE, WHENCE_EOF)
                    file_length_field = outfp.read(FILE_LENGTH_FIELD_SIZE)
                    origsize = struct.unpack('<Q', file_length_field)[0]
                    break

                chunk = new_chunk

            outfp.truncate(origsize)

# ------------------- Asking the user for input and output file names ----------------

encryptedFileName = input("Enter the name of the encrypted file: ")
outputFileName = input("Enter the name of the output file after decryption (with the extension): ")

# ------------------- Getting public key and secret key  ----------------

publicKeyFile = open("publicKey.txt", "r")
p = int(publicKeyFile.readline().rstrip())
g = int(publicKeyFile.readline().rstrip())
h = int(publicKeyFile.readline().rstrip())

secretKeyFile = open("secretKey.txt", "r")
a = int(secretKeyFile.readline().rstrip())

keyFile = open(encryptedFileName + "KEY", 'rb')
C2 = int(keyFile.readline().rstrip())
C3 = int(keyFile.readline().rstrip())

# Finding the key from C2 and C3
C2dash = squareNMultiply(C2, a, p)
C2dashInverse = findmultiplicativeinverse(C2dash, p)
Kdash = (C3 * C2dashInverse) % p
key_bytes = (Kdash.to_bytes(16, byteorder='little'))
key_string = b64encode(key_bytes).decode('utf-8')

# AES decryption
decrypt_file(key_string, encryptedFileName, outputFileName, 32)

print("File Decrypted")
