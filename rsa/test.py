import random
import sys
import time

import my_rsa
import sympy
import math
from egcd import egcd

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def generate_test_data():
    test_data = [0 for _ in range(3)]
    for i in range(3):
        test_data[i] = first_primes_list[random.randint(1, len(first_primes_list) - 1)]
        for _ in range(5):
            test_data[i] = test_data[i] * first_primes_list[random.randint(1, len(first_primes_list) - 1)]
    return test_data


test_data = generate_test_data()


def test_getPrime():
    primes_amount = 0
    rng = 1000
    for i in range(rng):
        if sympy.isprime(my_rsa.getPrime(2048)):
            primes_amount = primes_amount + 1
    print("Function getLowLevelPrime generated {} prime numbers while {} generations.".format(primes_amount, rng))


def test_Miller_Rabin():
    count = 0
    for i in range(3):
        if my_rsa.isMillerRabinPassed(
                sympy.randprime(0, sys.maxsize)):
            count = count + 1
        else:
            print("Miller Rubin failed in test №", i)
    for i in range(len(test_data)):
        if not my_rsa.isMillerRabinPassed(test_data[i]):
            count = count + 1
        else:
            print("Miller Rubin failed in test №", i + 3)
    if count == 6:
        print("Miller Rubin test passed all)")


def test_testPherma():
    count = 0
    for i in range(3):
        if my_rsa.IsPrime_Pherma(
                sympy.randprime(0, sys.maxsize)):
            count = count + 1
        else:
            print("Test Pherma failed in test №", i)
    for i in range(len(test_data)):
        if not my_rsa.IsPrime_Pherma(test_data[i]):
            count = count + 1
        else:
            print("Test Pherma failed in test №", i + 3)
    if count == 6:
        print("Test Pherma test passed all)")


def test_SolovoiShtrassen():
    count = 0
    for i in range(3):
        if my_rsa.solovoyShtrassen(
                sympy.randprime(0, sys.maxsize)):
            count = count + 1
        else:
            print("Test Solovoy-Shtrassen failed in test №", i)
    for i in range(len(test_data)):
        if not my_rsa.solovoyShtrassen(test_data[i]):
            count = count + 1
        else:
            print("Solovoy-Shtrassen failed in test №", i + 3)
    if count == 6:
        print("Solovoy-Shtrassen test passed all)")


def test_generate_pq():
    for _ in range(3):
        p, q = my_rsa.generate_pq(2048)
        if not sympy.isprime(p):
            print("Function for generating p ang q failed primary test by generating non-primary p(")
            return
        if not sympy.isprime(q):
            print("Function for generating p ang q failed primary test by generating non-primary q(")
            return
    print("Function for generating p ang q passed all tests)")


def check_RSA(e, n, d, euler_phi, p, q):
    if sympy.isprime(p) and sympy.isprime(q) and n == p * q:
        if math.gcd(e, p - 1) == 1 and math.gcd(e, q - 1) == 1:
            if math.gcd(e, euler_phi) == 1 and d == pow(e, -1, euler_phi):
                return True
    return False


def test_Gen():
    for i in range(3):
        e, n, d, euler_phi, p, q = my_rsa.Gen(2048)
        if not check_RSA(e, n, d, euler_phi, p, q):
            print("Gen algorith failed testing(")
            return
    print("Gen algorithm passed all tests)")


def test_encryption_decryption():
    for i in range(4):
        #print("Test {} ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||".format(i))
        e, n, d, euler_phi, p, q = my_rsa.Gen(2048)
        x = random.randint(100000, 1000000000)
        """print("p: ", p)
        print("q: ", q)
        print("e ", e)
        print("n ", n)
        print("carmichael function: ", euler_phi)
        print("d ", d)
        print("x: ", x)"""
        y_my = my_rsa.Encr(n, e, x)
        #print("Encrypted: ", y_my)
        x_my = my_rsa.Decr(n, d, y_my)
        #print("Decrypted: ", x_my)
        if x_my != x:
            print("Encrypting and decrypting algorithms failed testing(")
            return
    print("Encryption and Decryption functions passed all tests)")


def test_gcd():
    for _ in range(10):
        x = random.randint(2, 10 ** 6)
        y = random.randint(2, 10 ** 6)
        if math.gcd(x, y) != my_rsa.gcd(x, y):
            print("My gcd function failed testing(")
            return
    print("Function gcd passed all tests)")


def test_egcd():
    for _ in range(10):
        x = random.randint(2, 10 ** 6)
        y = random.randint(2, 10 ** 6)
        res = egcd(x, y)
        res_my = my_rsa.egcd(x, y)
        if res[0] != res_my[0] or res[1] != res_my[1] or res[2] != res_my[2]:
            print("My egcd function failed testing(")
            return
    print("Function egcd passed all tests)")


def test_modinverse():
    for _ in range(10):
        n = 2
        x = random.randrange(2, 100000)
        while my_rsa.gcd(x, n) != 1:
            n = random.randrange(2, 10 ** 5)
        y = pow(x, -1, n)
        if my_rsa.modinv(x, n) != y:
            print("My mod inverse function failed testing(")
            return
    print("My mod inverse function passed all tests)")


def test_MontomeryPow():
    for _ in range(10):
        x = random.randint(3, sys.maxsize)
        e = random.randint(3, sys.maxsize)
        n = random.randint(3, sys.maxsize)
        if my_rsa.ModPow_montgomery(x, e, n) != pow(x, e, n):
            print("My function for montgomery algorithm failed test(")
            return
    print("My function for montgomery algorithm passed all tests)")


def test_calculateJacobian():
    data = [[1111, 8093], [59, 79], [77, 257], [1783, 7523], [756479, 1298351], [4852777, 12408107]]
    results = [-1, -1, -1, 1, 1, -1]
    for i in range(len(data)):
        if my_rsa.calculateJacobian(data[i][0], data[i][1]) != results[i]:
            print("Function calculating Jacobian symbol failed testing(")
            return
    print("Function calculating Jacobian symbol passed all tests)")
    return


if __name__ == "__main__":
    start = time.time()
    test_getPrime()
    test_Miller_Rabin()
    test_testPherma()
    test_SolovoiShtrassen()
    test_generate_pq()
    test_Gen()
    test_encryption_decryption()
    test_gcd()
    test_egcd()
    test_modinverse()
    test_MontomeryPow()
    test_calculateJacobian()
    end = time.time() - start
    print(end)