# Altria Aquatics Marketplace
Program Python berbasis **Object-Oriented Programming (OOP)** yang mensimulasikan sistem marketplace untuk penjualan ikan hias dan akuarium. Program ini dikembangkan untuk memenuhi persyaratan tugas pemrograman yang mencakup materi **Class & Object**, **Atribut & Method**, **Encapsulation & Property**, **UML Class Relationships**, serta **Inheritance**.

---

## Kelas & Atribut
Program ini dibangun menggunakan 6 kelas utama (`RiwayatMutasi`, `Marketplace`, `Produk`, `User`, `AdminUser`, dan `MemberUser`) yang saling berinteraksi melalui berbagai relasi OOP. Berikut adalah rincian dari masing-masing komponen:

### 1. Kelas `RiwayatMutasi` (Class Pendukung Komposisi)
Kelas ini merepresentasikan catatan mutasi stok yang menjadi bagian dari objek `Produk`.
* **Atribut Instance:**
  * `tipe`: Jenis mutasi (`"Masuk"` atau `"Keluar"`).
  * `jumlah`: Banyaknya unit yang masuk/keluar.
  * `keterangan`: Deskripsi peristiwa mutasi (misal: `"Stok awal sistem"`, `"Dibeli oleh alia"`).
* **Metode Utama:**
  * `tampilkan_log(self)`: Mengembalikan representasi teks dari mutasi dengan simbol `+` atau `-` sesuai jenisnya.

### 2. Kelas `Marketplace` (Wadah Sistem - Agregasi)
Kelas ini merepresentasikan entitas toko secara global, menangani data bersama (*shared data*), serta menjadi penampung (*aggregator*) bagi seluruh produk dan user.
* **Atribut Kelas (Class Attributes):**
  * `nama_toko = "Altria Aquatics Marketplace"`: Nama resmi marketplace yang bersifat global.
  * `total_transaksi = 0`: Variabel penghitung global yang bertambah setiap kali transaksi berhasil.
  * `mata_uang = "IDR"`: Standar mata uang transaksi.
* **Atribut Instance (Agregasi):**
  * `wilayah`: Lokasi cabang toko.
  * `daftar_produk`: List yang menampung objek `Produk` (relasi agregasi).
  * `daftar_user`: List yang menampung objek `User` dan subclass-nya (relasi agregasi).
* **Metode Utama:**
  * `input_angka(pesan)`: **Static Method** (`@staticmethod`) yang berfungsi sebagai pengaman input menggunakan `try-except` dan `while True`.
  * `tambah_statistik(cls)`: **Class Method** (`@classmethod`) yang memodifikasi atribut kelas `total_transaksi`.
  * `info(self)`: **Instance Method** untuk mencetak informasi detail toko.
  * `tambah_produk_ke_sistem(self, produk)` & `tambah_user_ke_sistem(self, user)`: Metode untuk menambahkan objek ke dalam list agregasi.

### 3. Kelas `Produk` (Dengan Komposisi)
Kelas ini mengatur entitas barang yang dijual beserta aturan bisnis terkait harga dan stok.
* **Atribut Instance:**
  * `nama`, `kategori`: Atribut publik.
  * `__harga`: Atribut **private** yang dilindungi ketat.
  * `_stok`: Atribut **protected** (dapat diakses subclass jika diperlukan).
  * `log_stok`: List yang menampung objek `RiwayatMutasi` (**relasi komposisi** — objek ini dibuat di dalam `Produk` dan ikut musnah jika `Produk` dihapus).
* **Property & Setter:**
  * `@property harga` & `@harga.setter`: Validasi harga tidak boleh negatif (`raise ValueError`).
  * `@property stok`: Getter untuk atribut protected `_stok`.
* **Metode Utama:**
  * `_catat_mutasi(self, tipe, jumlah, keterangan)`: Membuat objek `RiwayatMutasi` baru dan menambahkannya ke `log_stok` (implementasi komposisi).
  * `kurangi_stok(self, jumlah, pembeli)`: Mengurangi stok sekaligus mencatat mutasi keluar.
  * `tampil(self)`: Mencetak informasi produk beserta status stok.

### 4. Kelas `User` (Superclass / Parent Class)
Kelas induk yang mendefinisikan atribut dan perilaku dasar semua pengguna sistem.
* **Atribut Instance:**
  * `nama`, `role`: Atribut publik.
  * `__password`: Atribut **private** — benar-benar rahasia, bahkan subclass tidak bisa mengaksesnya langsung.
  * `_saldo`: Atribut **protected** — dapat diakses dan dimanipulasi langsung oleh subclass (`AdminUser`, `MemberUser`).
* **Property & Metode:**
  * `@property saldo`: Getter untuk `_saldo`.
  * `cek_password(self, input_pass)`: Memverifikasi password tanpa mengekspos nilai aslinya.
  * `profil(self)`: Menampilkan identitas akun.
  * `beli(self, produk, jumlah)`: Logika pembelian standar (tanpa diskon).

### 5. Kelas `AdminUser` (Subclass - Inheritance)
Subclass turunan dari `User` yang mewakili administrator sistem.
* **Konstruktor:** Memanggil `super().__init__(...)` untuk mewarisi atribut induk, lalu menambahkan atribut unik `jabatan = "Pengelola Toko"`.
* **Metode Khusus:**
  * `hapus_produk(self, daftar_produk, index)`: Fitur eksklusif admin untuk menghapus produk dari katalog.

