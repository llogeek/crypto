import math
import random
import numpy as np
import time

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def nBitRandom(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def getPrime(n):
    while True:
        pc = nBitRandom(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
                break
        else:
            return pc

def generate_pq(l):
    n1 = random.randrange(l // 2 - 16, l // 2 + 16, 2)
    n2 = l - n1
    while True:
        p = getPrime(n1)
        if not isMillerRabinPassed(p):
            continue
        #print("Rabin miller passed for p")
        if not IsPrime_Pherma(p):
            continue
        #print("Pherma passed for p")
        if not solovoyShtrassen(p):
            continue
        #print("Solovoy Shtrassen passed for p")
        #print("Prime?: ", sympy.isprime(p))
        #print(len(bin(p)) - 2, "bit prime is: \n", p)
        break

    while True:
        q = getPrime(n2)
        if not isMillerRabinPassed(q):
            continue
        #print("Rabin miller passed for q")
        if not IsPrime_Pherma(q):
            continue
        #print("Pherma passed for q")
        if not solovoyShtrassen(q):
            continue
        #print("Solovoy Shtrassen passed for q")
        #print("Prime?: ", sympy.isprime(q))
        #print(len(bin(q)) - 2, "bit prime is: \n", q)
        break
    return p, q



def carmichael(p, q):
    return (p - 1) * (q - 1) // gcd(p - 1, q - 1)

def Gen(l=2048):
    p, q = generate_pq(l)
    n = p * q
    euler_phi = carmichael(p, q)#(p - 1) * (q - 1)
    e = random.choice([3, 17])
    while e < euler_phi:
        if gcd(e, euler_phi) == 1 and gcd(e, p - 1) == 1 and gcd(e, q - 1) == 1:
            break
        else:
            e += 1
    d = modinv(e, euler_phi)
    return e, n, d, euler_phi, p, q


def Encr(n, e, x):
    y = ModPow_montgomery(x, e, n)
    return y


def Decr(n, d, y):
    x = ModPow_montgomery(y, d, n)
    return x


# вспомогательные алгоритмы

def gcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    r0 = a
    r1 = b
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    while r1 != 0:
        temp = [r1, x1, y1]
        qi = r0 // r1
        r1 = r0 - qi * r1
        x1 = x0 - qi * x1
        y1 = y0 - qi * y1
        r0, x0, y0 = temp[0], temp[1], temp[2]
    return r0, x0, y0

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def ModPow_right_left(a, b, n):
    u = 1
    v = a
    l = round(np.log2(b))
    for i in range(l):
        bi = b % 2
        b = b // 2
        if bi != 0:
            u = (u * v) % n
        v = (v * v) % n
    return u
def ModPow_left_right(a, b, n):
    u = 1
    l = round(math.log2(b))
    num = b
    p = 2 ** (l - 1)
    bi = 0
    for i in range(l - 1, -1, -1):
        if num < p:
            bi = 0
        elif num >= p:
            bi = 1
            num = num - p
        elif p == 1:
            break
        p = p // 2
        u = (u * u) % n
        if bi != 0:
            u = (u * a) % n
    return u


def ModPow_montgomery(a, e, n):
    r = 1
    while e > 0:
        if (e & 1) == 0:
            e = e >> 1
            a = (a * a) % n
        else:
            e -= 1
            r = (r * a) % n
    return r

def isMillerRabinPassed(n):
    s = 0
    r = n - 1
    while r % 2 == 0:
        r >>= 1
        s += 1
    assert (2 ** s * r == n - 1)

    def check(a):
        if gcd(a, n) != 1:
            return True
        v = ModPow_montgomery(a, r, n)
        if v == 1:
            return False
        for i in range(s):
            if v == n - 1:
                return False
            v = ModPow_montgomery(v, 2, n)
        return True

    numberOfRabinTrials = 100
    for i in range(numberOfRabinTrials):
        a = random.randrange(2, n)
        if check(a):
            return False
    return True

def IsPrime_Pherma(n):
    count = 100
    for i in range(count):
        rnd = random.randint(1, n - 1)
        if gcd(rnd, n) != 1:
            return False
        if ModPow_montgomery(rnd, n - 1, n) != 1:
            return False
    return True


def calculateJacobian(a, n):
    if a == 0:
        return 0  # (0/n) = 0
    ans = 1
    if a < 0:
        # (a/n) = (-a/n)*(-1/n)
        a = -a
        if n % 4 == 3:
            # (-1/n) = -1 if n = 3 (mod 4)
            ans = -ans
    if a == 1:
        return ans  # (1/n) = 1

    while a:
        if a < 0:
            # (a/n) = (-a/n)*(-1/n)
            a = -a
            if n % 4 == 3:
                # (-1/n) = -1 if n = 3 (mod 4)
                ans = -ans
        while a % 2 == 0:
            a = a // 2
            if n % 8 == 3 or n % 8 == 5:
                ans = -ans
                # swap
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            ans = -ans
        a = a % n

        if a > n // 2:
            a = a - n
    if n == 1:
        return ans
    return 0


def solovoyShtrassen(n, iterations=100):
    if n < 2:
        return False
    if n != 2 and n % 2 == 0:
        return False
    for i in range(iterations):
        a = random.randrange(n - 1) + 1
        if gcd(a, n) > 1:
            return False
        jacobian = (n + calculateJacobian(a, n)) % n
        mod = ModPow_montgomery(a, (n - 1) // 2, n)
        if jacobian == 0 or mod != jacobian:
            return False
    return True

def print_rsa(n, e, d):
    print("RSA data generated:")
    print("n = {},\ne = {},\nd = {}\n".format(n, e, d))

if __name__ == "__main__":
    start = time.time()
    e, n, d, phi, p, q = Gen()
    print("p: ", p)
    print("q: ", q)
    print_rsa(n, e, d)
    x = 234
    print("Data for encryption: ", x)
    y = Encr(n, e, x)
    print("Encrypted data: ", y)
    x = Decr(n, d, y)
    print("Result of decrypting encrypted text: ", x)
    end = time.time() - start
    print(end)
