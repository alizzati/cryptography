import random
import math
from .utils import gcd, modInverse

def is_prime(n):
    """Cek apakah bilangan prima (Sederhana untuk demo)"""
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def generate_rabin_keys():
    """
    Generate Public Key (N) dan Private Key (p, q).
    Syarat Rabin: p dan q harus kongruen 3 mod 4.
    """
    # Range prima diperkecil agar cepat saat demo. 
    # Untuk skripsi real, gunakan range lebih besar (misal 1000-10000)
    primes = [i for i in range(100, 500) if is_prime(i) and i % 4 == 3]
    
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
        
    n = p * q
    return n, p, q

def rabin_encrypt_val(m, n):
    """Enkripsi Rabin: C = m^2 mod n"""
    return (m ** 2) % n

def rabin_decrypt_val(c, p, q):
    """Dekripsi Rabin menghasilkan 4 kemungkinan akar"""
    n = p * q
    
    # Algoritma CRT (Chinese Remainder Theorem)
    mp = pow(c, (p + 1) // 4, p)
    mq = pow(c, (q + 1) // 4, q)
    
    yp = p * modInverse(p, q)
    yq = q * modInverse(q, p)
    
    r1 = (yp * mp + yq * mq) % n
    r2 = n - r1
    r3 = (yp * mp - yq * mq) % n
    r4 = n - r3
    
    return [r1, r2, r3, r4]