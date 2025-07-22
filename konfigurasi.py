import os

# Lokasi file database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = "laporan_kriminal.db"
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Daftar kategori kriminal
KATEGORI_KRIMINAL = [
    "Pencurian",
    "Pembunuhan",
    "Narkoba",
    "Penipuan",
    "Kekerasan",
    "Lainnya"
]

# Kategori default saat form pertama dibuka
KATEGORI_DEFAULT = "Lainnya"

# Daftar status pelaku (digunakan di main_app.py)
STATUS_PELAKU = [
    "Tersangka",
    "Terdakwa",
    "Persidangan",
    "Narapidana"
]
