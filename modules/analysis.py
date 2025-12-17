# modules/analysis.py
import numpy as np
import math

def calculate_entropy(image):
    """Menghitung Shannon Entropy (Target: mendekati 8.0)"""
    img_arr = np.array(image)
    marginal = np.histogramdd(np.ravel(img_arr), bins=256)[0] / img_arr.size
    marginal = list(filter(lambda p: p > 0, np.ravel(marginal)))
    entropy = -np.sum(np.array(marginal) * np.log2(np.array(marginal)))
    return entropy

def calculate_correlation(image1, image2):
    """Menghitung Korelasi Pixel (Target: mendekati 0 untuk enkripsi)"""
    # Convert to grayscale for simplicity in calculation
    arr1 = np.array(image1.convert('L')).flatten()
    arr2 = np.array(image2.convert('L')).flatten()
    
    if len(arr1) != len(arr2): return 0
    
    mean1 = np.mean(arr1)
    mean2 = np.mean(arr2)
    
    numerator = np.sum((arr1 - mean1) * (arr2 - mean2))
    denominator = np.sqrt(np.sum((arr1 - mean1)**2) * np.sum((arr2 - mean2)**2))
    
    if denominator == 0: return 0
    return abs(numerator / denominator)

def calculate_psnr(original, compressed):
    """Peak Signal-to-Noise Ratio (Untuk mengukur kualitas noise)"""
    mse = np.mean((np.array(original) - np.array(compressed)) ** 2)
    if mse == 0: return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr