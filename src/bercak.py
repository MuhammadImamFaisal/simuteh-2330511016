"""bercak.py: analisis bercak SIMUTEH (dipakai ulang mulai P7)."""
import json
import cv2
import numpy as np
from utils_tepi import mask_daun_awal, bercak_awal

PARAM_BERCAK = {
    "kanal": 2,           # kanal terpilih (2 = R)
    "k": 4.0,             # ambang median + k x MAD
    "se_bentuk": "elips", # "elips", "persegi", "silang"
    "se_open": 5,         # ukuran SE opening (0 = tidak dipakai)
    "se_close": 5,        # ukuran SE closing (0 = tidak dipakai)
    "luas_min": 20,       # piksel
    "bulat_min": 0.5,
    "rasio_maks": 1.8,
    "batas_ringan": 0.1,  # persen bercak minimum kelas Ringan
    "batas_berat": 2.0,   # persen bercak minimum kelas Berat
    "mm_per_px": 0.4375,
}
_BENTUK = {"elips": cv2.MORPH_ELLIPSE, "persegi": cv2.MORPH_RECT, "silang": cv2.MORPH_CROSS}


def _se(p, uk):
    return cv2.getStructuringElement(_BENTUK[p["se_bentuk"]], (uk, uk))


def bersihkan(biner, p):
    """Opening membuang titik derau dan potongan tipis; closing menutup celah."""
    hasil = biner.copy()
    # TODO 1: opening = erosi lalu dilasi -> komponen yang lebih kecil/tipis dari SE hilang
    if p["se_open"] > 0:
        hasil = cv2.morphologyEx(hasil, cv2.MORPH_OPEN, _se(p, p["se_open"]))
    # TODO 2: closing = dilasi lalu erosi -> lubang dan celah sempit di dalam bercak tertutup
    if p["se_close"] > 0:
        hasil = cv2.morphologyEx(hasil, cv2.MORPH_CLOSE, _se(p, p["se_close"]))
    return hasil


def ukur_dan_saring(biner, p):
    """Mengembalikan mask bercak tersaring dan daftar ukuran setiap bercak."""
    keluar, daftar = np.zeros_like(biner), []
    # TODO 3: label komponen terhubung, konektivitas 8 (bercak nyata menyambung juga lewat diagonal)
    n, lbl, st, cen = cv2.connectedComponentsWithStats((biner > 0).astype(np.uint8),
                                                       connectivity=8)
    mm2 = p["mm_per_px"] ** 2
    for i in range(1, n):                       # label 0 = latar
        komp = (lbl == i).astype(np.uint8)
        # TODO 4: ukuran tiap komponen
        luas = int(st[i, cv2.CC_STAT_AREA])
        kontur, _ = cv2.findContours(komp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        keliling = cv2.arcLength(kontur[0], True)
        kebulatan = 0.0 if keliling == 0 else 4 * np.pi * luas / keliling ** 2
        w, h = cv2.minAreaRect(kontur[0])[1]
        rasio = max(w, h) / max(min(w, h), 1)
        # TODO 5: simpan hanya komponen yang lolos ketiga syarat
        if luas >= p["luas_min"] and kebulatan >= p["bulat_min"] and rasio <= p["rasio_maks"]:
            keluar[lbl == i] = 255
            daftar.append({"label": i, "luas_px": luas, "luas_mm2": round(luas * mm2, 2),
                           "keliling_px": round(keliling, 1), "kebulatan": round(kebulatan, 2),
                           "rasio_aspek": round(rasio, 2),
                           "cx": int(cen[i][0]), "cy": int(cen[i][1])})
    return keluar, daftar


def kelas_mutu(persen, p):
    """Kelas dari persen bercak: < batas_ringan Sehat, < batas_berat Ringan, sisanya Berat."""
    if persen < p["batas_ringan"]:
        return "Sehat"
    if persen < p["batas_berat"]:
        return "Bercak Ringan"
    return "Bercak Berat"


def analisis_daun(img_praproses, p=None):
    """Masukan: citra BGR hasil praproses. Keluaran: kamus hasil analisis."""
    p = {**PARAM_BERCAK, **(p or {})}
    m_daun = mask_daun_awal(img_praproses)
    biner = bercak_awal(img_praproses, m_daun, kanal=p["kanal"], k=p["k"])
    m_bercak, daftar = ukur_dan_saring(bersihkan(biner, p), p)
    # TODO 6: persen bercak = luas bercak / luas daun x 100
    luas_daun = int((m_daun > 0).sum())
    luas_bercak = int(((m_bercak > 0) & (m_daun > 0)).sum())
    persen = 0.0 if luas_daun == 0 else 100.0 * luas_bercak / luas_daun
    # TODO 7: kelas dengan batas_ringan dan batas_berat
    kelas = kelas_mutu(persen, p)
    return {"mask_daun": m_daun, "mask_bercak": m_bercak, "jumlah_bercak": len(daftar),
            "persen_bercak": round(float(persen), 3), "kelas": kelas, "bercak": daftar}


def simpan_param(p, path="../hasil/param_bercak.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BERCAK, **p}, f, indent=2)
