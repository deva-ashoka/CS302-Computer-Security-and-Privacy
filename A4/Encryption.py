import random
from base64 import b64encode
import os, sys
import struct
from Crypto import Random
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


# ------------------------- AES encryption ----------------------------
def encrypt_file(
        key, in_filename, out_filename=None, chunksize=DEFAULT_CHUNKSIZE
):
    if not out_filename:
        out_filename = in_filename + OUTPUT_FILE_DEFAULT_SUFFIX

    ivec = Random.new().read(IVEC_SIZE)
    encryptor = AES.new(key, AES_MODE, ivec)
    filesize = os.path.getsize(in_filename)

    file_length_field = struct.pack('<Q', filesize)

    with open(in_filename, 'rb') as infp:
        with open(out_filename, 'wb') as outfp:

            assert len(ivec) == IVEC_SIZE
            outfp.write(ivec)

            chunk = None
            final_chunk = False

            while True:

                # Encrypt the previous chunk, then read the next.
                if chunk is not None:
                    outfp.write(encryptor.encrypt(chunk))

                if final_chunk:
                    break

                chunk = infp.read(chunksize)

                # The first time we get anything other than a full
                # chunk, we've exhausted the input file and it's time
                # to add the padding and length indicator.
                if len(chunk) == 0 or len(chunk) % 16 != 0:
                    padding_size = (
                        16 - (len(chunk) + FILE_LENGTH_FIELD_SIZE) % 16
                    )
                    padding = ' ' * padding_size

                    chunk += str.encode(padding)
                    chunk += file_length_field
                    assert len(chunk) % 16 == 0

                    final_chunk = True


# ------------------- Generating the key and cipher required for AES encryption ----------------

randomBytes = os.urandom(16)
key_string = b64encode(randomBytes).decode('utf-8')
key_int = int.from_bytes(randomBytes, sys.byteorder)
iv = Random.new().read(AES.block_size)
cipher = AES.new(key_string, AES.MODE_CBC, iv)

# ------------------- Asking the user for input and output file names ----------------

msgFileName = input("Enter the name of the file to be encrypted (along with extension): ")
encryptedFileName = input("Enter the name of the output file after encryption: ")

# AES encryption
encrypt_file(key_string, msgFileName, encryptedFileName, 32)

publicKeyFile = open("publicKey.txt", "r")
p = int(publicKeyFile.readline().rstrip())
g = int(publicKeyFile.readline().rstrip())
h = int(publicKeyFile.readline().rstrip())

r = random.randint(0, p - 2)
C2 = squareNMultiply(g, r, p)
C3temp = squareNMultiply(h, r, p)
C3 = (key_int * C3temp) % p

cipherFile = open(encryptedFileName + "KEY", 'w')
cipherFile.write(str(C2))
cipherFile.write("\n")
cipherFile.write(str(C3))
cipherFile.close()

print("File Encrypted!")
