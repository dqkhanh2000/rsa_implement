from math import floor, sin, pow
import struct
import numpy as np
from enum import Enum
from bitarray import bitarray
#
# A = 0x67452301
# B = 0xEFCDAB89
# C = 0x98BADCFE
# D = 0x10325476

f1 = lambda b, c, d: ((b & c) | ((~b) & d)) & 0xFFFFFFFF
f2 = lambda b, c, d: ((b & d) | (c & (~d))) & 0xFFFFFFFF
f3 = lambda b, c, d: (b ^ c ^ d) & 0xFFFFFFFF
f4 = lambda b, c, d: (c ^ (b | (~d))) & 0xFFFFFFFF


def leftrotate(x, c):
    """ Left rotate the number x by c bytes."""
    x &= 0xFFFFFFFF
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def leftshift(x, c):
    """ Left shift the number x by c bytes."""
    return x << c



class HashMD5(object):
    def __init__(self):
        self.byteorder = 'little'
        self.block_size = 64
        self.digest_size = 16
        # Internal data
        s = [0] * 64
        K = [0] * 64
        # Initialize s, s specifies the per-round shift amounts
        s[0:16] = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
        s[16:32] = [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
        s[32:48] = [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
        s[48:64] = [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        for i in range(64):
            K[i] = floor(2 ** 32 * abs(sin(i + 1))) & 0xFFFFFFFF
        # Store it
        self._s = s
        self._K = K
        # Initialize variables:
        a0 = 0x67452301  # A
        b0 = 0xefcdab89  # B
        c0 = 0x98badcfe  # C
        d0 = 0x10325476  # D
        self.hash_pieces = [a0, b0, c0, d0]

    def hash(self, arg,type='text'):
        def readF(arg):
            return open(arg,'rb').read()
        if type == 'file':
            arg = readF(arg)
        else:
            arg = arg.encode('utf-8')
        s, K = self._s, self._K
        a0, b0, c0, d0 = self.hash_pieces

        data = bytearray(arg)
        origin_len_of_bits = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
        pres = 0x80

        print(int.from_bytes(b'0x80','big'))
        data.append(0x80)
        while len(data) % 64 != 56:
            data.append(0)
        data += origin_len_of_bits.to_bytes(8, byteorder='little')
        print(range(0, len(data), 64))
        for offset in range(0, len(data), 64):
            chunks = data[offset: offset + 64]

            A, B, C, D = a0, b0, c0, d0
            for i in range(64):
                if 0 <= i <= 15:
                    F = f1(B, C, D)
                    g = i
                elif 16 <= i <= 31:
                    F = f2(B, C, D)
                    g = (5 * i + 1) % 16
                elif 32 <= i <= 47:
                    F = f3(B, C, D)
                    g = (3 * i + 5) % 16
                elif 48 <= i <= 63:
                    F = f4(B, C, D)
                    g = (7 * i) % 16
                to_rotate = (A + F + K[i] + int.from_bytes(chunks[4 * g: 4 * g + 4], byteorder='little')) & 0xFFFFFFFF
                new_B = (B + leftrotate(to_rotate, s[i])) & 0xFFFFFFFF
                A, B, C, D = D, new_B, B, C
            a0 = (a0 + A) & 0xFFFFFFFF
            b0 = (b0 + B) & 0xFFFFFFFF
            c0 = (c0 + C) & 0xFFFFFFFF
            d0 = (d0 + D) & 0xFFFFFFFF
        self.hash_pieces = [a0, b0, c0, d0]

    def hexdigest(self):
        def digest(list_hash):
            return sum(leftshift(x, (32 * ig)) for ig, x in enumerate(list_hash))

        digest = digest(self.hash_pieces)
        raw = digest.to_bytes(16, byteorder="little")
        fortmatStr = '{:0' + str(2 * 16) + 'x}'
        print(fortmatStr)
        return fortmatStr.format(int.from_bytes(raw, byteorder="big"))

# if __name__ == '__main__':
#     h1 = HashMD5()
#     h1.hash('a')
#     print(h1.hexdigest())