### 6. Kelas `MemberUser` (Subclass - Inheritance + Overriding)
Subclass turunan dari `User` yang mewakili member dengan hak istimewa berupa diskon.
* **Konstruktor:** Memanggil `super().__init__(...)` lalu menambahkan atribut unik `diskon_persen`.
* **Method Overriding:**
  * `beli(self, produk, jumlah)`: **Mendefinisikan ulang** method `beli()` dari superclass dengan logika tambahan perhitungan diskon sebelum memotong saldo.

---

## Relasi UML yang Diterapkan

Program ini mengimplementasikan keempat jenis relasi OOP sesuai materi Modul 4 dan Modul 5:

| Jenis Relasi | Kata Kunci | Implementasi di Program |
|--------------|------------|-------------------------|
| **Asosiasi** | "Menggunakan" | Objek `User` **menggunakan** objek `Produk` saat memanggil method `beli(produk, jumlah)` — objek `Produk` diterima sebagai parameter, tidak disimpan permanen. |
| **Agregasi** | "Memiliki" | `Marketplace` **memiliki** `daftar_produk` dan `daftar_user`. Objek `Produk` dan `User` dibuat di luar lalu dimasukkan lewat method `tambah_produk_ke_sistem()` / `tambah_user_ke_sistem()`. Jika `Marketplace` dihapus, objek produk/user tetap ada. |
| **Komposisi** | "Terdiri dari" | `Produk` **terdiri dari** `RiwayatMutasi`. Objek `RiwayatMutasi` dibuat di dalam `Produk` lewat `_catat_mutasi()` dan tidak memiliki arti jika dipisahkan dari `Produk`. |
| **Inheritance** | "Adalah jenis dari" | `AdminUser` **adalah jenis dari** `User`. `MemberUser` **adalah jenis dari** `User`. Keduanya mewarisi atribut dan method superclass melalui `super().__init__()`. |

---

## Inheritance (Pewarisan)

Program menerapkan konsep **Hierarchical Inheritance** di mana satu superclass (`User`) diwarisi oleh dua subclass (`AdminUser`, `MemberUser`).

### Ciri Inheritance yang Diterapkan:
1. **Penggunaan `super().__init__()`** — Kedua subclass memanggil konstruktor superclass untuk menginisialisasi atribut warisan (`nama`, `__password`, `_saldo`, `role`).
2. **Atribut Unik Subclass**:
   * `AdminUser` → `jabatan`
   * `MemberUser` → `diskon_persen`
3. **Method Overriding** — Method `beli()` di `MemberUser` didefinisikan ulang dengan logika diskon, berbeda dari versi superclass.
4. **Tingkat Akses**:
   * `_saldo` (protected) → boleh diakses subclass untuk manipulasi langsung.
   * `__password` (private) → tetap rahasia, hanya bisa diakses lewat method `cek_password()`.
5. **Pengecekan Tipe** — Menggunakan `isinstance(user, AdminUser)` dan `isinstance(user, MemberUser)` untuk membedakan perilaku saat login dan menampilkan menu.

---

## Alur Program
Alur program **Altria Aquatics Marketplace** dimulai dengan proses inisialisasi sistem: sebuah objek `Marketplace` dibuat sebagai wadah agregasi, kemudian objek-objek `Produk` awal serta akun `AdminUser` dan `MemberUser` bawaan didaftarkan ke dalam sistem. 

Setelah itu, program memasuki loop utama yang secara berkala membersihkan layar konsol dan menampilkan menu berdasarkan status sesi. Ketika belum ada pengguna yang masuk, sistem menampilkan tiga pilihan: **Login**, **Register Member Baru**, dan **Keluar**. 

* **Login**: Sistem memverifikasi username dan password, lalu menggunakan `isinstance()` untuk mendeteksi apakah pengguna adalah `AdminUser` atau `MemberUser`, sehingga menampilkan menu yang sesuai.
* **Register Member Baru**: Hanya menghasilkan objek `MemberUser` (tidak bisa jadi admin). User baru langsung mendapat atribut diskon yang diinput sendiri.

Setelah berhasil masuk, menu dan hak akses disesuaikan dengan peran masing-masing. **Admin** memiliki wewenang penuh atas katalog produk dan daftar user, sedangkan **Member** dapat berbelanja dengan keuntungan diskon otomatis.

---

## Rincian Fitur Program
### Fitur Menu Admin (Khusus `AdminUser`)
1. **Tambah Produk** — Menambah produk baru ke sistem agregasi dengan validasi harga & stok.
2. **Lihat Semua Produk** — Menampilkan katalog lengkap.
3. **Edit Harga Produk** — Memperbarui harga produk. Fitur ini secara langsung mendemonstrasikan validasi **Setter** (jika admin memasukkan angka negatif, sistem akan menolak dan memunculkan pesan *error* `ValueError`).
4. **Hapus Produk** — Mengeluarkan produk dari katalog lewat method khusus subclass.
5. **Lihat Semua User** — Menampilkan daftar seluruh pengguna (admin & member).
6. **Info Toko** — Menampilkan informasi sistem termasuk total transaksi.
7. **Logout** — Kembali ke menu utama.

### Fitur Menu Member (Khusus `MemberUser`)
1. **Lihat Produk** — Menjelajahi katalog.
2. **Beli Produk (Dapat Diskon!)** — Transaksi dengan perhitungan diskon otomatis (*method overriding*).
3. **Isi Saldo** — Top-up saldo dengan akses langsung ke atribut protected `_saldo`.
4. **Profil Saya** — Menampilkan identitas dan diskon pribadi.
5. **Logout** — Kembali ke menu utama.

---