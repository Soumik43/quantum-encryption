import random
import math

# -------------------------------- parameters -------------------------------- #
# This will be the size of the cryptographic vectors
nvals = 20

B = []
e = []
# secret value s
s = 20
# Parameter q (matrices and vectors will be mod q)
q = 97

# ------------------------------ encryption function ----------------------------- #


def encrypt(public_key, message):
    # Our public key is made up of two vectors
    A = public_key[0]
    B = public_key[1]

    # Multiplying by 7 because each ascii character is 7 bits, and (u,v) ciphers only one bit
    u = [0] * len(message)
    v = [0] * len(message)

    for i in range(len(message)):
        u[i] = [0] * 7
        v[i] = [0] * 7

    for i in range(len(message)):
        for j in range(7):
            # Sampling random values ​​to use as an index For each bit of the message, we must sample
            sample = random.sample(range(nvals-1), nvals//4)

            for x in range(0, len(sample)):
                u[i][j] += A[sample[x]]
                v[i][j] += B[sample[x]]

            v[i][j] += math.floor(q/2) * int(message[i][j])
            v[i][j] %= q
            u[i][j] %= q

    # (u,v) is our ciphertext
    return u, v


# ----------------------------- Decryption function ---------------------------- #

def decrypt(secret_key, ciphertext):
    u = ciphertext[0]
    v = ciphertext[1]

    dec = [0] * len(u)
    ret = [0] * len(u)

    for i in range(len(u)):
        dec[i] = [0] * 7
        ret[i] = [0] * 7

    for i in range(len(u)):
        for j in range(7):
            dec[i][j] = (v[i][j] - s*u[i][j]) % q
            if (dec[i][j] > q/2):
                ret[i][j] = '1'
            else:
                ret[i][j] = '0'
        ret[i] = ''.join(ret[i])

    ret = '0b' + ''.join(ret)
    return ret
    # return int(ret, 2)


A = random.sample(range(q), nvals)

for x in range(0, len(A)):
    e.append(random.randint(1, 4))
    B.append((A[x]*s+e[x]) % q)


# ----------------------------- user input ----------------------------- #

public_key = (A, B)

text_bin = []
text = str(input("Enter the message to be encrypted:"))
text_bytes = text.encode('ascii')

for i in range(len(text_bytes)):
    a = bin(text_bytes[i])
    text_bin.append(a[2:])

# --------------------------- Encryption / Decryption -------------------------- #

ciphertext = encrypt(public_key, text_bin)
response = decrypt(s, ciphertext)

# ---------------------------------- Prints ---------------------------------- #

print(f'''Public key A:
{A}

Error vector:
{e}

secret key:
{s}

Public key B:
{B}

Ciphertext:
u: {ciphertext[0]}
v: {ciphertext[1]}

Deciphered text (binary): {response[2:]}
''')


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


bin_data = response[2:]
str_data = ' '
for i in range(0, len(bin_data), 7):
    temp_data = bin_data[i:i + 7]
    decimal_data = BinaryToDecimal(temp_data)
    str_data = str_data + chr(decimal_data)
print(str_data)
