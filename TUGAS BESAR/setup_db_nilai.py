import sqlite3
import os
from konfigurasi import DB_PATH  # Ambil path dari konfigurasi

def setup_database():
    print(f"Memeriksa/membuat database di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Buat tabel mahasiswa
        sql_mahasiswa = """
        CREATE TABLE IF NOT EXISTS mahasiswa (
            nim TEXT PRIMARY KEY,
            nama TEXT NOT NULL,
            jurusan TEXT NOT NULL,
            semester INTEGER NOT NULL
        );
        """
        print(" Membuat tabel 'mahasiswa' (jika belum ada)...")
        cursor.execute(sql_mahasiswa)

        # Buat tabel mata kuliah
        sql_mk = """
        CREATE TABLE IF NOT EXISTS mata_kuliah (
            kode_mk TEXT PRIMARY KEY,
            nama_mk TEXT NOT NULL
        );
        """
        print(" Membuat tabel 'mata_kuliah' (jika belum ada)...")
        cursor.execute(sql_mk)

        # Buat tabel nilai
        sql_nilai = """
        CREATE TABLE IF NOT EXISTS nilai (
            id_nilai INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT NOT NULL,
            kode_mk TEXT NOT NULL,
            nilai_angka REAL NOT NULL,
            FOREIGN KEY (nim) REFERENCES mahasiswa(nim),
            FOREIGN KEY (kode_mk) REFERENCES mata_kuliah(kode_mk)
        );
        """
        print(" Membuat tabel 'nilai' (jika belum ada)...")
        cursor.execute(sql_nilai)

        conn.commit()
        print(" -> Tabel 'mahasiswa', 'mata_kuliah', dan 'nilai' siap.")
        return True

    except sqlite3.Error as e:
        print(f" -> Error SQLite saat setup: {e}")
        return False

    finally:
        if conn:
            conn.close()
            print(" -> Koneksi DB ditutup.")

if __name__ == "__main__":
    print("--- Setup Database Manajemen Nilai Mahasiswa ---")
    if setup_database():
        print(f"\nSetup database '{os.path.basename(DB_PATH)}' selesai.")
    else:
        print(f"\nSetup database GAGAL.")
    print("--- Setup Database Selesai ---")
