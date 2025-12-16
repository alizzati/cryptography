// --- BAGIAN 1: HELPER MATEMATIKA ---

// Fungsi Modulo yang aman (karena hasil % di JS bisa negatif)
function mod(n, m) {
    return ((n % m) + m) % m;
}

// Cari Invers Modular (Brute force sederhana karena m=256 kecil)
// Mencari x dimana: (a * x) % m == 1
function modInverse(a, m) {
    a = mod(a, m);
    for (let x = 1; x < m; x++) {
        if ((a * x) % m === 1) return x;
    }
    return -1; // Tidak ada invers (jika determinan genap/kelipatan 2)
}

function invertMatrix(keyMatrix) {
    let k00 = keyMatrix[0][0]; let k01 = keyMatrix[0][1];
    let k10 = keyMatrix[1][0]; let k11 = keyMatrix[1][1];

    // 1. Hitung Determinan
    let det = (k00 * k11) - (k01 * k10);
    det = mod(det, 256);

    // 2. Cari Invers Determinan
    let detInv = modInverse(det, 256);
    if (detInv === -1) {
        throw new Error("Determinan tidak memiliki invers modulo 256. Ganti kunci!");
    }

    // 3. Matriks Adjoin (Tukar posisi diagonal utama, negasikan diagonal lain)
    // [ d, -b ]
    // [ -c, a ]
    let a = k11;
    let b = -k01;
    let c = -k10;
    let d = k00;

    // 4. Kalikan Adjoin dengan Invers Determinan
    let i00 = mod(d * detInv, 256);
    let i01 = mod(b * detInv, 256);
    let i10 = mod(c * detInv, 256);
    let i11 = mod(a * detInv, 256);

    return [[i00, i01], [i10, i11]];
}

/**
 * Mengenkripsi pasangan nilai [v1, v2] dengan matriks kunci 2x2
 */
function encryptVector(vector, keyMatrix) {
    let v1 = vector[0];
    let v2 = vector[1];
    
    // Rumus Hill Cipher: C = K * P mod 256
    let c1 = mod((keyMatrix[0][0] * v1 + keyMatrix[0][1] * v2), 256);
    let c2 = mod((keyMatrix[1][0] * v1 + keyMatrix[1][1] * v2), 256);
    
    return [c1, c2];
}

// --- BAGIAN 3: MANIPULASI GAMBAR (IMAGE PROCESSING) ---

function processImage(action) {
    const canvas = document.getElementById('myCanvas');
    const ctx = canvas.getContext('2d');
    const statusText = document.getElementById('statusText');

    if (canvas.width === 0) { alert("Upload gambar dulu!"); return; }

    let k00 = parseInt(document.getElementById('k00').value);
    let k01 = parseInt(document.getElementById('k01').value);
    let k10 = parseInt(document.getElementById('k10').value);
    let k11 = parseInt(document.getElementById('k11').value);

    // Cek Determinan Genap (Ganjil wajib untuk Hill Cipher Mod 256)
    let det = (k00 * k11) - (k01 * k10);
    if (mod(det, 2) === 0) {
        alert("Error: Determinan Matriks GENAP! Tidak bisa diproses. Ubah angka kunci (misal ganti 2 jadi 3).");
        return;
    }

    let keyMatrix = [[k00, k01], [k10, k11]];

    // JIKA DEKRIPSI: KITA BALIK MATRIKS KUNCINYA
    if (action === 'decrypt') {
        try {
            console.log("Menghitung Invers Matriks untuk Dekripsi...");
            keyMatrix = invertMatrix(keyMatrix); 
            console.log("Key Invers:", keyMatrix);
        } catch (e) {
            alert(e.message);
            return;
        }
        statusText.innerText = "Mendekripsi gambar... (Mengembalikan ke asal)";
    } else {
        statusText.innerText = "Mengenkrpsi gambar... (Mengacak piksel)";
    }
    
    // Eksekusi (Timeout agar UI tidak freeze)
    setTimeout(() => {
        executeProcess(ctx, canvas.width, canvas.height, keyMatrix, action);
    }, 50);
}

function executeProcess(ctx, width, height, keyMatrix, actionName) {
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data; 

    // --- PENGAMBILAN DATA (OPSIONAL HARI INI) ---
    console.time(actionName); // Mulai stopwatch

    let rgbValues = [];
    // Pisahkan data piksel (abaikan Alpha channel)
    for (let i = 0; i < data.length; i += 4) {
        rgbValues.push(data[i], data[i+1], data[i+2]);
    }
    // Padding jika ganjil
    let paddingAdded = false;
    if (rgbValues.length % 2 !== 0) {
        rgbValues.push(0);
        paddingAdded = true;
    }

    // --- CORE LOOP ---
    let resultValues = [];
    for (let i = 0; i < rgbValues.length; i += 2) {
        let vector = [rgbValues[i], rgbValues[i+1]];
        // Gunakan fungsi encryptVector yang sama (karena Dekripsi Hill = Enkripsi dengan Kunci Invers)
        let res = encryptVector(vector, keyMatrix);
        resultValues.push(res[0], res[1]);
    }

    console.timeEnd(actionName); // Stop stopwatch & lihat di Console

    // Masukkan kembali ke data gambar
    let idx = 0;
    for (let i = 0; i < data.length; i += 4) {
        data[i]   = resultValues[idx++]; 
        data[i+1] = resultValues[idx++];
        data[i+2] = resultValues[idx++];
        // Alpha tetap 255 (tidak transparan)
    }

    ctx.putImageData(imageData, 0, 0);
    document.getElementById('statusText').innerText = `Proses ${actionName} Selesai!`;
}

function encryptVector(vector, keyMatrix) {
    let v1 = vector[0]; let v2 = vector[1];
    let c1 = mod((keyMatrix[0][0] * v1 + keyMatrix[0][1] * v2), 256);
    let c2 = mod((keyMatrix[1][0] * v1 + keyMatrix[1][1] * v2), 256);
    return [c1, c2];
}

// --- BAGIAN 4: HELPER UPLOAD ---
// (Sama seperti sebelumnya)
document.getElementById('imageInput').addEventListener('change', function(e) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.getElementById('myCanvas');
            const ctx = canvas.getContext('2d');
            // Resize canvas agar pas dengan gambar
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            document.getElementById('statusText').innerText = `Gambar dimuat: ${img.width}x${img.height} px`;
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(e.target.files[0]);
});