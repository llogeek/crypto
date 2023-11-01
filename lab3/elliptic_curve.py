import random
import math
from sha1 import *
M = 13

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def isInt(n):
    return int(n) == float(n)



class EllipticCurve:
    def __init__(self, M):
        self.M = M
        self.params = []
        self.generate_params()
        self.elliptic_group = [Dot("inf", "inf", self)]
        self.a, self.b, self.G = self.build_group()
        print(self.a, self.b, self.G)
        self.key = self.key_exchange()
        self.print_exchange_data()

    def generate_params(self):
        for a in range(-M + 1, M):
            for b in range(-M + 1, M):
                if self.determinant(a, b) != 0:
                    self.params.append([a, b])

    def determine_G(self, a, b):
        self.elliptic_group_build(a, b)
        for dot in self.elliptic_group:
            ord = dot.determine_order()
            if is_prime(ord) and ord == M:
                self.G = dot
                self.print_elliptic_group()
                return dot
        return None

    def build_group(self):
        for params in self.params:
            self.a = params[0]
            self.b = params[1]
            G = self.determine_G(params[0], params[1])
            if G != None:
                return params[0], params[1], G
            else:
                self.elliptic_group = [Dot(0, 0, self)]
        return params[0], params[1], Dot(0, 0, self)

    def print_elliptic_group(self):
        print("Эллиптическая кривая: \n\t", self)
        print("Точки данной кривой: ")
        for i in range(0, len(self.elliptic_group) - 4, 4):
                print('\t', end='')
                print(self.elliptic_group[i],\
                      self.elliptic_group[i+1],\
                      self.elliptic_group[i+2],\
                      self.elliptic_group[i+3],sep = ',')

    def __repr__(self):
        return "y^2 = x^3 + {}*x + {}, Mod = {}".format(self.a, self.b, self.M)

    def determinant(self, a, b):
        return (4 * a**3 + 27 * b**2) % self.M

    def curve(self, x, a, b):
        return (x**3 + a * x + b) % self.M

    def elliptic_group_build(self, a, b):
        for x in range(M):
            y2= self.curve(x, a, b)
            for y in range(M):
                if y**2 % M == y2:
                    self.elliptic_group.append(Dot(x, y, self))

    def key_exchange(self):
        nA = random.randint(0, M)
        PA = self.G * nA
        nB = random.randint(0, M)
        PB = self.G * nB
        KA = PB * nA
        KB = PA * nB
        return {'nA':nA, 'nB': nB, 'PA':PA, 'PB':PB, 'KA':KA, 'KB':KB}

    def ecdsa(self, plaintext):
        hm = int(sha1(plaintext.encode()), 16)
        s, r = 0, 0
        while s == 0:
            while r == 0:
                k = random.randint(2, self.G.order - 2)
                dot1 = self.G * k
                r = dot1.x % self.G.order
            s = self.modinv(k, self.G.order) * (hm + r * self.key['nA']) % self.G.order
        print("Алгоритм ЭЦП на основе эллиптических кривых:\n\tПодпись r: {}, s: {}".format(r, s))
        return (r,s)

    def check_ECDSA(self, plaintext, r, s):
        hm = int(sha1(plaintext.encode()), 16)
        group = list(range(2, self.G.order-1))
        if 1< r < self.G.order - 1 and 1 < s < self.G.order:
            w = self.modinv(s, self.G.order)
            u1 = hm * w % self.G.order
            u2 = r * w % self.G.order
            dot1 = self.G * u1 + self.key['PA'] * u2
            r_ = dot1.x % self.G.order
            print("\tРезультат проверки подпси: {}".format(r == r_))
            if r == r_:
                return True
            else:
                return False
        else:
            return False


    def egcd(self, a, b):
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

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def print_exchange_data(self):
        print('Алгоритм обмена ключами:')
        print("\
\tСекретный ключ пользователя А: {}\n\
\tОткрытый ключ пользователя A: {}\n\
\tCекретный ключ пользователя B: {}\n\
\tОткрытый ключ пользователя B: {}\n\
\tОбщий секретный ключ (A, B): ({}, {})"
              .format(self.key['nA'], self.key['PA'],\
              self.key['nB'], self.key['PB'],\
                self.key['KA'], self.key['KB']))


class Dot(EllipticCurve):
    def __init__(self, x, y, elliptic_curve):
        self.x = x
        self.y = y
        self.order = None
        self.ec = elliptic_curve

    def __repr__(self):
        return "({}, {}, order: {})".format(self.x, self.y, self.order)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if self.x == other.x and self.y == (-1) * other.y % other.ec.M:
            return self.ec.elliptic_group[0]
        elif self == self.ec.elliptic_group[0]:
            return other
        elif other == self.ec.elliptic_group[0]:
            return self
        else:
            if self == other:
                lamb = (3 * self.x**2 + self.ec.a) * self.ec.modinv((2 * self.y),  self.ec.M)
            else:
                lamb = (other.y - self.y)* self.ec.modinv((other.x - self.x), self.ec.M)
        x3 = (lamb**2 - self.x - other.x) % self.ec.M
        y3 = (lamb * (self.x - x3) - self.y) % self.ec.M
        return Dot(x3, y3, self.ec)

    def __mul__(self, other: int):
        res = self
        other -= 1
        while other > 0:
            res = self + res
            other -= 1
        return res

    def determine_order(self):
        if self == self.ec.elliptic_group[0]:
            return 0
        ord = 1
        dot = self
        while True:
            if dot != self.ec.elliptic_group[0]:
                ord+=1
                dot = dot + self
            else:
                self.order = ord
                return ord




plaintext = "Hello"
ec = EllipticCurve(13)
r, s = ec.ecdsa(plaintext)
ec.check_ECDSA(plaintext, r, s)
