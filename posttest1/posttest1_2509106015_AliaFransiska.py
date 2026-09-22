import os

class Marketplace:
    nama_toko = "Altria Aquatics Marketplace"
    total_produk = 0
    mata_uang = "IDR"

    def __init__(self, wilayah):
        self.wilayah = wilayah

    @staticmethod
    def input_angka(pesan):
        while True:
            try:
                nilai = int(input(pesan))
                if nilai < 0:
                    print("Tidak boleh negatif!")
                    continue
                return nilai
            except ValueError:
                print("Harus angka!")

    @classmethod
    def tambah_produk(cls, jumlah=1):
        cls.total_produk += jumlah

    def info(self):
        print(f"\nToko: {self.nama_toko}")
        print(f"Wilayah: {self.wilayah}")
        print(f"Mata Uang: {self.mata_uang}")
        print(f"Total Produk: {self.total_produk}")

class Produk:
    def __init__(self, nama, kategori, harga, stok):
        self.nama = nama
        self.kategori = kategori
        self.__harga = harga
        self.__stok = stok
        Marketplace.tambah_produk()

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai_baru):
        if nilai_baru < 0:
            raise ValueError("Harga tidak boleh negatif!")
        self.__harga = nilai_baru

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai_baru):
        if not isinstance(nilai_baru, int) or nilai_baru < 0:
            raise ValueError("Stok harus angka bulat positif!")
        self.__stok = nilai_baru

    def tampilan(self):
        status = "Ada" if self.__stok > 0 else "Habis"
        print(f"[{self.kategori}] {self.nama} | Rp{self.__harga} | Stok: {self.__stok} ({status})")

    def kurangi_stok(self, jumlah):
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return 0
        if self.__stok >= jumlah:
            self.__stok -= jumlah
            total = self.__harga * jumlah
            print(f"Berhasil membeli {jumlah} {self.nama}. Total: Rp{total:,}")
            return total
        else:
            print(f"Stok {self.nama} cuma {self.__stok}.")
            return 0

class User:
    def __init__(self, nama, password, saldo, role):
        self.nama = nama
        self.__password = password
        self.__saldo = saldo
        self.role = role

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, topup):
        if topup < 0:
            raise ValueError("Topup tidak boleh negatif!")
        self.__saldo += topup
        print(f"Topup Rp{topup} berhasil")

    def cek_password(self, password_input):
        return self.__password == password_input

    def profil(self):
        print(f"\nNama: {self.nama}")
        print(f"Role: {self.role.upper()}")
        print(f"Saldo: Rp{self.__saldo}")

    def beli(self, produk, jumlah):
        print(f"\n>>> {self.nama} mau beli {produk.nama}...")
        biaya = produk.harga * jumlah
        if self.__saldo >= biaya:
            bayar = produk.kurangi_stok(jumlah)
            if bayar > 0:
                self.__saldo -= bayar
                print(f"Sisa saldo {self.nama}: Rp{self.__saldo}")
        else:
            print(f"Gagal! Saldo gak cukup. Butuh Rp{biaya}, punya Rp{self.__saldo}")

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

def cari_user(daftar, nama):
    for u in daftar:
        if u.nama.lower() == nama.lower():
            return u
    return None

