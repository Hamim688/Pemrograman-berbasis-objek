# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'management_nilai_mahasiswa.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)
MATA_KULIAH = ["Pemrograman Berbasis Objek", "Sistem Basis Data", "Bahasa Inggris", 
               "Kewarganegaraan","Jaringan Komputer", "Sistem Tertanam", "Kecerdasan Buatan", "Statistika"]
MATA_KULIAH_DEFAULT = "Pemrograman Berbasis Objek"
SKALA_NILAI = {
    "A": (85, 100),
    "B": (75, 84),
    "C": (65, 74),
    "D": (50, 64),
    "E": (0, 49)
}
BOBOT_NILAI = {
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0
}
