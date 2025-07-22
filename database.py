import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def insert_laporan(laporan: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO laporan (
            tanggal, kategori, deskripsi, latitude, longitude, status, nama, foto_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        laporan["tanggal"],
        laporan["kategori"],
        laporan["deskripsi"],
        laporan["latitude"],
        laporan["longitude"],
        laporan["status"],
        laporan["nama"],
        laporan.get("foto_path")  # aman meski None
    ))
    conn.commit()
    conn.close()

def get_dataframe():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM laporan", conn)
    conn.close()
    return df