if __name__ == "__main__":
    toko1 = Marketplace("Samarinda")
    toko2 = Marketplace("Balikpapan")
    
    daftar_produk = [
        Produk("Ikan Koi Kohaku", "Ikan Hias", 150000, 10),
        Produk("Akuarium Minimalis 40cm", "Akuarium", 250000, 5)
    ]
    
    daftar_user = [
        User("alia", "015", 1900000, "user")
    ]
    
    NAMA_ADMIN = "admin"
    PASS_ADMIN = "admin123"
    AKUN_ADMIN = User("admin", PASS_ADMIN, 0, "admin")
    
    pengguna_aktif = None

    while True:
        bersihkan_layar()
        print("=" * 50)
        print(f"   {Marketplace.nama_toko.upper()}")
        print("=" * 50)
        
        if pengguna_aktif is None:
            print("\n1. Login")
            print("2. Register")
            print("3. Keluar")
            print("4. Pengujian Program (Main Code)")
            pilih = input("Pilih menu: ")
            
            if pilih == "1":
                bersihkan_layar()
                print("== LOGIN ==")
                nama = input("Username: ")
                password = input("Password: ")
                
                if nama.lower() == NAMA_ADMIN and password == PASS_ADMIN:
                    pengguna_aktif = AKUN_ADMIN
                    print(f"Login berhasil! Selamat datang, {AKUN_ADMIN.nama} (ADMIN).")
                    input("\nTekan Enter...")
                else:
                    user = cari_user(daftar_user, nama)
                    if user and user.cek_password(password):
                        pengguna_aktif = user
                        print(f"Login berhasil! Selamat datang, {user.nama} (USER).")
                        input("\nTekan Enter...")
                    else:
                        print("Nama atau password salah!")
                        input("\nTekan Enter...")
                        
            elif pilih == "2":
                bersihkan_layar()
                print("== REGISTER AKUN BARU ==")
                nama = input("Nama: ")
                while not nama.strip():
                    print("Nama tidak boleh kosong!")
                    nama = input("Nama: ")
                
                if nama.lower() == NAMA_ADMIN:
                    print("ERROR: Nama 'admin' tidak boleh digunakan untuk register! Karena akun admin sudah ada!")
                    input("\nTekan Enter...")
                    continue
                
                if cari_user(daftar_user, nama):
                    print("Nama sudah terdaftar! Gunakan nama lain.")
                    input("\nTekan Enter...")
                    continue
                
                password = input("Password: ")
                while not password.strip():
                    print("Password tidak boleh kosong!")
                    password = input("Password: ")
                
                saldo = Marketplace.input_angka("Saldo Awal: ")
                
                user_baru = User(nama, password, saldo, "user")
                daftar_user.append(user_baru)
                
                print(f"\nPembuatan akun berhasil!")
                print(f"Nama: {user_baru.nama}")
                print(f"Role: {user_baru.role.upper()}")
                print(f"Saldo: Rp{user_baru.saldo}")
                print("\nSilakan login dengan akun yang baru dibuat.")
                input("\nTekan Enter...")
                
            elif pilih == "3":
                break

            elif pilih == "4":
                bersihkan_layar()

                # 2 objek untuk setiap class
                Toko11 = Marketplace("Tarakan")
                Toko12 = Marketplace("Bontang")
                Produk1 = Produk("Ikan Arwana", "Ikan Hias", 5000000, 3)
                Produk2 = Produk("Filter Akuarium", "Aksesoris", 150000, 20)
                User1 = User("arum", "arum123", 2000000, "user")
                User2 = User("dewi", "dewi123", 750000, "user")
                print("\n2 objek Marketplace:")
                print("Toko11 = Tarakan")
                print("Toko12 = Bontang")
                print("\n2 objek Produk:")
                print("Produk1 = Ikan Arwana")
                print("Produk2 = Filter Akuarium")
                print("\n2 objek User:")
                print("User1 = arum")
                print("User2 = dewi")

                # 2. Instance method
                print("\n== Instance Method ==")
                print("\n[info() dari Toko11]")
                Toko11.info()
                print("\n[tampilan() dari Produk1]")
                Produk1.tampilan()
                print("\n[profil() dari User1]")
                User1.profil()
                print("\n[cek_password() dari User1]")
                print("Password benar :", User1.cek_password("arum123"))
                print("Password salah  :", User1.cek_password("salah"))
                print("\n[beli() dari User1]")
                User1.beli(Produk2, 2)

                # 3. Class method
                print("\n== Class Method ==")
                print("Total produk awal:", Marketplace.total_produk)
                Marketplace.tambah_produk(5)
                print("Setelah tambah_produk(5):", Marketplace.total_produk)

                # 4. Static method
                print("\n== Static Method ==")
                angka = Marketplace.input_angka(
                    "Masukkan angka untuk pengujian: "
                )
                print("Angka yang dimasukkan:", angka)

                # 5. Setter valid
                print("\n== Pengujian Setter Data Valid ==")
                Produk1.harga = 6000000
                print("Harga Produk1 berhasil diubah:", Produk1.harga)
                Produk2.stok = 25
                print("Stok Produk2 berhasil diubah:", Produk2.stok)
                User1.saldo = 1000000
                print("Saldo User1 berhasil ditambah:", User1.saldo)

                # 6. Setter tidak valid
                print("\n== Pengujian Setter Data Tidak Valid ==")
                try:
                    Produk1.harga = -1000
                except ValueError as e:
                    print("Harga tidak valid:", e)
                try:
                    Produk2.stok = "dua puluh"
                except ValueError as e:
                    print("Stok tidak valid:", e)
                try:
                    User1.saldo = -50000
                except ValueError as e:
                    print("Saldo tidak valid:", e)
                input("\nTekan Enter untuk kembali ke menu login...")
            else:
                print("Pilihan salah!")
                input("\nTekan Enter...")
                
        else:
            print(f"\nHalo, {pengguna_aktif.nama} ({pengguna_aktif.role.upper()})")
            
            if pengguna_aktif.role == "admin":
                print("\n== MENU ADMIN ==")
                print("1. Tambah Produk")
                print("2. Lihat Semua Produk")
                print("3. Edit Harga Produk")
                print("4. Hapus Produk")
                print("5. Lihat Semua User")
                print("6. Logout")
            else:
                print("\n== MENU USER ==")
                print("1. Lihat Produk")
                print("2. Beli Produk")
                print("3. Isi Saldo")
                print("4. Profil Saya")
                print("5. Logout")
            
            pilih = input("Pilih menu: ")
            
            if pengguna_aktif.role == "admin":
                if pilih == "1":
                    nama = input("Nama Produk: ")
                    kat = input("Kategori: ")
                    harga = Marketplace.input_angka("Harga: ")
                    stok = Marketplace.input_angka("Stok: ")
                    daftar_produk.append(Produk(nama, kat, harga, stok))
                    print("Produk berhasil ditambah!")
                    input("\nTekan Enter...")
                    
                elif pilih == "2":
                    print("\n== Daftar Produk ==")
                    for i, p in enumerate(daftar_produk, 1):
                        print(f"{i}. ", end="")
                        p.tampilan()
                    input("\nTekan Enter...")
                    
                elif pilih == "3":
                    print("\n== Edit Produk ==")
                    for i, p in enumerate(daftar_produk, 1):
                        print(f"{i}. {p.nama} (Rp{p.harga:,})")
                    idx = Marketplace.input_angka("Nomor produk: ") - 1
                    if 0 <= idx < len(daftar_produk):
                        harga_baru = Marketplace.input_angka("Harga baru: ")
                        try:
                            daftar_produk[idx].harga = harga_baru
                            print("Harga berhasil diubah!")
                        except ValueError as e:
                            print(f"Gagal: {e}")
                    input("\nTekan Enter...")
                    
                elif pilih == "4":
                    print("\n== Hapus Produk ==")
                    for i, p in enumerate(daftar_produk, 1):
                        print(f"{i}. {p.nama}")
                    idx = Marketplace.input_angka("Nomor produk: ") - 1
                    if 0 <= idx < len(daftar_produk):
                        hapus = daftar_produk.pop(idx)
                        print(f"Produk {hapus.nama} berhasil dihapus!")
                    input("\nTekan Enter...")
                    
                elif pilih == "5":
                    print("\n== Daftar User ==")
                    for i, u in enumerate(daftar_user, 1):
                        print(f"{i}. {u.nama} - Saldo: Rp{u.saldo:,}")
                    input("\nTekan Enter...")
                    
                    
                elif pilih == "6":
                    pengguna_aktif = None
                    
                else:
                    print("Pilihan salah!")
                    input("\nTekan Enter...")
                    
            else:
                if pilih == "1":
                    print("\n== Daftar Produk ==")
                    for i, p in enumerate(daftar_produk, 1):
                        print(f"{i}. ", end="")
                        p.tampilan()
                    input("\nTekan Enter...")
                    
                elif pilih == "2":
                    print("\n== Beli Produk ==")
                    for i, p in enumerate(daftar_produk, 1):
                        print(f"{i}. ", end="")
                        p.tampilan()
                    idx = Marketplace.input_angka("Nomor produk: ") - 1
                    if 0 <= idx < len(daftar_produk):
                        jml = Marketplace.input_angka("Jumlah beli: ")
                        pengguna_aktif.beli(daftar_produk[idx], jml)
                    input("\nTekan Enter...")
                    
                elif pilih == "3":
                    nominal = Marketplace.input_angka("Nominal topup: ")
                    try:
                        pengguna_aktif.saldo = nominal
                    except ValueError as e:
                        print(f"Gagal: {e}")
                    input("\nTekan Enter...")
                    
                elif pilih == "4":
                    pengguna_aktif.profil()
                    input("\nTekan Enter...")
                    
                    
                elif pilih == "5":
                    pengguna_aktif = None
                    
                else:
                    print("Pilihan salah!")
                    input("\nTekan Enter...")

    print("\nTerima kasih telah menggunakan Altria Aquatics Marketplace!")