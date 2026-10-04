import os

class RiwayatMutasi:
    def __init__(self, tipe, jumlah, keterangan):
        self.tipe = tipe
        self.jumlah = jumlah
        self.keterangan = keterangan

    def tampilkan_log(self):
        simbol = "+" if self.tipe == "Masuk" else "-"
        return f"[{self.tipe}] {simbol}{self.jumlah} unit | {self.keterangan}"

class Marketplace:
    nama_toko = "Altria Aquatics Marketplace"
    total_transaksi = 0
    mata_uang = "IDR"

    def __init__(self, wilayah):
        self.wilayah = wilayah
        self.daftar_produk = []
        self.daftar_user = []

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
    def tambah_statistik(cls):
        cls.total_transaksi += 1

    def info(self):
        print(f"\nToko: {self.nama_toko}")
        print(f"Wilayah: {self.wilayah}")
        print(f"Mata Uang: {self.mata_uang}")
        print(f"Total Transaksi Sukses: {self.total_transaksi}")

    def tambah_produk_ke_sistem(self, produk):
        self.daftar_produk.append(produk)

    def tambah_user_ke_sistem(self, user):
        self.daftar_user.append(user)

class Produk:
    def __init__(self, nama, kategori, harga, stok_awal):
        self.nama = nama
        self.kategori = kategori
        self.__harga = harga
        self._stok = stok_awal
        self.log_stok = []
        self._catat_mutasi("Masuk", stok_awal, "Stok awal sistem")

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
        return self._stok

    def _catat_mutasi(self, tipe, jumlah, keterangan):
        mutasi = RiwayatMutasi(tipe, jumlah, keterangan)
        self.log_stok.append(mutasi)

    def kurangi_stok(self, jumlah, pembeli):
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return False
        if self._stok >= jumlah:
            self._stok -= jumlah
            self._catat_mutasi("Keluar", jumlah, f"Dibeli oleh {pembeli}")
            return True
        else:
            print(f"Stok {self.nama} cuma {self._stok}.")
            return False

    def tampil(self):
        status = "Ada" if self._stok > 0 else "Habis"
        print(f"[{self.kategori}] {self.nama} | Rp{self.__harga:,} | Stok: {self._stok} ({status})")

class User:
    def __init__(self, nama, password, saldo_awal, role):
        self.nama = nama
        self.__password = password
        self._saldo = saldo_awal
        self.role = role

    @property
    def saldo(self):
        return self._saldo

    def cek_password(self, input_pass):
        return self.__password == input_pass

    def profil(self):
        print(f"\nNama: {self.nama}")
        print(f"Role: {self.role.upper()}")
        print(f"Saldo: Rp{self._saldo:,}")

    def beli(self, produk, jumlah):
        print(f"\n>>> {self.nama} mau beli {produk.nama}...")
        biaya = produk.harga * jumlah
        
        if self._saldo >= biaya:
            if produk.kurangi_stok(jumlah, self.nama):
                self._saldo -= biaya
                Marketplace.tambah_statistik()
                print(f"Pembelian berhasil! Sisa saldo: Rp{self._saldo:,}")
                return True
        else:
            print(f"Gagal! Saldo gak cukup. Butuh Rp{biaya:,}, punya Rp{self._saldo:,}")
            return False

class AdminUser(User):
    def __init__(self, nama, password, saldo_awal):
        super().__init__(nama, password, saldo_awal, "admin")
        self.jabatan = "Pengelola Toko"

    def hapus_produk(self, daftar_produk, index):
        if 0 <= index < len(daftar_produk):
            hapus = daftar_produk.pop(index)
            print(f"Admin {self.nama} menghapus produk: {hapus.nama}")
        else:
            print("Index produk tidak valid.")

class MemberUser(User):
    def __init__(self, nama, password, saldo_awal, diskon_persen):
        super().__init__(nama, password, saldo_awal, "member")
        self.diskon_persen = diskon_persen

    def beli(self, produk, jumlah):
        print(f"\n>>> {self.nama} (Member) mau beli {produk.nama}...")
        
        harga_normal = produk.harga * jumlah
        potongan = int(harga_normal * (self.diskon_persen / 100))
        biaya_akhir = harga_normal - potongan
        
        print(f"Harga Normal: Rp{harga_normal:,} | Diskon: Rp{potongan:,}")
        print(f"Total Bayar: Rp{biaya_akhir:,}")

        if self._saldo >= biaya_akhir:
            if produk.kurangi_stok(jumlah, self.nama):
                self._saldo -= biaya_akhir
                Marketplace.tambah_statistik()
                print(f"Pembelian berhasil! Sisa saldo: Rp{self._saldo:,}")
                return True
        else:
            print(f"Gagal! Saldo gak cukup. Butuh Rp{biaya_akhir:,}, punya Rp{self._saldo:,}")
            return False

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

def cari_user(daftar, nama):
    for u in daftar:
        if u.nama.lower() == nama.lower():
            return u
    return None

