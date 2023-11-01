from random import randint
from functools import reduce


def miller_rabin(n, t):
    assert (n % 2 == 1)
    assert (n > 4)
    assert (t >= 1)

    # n - 1 = 2**s * r
    r, s = n - 1, 0
    while r % 2 == 0:
        s += 1
        r >>= 1  # r = (n - 1) / 2 ** s

    for i in range(t):
        a = randint(2, n - 2)  # НУЖНО n > 4

        y = pow(a, r, n)
        if y != 1 and y != n - 1:
            j = 1
            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != n - 1:
                return False

    return True


def is_prime(n):

    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False

    return miller_rabin(n, 10)


def nearest_prime(n):

    if is_prime(n):
        return n

    if n % 2 == 0:
        n += 1
    n1 = n - 2
    while True:
        if is_prime(n):
            return n
        if is_prime(n1):
            return n1
        n += 2
        n1 -= 2


def big_prime(size):
    n = randint(0, 9)
    for s in range(1, size):
        n += randint(0, 9) * 10 ** s

    return nearest_prime(n)


def jacobi(a, n):

    if a == 0:
        return 0
    if a == 1:
        return 1

    e = 0
    a1 = a
    while a1 % 2 == 0:
        e += 1
        a1 = a1 // 2
    assert 2 ** e * a1 == a

    s = 0

    if e % 2 == 0:
        s = 1
    elif n % 8 in {1, 7}:
        s = 1
    elif n % 8 in {3, 5}:
        s = -1

    if n % 4 == 3 and a1 % 4 == 3:
        s *= -1

    n1 = n % a1

    if a1 == 1:
        return s
    else:
        return s * jacobi(n1, a1)


def quadratic_non_residue(p):

    a = 0
    while jacobi(a, p) != -1:
        a = randint(1, p)

    return a


def xeuclid(a, b):

    x = [1, 0]
    y = [0, 1]
    sign = 1

    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x[1], x[0] = q * x[1] + x[0], x[1]
        y[1], y[0] = q * y[1] + y[0], y[1]
        sign = -sign

    x = sign * x[0]
    y = -sign * y[0]
    return a, x, y


def gauss_crt(a, m):

    modulus = reduce(lambda a, b: a * b, m)

    multipliers = []
    for m_i in m:
        M = modulus // m_i
        gcd, inverse, y = xeuclid(M, m_i)
        multipliers.append(inverse * M % modulus)

    result = 0
    for multi, a_i in zip(multipliers, a):
        result = (result + multi * a_i) % modulus
    return result


def pseudosquare(p, q):
    a = quadratic_non_residue(p)
    b = quadratic_non_residue(q)
    return gauss_crt([a, b], [p, q])


def generate_key(prime_size=6):
    p = big_prime(prime_size)
    q = big_prime(prime_size)
    while p == q:
        p = big_prime(prime_size)

    y = pseudosquare(p, q)
    n = p * q

    keys = {'pub': (n, y), 'priv': (p, q)}
    return keys


def encode(s):

    return int(''.join(("%03d" % c) for c in s.encode('ascii', 'ignore')))


def encrypt(m, pub_key):

    bin_m = [b == "1" for b in "{0:b}".format(encode(m))]
    n, y = pub_key

    def encrypt_bit(bit):

        x = randint(0, n)
        if bit:
            return (y * pow(x, 2, n)) % n
        return pow(x, 2, n)

    return list(map(encrypt_bit, bin_m))


def decode(dec):

    x = str(dec)
    chunks, chunk_size = len(x), 3
    if chunks % 3 == 1:
        x = "00" + x
    if chunks % 3 == 2:
        x = "0" + x
        chunks += 1
    l = [x[chunks - i - chunk_size: chunks - i] for i in range(0, chunks, chunk_size)]
    m = ""
    for x in l:
        c = chr(int(x))
        m = c + m
    return m


def decrypt(c, priv_key):
    p, q = priv_key

    def decrypt_bit(bit):

        e = jacobi(bit, p)
        if e == 1:
            return False
        return True

    m = list(map(decrypt_bit, c))
    s = ''.join(['1' if b else '0' for b in m])
    return decode(int(s, 2))


"""message = '10010101'

key = generate_key()
print(key)
enc = encrypt(message, key['pub'])
print("\nEncrypted:", enc)

dec = decrypt(enc, key['priv'])
print("\nDecrypted:", dec)"""