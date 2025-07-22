import sqlite3
from model import LaporanKriminal
from konfigurasi import DB_PATH
import database

class ManajerLaporan:
    def tambah_laporan(self, laporan: LaporanKriminal):
        """Menambahkan laporan kriminal ke dalam database."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO laporan (
                    tanggal, kategori, deskripsi, latitude, longitude, status, nama, foto_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                laporan.tanggal,
                laporan.kategori,
                laporan.deskripsi,
                laporan.latitude,
                laporan.longitude,
                laporan.status,
                laporan.nama,
                laporan.foto_path
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ Gagal menambahkan laporan: {e}")
        finally:
            if conn:
                conn.close()

    def ambil_data_laporan(self):
        """Mengambil seluruh data laporan dalam bentuk DataFrame."""
        return database.get_dataframe()

    def hapus_laporan(self, id_laporan: int):
        """Menghapus laporan berdasarkan ID."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM laporan WHERE id = ?", (id_laporan,))
            conn.commit()
        except Exception as e:
            print(f"❌ Gagal menghapus laporan: {e}")
        finally:
            if conn:
                conn.close()
