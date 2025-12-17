from flask import Flask, render_template, request
from modules.hill_cipher import generate_hill_key, process_image_hill
from modules.rabin import generate_rabin_keys, rabin_encrypt_val
from PIL import Image
import numpy as np
import io
import base64
import time

app = Flask(__name__)

def image_to_base64(img):
    """Helper untuk mengubah gambar jadi string agar bisa tampil di HTML"""
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
            
            # --- SKENARIO ENKRIPSI ---
            if action == 'encrypt':
                # 1. Generate Kunci Hill (Matriks)
                hill_key = generate_hill_key()
                
                # 2. Generate Kunci Rabin (Asimetris)
                n, p, q = generate_rabin_keys()
                
                # 3. Proses Enkripsi Gambar
                start_time = time.time()
                cipher_img = process_image_hill(img, hill_key, 'encrypt')
                end_time = time.time()
                
                # 4. Simulasi Pengamanan Kunci (Opsional, ditampilkan datanya)
                # Misal: Mengenkripsi salah satu elemen matriks menggunakan Rabin
                encrypted_key_element = rabin_encrypt_val(int(hill_key[0][0]), n)
                
                return render_template('index.html', 
                                       mode='encrypt',
                                       image_data=image_to_base64(cipher_img),
                                       hill_key=hill_key.tolist(),
                                       rabin_n=n,
                                       rabin_p=p,
                                       rabin_q=q,
                                       time_taken=end_time-start_time)

            # --- SKENARIO DEKRIPSI ---
            elif action == 'decrypt':
                try:
                    # Ambil input kunci dari user
                    k00 = int(request.form.get('k00'))
                    k01 = int(request.form.get('k01'))
                    k10 = int(request.form.get('k10'))
                    k11 = int(request.form.get('k11'))
                    
                    key_matrix = np.array([[k00, k01], [k10, k11]])
                    
                    # Proses Dekripsi
                    plain_img = process_image_hill(img, key_matrix, 'decrypt')
                    
                    return render_template('index.html',
                                           mode='decrypt',
                                           image_data=image_to_base64(plain_img))
                                           
                except Exception as e:
                    return render_template('index.html', error=f"Kunci Salah atau Tidak Valid: {e}")

        except Exception as e:
             return render_template('index.html', error=f"Terjadi Kesalahan File: {e}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)