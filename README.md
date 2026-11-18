# SIMUTEH - Pemeriksaan Mutu Daun Teh (P1-P6)

Sistem Pemeriksaan Mutu Daun Teh berbasis citra untuk kelompok tani teh rakyat di Kabupaten Sukabumi.
Repository ini memuat tahap **akuisisi** dan **praproses** (Pertemuan 1-4) mata kuliah Computer Vision.

- **Nama / NIM:** Muhammad Imam Faisal / 2330511016
- **SEED dataset:** `1016` (4 digit terakhir NIM)
- **Python:** 3.13

## Struktur

```
data/sintetis/   dataset sintetis hasil skrip (jangan diubah manual)
notebook/        B1..B5 (P1-P4), P5_tepi, P6_morfologi
src/             buat_dataset_sintetis.py, utils_cv.py, praproses.py, utils_tepi.py, bercak.py
hasil/           gambar, tabel .csv, param_praproses.json, param_bercak.json
laporan/         laporan PDF dan slide PPTX  
```

## Cara Menjalankan

1. Pasang pustaka (dari folder utama repository):
   ```
   pip install -r requirements.txt
   ```
2. Bangkitkan dataset sintetis (SEED = 1016):
   ```
   python src/buat_dataset_sintetis.py
   ```
   Hasilnya 60 citra di `data/sintetis/`.
3. Buka notebook di folder `notebook/` dan jalankan berurutan B1 sampai B5
   (Restart & Run All). Semua hasil tersimpan di `hasil/`.

## Rangkaian Praproses (src/praproses.py)

Urutan: ubah ukuran -> koreksi gamma -> CLAHE kanal V -> redam derau -> tajamkan.
Parameter final (`hasil/param_praproses.json`):

| Langkah | Parameter |
|---|---|
| Ubah ukuran | lebar 640 px, INTER_AREA |
| Koreksi gamma | 1.0 (tidak aktif) |
| CLAHE kanal V | clip 2.0, tile 8x8 |
| Redam derau | median 3x3 |
| Tajamkan | tajam_k 0 (tidak aktif) |

Pemakaian:
```python
from praproses import praproses
hasil = praproses(img_bgr)          # parameter bawaan
hasil = praproses(img_bgr, {"clahe_clip": 1.0})   # ubah sebagian parameter
```

## Ringkasan Hasil

- Kanal terbaik untuk memisahkan bercak dari daun: **R** (KB tertinggi di semua kondisi cahaya).
- Kontras Bercak (KB) kanal R sebelum -> sesudah praproses, 40 citra berbercak:

| Kondisi | KB sebelum | KB sesudah | Perubahan |
|---|---|---|---|
| normal | 8.84 | 10.15 | +14.88% |
| gelap | 9.52 | 15.89 | +66.88% |
| terang | 6.53 | 5.83 | -10.78% |
| kontras_rendah | 3.97 | 4.98 | +25.34% |
| bayangan | 4.09 | 7.50 | +83.22% |

- Uji bercak palsu pada 20 citra sehat: keragaman intensitas daun sehat turun pada empat kondisi
  dan hanya naik pada kondisi terang (+7,61%), sehingga kondisi terang paling berisiko memunculkan bercak palsu.
- Rencana perbaikan: gamma otomatis berdasarkan rerata intensitas dan pengujian clip CLAHE yang lebih rendah.

## Catatan

Dataset bersifat sintetis dan tidak dimaksudkan sebagai acuan diagnosis penyakit tanaman.
Sebagian kode dibantu alat AI generatif; rinciannya dicantumkan pada bagian refleksi laporan.

## P5-P6: Deteksi Tepi, Morfologi, dan Analisis Bercak (tag v0.2-tepi, v0.3-morfologi)

Notebook: `notebook/P5_tepi.ipynb` (Bagian 1-2) dan `notebook/P6_morfologi.ipynb` (Bagian 3-5).
Praproses memakai `src/praproses.py` milik sendiri dengan `hasil/param_praproses.json`.

### Ringkasan hasil

| Temuan | Angka |
|---|---|
| Operator tepi terbaik | Canny kanal R: F1 0,981 (mentah), 0,964 (praproses) |
| Ambang Canny otomatis | Persentil q = 99 magnitudo gradien, kanal R: F1 0,980-0,987 di 5 kondisi (ambang median: 0,308-0,946) |
| Batas daun | Gradien morfologi mask daun F1 0,97-0,98 (normal, gelap), tetapi 0,29 pada kontras rendah |
| Penyaringan bercak | luas + kebulatan + rasio: galat jumlah daun sehat 2,40 -> 0,55 |
| Modul bercak.py | akurasi kelas 95%, galat persen 0,689, korelasi 0,925; 0 daun sehat dinilai berbercak |

Keputusan: deteksi tepi dipakai untuk tampilan batas bercak dan fitur bentuk, bukan untuk mengukur luas.

### Memakai analisis_daun

```python
import json
from praproses import praproses
from bercak import analisis_daun
PB = json.load(open("../hasil/param_bercak.json"))
h = analisis_daun(praproses(img_bgr), PB)
print(h["kelas"], h["persen_bercak"], h["jumlah_bercak"])   # juga: mask_daun, mask_bercak, bercak (ukuran tiap bercak)
```

Parameter final (`hasil/param_bercak.json`): kanal R, k = 4, SE elips 5 (opening dan closing), luas_min 40 px,
bulat_min 0,5, rasio_maks 1,8, batas kelas 0,1% (ringan) dan 1,2% (berat), 0,4375 mm/piksel.
