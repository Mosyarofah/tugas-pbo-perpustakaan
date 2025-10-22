# 🏫 Sistem Perpustakaan (GUI + MySQL)

Aplikasi **Sistem Perpustakaan** ini dibuat menggunakan **Python (Tkinter)** untuk antarmuka grafis (GUI) dan **MySQL** sebagai database backend.
Program ini memiliki fitur login, dashboard, manajemen buku, serta manajemen anggota.

---

## 📌 Fitur Utama

### 1. Login
- Validasi username dan password dari tabel `users`.
- Hanya user yang terdaftar yang dapat masuk ke sistem.

### 2. Dashboard
- Menampilkan jumlah total buku dan anggota.
- Tombol navigasi menuju **Manajemen Buku** dan **Manajemen Anggota**.
- Tombol Logout untuk keluar dari aplikasi.

### 3. Manajemen Buku
- Tambah, ubah, hapus, dan cari data buku.
- Validasi input seperti tahun terbit dan stok harus angka.
- Data ditampilkan menggunakan tabel Treeview.

### 4. Manajemen Anggota
- Tambah, ubah, hapus, dan tampilkan data anggota.
- Validasi nomor telepon dan email.
- Tampilan tabel anggota dengan Treeview.

---

## 🗄️ Struktur Database

### Database: `perpustakaan_db`

#### Tabel `users`
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin'
);
```

#### Tabel `buku`
```sql
CREATE TABLE buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_buku VARCHAR(20) UNIQUE,
    judul VARCHAR(200),
    pengarang VARCHAR(100),
    penerbit VARCHAR(100),
    tahun_terbit INT,
    stok INT
);
```

#### Tabel `anggota`
```sql
CREATE TABLE anggota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_anggota VARCHAR(20) UNIQUE,
    nama VARCHAR(100),
    alamat TEXT,
    telepon VARCHAR(20),
    email VARCHAR(100)
);
```

---

## 📚 Contoh Data Awal

### User Login
```sql
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
```

### Data Buku
```sql
INSERT INTO buku (kode_buku, judul, pengarang, penerbit, tahun_terbit, stok) VALUES
('BK001', 'Algoritma dan Pemrograman', 'Andi Setiawan', 'Informatika Press', 2022, 10),
('BK002', 'Struktur Data dalam Python', 'Dewi Lestari', 'Gramedia', 2021, 7);
```

### Data Anggota
```sql
INSERT INTO anggota (kode_anggota, nama, alamat, telepon, email) VALUES
('A01', 'Mosyarofah', 'Jl. Melati No.12', '08123456789', 'budi@gmail.com'),



---

## ⚙️ Cara Menjalankan

1. **Pastikan Python dan MySQL sudah terinstal.**
2. Buat database dengan nama `perpustakaan_db`.
3. Jalankan query SQL di atas untuk membuat tabel.
4. Pastikan Anda mengatur koneksi di fungsi `get_connection()` sesuai konfigurasi lokal Anda.
5. Jalankan program dengan perintah:
   ```bash
   python perpustakaan_db.py
   ```

---

## 🧩 Modul yang Digunakan
- `tkinter` — GUI utama
- `mysql.connector` — koneksi database
- `re` — validasi pola (regex)
- `ttk` — tampilan tabel modern

---

## 👨‍💻 Pengembang
Dibuat oleh: **Aplikasi Edukasi Sistem Perpustakaan**
