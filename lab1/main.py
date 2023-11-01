import kasiski
import freq_analysis as fa
import re
from collections import defaultdict
from vigenere import encrypt, decrypt
from vigenere import english_alphabet
import matplotlib.pyplot as plt

fixed_txt_len = defaultdict(list)
fixed_key = defaultdict(list)
key_length = [i for i in range(3, 16)]
text_length = [i for i in range(500, 1501, 100)]

# function for cleaning text_data; files: List
def get_texts(files):
    texts = []
    for file in files:
        with open (file) as f:
            text = f.read()
        text = re.sub("[^A-Za-z]","",text)
        texts.append(text[:3000].upper())
    return texts

# function for reading key_file: kfile: path to file
def get_key(kfile):
    with open(kfile) as f:
        key = f.read()
    return key.upper()

# function for processing texts; texts: List
def process_text_for_file(texts, key_data):
    for i in range(len(texts)):
        for j in range(len(key_length)):
            encrypted = encrypt(texts[i][:1000], key_data[:(key_length[j])])
            fixed_txt_len[key_data[:(key_length[j])]].append(encrypted)
    for i in range(len(texts)):
        for j in range(len(text_length)):
            encrypted2 = encrypt(texts[i][:text_length[j]], key_data[:7])
            fixed_key[text_length[j]].append(encrypted2)

# function for attacking vigenere cipher; ciphertext: str in uppercase; key: str in uppercase
def attack(ciphertext, key):
    key_len = kasiski.kasiski_test(ciphertext)
    key_restored = fa.restore_key(ciphertext, key_len)
    #print('Chosen key length: '+str(key_len))
    #print('Restored key: '+str(key_restored))
    if key.upper() == key_restored:
        print("Key restored)") 
        return 1, key_restored
    else:
        print("Failed restorage(")
        return 0, key_restored

# put the key attack data in a dict()
def get_probability_key():
    print('Attack for different key length...')
    result_table_keys = {}
    for key in fixed_txt_len.keys():
        j = len(key)
        print("Current key length: ", j)
        for text in fixed_txt_len[key]:
            result = attack(text, key)[0]
            result_table_keys[j] = result_table_keys.get(j, 0) + result
        x = result_table_keys.keys()
    y = [ i / len(texts) for i in result_table_keys.values()]
    return x, y

# put the text attack data in a dict()
def get_probability_text():
    print('Attack for different ciphertext length...')
    result_table_texsts = {}
    for key in fixed_key.keys():
        print("Current text length: ", key)
        for text in fixed_key[key]:
            result = attack(text, init_key[:7])[0]
            result_table_texsts[len(text)] = result_table_texsts.get(len(text), 0) + result
    x = result_table_texsts.keys()
    y = [ i / len(texts) for i in result_table_texsts.values()]
    return x, y

def decrypt_text():
    print("Decrypting texts...")
    decrypted = defaultdict()
    for key in fixed_txt_len.keys():
        for text in fixed_txt_len[key]:
            result, restored_key = attack(text, key)
            if result == 1:
                decr = decrypt(text, restored_key)
                if key not in decrypted.keys():
                    decrypted[key] = []
                decrypted[key].append(decr)
    with open('decrypted_texts.txt', 'w') as f:
        for key in decrypted.keys():
            f.write(key)
            f.write("Decrypted texts:")
            for text in decrypted[key]:
                f.write(text)


 # files with test data   
files = ['D:\\lolita\\university\\7semester\\kbrs\\practice\\lab1\\lab1\\texts\\' + 'text' + str(i) +'.txt' for i in range(1, 11)]
kfile = 'D:\\lolita\\university\\7semester\\kbrs\\practice\\lab1\\lab1\\texts\\key.txt'

# getting text data from files
texts = get_texts(files)

# reading key information
init_key = get_key(kfile)

# prepare encrypted texts
process_text_for_file(texts, init_key)

# get probability data

keyX, keyY = get_probability_key()
textX, textY = get_probability_text()
# decrypting texts
decrypt_text()

plt.subplot(1, 2, 1) 
plt.plot(keyX, keyY)
plt.title("Different key length")
plt.xlabel('Key length')
plt.ylabel('P')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(textX, textY)
plt.title("Different ciphertext length")
plt.xlabel('Ciphertext length')
plt.ylabel('P')
plt.grid(True)

plt.show()