import os
import binascii
import random
import struct
import string

from serpent import _encrypt_, _decrypt_, bin2hex
path = "/files/tex1.txt"
hex_string = '0123456789abcdef'
def get_session_key(length):
    return ''.join([random.choice(hex_string) for x in range(32)])


text = "Hello world Hello world Hello world"
"""pt = "".join(format(ord(x), 'b') for x in text)
print(len(pt[:128]))
key = "".join([str(random.choice([0, 1])) for i in range(256)])
print(len(key))
ct = _encrypt_(pt[:128], key)
pt_2 = _decrypt_(ct, key)
print("plain text: ", pt[:128])
print("deciphered: ", pt_2)"""
