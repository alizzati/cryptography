import numpy as np
from PIL import Image
from .utils import gcd, matrix_mod_inverse

def generate_hill_key(n=2):
    """Generate Matriks Kunci NxN yang memiliki invers modulo 256"""
    while True:
        key = np.random.randint(0, 256, (n, n))
        det = int(np.round(np.linalg.det(key)))
        # Syarat: Determinan tidak boleh 0 dan harus koprima dengan 256
        if det != 0 and gcd(det, 256) == 1:
            return key

def process_image_hill(img, key, mode='encrypt'):
    """Proses Enkripsi/Dekripsi Gambar"""
    img_array = np.array(img)
    original_shape = img_array.shape
    
    # Ratakan array (Flatten)
    flat_array = img_array.flatten()
    
    # Padding jika jumlah pixel ganjil
    padding = 0
    if len(flat_array) % 2 != 0:
        padding = 1
        flat_array = np.append(flat_array, 0)
    
    # Ubah bentuk array agar sesuai perkalian matriks (N x 2)
    reshaped_array = flat_array.reshape(-1, 2)
    
    if mode == 'encrypt':
        # Rumus Enkripsi: C = P * K mod 256
        processed_array = np.dot(reshaped_array, key) % 256
    else:
        # Rumus Dekripsi: P = C * K^-1 mod 256
        inv_key = matrix_mod_inverse(key, 256)
        processed_array = np.dot(reshaped_array, inv_key) % 256
        
    # Kembalikan ke bentuk asal
    result_flat = processed_array.flatten()
    
    if padding:
        result_flat = result_flat[:-padding]
        
    result_array = result_flat.reshape(original_shape).astype(np.uint8)
    return Image.fromarray(result_array)