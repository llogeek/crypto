from serpent import _encrypt_, binaryXor
import random

def my_xor(x1, x2):
    if len(x1) !=len(x2):
        raise ValueError("Can not xor values oof differnet length!")
    else:
        res = ""
        for i in range(len(x1)):
            if x1[i] == x2[i]:
                res += '0'
            if x1[i] != x2[i]:
                res += '1'
    return res

def _cfb_encrypt(plaintext, key, k=128):
    ciphertext = "".join([str(random.choice([0, 1])) for _ in range(k)])
    if len(plaintext) % 128 != 0:
        plaintext  = plaintext + '0'*(128 - len(plaintext) % 128)
    for i in range(0, len(plaintext), k):
        ciphertext = ciphertext + binaryXor(_encrypt_(ciphertext[i:(i+k)], key), plaintext[i:(i+k)])
    return ciphertext

def _cfb_decrypt(ciphertext, key, k = 128):
    plaintext = ""
    for i in range(k, len(ciphertext), k):
        plaintext = plaintext + binaryXor(_encrypt_(ciphertext[(i - k):i], key), ciphertext[i:(i+k)])
    return plaintext

"""
text = "Hello world Hello world Hello world"
pt = "".join(format(ord(x), 'b') for x in text)
print(len(pt[:128]))
key = "".join([str(random.choice([0, 1])) for i in range(256)])
print(len(key))
"""
"""ct = _cfb_encrypt(pt[:128], key)
pt_2 = _cfb_decrypt(ct, key)
print("plain text: ", pt[:128])
print("deciphered: ", pt_2)
""""""
iv = "".join([str(random.choice([0, 1])) for _ in range(128)])
ct = _cfb_encrypt(pt[:128], key, 128)
pt_2 = _cfb_decrypt(ct, key, 128)
print("plain text: ", pt[:128])
print("deciphered: ", pt_2)
"""