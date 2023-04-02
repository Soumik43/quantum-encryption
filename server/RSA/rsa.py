import math
import random
from flask_cors import CORS
from flask import Flask, request
import json
app = Flask(__name__)
CORS(app)


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


def encrypt(public_key, message, q):
    nvals = 20
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


def decrypt(s, ciphertext, q):
    u = ciphertext[0]
    v = ciphertext[1]
    dec = [0] * len(u)
    ret = [0] * len(u)

    for i in range(len(u)):
        dec[i] = [0] * 7
        ret[i] = [0] * 7

    for i in range(len(u)):
        for j in range(7):
            dec[i][j] = (int(v[i][j]) - int(s*u[i][j])) % int(q)
            if (int(dec[i][j]) > int(q)/2):
                ret[i][j] = '1'
            else:
                ret[i][j] = '0'
        ret[i] = ''.join(ret[i])

    ret = '0b' + ''.join(ret)
    return ret
    # return int(ret, 2)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime():
    while True:
        n = random.randint(2, 200)
        if is_prime(n):
            return n


@app.route("/", methods=['GET'])
def home():
    return "<h1>SERVER IS WORKING</h1>"


@app.route("/rsa", methods=["GET", "POST"])
def rsa():
    if request.method == 'POST':
        plaintext = request.form['data']
        return ({"cipher": plaintext})


@app.route("/lwe", methods=["GET", "POST"])
def lwe():
    if request.method == 'POST':
        plaintext = request.data.decode()
        plaintext = json.loads(plaintext)
        plaintext = plaintext['body']
        nvals = 20
        B = []
        e = []
        s = 20
        q = 97
        A = random.sample(range(q), nvals)
        for x in range(0, len(A)):
            e.append(random.randint(1, 4))
            B.append((A[x]*s+e[x]) % q)
        public_key = (A, B)
        e = []
        text_bin = []
        text_bytes = str(plaintext).encode('ascii')

        for i in range(len(text_bytes)):
            a = bin(text_bytes[i])
            a += '0' if text_bytes[i] == 32 else ''
            text_bin.append(a[2:])

        ciphertext = encrypt(public_key, text_bin, q)
        response = decrypt(s, ciphertext, q)
        print(type(s), "typeofs")
        bin_data = response[2:]
        str_data = ' '
        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i + 7]
            decimal_data = BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)

        return {"data": {"u": ciphertext[0], "v": ciphertext[1], "res": str_data}}


@app.route("/lwe-decrypt", methods=["GET", "POST"])
def lwe_decrypt():
    if request.method == 'POST':
        ciphertext = request.data.decode()
        ciphertext = json.loads(ciphertext)
        q = ciphertext['q']
        s = ciphertext['s']
        ciphertext = ciphertext['u'], ciphertext['v']
        print(((s), ciphertext, (q)))
        res = decrypt(s, ciphertext, q)
        bin_data = res[2:]
        str_data = ' '
        for i in range(0, len(bin_data), 7):
            temp_data = bin_data[i:i + 7]
            decimal_data = BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)
        str_data = str_data.replace("@", " ")
        return {"string": str_data, "binary": res}


if __name__ == '__main__':

    app.run()
