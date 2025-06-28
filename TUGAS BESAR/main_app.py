# main_app.py
import streamlit as st
import pandas as pd

try:
    from model import Mahasiswa, MataKuliah, Nilai
    from management_nilai import ManajemenNilaiMahasiswa
    from konfigurasi import MATA_KULIAH
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan file .py lain ada.")
    st.stop()

st.set_page_config(page_title="Manajemen Nilai Mahasiswa", layout="wide")

@st.cache_resource
def get_manager():
    return ManajemenNilaiMahasiswa()

manager = get_manager()

# ---------------------- Halaman Input Nilai ----------------------
def halaman_input_nilai(manager: ManajemenNilaiMahasiswa):
    st.header("Input Nilai Mahasiswa")
    daftar_mahasiswa = manager.get_semua_mahasiswa()
    daftar_mk = manager.get_semua_mk()

    if not daftar_mahasiswa or not daftar_mk:
        st.warning("Pastikan data mahasiswa dan mata kuliah sudah diinput.")
        return

    nim_list = [f"{mhs.nim} - {mhs.nama}" for mhs in daftar_mahasiswa]
    mk_list = [f"{mk.kode_mk} - {mk.nama_mk}" for mk in daftar_mk]

    with st.form("form_nilai", clear_on_submit=True):
        nim_pilihan = st.selectbox("Pilih Mahasiswa:", nim_list)
        mk_pilihan = st.selectbox("Pilih Mata Kuliah:", mk_list)
        nilai = st.number_input("Nilai Angka:", min_value=0.0, max_value=100.0)
        submitted = st.form_submit_button("Simpan Nilai")
        if submitted:
            nim = nim_pilihan.split(" - ")[0]
            kode_mk = mk_pilihan.split(" - ")[0]
            nilai_obj = Nilai(nim=nim, kode_mk=kode_mk, nilai_angka=nilai)
            if manager.tambah_nilai(nilai_obj):
                st.success("Nilai berhasil disimpan.")
            else:
                st.error("Gagal menyimpan nilai.")

# ---------------------- Halaman Riwayat ----------------------
def halaman_riwayat_nilai(manager: ManajemenNilaiMahasiswa):
    st.header("Riwayat Nilai Mahasiswa")
    daftar_mahasiswa = manager.get_semua_mahasiswa()
    if not daftar_mahasiswa:
        st.warning("Belum ada data mahasiswa.")
        return

    nim_pilihan = st.selectbox("Pilih Mahasiswa:", [f"{m.nim} - {m.nama}" for m in daftar_mahasiswa])
    nim = nim_pilihan.split(" - ")[0]
    df = manager.get_dataframe_nilai(nim)
    if df.empty:
        st.info("Belum ada nilai untuk mahasiswa ini.")
    else:
        st.dataframe(df, use_container_width=True)

# ---------------------- Halaman IPK ----------------------
def halaman_ipk(manager: ManajemenNilaiMahasiswa):
    st.header("Perhitungan IPK Mahasiswa")
    daftar_mahasiswa = manager.get_semua_mahasiswa()
    if not daftar_mahasiswa:
        st.warning("Belum ada data mahasiswa.")
        return

    nim_pilihan = st.selectbox("Pilih Mahasiswa:", [f"{m.nim} - {m.nama}" for m in daftar_mahasiswa])
    nim = nim_pilihan.split(" - ")[0]
    ipk = manager.hitung_ipk(nim)
    st.metric("IPK Saat Ini", value=ipk)

# ---------------------- Menu Utama ----------------------
def main():
    st.sidebar.title("📚 Menu Aplikasi Nilai")
    menu = st.sidebar.radio("Navigasi:", ["Input Nilai", "Riwayat Nilai", "Hitung IPK"])

    if menu == "Input Nilai":
        halaman_input_nilai(manager)
    elif menu == "Riwayat Nilai":
        halaman_riwayat_nilai(manager)
    elif menu == "Hitung IPK":
        halaman_ipk(manager)

if __name__ == "__main__":
    main()
