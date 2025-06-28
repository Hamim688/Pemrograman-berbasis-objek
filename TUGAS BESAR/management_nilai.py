# management_nilai.py
import pandas as pd
from model import Mahasiswa, MataKuliah, Nilai
import database

class ManajemenNilaiMahasiswa:
    """Mengelola logika bisnis manajemen nilai mahasiswa."""

    _db_setup_done = False

    def __init__(self):
        if not ManajemenNilaiMahasiswa._db_setup_done:
            print("[ManajemenNilaiMahasiswa] Setup database awal...")
            if database.setup_database_initial():
                ManajemenNilaiMahasiswa._db_setup_done = True
                print("[ManajemenNilaiMahasiswa] Database siap.")
            else:
                print("[ManajemenNilaiMahasiswa] KRITICAL: Setup DB GAGAL.")

    # -- Mahasiswa --
    def tambah_mahasiswa(self, mhs: Mahasiswa) -> bool:
        if not isinstance(mhs, Mahasiswa): return False
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan, semester) VALUES (?, ?, ?, ?)"
        params = (mhs.nim, mhs.nama, mhs.jurusan, mhs.semester)
        return database.execute_query(sql, params) is not None

    def get_semua_mahasiswa(self) -> list[Mahasiswa]:
        sql = "SELECT * FROM mahasiswa ORDER BY nim"
        rows = database.fetch_query(sql)
        return [Mahasiswa(**dict(r)) for r in rows] if rows else []

    # -- Mata Kuliah --
    def tambah_mata_kuliah(self, mk: MataKuliah) -> bool:
        if not isinstance(mk, MataKuliah): return False
        sql = "INSERT INTO mata_kuliah (kode_mk, nama_mk) VALUES (?, ?)"
        params = (mk.kode_mk, mk.nama_mk)
        return database.execute_query(sql, params) is not None

    def get_semua_mk(self) -> list[MataKuliah]:
        sql = "SELECT * FROM mata_kuliah ORDER BY kode_mk"
        rows = database.fetch_query(sql)
        return [MataKuliah(**dict(r)) for r in rows] if rows else []

    # -- Nilai --
    def tambah_nilai(self, nilai: Nilai) -> bool:
        if not isinstance(nilai, Nilai): return False
        sql = "INSERT INTO nilai (nim, kode_mk, nilai_angka) VALUES (?, ?, ?)"
        params = (nilai.nim, nilai.kode_mk, nilai.nilai_angka)
        return database.execute_query(sql, params) is not None

    def get_nilai_mahasiswa(self, nim: str) -> list[Nilai]:
        sql = "SELECT id_nilai, nim, kode_mk, nilai_angka FROM nilai WHERE nim = ? ORDER BY kode_mk"
        rows = database.fetch_query(sql, (nim,))
        return [Nilai(**dict(r)) for r in rows] if rows else []

    def get_dataframe_nilai(self, nim: str) -> pd.DataFrame:
        sql = """
        SELECT mk.nama_mk AS 'Mata Kuliah', n.nilai_angka AS 'Nilai Angka'
        FROM nilai n
        JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
        WHERE n.nim = ?
        ORDER BY mk.nama_mk
        """
        df = database.get_dataframe(sql, params=(nim,))
        if not df.empty:
            df['Nilai Huruf'] = df['Nilai Angka'].apply(lambda n: Nilai(nim, "", n).nilai_huruf())
            df['Bobot'] = df['Nilai Angka'].apply(lambda n: Nilai(nim, "", n).bobot())
        return df

    def hitung_ipk(self, nim: str) -> float:
        df = self.get_dataframe_nilai(nim)
        if df.empty:
            return 0.0
        return round(df['Bobot'].mean(), 2)
    
    
    def get_matkul_by_semester(self, semester: int) -> list[MataKuliah]:
        sql = "SELECT kode_mk, nama_mk, sks, semester FROM mata_kuliah WHERE semester = ?"
        rows = database.fetch_query(sql, (semester,))
        return [MataKuliah(kode_mk=r["kode_mk"], nama_mk=r["nama_mk"], sks=r["sks"], semester=r["semester"]) for r in rows] if rows else []

