import binascii
import base64
import string
import time
import random


class mersenneTwister:
    def __init__(self, seed):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.b = 0x9D2C5680
        self.c = 0xEFC60000
        self.s = 7
        self.t = 15
        self.u = 11
        self.d = 0xFFFFFFFF
        self.l = 18
        self.f = 1812433253
        self.UMASK = (self.d << self.r) & self.d
        self.LMASK = (self.d >> (self.w - self.r)) & self.d
        self.state = [0] * self.n
        self.state[0] = seed & self.d

        for i in range(1, self.n):
            self.state[i] = (self.f * (self.state[i - 1] ^ (self.state[i - 1] >> (self.w - 2))) + i) & self.d

        self.idx = 0

    def twist(self):
        for i in range(self.n):
            x = (self.state[i] & self.UMASK) | (self.state[(i + 1) % self.n] & self.LMASK)

            xA = x >> 1
            if x & 1:
                xA ^= self.a

            self.state[i] = (self.state[(i + self.m) % self.n] ^ xA) & self.d
        self.idx = 0
    
    def get_random_num(self):
        if self.idx >= self.n:
            self.twist()

        y = self.state[self.idx]
        self.idx += 1

        y ^= (y >> self.u)
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= (y >> self.l)

        return y & 0xFFFFFFFF

def oracle():
    # wait between 5 and 60 seconds, generated randomly
    wait = random.randint(5, 60)
    time.sleep(wait)
    utime = int(time.time())
    # seed MT19937 with utime
    twist = mersenneTwister(utime)
    wait = random.randint(5, 60)
    num = twist.get_random_num()
    decimal_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    base64_encoded = base64.b64encode(decimal_bytes).decode('utf-8')

    return base64_encoded

# def mersenne(seed):

#     # word size
#     w = 32

#     # state size
#     n = 624

#     # middle word
#     m = 397

#     # separation point
#     r = 31

#     # bit masks:

#     # twisting coefficient
#     a = 0x9908B0DF

#     # tempering masks
#     b = 0x9D2C5680
#     c = 0xEFC60000

#     # tempering bit shifts
#     s = 7
#     t = 15

#     # additional tempering
#     u = 11
#     d = 0xFFFFFFFF
#     l = 18

#     # some parameter not part of the alg but needed for func
#     f = 1812433253

#     # upper mask and lower mask
#     UMASK = (0xFFFFFFFF << r) & 0xFFFFFFFF
#     LMASK = (0xFFFFFFFF >> (w - r)) & 0xFFFFFFFF

#     state = [0] * n

#     state[0] = seed

#     for i in range(1, n):
#         state[i] = (f * (state[i - 1] ^ (state[i - 1] >> (w - 2))) + i) & 0xFFFFFFFF

#     idx = 0
        
#     def twist():
#         nonlocal idx
#         j = idx - (n - 1)

#         if j < 0:
#             j += n

#         x = (state[idx] & UMASK) | (state[(j) % n] & LMASK)
#         xA = x >> 1
        
#         if x & 1:
#             xA ^= a

#         j = idx - (n - m)
#         if j < 0:
#             j += n

#         x = state[j] ^ xA
#         state[idx] = x
#         idx += 1

#         if idx >= n:
#             idx = 0

#         y = x ^ (x >> u)
#         y = y ^ ((y << s) & b)
#         y = y ^ ((y << t) & c)
#         z = y ^ (y >> l)

#         return z & 0xFFFFFFFF
    
#     return twist()


"""twist = mersenneTwister(123)
num1 = twist.get_random_num()
num2 = twist.get_random_num()
num3 = twist.get_random_num()

print(num1)
print(num2)
print(num3)"""

print(oracle())
#print(time.time())

# make sure seed is 32 bits












