#  Altria Aquatics Marketplace

##  Kelas & Atribut

Program ini dibangun menggunakan 3 kelas utama (`Marketplace`, `Produk`, dan `User`) serta fungsi bantu pendukung. Berikut adalah rincian dari masing-masing komponen:

### 1. Kelas `Marketplace`
Kelas ini merepresentasikan entitas toko secara global, menangani data bersama (*shared data*), serta menyediakan fungsi utilitas sistem.
* **Atribut Kelas (Class Attributes):**
  * `nama_toko = "Altria Aquatics Marketplace"`: Nama resmi marketplace yang bersifat global untuk semua objek.
  * `total_produk = 0`: Variabel penghitung (*counter*) global yang otomatis bertambah setiap kali objek dari kelas `Produk` diinisialisasi.
  * `mata_uang = "IDR"`: Standar mata uang yang digunakan dalam transaksi.
* **Atribut Instance:**
  * `wilayah`: Menyimpan lokasi cabang toko (contoh: `"Samarinda"`, `"Balikpapan"`, `"Tarakan"`).
* **Metode Utama:**
  * `__init__(self, wilayah)`: Konstruktor untuk menginisialisasi wilayah cabang toko saat objek dibuat.
  * `tambah_produk(cls, jumlah=1)`: **Class Method** (`@classmethod`) yang memodifikasi atribut kelas `total_produk` secara langsung menggunakan parameter `cls`.
  * `input_angka(pesan)`: **Static Method** (`@staticmethod`) yang berfungsi sebagai pengaman input. Metode ini menggunakan blok `while True`, `try-except`, dan validasi `ValueError` untuk memastikan user hanya menginput angka bulat positif, mencegah program *crash* jika user memasukkan huruf atau nilai negatif.
  * `info(self)`: **Instance Method** untuk mencetak informasi detail mengenai toko (nama toko, wilayah, mata uang, dan total produk saat ini).

### 2. Kelas `Produk`
Kelas ini mengatur entitas barang yang dijual di dalam marketplace beserta aturan bisnis terkait harga dan ketersediaan stok.
* **Atribut Instance (Encapsulated):**
  * `nama`: Nama produk (akses publik).
  * `kategori`: Kategori produk, seperti *Ikan Hias* atau *Aksesoris* (akses publik).
  * `__harga`: Harga satuan produk yang dilindungi secara privasi (*private attribute*).
  * `__stok`: Jumlah ketersediaan stok produk yang juga dilindungi secara privasi (*private attribute*).
* **Property & Setter (Encapsulation Control):**
  * `@property harga` & `@harga.setter`: Memungkinkan akses ke variabel `__harga` layaknya atribut biasa, namun dilengkapi validasi ketat di dalam setter agar nilai harga tidak boleh negatif (`ValueError`).
  * `@property stok` & `@stok.setter`: Mengamankan variabel `__stok` dengan validasi tipe data (`isinstance`) dan memastikan nilai stok berupa angka bulat positif.
* **Metode Utama:**
  * `__init__(...)`: Menginisialisasi data produk sekaligus memanggil `Marketplace.tambah_produk()` agar penghitung produk otomatis bertambah.
  * `tampilan(self)`: Mencetak informasi ringkas produk beserta status ketersediaan stok secara dinamis (`"Ada"` jika stok > 0, atau `"Habis"` jika stok = 0).
  * `kurangi_stok(self, jumlah)`: Mengurangi stok berdasarkan jumlah pembelian, menghitung total biaya, serta mengembalikan total harga jika transaksi valid.

### 3. Kelas `User`
Kelas ini merepresentasikan pengguna sistem, baik sebagai pelanggan umum maupun administrator.
* **Atribut Instance (Encapsulated):**
  * `nama`: Nama pengguna / username.
  * `__password`: Kata sandi pengguna yang disembunyikan menggunakan enkapsulasi private (`__`).
  * `__saldo`: Saldo digital pengguna yang dilindungi untuk mencegah manipulasi langsung.
  * `role`: Hak akses pengguna (bernilai `"user"` atau `"admin"`).
* **Property & Setter:**
  * `@property saldo` & `@saldo.setter`: Mengontrol penambahan saldo (fitur top-up). Setter memvalidasi agar nilai top-up tidak negatif dan secara otomatis menambahkan nominal ke saldo lama.
