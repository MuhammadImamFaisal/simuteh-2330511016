# SIMUTEH - Praproses Citra Daun Teh

## Deskripsi
Proyek ini merupakan rangkaian praproses citra daun teh untuk membantu
meningkatkan kontras bercak dan mengurangi noise sebelum tahap analisis
Computer Vision.

## Urutan Pipeline
1. Resize citra dengan lebar 640 piksel.
2. Gamma correction dengan gamma 1.0.
3. CLAHE pada kanal Value (HSV), clip limit 2.0 dan tile 8.
4. Denoising menggunakan median filter dengan kernel 3.
5. Sharpening dengan tajam_k 0.0 (dinonaktifkan).

## Parameter
Parameter praproses disimpan di:
`hasil/param_praproses.json`

## Cara Menjalankan
1. Buka notebook Google Colab proyek SIMUTEH.
2. Jalankan cell inisialisasi dan impor modul.
3. Pastikan dataset tersedia di folder `data/sintetis`.
4. Jalankan seluruh cell notebook dari awal sampai akhir.
5. Hasil evaluasi tersimpan di folder `hasil`.

## Seed
Nilai SEED: 1016

## Ringkasan Hasil
Evaluasi terhadap 40 citra dengan bercak menunjukkan:
- Bayangan: KB meningkat 83.22%.
- Gelap: KB meningkat 66.88%.
- Kontras rendah: KB meningkat 25.34%.
- Normal: KB meningkat 14.88%.
- Terang: KB menurun 10.78%.

Pengujian terhadap 20 citra sehat menunjukkan standar deviasi
area daun menurun pada kondisi bayangan, gelap, kontras rendah,
dan normal. Pada kondisi terang, standar deviasi meningkat.

## File Hasil
- `hasil/param_praproses.json`
- `hasil/b5_evaluasi_praproses.csv`
- `hasil/b5_tabel12.csv`
- `hasil/b5_uji_bercak_palsu.csv`
- `hasil/b5_tabel13_justifikasi.csv`
- `hasil/b5_diagram_pipeline.png`
