import os
from abc import ABC, abstractmethod

class RiwayatMutasi:
    def __init__(self, tipe, jumlah, keterangan):
        self.tipe = tipe
        self.jumlah = jumlah
        self.keterangan = keterangan

    def tampilkan_log(self):
        if self.tipe == "Masuk":
            simbol = "+"
        else:
            simbol = "-"
        return f"[{self.tipe}] {simbol}{self.jumlah} unit | {self.keterangan}"


class Produk:
    def __init__(self, nama, kategori, harga, stok_awal):
        self.nama = nama
        self.kategori = kategori
        self.__harga = 0
        self.harga = harga
        
        if stok_awal < 0:
            self._stok = 0
        else:
            self._stok = stok_awal
            
        self.log_stok = []
        if stok_awal > 0:
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
        mutasi_baru = RiwayatMutasi(tipe, jumlah, keterangan)
        self.log_stok.append(mutasi_baru)

    def kurangi_stok(self, jumlah, pembeli):
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return False
            
        if self._stok < jumlah:
            print(f"Stok {self.nama} cuma {self._stok}.")
            return False
            
        self._stok = self._stok - jumlah
        self._catat_mutasi("Keluar", jumlah, f"Dibeli oleh {pembeli}")
        return True

    def tampil(self):
        if self._stok > 0:
            status = "Ada"
        else:
            status = "Habis"
            
        print(f"[{self.kategori}] {self.nama} | Rp{self.harga:,} | Stok: {self._stok} ({status})")

    def __str__(self):
        return f"{self.nama} (Rp{self.harga:,}, stok {self.stok})"


class Marketplace:
    nama_toko = "Altria Aquatics Marketplace"
    total_transaksi = 0
    mata_uang = "IDR"

    def __init__(self, wilayah):
        self.wilayah = wilayah
        self.daftar_produk = []
        self.daftar_user = []

    @staticmethod
    def input_angka(pesan, minimum=0):
        while True:
            try:
                nilai = int(input(pesan))
                if nilai < minimum:
                    print(f"Nilai minimal {minimum}.")
                    continue
                return nilai
            except ValueError:
                print("Harus angka!")

    @classmethod
    def tambah_statistik(cls):
        cls.total_transaksi = cls.total_transaksi + 1

    def info(self):
        print(f"\nToko: {self.nama_toko}\nWilayah: {self.wilayah}")
        print(f"Mata Uang: {self.mata_uang}\nTotal Transaksi Sukses: {self.total_transaksi}")

    def tambah_produk_ke_sistem(self, produk):
        self.daftar_produk.append(produk)

    def tambah_user_ke_sistem(self, user):
        self.daftar_user.append(user)

    def tampilkan_produk(self):
        if len(self.daftar_produk) == 0:
            print("Belum ada produk.")
        else:
            nomor = 1
            for produk in self.daftar_produk:
                print(f"{nomor}. ", end="")
                produk.tampil()
                nomor = nomor + 1

    def pilih_produk(self, pesan="Nomor produk: "):
        self.tampilkan_produk()
        indeks = self.input_angka(pesan, 1) - 1
        
        if indeks >= len(self.daftar_produk):
            print("Nomor produk tidak valid.")
            return None
            
        return self.daftar_produk[indeks]


class BaseUser(ABC):
    def __init__(self, nama, password, saldo_awal):
        self.nama = nama
        self.__password = password
        self._saldo = saldo_awal

    @property
    def saldo(self):
        return self._saldo

    def cek_password(self, input_pass):
        if self.__password == input_pass:
            return True
        else:
            return False

    def profil(self):
        print(f"\nNama: {self.nama}\nSaldo: Rp{self._saldo:,}")

    @abstractmethod
    def menu_khusus(self, marketplace):
        pass

    @abstractmethod
    def tampilkan_peran(self):
        pass

    @abstractmethod
    def akses_menu(self):
        pass

    def beli(self, produk, jumlah, diskon_persen=0):
        print(f"\n>>> {self.nama} mau beli {produk.nama}...")
        harga_normal = produk.harga * jumlah
        potongan = int(harga_normal * diskon_persen / 100)
        total = harga_normal - potongan

        if diskon_persen > 0:
            print(f"Harga normal: Rp{harga_normal:,} | Diskon: Rp{potongan:,}")
            print(f"Total bayar: Rp{total:,}")

        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return False
            
        if self._saldo < total:
            print(f"Gagal! Saldo gak cukup. Butuh Rp{total:,}, punya Rp{self._saldo:,}")
            return False
            
        berhasil_kurangi = produk.kurangi_stok(jumlah, self.nama)
        if berhasil_kurangi == False:
            return False

        self._saldo = self._saldo - total
        Marketplace.tambah_statistik()
        print(f"Pembelian berhasil! Sisa saldo: Rp{self._saldo:,}")
        return True


