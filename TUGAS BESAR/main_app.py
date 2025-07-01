import streamlit as st
import pandas as pd

try:
    from model import Mahasiswa, MataKuliah, Nilai
    from management_nilai import ManajemenNilaiMahasiswa
    from konfigurasi import MATA_KULIAH_PER_SEMESTER
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan file .py lain ada.")
    st.stop()

# Setting konfigurasi Streamlit
st.set_page_config(page_title="Manajemen Nilai Mahasiswa TRK", layout="wide")

# Mengambil Manajer Nilai
@st.cache_resource
def get_manager():
    return ManajemenNilaiMahasiswa()

manager = get_manager()

# Halaman Input Mahasiswa
def halaman_input_mahasiswa(manager: ManajemenNilaiMahasiswa):
    st.header("📥 Input Mahasiswa")
    with st.form("form_mahasiswa", clear_on_submit=True):
        nim = st.text_input("NIM")
        nama = st.text_input("Nama Lengkap")
        semester = st.selectbox("Semester", list(range(1, 9)))
        submitted = st.form_submit_button("Simpan Mahasiswa")

        if submitted:
            if not nim or not nama:
                st.warning("Mohon lengkapi semua data mahasiswa.")
            else:
                mahasiswa = Mahasiswa(nim=nim, nama=nama, semester=semester)
                if manager.tambah_mahasiswa(mahasiswa):
                    st.success("✅ Mahasiswa berhasil disimpan.")
                else:
                    st.error("❌ Gagal menyimpan data mahasiswa.")

# Halaman Input Nilai Mahasiswa
def halaman_input_nilai(manager: ManajemenNilaiMahasiswa):
    st.header("🎓 Input Nilai Mahasiswa")

    daftar_mahasiswa = manager.get_semua_mahasiswa()
    if not daftar_mahasiswa:
        st.warning("Belum ada data mahasiswa.")
        return

    mahasiswa_pilihan = st.selectbox("Pilih Mahasiswa:", [f"{m.nim} - {m.nama}" for m in daftar_mahasiswa])
    nim = mahasiswa_pilihan.split(" - ")[0]

    semester_dipilih = st.selectbox("Pilih Semester:", list(MATA_KULIAH_PER_SEMESTER.keys()))
    matkul_list = MATA_KULIAH_PER_SEMESTER.get(semester_dipilih, [])

    if not matkul_list:
        st.warning("Belum ada mata kuliah untuk semester ini.")
        return

    matkul_pilihan = st.selectbox("Pilih Mata Kuliah:", matkul_list)
    nilai_angka = st.number_input("Nilai Angka:", min_value=0.0, max_value=100.0)

    if st.button("Simpan Nilai"):
        kode_mk = matkul_pilihan.replace(" ", "_").lower()
        mk_obj = MataKuliah(kode_mk=kode_mk, nama_mk=matkul_pilihan)
        manager.tambah_mata_kuliah(mk_obj)
        nilai = Nilai(nim=nim, kode_mk=kode_mk, nilai_angka=nilai_angka)
        if manager.tambah_nilai(nilai):
            st.success("✅ Nilai berhasil disimpan.")
        else:
            st.error("❌ Gagal menyimpan nilai.")

# Halaman Riwayat Nilai Mahasiswa
def halaman_riwayat(manager: ManajemenNilaiMahasiswa):
    st.header("📋 Riwayat Nilai Mahasiswa")
    daftar_mahasiswa = manager.get_semua_mahasiswa()
    if not daftar_mahasiswa:
        st.warning("Belum ada data mahasiswa.")
        return

    mahasiswa_pilihan = st.selectbox("Pilih Mahasiswa:", [f"{m.nim} - {m.nama}" for m in daftar_mahasiswa])
    nim = mahasiswa_pilihan.split(" - ")[0]

    df = manager.get_dataframe_nilai(nim)
    if df.empty:
        st.info("Belum ada data nilai.")
    else:
        st.dataframe(df, use_container_width=True)

# Halaman Hitung IPK Mahasiswa
def halaman_ipk(manager: ManajemenNilaiMahasiswa):
    st.header("📊 Hitung Rata-rata Nilai Mahasiswa")
    daftar_mahasiswa = manager.get_semua_mahasiswa()
    if not daftar_mahasiswa:
        st.warning("Belum ada data mahasiswa.")
        return

    mahasiswa_pilihan = st.selectbox("Pilih Mahasiswa:", [f"{m.nim} - {m.nama}" for m in daftar_mahasiswa])
    nim = mahasiswa_pilihan.split(" - ")[0]

    ipk = manager.hitung_ipk(nim)
    st.metric(label="Rata-rata Nilai", value=f"{ipk:.2f}")

# Fungsi utama aplikasi
def main():
    st.sidebar.title("📚 Manajemen Nilai Mahasiswa TRK")
    menu = st.sidebar.radio("Menu:", ["Input Mahasiswa", "Input Nilai", "Riwayat Nilai", "Hitung IPK"])

    if menu == "Input Mahasiswa":
        halaman_input_mahasiswa(manager)
    elif menu == "Input Nilai":
        halaman_input_nilai(manager)
    elif menu == "Riwayat Nilai":
        halaman_riwayat(manager)
    elif menu == "Hitung IPK":
        halaman_ipk(manager)

if __name__ == "__main__":
    main()
