# model.py
class Mahasiswa:
    """Merepresentasikan data mahasiswa."""
    
    def __init__(self, nim: str, nama: str, semester: int):
        self.nim = nim.strip().upper()
        self.nama = nama.strip().title()
        try:
            self.semester = int(semester)
            if self.semester <= 0:
                print(f"Peringatan: Semester harus lebih dari 0. Diberi: {semester}")
                self.semester = 1
        except ValueError:
            print(f"Peringatan: Semester tidak valid: {semester}")
            self.semester = 1

    def __repr__(self) -> str:
        return f"Mahasiswa(NIM:{self.nim}, Nama:{self.nama}, Semester:{self.semester})"

    def to_dict(self) -> dict:
        return {
            "nim": self.nim,
            "nama": self.nama,
            "semester": self.semester
        }

class MataKuliah:
    """Merepresentasikan data mata kuliah."""
    
    def __init__(self, kode_mk: str, nama_mk: str):
        self.kode_mk = kode_mk.strip().upper()
        self.nama_mk = nama_mk.strip().title()

    def __repr__(self) -> str:
        return f"MataKuliah(Kode:{self.kode_mk}, Nama:{self.nama_mk})"

    def to_dict(self) -> dict:
        return {
            "kode_mk": self.kode_mk,
            "nama_mk": self.nama_mk,
        }
    
class Nilai:
    """Merepresentasikan nilai mahasiswa pada mata kuliah tertentu."""
    
    def __init__(self, nim: str, kode_mk: str, nilai_angka: float, id_nilai: int | None = None):
        self.id_nilai = id_nilai
        self.nim = nim.strip().upper()
        self.kode_mk = kode_mk.strip().upper()
        try:
            nilai_flt = float(nilai_angka)
            if 0 <= nilai_flt <= 100:
                self.nilai_angka = nilai_flt
            else:
                print(f"Peringatan: Nilai di luar rentang 0-100: {nilai_angka}")
                self.nilai_angka = 0.0
        except ValueError:
            print(f"Peringatan: Nilai tidak valid: {nilai_angka}")
            self.nilai_angka = 0.0

    def nilai_huruf(self) -> str:
        """Mengembalikan nilai huruf berdasarkan rentang nilai angka."""
        n = self.nilai_angka
        if n >= 85.00:
            return "A"
        elif n >= 77.50:
            return "AB"
        elif n >= 70.00:
            return "B"
        elif n >= 62.50:
            return "BC"
        elif n >= 55.00:
            return "C"
        elif n >= 40.00:
            return "D"
        else:
            return "E"

    def bobot(self) -> float:
        """Mengembalikan bobot nilai berdasarkan nilai huruf."""
        huruf = self.nilai_huruf()
        return {
            "A": 4.0,
            "AB": 3.5,
            "B": 3.0,
            "BC": 2.5,
            "C": 2.0,
            "D": 1.0,
            "E": 0.0
        }.get(huruf, 0.0)
    
    def __repr__(self) -> str:
        return f"Nilai(ID:{self.id_nilai}, NIM:{self.nim}, MK:{self.kode_mk}, Nilai:{self.nilai_angka}, Huruf:{self.nilai_huruf()})"

    def to_dict(self) -> dict:
        return {
            "nim": self.nim,
            "kode_mk": self.kode_mk,
            "nilai_angka": self.nilai_angka,
            "nilai_huruf": self.nilai_huruf(),
            "bobot": self.bobot()
        }