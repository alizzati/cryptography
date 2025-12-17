import numpy as np

def gcd(a, b):
    """Mencari Faktor Persekutuan Terbesar"""
    while b:
        a, b = b, a % b
    return a

def modInverse(a, m):
    """Mencari Invers Modulo (Algoritma Extended Euclidean)"""
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x

def matrix_mod_inverse(matrix, modulus):
    """Mencari Invers Matriks dalam Modulo tertentu"""
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = modInverse(det, modulus)
    
    matrix_inv = np.linalg.inv(matrix) * det
    matrix_inv = np.round(matrix_inv).astype(int)
    
    return (matrix_inv * det_inv) % modulus