class AdminUser(BaseUser):
    def __init__(self, nama, password, saldo_awal=0):
        super().__init__(nama, password, saldo_awal)
        self.jabatan = "Pengelola Toko"

    def tampilkan_peran(self):
        print(f"Admin | Jabatan: {self.jabatan}")

    def akses_menu(self):
        print("\n== MENU ADMIN ==")
        print("1. Tambah Produk\n2. Lihat Semua Produk\n3. Edit Harga Produk")
        print("4. Hapus Produk\n5. Lihat Semua User\n6. Info Toko\n7. Laporan Transaksi\n8. Logout")

    def hapus_produk(self, marketplace):
        produk = marketplace.pilih_produk("Nomor produk dihapus: ")
        if produk != None:
            marketplace.daftar_produk.remove(produk)
            print(f"Admin {self.nama} menghapus produk: {produk.nama}")

    def menu_khusus(self, marketplace):
        pilih = input("Pilih menu: ")

        if pilih == "1":
            nama = input("Nama Produk: ")
            kategori = input("Kategori: ")
            harga = marketplace.input_angka("Harga: ")
            stok = marketplace.input_angka("Stok: ")
            
            produk_baru = Produk(nama, kategori, harga, stok)
            marketplace.tambah_produk_ke_sistem(produk_baru)
            print("Produk ditambah ke sistem!")
            
        elif pilih == "2":
            marketplace.tampilkan_produk()
            
        elif pilih == "3":
            produk = marketplace.pilih_produk()
            if produk != None:
                try:
                    harga_baru = marketplace.input_angka("Harga baru: ")
                    produk.harga = harga_baru
                    print("Harga berhasil diubah!")
                except ValueError as error:
                    print(f"Gagal: {error}")
                    
        elif pilih == "4":
            self.hapus_produk(marketplace)
            
        elif pilih == "5":
            for user in marketplace.daftar_user:
                print(f"- {user.nama}: ", end="")
                user.tampilkan_peran()
                
        elif pilih == "6":
            marketplace.info()
            
        elif pilih == "7":
            laporan = LaporanKeuangan(marketplace.total_transaksi)
            sampaikan_info(laporan)
            
        elif pilih == "8":
            return False
            
        else:
            print("Pilihan salah!")

        return True


class MemberUser(BaseUser):
    def __init__(self, nama, password, saldo_awal, diskon_persen):
        super().__init__(nama, password, saldo_awal)
        
        if diskon_persen < 0:
            self.diskon_persen = 0
        elif diskon_persen > 50:
            self.diskon_persen = 50
        else:
            self.diskon_persen = diskon_persen

    def tampilkan_peran(self):
        print(f"Member | Diskon: {self.diskon_persen}%")

    def akses_menu(self):
        print("\n== MENU MEMBER ==")
        print("1. Lihat Produk\n2. Beli Produk (Dapat Diskon!)\n3. Isi Saldo\n4. Profil Saya\n5. Logout")

    def menu_khusus(self, marketplace):
        pilih = input("Pilih menu: ")

        if pilih == "1":
            marketplace.tampilkan_produk()
            
        elif pilih == "2":
            produk = marketplace.pilih_produk()
            if produk != None:
                jumlah = marketplace.input_angka("Jumlah: ", 1)
                self.beli(produk, jumlah, self.diskon_persen)
                
        elif pilih == "3":
            nominal = marketplace.input_angka("Nominal topup: ")
            self._saldo = self._saldo + nominal
            print(f"Saldo bertambah Rp{nominal:,}")
            
        elif pilih == "4":
            self.profil()
            self.tampilkan_peran()
            
        elif pilih == "5":
            return False
            
        else:
            print("Pilihan salah!")

        return True


