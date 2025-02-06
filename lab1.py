import binascii
import base64
import string
import datetime
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

def mt_brute_force(oracle):
    #print(oracle, "\n")
    # start: utime for beginning of day
    # end: current time
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    unix_timestamp = int(time.mktime(start_of_day.timetuple()))

    for i in range(unix_timestamp, (unix_timestamp + 86400), 1):
        twist = mersenneTwister(i)
        num = twist.get_random_num()
        decimal_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
        base64_encoded = base64.b64encode(decimal_bytes).decode('utf-8')
        #print(base64_encoded)
        if base64_encoded == oracle:
            return i
    return -1

def unmix(slst):
    # inverse of get_random_num (extract_number)
    """
    need to go reverse steps
    1: xor returned y with itself to get og y
    2: split new y into 11 bits, xor with y >> 11, mask, and????
    3: continue, then do the same process for the last 10 bits
    4: ????????
    """
    state = []
    samples = []
    L = 18
    T = 15
    C = 0xEFC60000
    S = 7
    B = 0x9D2C5680
    U = 11
    for s in slst:
        stemp = base64.b64decode(s).split(b':')
        for a in stemp:
            samples.append(a)

    for sample in samples:
        y = undo_right_transform(sample, L)
        y = undo_left_transform(y, T, C)
        y = undo_left_transform(y, S, B)
        y = undo_right_transform(y, U)
        state.append(y)

    return state
    

def undo_right_transform(value, shift):
    W = 32 # Word size, defined by MT19937
    res = value

    for i in range(0, W, shift):
        # Work on the next shift sized portion at a time by generating a mask for it.
        portion_mask = '0' * i + '1' * shift + '0' * (W - shift - i)
        portion_mask = int(portion_mask[:W], 2)
        portion = int(res) & portion_mask

        res = int(res) ^ int(portion >> shift)

    return res

def undo_left_transform(value, shift, mask):
    W = 32 # Word size, defined by MT19937
    res = value
    for i in range(0, W, shift):
        # Work on the next shift sized portion at a time by generating a mask for it.
        portion_mask = '0' * (W - shift - i) + '1' * shift + '0' * i
        portion_mask = int(portion_mask, 2)
        portion = int(res) & portion_mask

        res ^= ((portion << shift) & mask)

    return res

t = ["MjMyMTc0NzE2NzoxNDIxNjIwNzk3OjI4ODc3NDUwOTY6NzM5MzIxNDQzOjE4MTI2MTU1NTI6MzIzMDEwMjgyMTo5OTc3OTc5ODI6NDQwNTkyMTQ2",
     "Mzk3Njk1MTI2MTozMDUzODkyNzIwOjI3MDQ1MDIxNzE6MTI5MTEzODkxNToxMTk3MTk5NTAxOjI4MTA2MDU5NzoxODQ5NjQ2NDIwOjM0NjM2OTMxNA==",
     "MTcwMzkzNzcwOjM0MTM2MjEwODk6MzUzMTA2NDU5MDoyNTQ5Mjc0MzMzOjIyMTEwOTg2NDk6MjYxMDcwODcxODozMDMzMDc5MTQwOjE4NzcxNTI0ODQ=",
     "MjYzMTYxNTYxNzoxNDg5OTk2NzUwOjI3Njc1OTY0Nzk6MTkwOTU0NDAwOToxNTk0MzMyODg5OjQxMjU4ODcyNzU6MzE4MzAwNDk4MDoxNDc3NzYyOTk5",
     "NDE1Mzg4NzM3OTozODczODQ4MDAyOjI3MTkwNTE5MTg6ODU0MzE2NzE0OjIyODMxNzQxNTk6MTE4ODE5MjM4NzozNjkxNjkxODg0OjY2ODkxMzc0NA==",
     "MzE0NzU5OTE5MzoxMjUyODIzODM6MzcwOTcxNzMzMjoyMDkxMjk3MDYwOjE3OTA2NjAzODA6NzA3MzY5NzQ0OjMxOTk2NzQyMzc6MzIzOTQ5NzcxMg==",
     "MjQ1ODU3ODM1NDoxOTk4NzY2OTAxOjg0NDM3MDkyOjM4OTc2NjY0MDU6MzQ3Nzg2NzEyOjQxMzg3MTQyMDM6Mzc2MDc5MTEwMDoyNTk4NTc0Mjk4"]
print(base64.b64decode(t[0]).split(b':'))
#print(unmix(t))
x = unmix(t)
print(x)
#a = (x[1]).to_bytes(32)
#print(mt_brute_force(base64.b64encode(a)))
#print(mt_brute_force(x[1]))
#print(unmix(samples))


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

#print(mt_brute_force(oracle()))
#print(time.time())

# make sure seed is 32 bits












