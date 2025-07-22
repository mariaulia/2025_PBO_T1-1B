from datetime import date

class LaporanKriminal:
    def __init__(self, tanggal: date, kategori: str, deskripsi: str,
                 latitude: float, longitude: float, status: str,
                 nama: str, foto_path: str = None):
        self.tanggal = tanggal
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.nama = nama
        self.foto_path = foto_path

    def to_dict(self) -> dict:
        return {
            "tanggal": self.tanggal.strftime("%Y-%m-%d"),
            "kategori": self.kategori,
            "deskripsi": self.deskripsi,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
            "nama": self.nama,
            "foto_path": self.foto_path
        }
