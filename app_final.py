import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="AMS - JUARA PLAFON", layout="wide")

FILE_DB = "D:/Downloads/database_pvc.csv"

def muat_data():
    kolom = ["Batch ID (Code)", "Tanggal", "Nama Barang", "Ukuran", "Tipe Transaksi", "Stok", "Harga Satuan (Rp)", "Keterangan", "Oleh Pengguna"]
    if os.path.exists(FILE_DB):
        try:
            return pd.read_csv(FILE_DB)
        except:
            return pd.DataFrame(columns=kolom)
    return pd.DataFrame(columns=kolom)

def simpan_data(df):
    df.to_csv(FILE_DB, index=False)

df_stok = muat_data()

DAFTAR_AKUN = {"pemilik": "pvc123", "admin": "adminpvc", "staf": "stafpvc"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    # 1. HALAMAN LOGIN: TENGAH & PT LEBIH BESAR
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #ffffff; font-size: 42px; margin-bottom: 5px; font-weight: bold;'>PT. CAHAYA ANDALAN PERTAMA</h1>
            <h3 style='color: #38bdf8; font-size: 24px; margin-top: 0;'>JUARA PLAFON</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>Asset Management System Login</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    col_login, _ = st.columns(2)
    with col_login:
        input_user = st.text_input("Username").strip().lower()
        input_pass = st.text_input("Password", type="password")
        if st.button("Masuk Aplikasi", use_container_width=True):
            if input_user in DAFTAR_AKUN and DAFTAR_AKUN[input_user] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.rerun()
            else:
                st.error("Username atau Password salah!")
else:
    # 2. HALAMAN DASHBOARD: BANNER TENGAH & PT LEBIH BESAR
    st.markdown("""
        <div style='background-color:#1e293b; padding:25px; border-radius:10px; margin-bottom: 25px; text-align: center; border-left: 5px solid #38bdf8;'>
            <h1 style='color:#ffffff; font-size: 40px; margin:0; font-weight: 900; letter-spacing: 1px;'>PT. CAHAYA ANDALAN PERTAMA</h1>
            <h3 style='color:#38bdf8; font-size: 22px; margin:8px 0 0 0; font-weight: normal;'>AMS - JUARA PLAFON</h3>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🏢 MENU NAVIGASI")
    st.sidebar.write(f"👤 Pengguna: **{st.session_state.username.upper()}**")
    if st.sidebar.button("🚪 Keluar / Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.sidebar.markdown("---")
    menu_pilihan = st.sidebar.radio("Pilih Menu:", ["📊 Dashboard & Stok", "➕ Tambah Aset Baru", "🔄 Scan / Mutasi Stok"])

    if menu_pilihan == "📊 Dashboard & Stok":
        st.subheader("📊 Live Summary & Analisis Inventori")
        if not df_stok.empty and "Tipe Transaksi" in df_stok.columns:
            total_jenis = len(df_stok["Nama Barang"].unique())
            df_masuk = df_stok[df_stok["Tipe Transaksi"] == "BARANG MASUK"]
            df_keluar = df_stok[df_stok["Tipe Transaksi"] == "BARANG KELUAR"]
            total_stok = df_masuk["Stok"].sum() - df_keluar["Stok"].sum()
            total_keluar = df_keluar["Stok"].sum()
            total_transaksi = len(df_stok)
        else:
            total_jenis, total_stok, total_transaksi, total_keluar = 0, 0, 0, 0

        st.markdown("""
            <style>
            .box-blue { background-color: #0369a1; padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px; }
            .box-green { background-color: #15803d; padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px; }
            .box-yellow { background-color: #b45309; padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px; }
            .box-dark { background-color: #334155; padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px; }
            .box-title { font-size: 13px; font-weight: bold; opacity: 0.9; margin-bottom: 5px; }
            .box-number { font-size: 30px; font-weight: bold; }
            </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"<div class='box-blue'><div class='box-title'>TOTAL KESELURUHAN ASET</div><div class='box-number'>{total_jenis} Jenis</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='box-green'><div class='box-title'>READY STOCK AKTIF</div><div class='box-number'>{total_stok} Pcs</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='box-yellow'><div class='box-title'>BARANG KELUAR / TERJUAL</div><div class='box-number'>{total_keluar} Pcs</div></div>", unsafe_allow_html=True)
        with col4: st.markdown(f"<div class='box-dark'><div class='box-title'>LOG RIWAYAT TRANSAKSI</div><div class='box-number'>{total_transaksi} Batch</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.write("### 🕒 Log & Riwayat Mutasi Aset")
        col_cari, col_ref = st.columns(2)
        with col_cari: cari = st.text_input("🔍 Cari data barang, transaksi...", placeholder="Ketik kata kunci...")
        with col_ref: st.write(""); st.button("🔄 Refresh Data", use_container_width=True)

        df_tampil = df_stok.copy()
        if cari and not df_tampil.empty:
            df_tampil = df_tampil[df_tampil.astype(str).apply(lambda x: x.str.contains(cari, case=False)).any(axis=1)]
        if not df_tampil.empty:
            st.dataframe(df_tampil.iloc[::-1], use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data barang atau mutasi.")

    elif menu_pilihan == "➕ Tambah Aset Baru":
        st.subheader("📦 Input Data Master Aset Baru")
        with st.form("Form Tambah"):
            nama = st.text_input("Nama Barang / Tipe Plafon PVC")
            ukuran = st.selectbox("Ukuran / Panjang", ["2.9 Meter", "3 Meter", "4 Meter", "Custom"])
            stok = st.number_input("Jumlah Stok Masuk (Pcs)", min_value=1, step=1)
            harga = st.number_input("Harga Satuan (Rp)", min_value=0, step=1000)
            ket = st.text_input("Keterangan Tambahan", "Masuk Gudang Pusat Juara Plafon")
            if st.form_submit_button("Simpan ke Master Aset") and nama:
                dt_str = datetime.now().strftime("%d/%m/%Y %H:%M")
                b_id = f"TRX-IN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                b_data = pd.DataFrame([{"Batch ID (Code)": b_id, "Tanggal": dt_str, "Nama Barang": nama, "Ukuran": ukuran, "Tipe Transaksi": "BARANG MASUK", "Stok": stok, "Harga Satuan (Rp)": harga, "Keterangan": ket, "Oleh Pengguna": st.session_state.username}])
                df_stok = pd.concat([df_stok, b_data], ignore_index=True)
                simpan_data(df_stok)
                st.success(f"Berhasil Mendaftarkan {nama}!")
                st.balloons()

    elif menu_pilihan == "🔄 Scan / Mutasi Stok":
        st.subheader("🔄 Form Pengurangan / Mutasi Stok Keluar (Penjualan)")
        if df_stok.empty:
            st.warning("Belum ada aset masuk terdaftar.")
        else:
            with st.form("Form Mutasi"):
                brg_pilih = st.selectbox("Pilih Barang yang Keluar", df_stok["Nama Barang"].unique())
                jml_keluar = st.number_input("Jumlah Unit Keluar (Pcs)", min_value=1, step=1)
                tujuan = st.text_input("Tujuan / Nama Pembeli", "Pelanggan Toko")
                if st.form_submit_button("Proses Mutasi"):
                    idx = df_stok[df_stok["Nama Barang"] == brg_pilih].index[-1]
                    h_asli = df_stok.loc[idx, "Harga Satuan (Rp)"]
                    u_asli = df_stok.loc[idx, "Ukuran"]
                    dt_str = datetime.now().strftime("%d/%m/%Y %H:%M")
                    b_id = f"TRX-OUT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                    m_data = pd.DataFrame([{"Batch ID (Code)": b_id, "Tanggal": dt_str, "Nama Barang": brg_pilih, "Ukuran": u_asli, "Tipe Transaksi": "BARANG KELUAR", "Stok": jml_keluar, "Harga Satuan (Rp)": h_asli, "Keterangan": f"Mutasi Keluar ke {tujuan}", "Oleh Pengguna": st.session_state.username}])
                    df_stok = pd.concat([df_stok, m_data], ignore_index=True)
                    simpan_data(df_stok)
                    st.success("Mutasi Stok Keluar Sukses Diproses!")
                    st.balloons()
