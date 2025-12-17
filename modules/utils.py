import numpy as np

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modInverse(a, m):
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
    # Hitung determinan dengan pembulatan yang aman
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = modInverse(det, modulus)
    
    # Hitung Invers menggunakan Adjoin (Inverse * det)
    # Ini trik agar kita tidak bermain dengan float 1/det
    matrix_inv = np.linalg.inv(matrix) * det
    matrix_inv = np.round(matrix_inv).astype(int)
    
    # Hasil akhir modulo modulus
    return (matrix_inv * det_inv) % modulus