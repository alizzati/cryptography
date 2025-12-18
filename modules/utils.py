import numpy as np

def gcd(a, b):
    """Mencari Faktor Persekutuan Terbesar"""
    while b:
        a, b = b, a % b
    return a

def modInverse(a, m):
    """
    Mencari Invers Modulo.
    Menggunakan int() untuk memastikan tipe data bukan numpy.int64
    agar fungsi pow() bawaan Python tidak error.
    """
    try:
        # WAJIB CAST ke int() agar tidak crash dengan NumPy
        return pow(int(a), -1, int(m))
    except ValueError:
        return None

def matrix_mod_inverse(matrix, modulus):
    """
    Mencari Invers Matriks Modulo.
    Menangani matriks 2x2 secara manual dengan integer murni.
    """
    # Khusus Matriks 2x2 (Sesuai Hill Cipher Skripsi)
    if matrix.shape == (2, 2):
        # Ambil elemen dan paksa jadi integer Python standar
        a = int(matrix[0, 0])
        b = int(matrix[0, 1])
        c = int(matrix[1, 0])
        d = int(matrix[1, 1])
        
        # 1. Hitung Determinan (ad - bc)
        det = a * d - b * c
        
        # 2. Cari Invers Determinan dalam Modulo
        # Gunakan % modulus agar determinan negatif jadi positif
        det_inv = modInverse(det % modulus, modulus)
        
        if det_inv is None:
            raise ValueError("Determinan matriks tidak memiliki invers modulo (Kunci Hill Tidak Valid)")
            
        # 3. Matriks Adjoin 2x2: [[d, -b], [-c, a]]
        #    Langsung dimodulo agar tidak ada angka negatif
        adj = np.array([
            [d, -b],
            [-c, a]
        ])
        
        # 4. Kalikan Adjoin dengan Invers Determinan
        matrix_inv = (adj * det_inv) % modulus
        
        return matrix_inv.astype(int)

    else:
        # Fallback untuk matriks NxN (Umum)
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = modInverse(det % modulus, modulus)
        
        if det_inv is None:
            raise ValueError("Determinan matriks tidak memiliki invers modulo")

        matrix_inv = np.linalg.inv(matrix) * det
        matrix_inv = np.round(matrix_inv).astype(int)
        
        return (matrix_inv * det_inv) % modulus