* **Metode Utama:**
  * `cek_password(self, password_input)`: Memverifikasi kesesuaian sandi saat proses autentikasi login.
  * `profil(self)`: Menampilkan informasi detail mengenai profil akun yang sedang aktif.
  * `beli(self, produk, jumlah)`: Mengatur logika bisnis pembelian. Memeriksa apakah saldo user mencukupi total biaya pembelian, memanggil fungsi pengurangan stok pada produk, mengurangi saldo user, dan mencetak sisa saldo terkini.

---

##  Alur Program

Alur program **Altria Aquatics Marketplace** dimulai dengan proses inisialisasi data default, di mana sistem secara otomatis mempersiapkan objek toko, daftar produk awal, serta akun bawaan untuk admin dan pengguna. Setelah itu, program memasuki loop utama berkelanjutan yang secara berkala membersihkan layar konsol dan menampilkan menu antarmuka berdasarkan status sesi aktif (*pengguna_aktif*). 

Ketika belum ada pengguna yang masuk (*status login null*), sistem menyajikan empat opsi menu utama: **Login**, **Register**, **Keluar**, dan **Pengujian Program**. Pada menu Login, sistem akan memverifikasi kredensial input dan mengarahkan pengguna ke dashboard admin jika memasukkan akun khusus, atau ke dashboard user biasa apabila data cocok dengan daftar yang tersimpan. Menu Register memungkinkan pengguna baru untuk mendaftarkan akun dengan memasukkan nama, password, dan saldo awal yang divalidasi keamanannya agar tidak terjadi duplikasi dengan nama admin. Sementara itu, opsi pengujian menjalankan demonstrasi kode OOP secara menyeluruh, dan opsi keluar akan menghentikan eksekusi program.

Setelah berhasil masuk ke dalam sistem, menu dan hak akses akan disesuaikan secara otomatis dengan peran (*role*) masing-masing pengguna. Jika masuk sebagai **Admin**, pengguna memiliki wewenang penuh untuk menambah produk baru ke katalog, melihat daftar seluruh produk dan user beserta saldonya, memperbarui harga produk menggunakan *setter* bervalidasi, menghapus produk tertentu melalui fungsi manipulasi list, hingga mengakhiri sesi lewat menu *logout*. Sebaliknya, jika masuk sebagai **User**, pengguna dapat menjelajahi katalog produk, melakukan transaksi pembelian yang divalidasi langsung dengan ketersediaan stok dan besaran saldo, melakukan isi ulang (*top-up*) saldo, melihat detail profil pribadi, maupun kembali melakukan *logout* untuk mengembalikan status aplikasi ke menu awal.

---

##  Rincian Fitur Program

###  Fitur Menu Admin
Menu khusus ini hanya dapat diakses setelah login menggunakan admin. Admin memiliki kendali penuh terhadap manajemen sistem:
1. **Tambah Produk Baru:** Memasukkan produk baru ke katalog dengan validasi harga dan stok agar terhindar dari input negatif serta otomatis memperbarui *total_produk* toko.
2. **Lihat Semua Produk:** Menampilkan daftar seluruh item lengkap dengan kategori, harga, sisa stok, dan status ketersediaan (*Ada* atau *Habis*).
3. **Edit Harga Produk:** Memperbarui harga produk yang ada di katalog menggunakan *setter* bervalidasi.
4. **Hapus Produk:** Mengeluarkan suatu produk dari daftar katalog marketplace menggunakan indeks list.
5. **Lihat Semua User:** Menampilkan daftar seluruh akun pelanggan yang terdaftar beserta informasi saldo digital mereka.
6. **Logout:** Mengakhiri sesi aktif administrator dan kembali ke menu utama.

###  Fitur Menu User (Pelanggan / Pengguna Umum)
Menu ini aktif ketika pengguna melakukan login menggunakan akun user:
1. **Lihat Produk:** Menjelajahi katalog lengkap produk ikan hias dan perlengkapan akuatik beserta informasi harganya.
2. **Beli Produk:** Melakukan transaksi pembelian dengan sistem validasi otomatis terhadap ketersediaan stok dan besaran saldo digital pengguna.
3. **Isi Saldo / Top-Up:** Menambah saldo akun digital dengan validasi nominal agar tidak bernilai negatif.
4. **Profil Saya:** Menampilkan informasi ringkas mengenai identitas akun, hak akses (*USER*), dan sisa saldo terkini.
5. **Logout:** Mengakhiri sesi masuk pengguna saat ini dan mengembalikan aplikasi ke tampilan menu awal.

---