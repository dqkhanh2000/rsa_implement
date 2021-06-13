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
        p = generate_big_prime(32)
    if q == 0:
        q = generate_big_prime(32)
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

def split_big_int(data, n_in_key):
    """
    plit data into multiple numbers less than n in key

    Args:
        data (int): big number
        n_in_key (int): number n in the private key

    Returns:
        list: list number
    """
    list_lest_than_n = []
    x = ""
    size_n = len(str(n_in_key))
    while size_n % 4 != 0:
        size_n -= 1
    for i in data:
        if len(x) == size_n:
            list_lest_than_n.append(int(x))
            x = ""
        x+= i
    list_lest_than_n.append(int(x))
    return list_lest_than_n

def encrypt(key, plaintext):
    """encrypt data C = (𝑚^𝑒) 𝑚𝑜𝑑 𝑛

    Args:
        public_key (e, n)
        plaintext (string)

    Returns:
        string base 64 encrypt data
    """
    e, n = key
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    plain_int = string_to_int(plaintext)
    print(f'plain in integer: {plain_int}, length: {len(str(int(plain_int)))}')

    split_data = split_big_int(plain_int, n)
    ciphers = ''
    for m in split_data:
        c = pow(m, e, n)
        cipher = int_to_base64(c)
        ciphers += cipher +' '

    return ciphers

def decrypt(pk, ciphertext):
    """decrypt cipher text using C=𝑐^𝑑 𝑚𝑜𝑑 𝑛

    Args:
        public_key (d, n)
        plaintext (string)

    Returns:
        string plain text
    """

    d, n = pk
    plain_text = ''
    list_base = ciphertext.split(' ')
    list_base.pop()
    for c in list_base:
        cipher_int = base64_to_int(c)
        plain_int = pow(cipher_int, d, n)
        str_plaint_int = str(plain_int)
        while len(str_plaint_int) % 4 != 0:
            str_plaint_int = '0'+str_plaint_int
            
        plain_text += str_plaint_int
    return int_to_string(plain_text)

if __name__ == '__main__':
    p = generate_big_prime(16)
    q = generate_big_prime(16)
    pub, pri = generate_keypair(p, q)
    print(f'public key: e={pub[0]}, n={pub[1]}')
    print(f'private key: d={pri[0]}, n={pri[1]}')
    mess = "hello khánh"
    print(f'mess: {mess}')
    encrypts = encrypt(pri, mess)
    print(f'cipher signature: {encrypts}')
    dmess = decrypt(pub, encrypts)
    print(f'decrypt mess: {dmess}')