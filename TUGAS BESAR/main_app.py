import streamlit as st
import os
import datetime
import pandas as pd
import folium
import base64
from streamlit_folium import st_folium

from model import LaporanKriminal
from manajer_laporan import ManajerLaporan
from konfigurasi import KATEGORI_KRIMINAL, STATUS_PELAKU

# Fungsi konversi gambar ke base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Untuk rerun
try:
    from streamlit.runtime.scriptrunner import rerun
except ImportError:
    rerun = st.rerun

# Konfigurasi Halaman
st.set_page_config(page_title="Laporan Kriminal Harian", layout="wide", page_icon="🕵️‍♂️")

# Ambil background image base64
image_path = "foto_tersangka/polres.jpeg"
bg_image_base64 = get_base64_of_bin_file(image_path)

# CSS Tampilan dengan background dari gambar base64
st.markdown(f"""
    <style>
        /* Background full-page sebagai layer bawah */
        .stApp {{
            background: none;
        }}

        body::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/jpeg;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            opacity: 0.35;
            z-index: -1;
        }}

        /* Container utama agar tetap bisa dibaca */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.75);
            padding: 2rem;
            border-radius: 12px;
            color: white;
        }}

        /* Warna tulisan semua elemen */
        h1, h2, h3, p, label, span, div, .stMarkdown, .stText, .stTextInput, .stSelectbox {{
            color: white !important;
        }}

        .custom-header {{
            background-color: rgba(54, 35, 18, 0.9); 
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
        }}

        div[data-testid="stForm"] {{
            background-color: rgba(126, 72, 28, 0.85);
            padding: 20px;
            border-radius: 10px;
        }}

        .stTabs [data-baseweb="tab"] {{
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)


# Header Aplikasi
st.markdown('<div class="custom-header">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("logo_kepolisian.png", width=100)
with col_title:
    st.markdown("## 🕵️‍♀️ RESERSE KRIMINAL POLRESTABES SEMARANG")
    st.caption("Sistem Laporan Kriminal Harian unit Jatanras")
st.markdown('</div>', unsafe_allow_html=True)

ml = ManajerLaporan()
tab_input, tab_data, tab_peta, tab_statistik = st.tabs(["📝 Input Laporan", "📋 Data Laporan", "🌍 Peta Lokasi", "📈 Statistik"])

# Tab Input
with tab_input:
    st.subheader("📌 Tambah Laporan Kriminal")
    with st.form("form_laporan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal Kejadian", datetime.date.today())
            kategori = st.selectbox("Kategori Kriminal", KATEGORI_KRIMINAL)
            status = st.selectbox("Status Pelaku", STATUS_PELAKU)
            nama = st.text_input("Nama Tersangka")
        with col2:
            latitude = st.number_input("Latitude", format="%.6f")
            longitude = st.number_input("Longitude", format="%.6f")
        deskripsi = st.text_area("Deskripsi Kejadian")
        foto = st.file_uploader("📸 Upload Foto Tersangka", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("📏 Simpan Laporan")

        if submitted:
            foto_path = None
            if foto:
                folder = "foto_tersangka"
                os.makedirs(folder, exist_ok=True)
                foto_path = os.path.join(folder, foto.name)
                with open(foto_path, "wb") as f:
                    f.write(foto.read())
            laporan = LaporanKriminal(tanggal, kategori, deskripsi, latitude, longitude, status, nama, foto_path)
            ml.tambah_laporan(laporan)
            st.success("✅ Laporan berhasil disimpan!")

# Tab Data
with tab_data:
    st.subheader("📊 Tabel Laporan Kriminal")
    df = ml.ambil_data_laporan()
    if df.empty:
        st.warning("⚠️ Belum ada data.")
    else:
        nama_cari = st.text_input("🔍 Cari Nama Tersangka")
        if nama_cari:
            df = df[df["nama"].str.contains(nama_cari, case=False)]

        st.dataframe(df, use_container_width=True)

        id_hapus = st.selectbox("🗑️ Hapus laporan berdasarkan ID:", df["id"])
        if st.button("Hapus Laporan"):
            ml.hapus_laporan(id_hapus)
            st.success(f"✅ Laporan ID {id_hapus} telah dihapus.")
            rerun()

        st.markdown("### ✏️ Edit Laporan")
        id_edit = st.selectbox("Pilih ID laporan yang ingin diedit:", df["id"], key="edit")
        data_lama = df[df["id"] == id_edit].iloc[0]

        with st.form("form_edit"):
            tanggal_baru = st.date_input("Tanggal Kejadian", value=pd.to_datetime(data_lama["tanggal"]))
            kategori_baru = st.selectbox("Kategori Kriminal", KATEGORI_KRIMINAL, index=KATEGORI_KRIMINAL.index(data_lama["kategori"]))
            status_baru = st.selectbox("Status Pelaku", STATUS_PELAKU, index=STATUS_PELAKU.index(data_lama["status"]))
            nama_baru = st.text_input("Nama Tersangka", value=data_lama["nama"])
            deskripsi_baru = st.text_area("Deskripsi Kejadian", value=data_lama["deskripsi"])
            if st.form_submit_button("💾 Simpan Perubahan"):
                st.success("✅ Perubahan berhasil disimpan. (Note: Fitur update ke DB perlu ditambahkan di ManajerLaporan)")

# Tab Peta
with tab_peta:
    st.subheader("🗺️ Visualisasi Lokasi Kejadian di Peta")
    if df.empty:
        st.info("Belum ada data lokasi.")
    else:
        lokasi_tengah = [df["latitude"].mean(), df["longitude"].mean()]
        peta = folium.Map(location=lokasi_tengah, zoom_start=12)
        for _, row in df.iterrows():
            foto_html = ""
            if row.get("foto_path") and os.path.exists(row["foto_path"]):
                with open(row["foto_path"], "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode()
                    ext = os.path.splitext(row["foto_path"])[1].replace(".", "")
                    foto_html = f"""
                        <div style='flex: 1;'>
                            <img src='data:image/{ext};base64,{encoded}' width='200'>
                        </div>
                    """
            info_html = f"""
                <div style='flex: 2; padding-left: 10px;'>
                    <b>{row['tanggal']}</b> - {row['kategori']} ({row['status']})<br>
                    <b>Nama:</b> {row['nama']}<br>
                    {row['deskripsi']}
                </div>
            """
            popup_html = f"""
                <div style='display: flex; gap: 10px; max-width: 500px; min-width: 500px;'>
                    {foto_html}{info_html}
                </div>
            """
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=popup_html,
                tooltip=row["kategori"],
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(peta)
        st_folium(peta, width=True, height=500)

# Tab Statistik
with tab_statistik:
    st.subheader("📈 Statistik Laporan Kriminal")
    if df.empty:
        st.info("Belum ada data statistik untuk ditampilkan.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Jumlah Laporan per Kategori")
            kategori_count = df["kategori"].value_counts()
            st.bar_chart(kategori_count)

        with col2:
            st.markdown("#### Jumlah Laporan per Status")
            status_count = df["status"].value_counts()
            st.bar_chart(status_count)

        st.markdown("#### Tren Laporan per Tanggal")
        tren = df.groupby("tanggal").size()
        st.line_chart(tren)
