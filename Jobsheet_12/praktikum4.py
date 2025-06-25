import pandas as pd
from abc import ABC, abstractmethod  # Diperlukan untuk definisi kelas

# --- Definisi Kelas (Salin dari Praktikum 3) ---
class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError, SystemError):
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

    def __str__(self) -> str:
        return f"{self.nama} [{type(self).__name__}]"

class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, menu_andalan: str):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>Menu Andalan: {self.menu_andalan}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, agama: str = "Umum", deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

# --- Fungsi baca data (Salin dari Praktikum 2) ---
def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    try:
        dataframe = pd.read_csv(nama_file)
        return dataframe
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"ERROR saat membaca file CSV: {type(e).__name__} - {e}")
        return None

# --- Fungsi Inti Praktikum Ini ---
def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    """
    Mengiterasi DataFrame Pandas dan membuat list berisi objek-objek
    Lokasi (atau turunannya) berdasarkan data di setiap baris.

    Args:
    dataframe (pd.DataFrame): DataFrame yang berisi data lokasi
    dengan kolom 'Nama', 'Latitude', 'Longitude', 'Tipe', 'Deskripsi'.

    Returns:
    list: List berisi instance objek Lokasi atau turunannya.
    """
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        print("DataFrame kosong atau None, tidak ada objek dibuat.")
        return list_objek_lokasi

    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')

        objek = None
        if nama is None or lat is None or lon is None:
            print(f" -> Melewati baris {index}: Data Nama/Latitude/Longitude tidak lengkap.")
            continue

        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                if "Islam" in tipe:
                    agama_info = "Islam"
                elif "Kristen" in tipe:
                    agama_info = "Kristen"
                elif "Klenteng" in tipe:
                    agama_info = "Tridharma"
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
            else:
                print(f" -> Peringatan: Tipe '{tipe}' untuk '{nama}' tidak dikenali. Tidak membuat objek spesifik.")
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")
            continue

        if objek:
            list_objek_lokasi.append(objek)

    print(f"Total {len(list_objek_lokasi)} objek lokasi berhasil dibuat dari {len(dataframe)} baris data.")
    return list_objek_lokasi

# --- Kode Utama ---
if __name__ == "__main__":
    NAMA_FILE_CSV = "lokasi_semarang.csv"

    print("--- Memulai Praktikum 4: Membuat Objek dari Data Pandas ---")
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    print("\n--- Daftar Objek Lokasi yang Berhasil Dibuat ---")
    if list_semua_lokasi:
        for idx, lok in enumerate(list_semua_lokasi):
            print(f"{idx+1}. {repr(lok)}")
    else:
        print("Tidak ada objek lokasi yang dibuat.")

    print("\n--- Praktikum 4 Selesai ---")
