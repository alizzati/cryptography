from flask import Flask, render_template, request
from modules.hill_cipher import generate_hill_key, process_image_hill
from modules.rabin_p import generate_rabin_keys, rabin_encrypt_val
from modules.analysis import calculate_entropy, calculate_correlation, calculate_psnr, calculate_npcr_uaci, generate_histogram, calculate_mse
from PIL import Image
import numpy as np
import io
import base64
import time

app = Flask(__name__)

def image_to_base64(img):
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode('ascii')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        file = request.files.get('image')
        
        if not file:
            return render_template('index.html', error="File belum diupload!")

        try:
            img = Image.open(file)
            
            if action == 'encrypt':
                hill_key = generate_hill_key()
                n, p, q = generate_rabin_keys()
                
                # 1. Analisis Gambar Asli
                entropy_original = calculate_entropy(img)
                hist_original = generate_histogram(img, "Histogram: Gambar Asli")
                
                # 2. Proses Enkripsi
                start_time = time.time()
                cipher_img = process_image_hill(img, hill_key, 'encrypt')
                end_time = time.time()
                
                # 3. Analisis Gambar Cipher
                entropy_cipher = calculate_entropy(cipher_img)
                correlation_val = calculate_correlation(img, cipher_img)
                psnr_val = calculate_psnr(img, cipher_img)
                npcr_val, uaci_val = calculate_npcr_uaci(img, cipher_img)
                hist_cipher = generate_histogram(cipher_img, "Histogram: Cipher Image")
                
                return render_template('index.html', 
                                       mode='encrypt',
                                       image_data=image_to_base64(cipher_img),
                                       hill_key=hill_key.tolist(),
                                       rabin_n=n, rabin_p=p, rabin_q=q,
                                       time_taken=end_time-start_time,
                                       entropy_orig=round(entropy_original, 5),
                                       entropy_enc=round(entropy_cipher, 5),
                                       correlation=round(correlation_val, 5),
                                       psnr=round(psnr_val, 5),
                                       npcr=round(npcr_val, 4),
                                       uaci=round(uaci_val, 4),
                                       hist_orig=hist_original,
                                       hist_enc=hist_cipher)

            elif action == 'decrypt':
                try:
                    k00 = int(request.form.get('k00'))
                    k01 = int(request.form.get('k01'))
                    k10 = int(request.form.get('k10'))
                    k11 = int(request.form.get('k11'))
                    
                    # Cek apakah ada file Original Image untuk verifikasi MSE
                    original_file = request.files.get('original_image_verify')
                    
                    key_matrix = np.array([[k00, k01], [k10, k11]])
                    
                    # 1. Proses Dekripsi
                    start_time = time.time()
                    plain_img = process_image_hill(img, key_matrix, 'decrypt')
                    end_time = time.time()

                    # 2. Analisis Dasar (Histogram & Entropy Hasil Dekripsi)
                    hist_dec = generate_histogram(plain_img, "Histogram: Hasil Dekripsi")
                    entropy_dec = calculate_entropy(plain_img)

                    # 3. Analisis Perbandingan (Jika user upload gambar asli)
                    analysis_data = None
                    if original_file:
                        orig_img_verify = Image.open(original_file)
                        mse_val = calculate_mse(orig_img_verify, plain_img)
                        psnr_val = calculate_psnr(orig_img_verify, plain_img)
                        corr_val = calculate_correlation(orig_img_verify, plain_img)
                        
                        analysis_data = {
                            'mse': round(mse_val, 5),
                            'psnr': round(psnr_val, 5),
                            'correlation': round(corr_val, 5)
                        }

                    return render_template('index.html', 
                                           mode='decrypt', 
                                           image_data=image_to_base64(plain_img),
                                           time_taken=end_time-start_time,
                                           hist_dec=hist_dec,
                                           entropy_dec=round(entropy_dec, 5),
                                           analysis=analysis_data)
                except Exception as e:
                    return render_template('index.html', error=f"Kunci Salah: {e}")

        except Exception as e:
             return render_template('index.html', error=f"Error: {e}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)