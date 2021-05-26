import random
import math
from lib import *

def _gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def GCD_extended(a, b):
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, b
    while v3 != 0:
        q = u3//v3
        t1, t2, t3 = u1 - q*v1, u2 - q*v2, u3 - q*v3
        u1, u2, u3 = v1, v2, v3
        v1, v2, v3 = t1, t2, t3
    return u1, u2, u3

def _get_d(e, phi):
    d = GCD_extended(e,phi)[0] #[x,y,z] #d = x
    if d < 0:
        d+= phi
    
    return d

def _random_n_bit(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)

def _first_primes_list(limit):
    limitn = limit+1
    primes = dict()
    for i in range(2, limitn): primes[i] = True

    for i in primes:
        factors = range(i,limitn, i)
        for f in factors[1:]:
            primes[f] = False
    return [i for i in primes if primes[i]==True]

def _get_low_level_prime(n):
    while True:
        pc = _random_n_bit(n)
        for divisor in _first_primes_list(1000):
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc

def _rabin_miller_test(n):
    s = 0
    m = n-1
    while m % 2 == 0:
        m >>= 1
        s += 1
    assert(2**s * m == n-1)
  
    def trial_composite(a):
        if pow(a, m, n) == 1:  # (a^m) mod n == 1
            return False
        for i in range(s):
            if pow(a, 2**i * m, n) == n-1:
                return False
        return True
 
    for i in range(20):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True

def generate_big_prime(bits):
    p = _get_low_level_prime(bits)
    while not _rabin_miller_test(p):
        p = _get_low_level_prime(bits)
    return p

def generate_keypair(p = 0, q = 0):
    if p == 0:
        p = generate_big_prime(256)
    if q == 0:
        q = generate_big_prime(256)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    g = _gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = _gcd(e, phi)
    d = _get_d(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    plain_int = string_to_int(plaintext, len(plaintext))
    cipher_int = pow(plain_int, key, n)
    ciphers = int_to_base64(cipher_int)
    return ciphers

def decrypt(pk, ciphertext):
    key, n = pk
    cipher_int = base64_to_int(ciphertext)
    plain_int = pow(cipher_int, key, n)
    str_plaint_int = str(plain_int)
    while len(str_plaint_int) % 4 != 0:
        str_plaint_int = '0'+str_plaint_int
    i = 0
    plain_text = ''
    while i != len (str_plaint_int):
        c = str_plaint_int[i:i+4]
        i += 4
        plain_text += chr(int(c))
    return plain_text

if __name__ == '__main__':
    p = generate_big_prime(128)
    q = generate_big_prime(128)
    pub, pri = generate_keypair(p, q)
    mess = "hello khánh"
    print(f'mess: {mess}')
    encrypts = encrypt(pri, mess)
    print(f'encrypt signature: {encrypts}')
    dmess = decrypt(pub, encrypts)
    print(f'decrypt mess: {dmess}')