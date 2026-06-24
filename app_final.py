import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="AMS - JUARA PLAFON", layout="wide")

# Menggunakan folder /tmp agar pasti diizinkan menulis file oleh server Streamlit Cloud
FILE_DB = "/tmp/database_pvc.csv"

def muat_data():
    kolom = ["Batch ID (Code)", "Tanggal", "Nama Barang", "Ukuran", "Tipe Transaksi", "Stok", "Harga Satuan (Rp)", "Keterangan", "Oleh Pengguna"]
    if os.path.exists(FILE_DB):
        try:
            return pd.read_csv(FILE_DB)
        except:
            return pd.DataFrame(columns=kolom)
    return pd.DataFrame(columns=kolom)

def simpan_data(df):
    # Pastikan folder penyimpanan tersedia sebelum menyimpan file
    if os.path.dirname(FILE_DB):
        os.makedirs(os.path.dirname(FILE_DB), exist_ok=True)
    df.to_csv(FILE_DB, index=False)

df_stok = muat_data()

DAFTAR_AKUN = {"pemilik": "pvc123", "admin": "adminpvc", "staf": "stafpvc"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
