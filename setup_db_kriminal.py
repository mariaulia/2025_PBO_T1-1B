import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    print(f"🔧 Menyiapkan database di: {DB_PATH}")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS laporan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal DATE NOT NULL,
                kategori TEXT NOT NULL,
                deskripsi TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                status TEXT NOT NULL,
                nama TEXT NOT NULL,
                foto_path TEXT
            );
        """)
        conn.commit()
        print("✅ Tabel 'laporan' berhasil dibuat atau sudah tersedia.")
        return True
    except Exception as e:
        print(f"❌ Error saat membuat tabel: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
