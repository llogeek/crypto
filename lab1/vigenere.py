import string
english_alphabet = string.ascii_uppercase

class Info:
    def __init__(self, message, alphabet, key):
        try:
            self.message = message
            self.alphabet = alphabet
            self.key = key
            if self.key == 0 or self.key is None:
                raise ValueError('None key')
            if self.alphabet is None or len(self.alphabet) == 0:
                raise ValueError("None alphabet!")
            else:
                self.M = len(self.alphabet)
        except ValueError:
            raise ValueError('Empty data in test {0}!'.format(self.test))

    def checkVigenere(self):
        count = 0
        try:
            for i in self.key:
                if i in self.alphabet:
                    count = count + 1
        except ValueError:
            raise ValueError("Test {0} for Vigenere Cipher crashed while checking the key!".format(self.test))
        if count == len(self.key):
            return 1
        else:
            raise ValueError("Key has not alphabet element(s) in test {0}!".format(self.test))



class VigenereCipher:
    def __init__(self, info):
        if info.checkVigenere() == 1:
            self.key = info.key
            self.info = info

    def encrypt(self):
        try:
            ciphertext = ""
            for i in range(len(self.info.message)):
                temp = self.info.alphabet.index(self.info.message[i]) + self.info.alphabet.index(self.key[i % len(self.key)])
                temp = temp % len(self.info.alphabet)
                ciphertext += self.info.alphabet[temp]
            return ciphertext
        except ValueError:
           raise ValueError("Vigenere Cipher: Error encrypt!")

    def decrypt(self):
        try:
            plaintext = ""
            for i in range(len(self.info.message)):
                temp = self.info.alphabet.index(self.info.message[i]) - self.info.alphabet.index(
                    self.key[i % len(self.key)])
                temp = temp % len(self.info.alphabet)
                plaintext += self.info.alphabet[temp]
            return plaintext
        except ValueError:
            raise ValueError("Vigenere Cipher: Error in decrypt!")


def decrypt(ciphertext, key):
   info_1 = Info(ciphertext, english_alphabet, key)
   vigenere = VigenereCipher(info_1)
   return vigenere.decrypt()

def encrypt(plaintext, key):
   info_1 = Info(plaintext, english_alphabet, key)
   vigenere = VigenereCipher(info_1)
   return vigenere.encrypt()