if __name__ == "__main__":
    sistem = Marketplace("Samarinda")
    
    p1 = Produk("Ikan Koi Kohaku", "Ikan Hias", 150000, 10)
    p2 = Produk("Akuarium Minimalis 40cm", "Akuarium", 250000, 5)
    
    sistem.tambah_produk_ke_sistem(p1)
    sistem.tambah_produk_ke_sistem(p2)
    
    admin = AdminUser("admin", "admin123", 0)
    sistem.tambah_user_ke_sistem(admin)
    
    member = MemberUser("alia", "015", 1900000, 10)
    sistem.tambah_user_ke_sistem(member)
    
    pengguna_aktif = None

    while True:
        bersihkan_layar()
        print("=" * 50)
        print(f"   {Marketplace.nama_toko.upper()}")
        print("=" * 50)
        
        if pengguna_aktif is None:
            print("\n1. Login")
            print("2. Register Member")
            print("3. Keluar")
            pilih = input("Pilih menu: ")
            
            if pilih == "1":
                bersihkan_layar()
                print("== LOGIN ==")
                nama = input("Username: ")
                password = input("Password: ")
                
                user = cari_user(sistem.daftar_user, nama)
                
                if isinstance(user, AdminUser) and user.cek_password(password):
                    pengguna_aktif = user
                    print(f"Login Admin Berhasil! Jabatan: {user.jabatan}")
                    input("\nTekan Enter...")
                elif isinstance(user, MemberUser) and user.cek_password(password):
                    pengguna_aktif = user
                    print(f"Login Member Berhasil! Diskon: {user.diskon_persen}%")
                    input("\nTekan Enter...")
                else:
                    print("Nama atau password salah!")
                    input("\nTekan Enter...")
                    
            elif pilih == "2":
                bersihkan_layar()
                print("== REGISTER MEMBER BARU ==")
                nama = input("Nama: ")
                if cari_user(sistem.daftar_user, nama):
                    print("Nama sudah ada!")
                    input("\nTekan Enter...")
                    continue
                
                password = input("Password: ")
                saldo = Marketplace.input_angka("Saldo Awal: ")
                diskon = Marketplace.input_angka("Persen Diskon (0-50): ")
                
                user_baru = MemberUser(nama, password, saldo, diskon)
                sistem.tambah_user_ke_sistem(user_baru)
                print("Registrasi Member Berhasil!")
                input("\nTekan Enter...")
                
            elif pilih == "3":
                break
            else:
                print("Pilihan salah!")
                input("\nTekan Enter...")
                
        else:
            if isinstance(pengguna_aktif, AdminUser):
                print("\n== MENU ADMIN ==")
                print("1. Tambah Produk")
                print("2. Lihat Semua Produk")
                print("3. Edit Harga Produk")
                print("4. Hapus Produk")
                print("5. Lihat Semua User")
                print("6. Info Toko")
                print("7. Logout")
            
            else:
                print("\n== MENU MEMBER ==")
                print("1. Lihat Produk")
                print("2. Beli Produk (Dapat Diskon!)")
                print("3. Isi Saldo")
                print("4. Profil Saya")
                print("5. Logout")
            
            pilih = input("Pilih menu: ")
            
            if isinstance(pengguna_aktif, AdminUser):
                if pilih == "1":
                    nama = input("Nama Produk: ")
                    kat = input("Kategori: ")
                    harga = Marketplace.input_angka("Harga: ")
                    stok = Marketplace.input_angka("Stok: ")
                    baru = Produk(nama, kat, harga, stok)
                    sistem.tambah_produk_ke_sistem(baru)
                    print("Produk ditambah ke sistem!")
                    input("\nTekan Enter...")
                    
                elif pilih == "2":
                    for i, p in enumerate(sistem.daftar_produk, 1):
                        print(f"{i}. ", end=""); p.tampil()
                    input("\nTekan Enter...")
                    
                elif pilih == "3":
                    print("\n== Edit Harga Produk ==")
                    for i, p in enumerate(sistem.daftar_produk, 1):
                        print(f"{i}. {p.nama} (Harga saat ini: Rp{p.harga:,})")
                    idx = Marketplace.input_angka("Nomor produk: ") - 1
                    if 0 <= idx < len(sistem.daftar_produk):
                        harga_baru = Marketplace.input_angka("Harga baru: ")
                        try:
                            sistem.daftar_produk[idx].harga = harga_baru
                            print("Harga berhasil diubah!")
                        except ValueError as e:
                            print(f"Gagal: {e}")
                    else:
                        print("Nomor produk tidak valid.")
                    input("\nTekan Enter...")
                    
                elif pilih == "4":
                    for i, p in enumerate(sistem.daftar_produk, 1):
                        print(f"{i}. {p.nama}")
                    idx = Marketplace.input_angka("Nomor produk dihapus: ") - 1
                    pengguna_aktif.hapus_produk(sistem.daftar_produk, idx)
                    input("\nTekan Enter...")
                    
                elif pilih == "5":
                    for u in sistem.daftar_user:
                        print(f"- {u.nama} ({u.role})")
                    input("\nTekan Enter...")
                    
                elif pilih == "6":
                    sistem.info()
                    input("\nTekan Enter...")
                    
                elif pilih == "7":
                    pengguna_aktif = None
                    
            else:
                if pilih == "1":
                    for i, p in enumerate(sistem.daftar_produk, 1):
                        print(f"{i}. ", end=""); p.tampil()
                    input("\nTekan Enter...")
                    
                elif pilih == "2":
                    for i, p in enumerate(sistem.daftar_produk, 1):
                        print(f"{i}. ", end=""); p.tampil()
                    idx = Marketplace.input_angka("Nomor produk: ") - 1
                    if 0 <= idx < len(sistem.daftar_produk):
                        jml = Marketplace.input_angka("Jumlah: ")
                        pengguna_aktif.beli(sistem.daftar_produk[idx], jml)
                    input("\nTekan Enter...")
                    
                elif pilih == "3":
                    nominal = Marketplace.input_angka("Nominal topup: ")
                    pengguna_aktif._saldo += nominal
                    print(f"Saldo bertambah Rp{nominal:,}")
                    input("\nTekan Enter...")
                    
                elif pilih == "4":
                    pengguna_aktif.profil()
                    input("\nTekan Enter...")
                    
                elif pilih == "5":
                    pengguna_aktif = None

    print("\nTerima kasih telah menggunakan Altria Aquatics Marketplace!")