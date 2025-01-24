import binascii
import base64
import string


def init_state(seed):

    # word size
    w = 32

    # state size
    n = 624

    # middle word
    m = 397

    # separation point
    r = 31

    # bit masks:

    # twisting coefficient
    a = 0x9908B0DF

    # tempering masks
    b = 0x9D2C5680
    c = 0xEFC60000

    # tempering bit shifts
    s = 7
    t = 15

    # additional tempering
    u = 11
    d = 0xFFFFFFFF
    l = 18

    # some parameter not part of the alg but needed for func
    f = 1812433253


    state = [0] * n

    state[0] = seed

    for i in range(1, n-1):
        seed = f * (seed ^ (seed >> (w - 2))) + i









