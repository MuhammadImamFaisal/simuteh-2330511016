# SIMUTEH - Praproses Citra Daun Teh (Evaluasi P1-P4)

Sistem Pemeriksaan Mutu Daun Teh berbasis citra untuk kelompok tani teh rakyat di Kabupaten Sukabumi.
Repository ini memuat tahap **akuisisi** dan **praproses** (Pertemuan 1-4) mata kuliah Computer Vision.

- **Nama / NIM:** Muhammad Imam Faisal / 2330511016
- **SEED dataset:** `1016` (4 digit terakhir NIM)
- **Python:** 3.13

## Struktur

```
data/sintetis/   dataset sintetis hasil skrip (jangan diubah manual)
notebook/        B1_lingkungan, B2_citra_warna, B3_histogram, B4_penapisan, B5_praproses
src/             buat_dataset_sintetis.py, utils_cv.py, praproses.py
hasil/           gambar, tabel .csv, param_praproses.json
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

- Uji bercak palsu pada 20 citra sehat: keragaman intensitas daun sehat naik pada kondisi
  terang dan kontras_rendah, sehingga kedua kondisi ini paling berisiko memunculkan bercak palsu.
- Rencana perbaikan: gamma otomatis berdasarkan rerata intensitas dan pengujian clip CLAHE yang lebih rendah.

## Catatan

Dataset bersifat sintetis dan tidak dimaksudkan sebagai acuan diagnosis penyakit tanaman.
Sebagian kode dibantu alat AI generatif; rinciannya dicantumkan pada bagian refleksi laporan.