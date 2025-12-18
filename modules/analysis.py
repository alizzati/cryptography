# modules/analysis.py
import numpy as np
import math
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64

def calculate_entropy(image):
    """Menghitung Shannon Entropy"""
    img_arr = np.array(image)
    marginal = np.histogramdd(np.ravel(img_arr), bins=256)[0] / img_arr.size
    marginal = list(filter(lambda p: p > 0, np.ravel(marginal)))
    entropy = -np.sum(np.array(marginal) * np.log2(np.array(marginal)))
    return entropy

def calculate_correlation(image1, image2):
    """Menghitung Korelasi Pixel"""
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
    """Peak Signal-to-Noise Ratio"""
    mse = np.mean((np.array(original) - np.array(compressed)) ** 2)
    if mse == 0: return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def calculate_npcr_uaci(img1, img2):
    """Menghitung NPCR & UACI"""
    arr1 = np.array(img1.convert('RGB'))
    arr2 = np.array(img2.convert('RGB'))
    
    if arr1.shape != arr2.shape: return 0, 0

    diff = arr1 != arr2
    npcr = (np.sum(diff) / diff.size) * 100

    diff_val = np.abs(arr1.astype(int) - arr2.astype(int))
    uaci = (np.sum(diff_val) / (diff_val.size * 255)) * 100

    return npcr, uaci

def generate_histogram(image, title="Histogram"):
    """
    Membuat Grafik Histogram dengan metode Object-Oriented (Thread Safe)
    agar gambar tidak hilang/blank saat diakses di Web.
    """
    img_arr = np.array(image)
    
    # Gunakan plt.subplots agar instance grafik terisolasi (aman untuk web)
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.set_title(title)
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")
    
    if len(img_arr.shape) == 3: # Gambar RGB
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            hist, bins = np.histogram(img_arr[:,:,i], bins=256, range=(0, 256))
            ax.plot(bins[:-1], hist, color=color, alpha=0.7)
    else: # Gambar Grayscale
        hist, bins = np.histogram(img_arr, bins=256, range=(0, 256))
        ax.plot(bins[:-1], hist, color='black')
        
    ax.set_xlim([0, 256])
    ax.grid(alpha=0.3)
    
    # Simpan ke buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    
    # Wajib close figure secara eksplisit
    plt.close(fig) 
    
    return data

def calculate_mse(image1, image2):
    """Menghitung Mean Squared Error (MSE). Target Dekripsi: 0"""
    arr1 = np.array(image1.convert('RGB'))
    arr2 = np.array(image2.convert('RGB'))
    
    if arr1.shape != arr2.shape:
        # Resize jika beda ukuran dikit (opsional, biar gak crash)
        image2 = image2.resize(image1.size)
        arr2 = np.array(image2.convert('RGB'))

    mse = np.mean((arr1 - arr2) ** 2)
    return mse

def calculate_entropy(image):
    img_arr = np.array(image)
    marginal = np.histogramdd(np.ravel(img_arr), bins=256)[0] / img_arr.size
    marginal = list(filter(lambda p: p > 0, np.ravel(marginal)))
    entropy = -np.sum(np.array(marginal) * np.log2(np.array(marginal)))
    return entropy

def calculate_correlation(image1, image2):
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
    mse = np.mean((np.array(original) - np.array(compressed)) ** 2)
    if mse == 0: return 100 # Anggap 100 dB sebagai Infinity (Sempurna)
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def calculate_npcr_uaci(img1, img2):
    arr1 = np.array(img1.convert('RGB'))
    arr2 = np.array(img2.convert('RGB'))
    if arr1.shape != arr2.shape: return 0, 0
    diff = arr1 != arr2
    npcr = (np.sum(diff) / diff.size) * 100
    diff_val = np.abs(arr1.astype(int) - arr2.astype(int))
    uaci = (np.sum(diff_val) / (diff_val.size * 255)) * 100
    return npcr, uaci

def generate_histogram(image, title="Histogram"):
    img_arr = np.array(image)
    plt.figure(figsize=(6, 4))
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    if len(img_arr.shape) == 3:
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            hist, bins = np.histogram(img_arr[:,:,i], bins=256, range=(0, 256))
            plt.plot(bins[:-1], hist, color=color, alpha=0.7)
    else:
        hist, bins = np.histogram(img_arr, bins=256, range=(0, 256))
        plt.plot(bins[:-1], hist, color='black')
    plt.xlim([0, 256])
    plt.grid(alpha=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    plt.close()
    return data