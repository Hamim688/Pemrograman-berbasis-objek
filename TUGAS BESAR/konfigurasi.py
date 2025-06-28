# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'management_nilai_mahasiswa.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)
MATA_KULIAH_PER_SEMESTER = {
    1: ["Bahasa Indonesia", "Algoritma Dan Pemrograman", "Sistem Operasi", "Matematika Diskrit", "Etika Profesi & K3", "Pengantar Teknologi Informasi", "Arsitektur dan Organisasi Komputer", "Sistem Basis Data I", "Desain dan Multimedia"],
    2: ["Teknik Digital dan Sistem Tertanam", "Bahasa Inggris I", "Kewarganegaraan", "Sistem Basis Data II", "Kecerdasan Buatan", "Pemrograman Berorientasi Objek", "Jaringan Komputer I", "Statistika"],
    3: ["Jaringan Komputer 2", "Mobile Programming", "Pemrograman Web Dinamis", "Mikroprosesor & Mikrokontroller", "Agama"],
    4: ["Machine Learning", "Keamanan Jaringan", "Pancasila", "Pemrograman Game", "Interoperabilitas", "Pemrograman Web Berbasis Framework", "Image Processing"],
    5: ["Bahasa Inggris II", "Desain dan Perancangan Sistem informasi", "Sistem Multimedia", "Internet of Things (IoT)", "Data Mining", "Cloud Computing", "Interaksi Manusia dan Komputer"],
    6: ["Sistem Informasi Enterprise", "Simulasi dan Pemrograman Robot ", "Big Data", "Real-Time System", "Manajemen Proyek ", "Metodologi Penelitian", "Technopreneurship", "Pengembangan Game"],
    7: ["Virtual System & Services", "Integrative Programming", "Special Topic in Industrial Informatic", "Automasi Industri", "Tugas Akhir"],
    8: ["MAGANG"]
}
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