class LaporanKeuangan:
    def __init__(self, jumlah_transaksi):
        self.jumlah_transaksi = jumlah_transaksi

    def cetak_info(self):
        print(f"Laporan: {self.jumlah_transaksi} transaksi sukses tercatat.")


class NotifikasiSistem:
    def __init__(self, pesan):
        self.pesan = pesan

    def cetak_info(self):
        print(f"Notifikasi: {self.pesan}")


def sampaikan_info(sumber):
    sumber.cetak_info()


def bersihkan_layar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def cari_user(daftar, nama):
    for user in daftar:
        if user.nama.lower() == nama.lower():
            return user
    return None


def demo_oop():
    try:
        akun_abstrak = BaseUser("contoh", "rahasia", 0)
    except TypeError:
        print("BaseUser abstrak dan tidak dapat dibuat: Tidak bisa membuat objek dari kelas abstrak BaseUser karena method 'akses_menu', 'menu_khusus', dan 'tampilkan_peran' belum dibuat implementasinya.")

    pengguna = []
    admin_demo = AdminUser("admin-demo", "x")
    member_demo = MemberUser("member-demo", "x", 0, 10)
    
    pengguna.append(admin_demo)
    pengguna.append(member_demo)
    
    for user in pengguna:
        user.tampilkan_peran()

    laporan_awal = LaporanKeuangan(0)
    sampaikan_info(laporan_awal)
    
    notif = NotifikasiSistem("Sistem siap digunakan.")
    sampaikan_info(notif)
    
    produk_contoh = Produk('Pakan Ikan', 'Pakan', 25000, 4)
    print(f"Contoh __str__: {produk_contoh}")

    input("\nTekan Enter untuk lanjut ke marketplace...")


def jalankan_marketplace():
    sistem = Marketplace("Samarinda")
    
    produk1 = Produk("Ikan Koi Kohaku", "Ikan Hias", 150000, 10)
    produk2 = Produk("Akuarium Minimalis 40cm", "Akuarium", 250000, 5)
    sistem.tambah_produk_ke_sistem(produk1)
    sistem.tambah_produk_ke_sistem(produk2)
    
    admin_utama = AdminUser("admin", "admin123")
    member_utama = MemberUser("alia", "015", 1900000, 10)
    sistem.tambah_user_ke_sistem(admin_utama)
    sistem.tambah_user_ke_sistem(member_utama)
    
    pengguna_aktif = None

    while True:
        bersihkan_layar()
        print("=" * 50)
        print(f"   {Marketplace.nama_toko.upper()}")
        print("=" * 50)

        if pengguna_aktif == None:
            print("\n1. Login\n2. Register Member\n3. Keluar")
            pilih = input("Pilih menu: ")

            if pilih == "1":
                nama = input("Username: ")
                password = input("Password: ")
                user = cari_user(sistem.daftar_user, nama)

                if user != None and user.cek_password(password) == True:
                    pengguna_aktif = user
                    print("Login berhasil!")
                    user.tampilkan_peran()
                else:
                    print("Nama atau password salah!")

                input("\nTekan Enter...")
                
            elif pilih == "2":
                nama = input("Nama: ")
                user_ditemukan = cari_user(sistem.daftar_user, nama)

                if user_ditemukan != None:
                    print("Nama sudah ada!")
                else:
                    password = input("Password: ")
                    saldo = sistem.input_angka("Saldo Awal: ")
                    diskon = sistem.input_angka("Persen Diskon (0-50): ")
                    
                    user_baru = MemberUser(nama, password, saldo, diskon)
                    sistem.tambah_user_ke_sistem(user_baru)
                    print("Registrasi Member Berhasil!")

                input("\nTekan Enter...")
                
            elif pilih == "3":
                break
                
            else:
                print("Pilihan salah!")
                input("\nTekan Enter...")

            continue

        pengguna_aktif.akses_menu()
        lanjut = pengguna_aktif.menu_khusus(sistem)
        
        if lanjut == False:
            pengguna_aktif = None
        else:
            input("\nTekan Enter...")

    print("\nTerima kasih telah menggunakan Altria Aquatics Marketplace!")


if __name__ == "__main__":
    demo_oop()
    jalankan_marketplace()
    