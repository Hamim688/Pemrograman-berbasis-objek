class Buku:
    def __init__(self, judul, penulis, tahun, jml_halaman):
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun
        self.jml_halaman = max(0, jml_halaman) # Pastikan non-negatif

    def __str__(self):
        # Versi singkat untuk kejelasan perbandingan
        return f"'{self.judul}' ({self.tahun})"
    
    def __repr__(self):
        return f"Buku(judul='{self.judul}', penulis='{self.penulis}', tahun={self.tahun}, jml_halaman={self.jml_halaman})"
    
    def __len__(self):
        return self.jml_halaman
    
    # --- Imlementasi Perbandingan ---

    # __eq__ : Dipanggil saat menggunakan operator ==
    def __eq__(self, other):
        """Membandingkan kesamaan dua objek BUku berdasarkan judul dan penulis."""
        print(f"-> Memanggil __eq__: Membandingkan '{self.judul}' == '{getattr(other, 'judul', '?')}'")
        # cek apakah 'other' adalah instance dari kelas Buku
        if isinstance(other, Buku):
            # Logika kesamaan: Judul DAN penulis harus sama
            return (self.judul == other.judul) and (self.penulis == other.penulis)
        # Jika tipe berbeda, kembalikan NotImplemented agar Python bisa coba cara lain
        # atau menghasilkan TypeError jika tidak ada cara yang lain.
        return NotImplemented
    
    # __it__ : Dipanggil saat menggunakan operator < 
    def __it__(self, other):
        """Membandingkan objek Buku berdasarkan tahun terbit (lebih kecil dari)."""
        print(f"-> Memanggil __it__: Membandingkan '{self.judul}'({self.tahun}) < '{getattr(other, 'judul', '?')}' ({getattr(other, 'tahun','?')})")
        # Cek apakah 'other' adalah instance dari kelas Buku
        if isinstance(other, Buku):
            # Logika perbandingan: bandingkan tahun terbit
            return self.tahun < other.tahun
        # Jika tipe berbeda, operasi tidak didukung
        return NotImplemented
    
    # Catatan: Jika Anda implementasi __eq__ dan __lt__, Python seringkali
    # bisa secara otomatis menyediakan implementasi untuk __ne__, __gt__,
    # __le__,__ge__ berdasarkan logika __eq__ dan __lt__.
    # Namun, untuk kontrol penuh atau optimasi, Anda bisa implementasikan
    # semuanya secara eksplisit jika perlu.

# --- Kode Utama ---
if __name__ == "__main__":
    buku_A = Buku("Sejarah Jawa Kuno", "Prof. X", 1995, 450)
    buku_B = Buku("Teknologi AI", "Dr. Y", 2022, 300)
    buku_C = Buku("Sejarah Jawa Kuno", "Prof. X", 1995, 500) # sama judul&penulis dgn A
    buku_D = Buku("Pengantar Python", "Prof. X", 2018, 400)

    print("\n--- Perbandingan Kesamaan (==) ---")