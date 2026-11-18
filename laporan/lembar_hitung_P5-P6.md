# Lembar Hitung Manual P5–P6 SIMUTEH
Muhammad Imam Faisal — NIM 2330511016 — Kelas 7A

Semua kernel diterapkan sebagai **korelasi** (tanpa dibalik), sama seperti `cv2.filter2D`. Angka akhir sudah dicek ulang dengan kode (lihat sel "verifikasi lembar hitung" di notebook).

---

## Lembar Hitung 1.1 — Gradien, Sobel, Prewitt, Laplacian

Potongan kanal R:

```
A = [[52, 55, 180],
     [50, 58, 185],
     [54, 60, 190]]
```

### a) Sobel

**Gx** (Kx = [[-1,0,1],[-2,0,2],[-1,0,1]]), yaitu kolom kanan dikurangi kolom kiri dengan bobot 1-2-1:

- baris 1: (180 − 52) × 1 = 128
- baris 2: (185 − 50) × 2 = 270
- baris 3: (190 − 54) × 1 = 136
- **Gx = 128 + 270 + 136 = 534**

**Gy** (Ky = [[-1,-2,-1],[0,0,0],[1,2,1]]), yaitu baris bawah dikurangi baris atas dengan bobot 1-2-1:

- kolom 1: (54 − 52) × 1 = 2
- kolom 2: (60 − 55) × 2 = 10
- kolom 3: (190 − 180) × 1 = 10
- **Gy = 2 + 10 + 10 = 22**

- Magnitudo |G| = √(534² + 22²) = √(285 156 + 484) = √285 640 = **534,45**
- Pendekatan |Gx| + |Gy| = 534 + 22 = **556** (lebih besar ±4% dari nilai eksak)
- Arah gradien θ = atan2(22, 534) = **2,36°**

### b) Prewitt

**Gx** (bobot 1-1-1): (180−52) + (185−50) + (190−54) = 128 + 135 + 136 = **399**
**Gy**: (54−52) + (60−55) + (190−180) = 2 + 5 + 10 = **17**

- |G| = √(399² + 17²) = √(159 201 + 289) = √159 490 = **399,36**
- |Gx| + |Gy| = **416**
- θ = atan2(17, 399) = **2,44°**

Perbandingan: |G|Sobel / |G|Prewitt = 534,45 / 399,36 ≈ **1,34**. Sobel memberi bobot 2 pada baris tengah, jadi jumlah bobot per sisi kernel 4, sedangkan Prewitt hanya 3. Untuk tepi yang rata secara vertikal, rasionya mendekati 4/3.

### c) Laplacian

Kernel [[0,1,0],[1,−4,1],[0,1,0]]:
L = 55 + 50 + 185 + 60 − 4 × 58 = 350 − 232 = **+118**

Tanda **positif** berarti piksel tengah (58) lebih gelap daripada rerata empat tetangganya (87,5). Artinya piksel tengah berada di **sisi gelap** tepi. Perlintasan nol (lokasi tepi) ada di antara kolom tengah dan kolom kanan. Kalau hasilnya negatif, piksel berada di sisi terang.

### d) Arah tepi

Arah gradien ≈ 2,4°, hampir horizontal dan menunjuk ke kanan (ke arah bercak yang terang). Tepi selalu **tegak lurus** gradien, jadi tepinya ≈ 92,4° (atau −87,6°), yaitu **tepi vertikal** yang memanjang dari atas ke bawah, memisahkan daun gelap di kiri dari bercak terang di kanan.

---

## Lembar Hitung 2.1 — NMS dan Hysteresis

### a) Non-maximum suppression

Piksel tengah dibandingkan dengan dua tetangga **searah gradien**:
- arah 0° → bandingkan kiri dan kanan (baris tengah)
- arah 90° → bandingkan atas dan bawah (kolom tengah)

| Matriks | Arah | Tetangga | Tengah | Keputusan |
|---|---|---|---|---|
| M1 | 0° | kiri 90, kanan 95 | 100 | 100 ≥ 90 dan ≥ 95 → **dipertahankan** |
| M1 | 90° | atas 40, bawah 30 | 100 | 100 ≥ 40 dan ≥ 30 → **dipertahankan** |
| M2 | 0° | kiri 85, kanan 70 | 80 | 80 < 85 → **ditekan (0)** |
| M2 | 90° | atas 60, bawah 45 | 80 | 80 ≥ 60 dan ≥ 45 → **dipertahankan** |

### b) Hysteresis (bawah = 50, atas = 100)

| Indeks | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Magnitudo | 20 | 60 | 120 | 80 | 40 | 90 | 30 |
| Kategori | buang | lemah | **kuat** | lemah | buang | lemah | buang |
| Tepi akhir | 0 | 1 | 1 | 1 | 0 | 0 | 0 |

- Kuat (≥ 100): indeks 2 (120).
- Lemah (50 ≤ M < 100): indeks 1 (60), 3 (80), 5 (90).
- Lemah yang **tersambung** ke piksel kuat ikut jadi tepi: 60 dan 80 bertetangga langsung dengan 120.
- 90 (indeks 5) **dibuang** walaupun > 50, karena terpisah dari piksel kuat oleh 40 (< 50). Rantai terputus, jadi 90 dianggap derau.
- **Tepi akhir = [0, 1, 1, 1, 0, 0, 0]**

---

## Lembar Hitung 3.1 — Morfologi (SE persegi 3×3, luar citra = 0)

