# Altria Aquatics Marketplace

## Deskripsi

**Altria Aquatics Marketplace** adalah program marketplace sederhana berbasis Python dengan pendekatan **Object-Oriented Programming (OOP)**. Program ini mengangkat tema **marketplace ikan hias dan perlengkapan akuarium**.

Program dibuat untuk menerapkan materi dari tiga modul pembelajaran, yaitu:
- **Modul 1:** Class & Object
- **Modul 2:** Atribut & Method
- **Modul 3:** Encapsulation & Property

Selain menyediakan fitur marketplace untuk Admin dan User, program juga memiliki menu **Pengujian Program** untuk mendemonstrasikan penerapan class, object, method, property, dan validasi data.

---

## Tema

**Sistem Marketplace Ikan Hias dan Perlengkapan Akuarium**

Nama marketplace:

> **Altria Aquatics Marketplace**

---

## Class Utama

Program memiliki 3 class utama:

### 1. Marketplace

Class `Marketplace` digunakan untuk menyimpan informasi umum marketplace.

**Atribut kelas:**
- `nama_toko`
- `total_produk`
- `mata_uang`

**Atribut instance:**
- `wilayah`

**Method:**
- `info()`
- `tambah_produk()` — Class Method
- `input_angka()` — Static Method

### 2. Produk

Class `Produk` digunakan untuk menyimpan informasi produk yang dijual.

**Atribut public:**
- `nama`
- `kategori`

**Atribut private:**
- `__harga`
- `__stok`

**Property:**
- `harga`
- `stok`

**Method:**
- `tampilan()`
- `kurangi_stok()`

### 3. User

Class `User` digunakan untuk menyimpan informasi pengguna marketplace.

**Atribut public:**
- `nama`
- `role`

**Atribut private:**
- `__password`
- `__saldo`

**Property:**
- `saldo`

**Method:**
- `cek_password()`
- `profil()`
- `beli()`

---