```
B = baris 0: 0 0 0 0 0 0 0 0 0
    baris 1: 0 1 1 1 0 0 0 0 0
    baris 2: 0 1 0 1 0 0 0 1 0     ← (2,7) titik derau; (2,2) lubang bercak
    baris 3: 0 1 1 1 0 0 0 0 0
    baris 4: 0 0 0 0 1 0 0 0 0     ← (4,4) piksel diagonal
    baris 5: 0 0 0 0 0 0 0 0 0
    baris 6: 0 0 0 0 0 0 0 0 0
    baris 7: 0 1 1 1 1 1 1 0 0     ← garis seperti tulang daun
    baris 8: 0 0 0 0 0 0 0 0 0
```

### a) Komponen terhubung

- **Konektivitas 4: 4 komponen.** Cincin bercak (8 piksel), titik derau (2,7), piksel diagonal (4,4), dan garis baris 7. Piksel (4,4) hanya bersentuhan sudut dengan (3,3), jadi terpisah.
- **Konektivitas 8: 3 komponen.** (4,4) menyatu dengan cincin bercak lewat tetangga diagonal (3,3); titik derau dan garis tetap terpisah.

### b) Erosi dan opening

Erosi mempertahankan piksel hanya bila **seluruh** 3×3 di sekitarnya bernilai 1. Tidak ada satu pun piksel yang memenuhi syarat itu: cincin bercak berlubang di (2,2), garis hanya setebal 1, dan derau hanya 1 piksel.

```
Erosi(B)   = semua 0 (citra 9×9 kosong)
Opening(B) = Dilasi(Erosi(B)) = semua 0
```

Erosi dan opening **menghapus bercak berlubang** bersama derau dan garis.

### c) Closing (dilasi lalu erosi)

```
Closing(B) = 0 0 0 0 0 0 0 0 0
             0 1 1 1 0 0 0 0 0
             0 1 1 1 0 0 0 1 0     ← lubang (2,2) tertutup; derau (2,7) tetap
             0 1 1 1 0 0 0 0 0
             0 0 0 0 1 0 0 0 0
             0 0 0 0 1 0 0 0 0     ← (5,4) dan (6,4) terisi:
             0 0 0 0 1 0 0 0 0        jembatan piksel diagonal → garis
             0 1 1 1 1 1 1 0 0
             0 0 0 0 0 0 0 0 0
```

- Lubang bercak tertutup, jadi bercak menjadi 3×3 penuh.
- Celah 2 baris antara piksel diagonal (4,4) dan garis (baris 7) **ikut terisi**, sehingga bercak, piksel diagonal, dan garis menjadi **satu komponen**. Hasilnya 2 komponen (konektivitas 8): gabungan bercak-garis dan titik derau.

### d) Closing lalu opening

```
Opening(Closing(B)) = 0 0 0 0 0 0 0 0 0
                      0 1 1 1 0 0 0 0 0
                      0 1 1 1 0 0 0 0 0
                      0 1 1 1 0 0 0 0 0
                      0 0 0 0 0 0 0 0 0
                      ... (baris 4–8 semua 0)
```

Hasilnya hanya **bercak 3×3 penuh** (1 komponen). Derau, jembatan, dan garis tipis hilang karena tidak muat SE 3×3. Urutan **closing dulu lalu opening** menyelamatkan bercak berlubang yang pada butir (b) habis terhapus.

---

## Lembar Hitung 4.1 — Ukuran Komponen (1 px = 0,4375 mm, 1 px² = 0,19140625 mm²)

Keliling = jumlah sisi piksel yang berbatasan dengan latar.

### a) Bercak 3×3 (hasil 3.1 d)

- Luas = 9 px = 9 × 0,19140625 = **1,72 mm²**
- Keliling = 4 sisi × 3 = **12** (sisi piksel)
- Kebulatan = 4π × 9 / 12² = 113,10 / 144 = **0,785**
- Rasio aspek = 3 / 3 = **1,0**

### b) Garis 1×6 (baris 7)

- Luas = 6 px = 6 × 0,19140625 = **1,15 mm²**
- Keliling = 2 × (6 + 1) = **14**
- Kebulatan = 4π × 6 / 14² = 75,40 / 196 = **0,385**
- Rasio aspek = 6 / 1 = **6,0**

### c) Aturan sederhana

Bercak itu kompak dan hampir bulat, sedangkan tulang daun tipis dan memanjang. Aturan yang diusulkan:

> **Komponen dianggap bercak bila kebulatan ≥ 0,5 DAN rasio aspek ≤ 1,8**, ditambah luas ≥ luas minimum untuk membuang titik derau.

Bercak 3×3 (0,785; 1,0) lolos, garis (0,385; 6,0) tertolak oleh kedua syarat.

**Catatan untuk P4.1.** OpenCV menghitung keliling dengan `cv2.arcLength`, yaitu panjang kontur yang melewati **pusat** piksel batas, bukan sisi luarnya. Untuk bercak 3×3, keliling OpenCV = 8 (bukan 12), sehingga kebulatannya 4π×9/64 = **1,77 > 1**. Untuk garis 1×6, keliling = 10 dan kebulatan = 0,75, padahal hitungan manual 0,385. Rasio aspek `minAreaRect` = 5/max(0,1) = 5. Karena itu, pada komponen sangat kecil, syarat **luas minimum** dan **rasio aspek** lebih bisa diandalkan daripada kebulatan.
