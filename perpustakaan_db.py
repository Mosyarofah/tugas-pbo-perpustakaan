import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import re

# ===== KONEKSI DATABASE =====
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="perpustakaan_db"
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return None


# ====== LOGIN WINDOW ======
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Sistem Perpustakaan")
        self.root.geometry("350x250")
        self.root.config(bg="#e8f0fe")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Sistem Perpustakaan", font=("Helvetica", 16, "bold"), bg="#e8f0fe", fg="#1a73e8").pack(pady=10)
        tk.Label(self.root, text="Masuk ke akun Anda", font=("Arial", 10), bg="#e8f0fe").pack(pady=5)

        frame = tk.Frame(self.root, bg="#e8f0fe")
        frame.pack(pady=10)

        tk.Label(frame, text="Username", bg="#e8f0fe").grid(row=0, column=0, sticky="w", pady=5)
        self.username = tk.Entry(frame, width=25)
        self.username.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password", bg="#e8f0fe").grid(row=1, column=0, sticky="w", pady=5)
        self.password = tk.Entry(frame, width=25, show="*")
        self.password.grid(row=1, column=1, pady=5)

        tk.Button(self.root, text="Login", command=self.login, bg="#1a73e8", fg="white", width=15, font=("Arial", 10, "bold")).pack(pady=15)

        self.root.mainloop()

    def login(self):
        user = self.username.get()
        pw = self.password.get()

        if not user or not pw:
            messagebox.showwarning("Validasi", "Semua field wajib diisi!")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
            result = cursor.fetchone()
            conn.close()

            if result:
                messagebox.showinfo("Login Berhasil", f"Selamat datang, {result['username']}")
                self.root.destroy()
                Dashboard(result)
            else:
                messagebox.showerror("Gagal", "Username atau password salah!")


# ====== DASHBOARD WINDOW ======
class Dashboard:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Dashboard - Sistem Perpustakaan")
        self.root.geometry("600x400")
        self.root.config(bg="#f1f3f4")

        tk.Label(self.root, text="📚 Dashboard Sistem Perpustakaan", font=("Helvetica", 16, "bold"), bg="#f1f3f4", fg="#1a73e8").pack(pady=10)
        tk.Label(self.root, text=f"Selamat Datang, {user['username']} ({user['role']})", bg="#f1f3f4", font=("Arial", 11)).pack(pady=5)

        frame = tk.Frame(self.root, bg="#f1f3f4")
        frame.pack(pady=20)

        tk.Button(frame, text="Manajemen Buku", width=20, command=self.open_buku, bg="#34a853", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frame, text="Manajemen Anggota", width=20, command=self.open_anggota, bg="#fbbc04", fg="black", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frame, text="Logout", width=20, command=self.logout, bg="#ea4335", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=8)

        self.label_stats = tk.Label(self.root, text="", font=("Arial", 11), bg="#f1f3f4", fg="#333")
        self.label_stats.pack(pady=20)
        self.update_stats()

        self.root.mainloop()

    def update_stats(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM buku")
            buku = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM anggota")
            anggota = cursor.fetchone()[0]
            conn.close()
            self.label_stats.config(text=f"Total Buku: {buku} | Total Anggota: {anggota}")

    def open_buku(self):
        self.root.destroy()
        BukuWindow(self.user)

    def open_anggota(self):
        self.root.destroy()
        AnggotaWindow(self.user)

    def logout(self):
        self.root.destroy()
        LoginWindow()


# ====== MANAJEMEN BUKU ======
class BukuWindow:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Manajemen Buku")
        self.root.geometry("850x550")
        self.root.config(bg="#ffffff")

        tk.Label(self.root, text="📖 Manajemen Buku", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1a73e8").pack(pady=10)

        frame_input = tk.Frame(self.root, bg="#ffffff")
        frame_input.pack(pady=5)

        labels = ["Kode Buku", "Judul", "Pengarang", "Penerbit", "Tahun Terbit", "Stok"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame_input, text=label, bg="#ffffff").grid(row=i, column=0, sticky="w", pady=3)
            entry = tk.Entry(frame_input, width=35)
            entry.grid(row=i, column=1, pady=3)
            self.entries[label] = entry

        frame_btn = tk.Frame(self.root, bg="#ffffff")
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Simpan", command=self.simpan, bg="#34a853", fg="white", width=10).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Update", command=self.update, bg="#fbbc04", fg="black", width=10).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Hapus", command=self.hapus, bg="#ea4335", fg="white", width=10).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Kembali", command=self.kembali, bg="#1a73e8", fg="white", width=10).grid(row=0, column=3, padx=5)

        frame_search = tk.Frame(self.root, bg="#ffffff")
        frame_search.pack(pady=10)
        tk.Label(frame_search, text="Cari Buku:", bg="#ffffff").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(frame_search, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_search, text="Cari", command=self.cari, bg="#1a73e8", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_search, text="Tampilkan Semua", command=self.load_data, bg="#9aa0a6", fg="white").pack(side=tk.LEFT, padx=5)

        # === Tabel Buku ===
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        self.tree = ttk.Treeview(self.root, columns=("kode", "judul", "pengarang", "penerbit", "tahun", "stok"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, pady=10)

        self.load_data()
        self.root.mainloop()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok FROM buku")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()

    def cari(self):
        keyword = self.search_entry.get().strip()
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            if keyword == "":
                cursor.execute("SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok FROM buku")
            else:
                cursor.execute("""SELECT kode_buku, judul, pengarang, penerbit, tahun_terbit, stok 
                                  FROM buku WHERE judul LIKE %s OR pengarang LIKE %s""",
                               (f"%{keyword}%", f"%{keyword}%"))
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()

    def simpan(self):
        data = {k: e.get() for k, e in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Validasi", "Semua field harus diisi!")
            return
        if not data["Tahun Terbit"].isdigit() or not data["Stok"].isdigit():
            messagebox.showerror("Validasi", "Tahun dan Stok harus angka!")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO buku (kode_buku, judul, pengarang, penerbit, tahun_terbit, stok) VALUES (%s,%s,%s,%s,%s,%s)",
                    tuple(data.values()))
                conn.commit()
                messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
                self.load_data()
            except Error as e:
                messagebox.showerror("Error", str(e))
            conn.close()

    def update(self):
        kode = self.entries["Kode Buku"].get()
        if not kode:
            messagebox.showwarning("Validasi", "Masukkan kode buku yang akan diupdate!")
            return
        data = {k: e.get() for k, e in self.entries.items()}
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE buku SET judul=%s, pengarang=%s, penerbit=%s, tahun_terbit=%s, stok=%s WHERE kode_buku=%s""",
                           (data["Judul"], data["Pengarang"], data["Penerbit"], data["Tahun Terbit"], data["Stok"], kode))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data buku berhasil diupdate!")
            self.load_data()

    def hapus(self):
        kode = self.entries["Kode Buku"].get()
        if not kode:
            messagebox.showwarning("Validasi", "Masukkan kode buku yang akan dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus buku {kode}?"):
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM buku WHERE kode_buku=%s", (kode,))
                conn.commit()
                conn.close()
                self.load_data()

    def kembali(self):
        self.root.destroy()
        Dashboard(self.user)


# ====== MANAJEMEN ANGGOTA ======
class AnggotaWindow:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Manajemen Anggota")
        self.root.geometry("850x550")
        self.root.config(bg="#ffffff")

        tk.Label(self.root, text="👥 Manajemen Anggota", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1a73e8").pack(pady=10)

        frame_input = tk.Frame(self.root, bg="#ffffff")
        frame_input.pack(pady=5)

        labels = ["Kode Anggota", "Nama", "Alamat", "Telepon", "Email"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame_input, text=label, bg="#ffffff").grid(row=i, column=0, sticky="w", pady=3)
            entry = tk.Entry(frame_input, width=35)
            entry.grid(row=i, column=1, pady=3)
            self.entries[label] = entry

        frame_btn = tk.Frame(self.root, bg="#ffffff")
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Simpan", command=self.simpan, bg="#34a853", fg="white", width=10).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Update", command=self.update, bg="#fbbc04", fg="black", width=10).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Hapus", command=self.hapus, bg="#ea4335", fg="white", width=10).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Kembali", command=self.kembali, bg="#1a73e8", fg="white", width=10).grid(row=0, column=3, padx=5)

        # === Tabel Anggota ===
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        self.tree = ttk.Treeview(self.root, columns=("kode", "nama", "alamat", "telepon", "email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, pady=10)

        self.load_data()
        self.root.mainloop()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT kode_anggota, nama, alamat, telepon, email FROM anggota")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()

    def simpan(self):
        data = {k: e.get() for k, e in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Validasi", "Semua field wajib diisi!")
            return
        if not data["Telepon"].isdigit():
            messagebox.showerror("Validasi", "Nomor telepon harus berupa angka!")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["Email"]):
            messagebox.showerror("Validasi", "Format email tidak valid!")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO anggota (kode_anggota, nama, alamat, telepon, email) VALUES (%s,%s,%s,%s,%s)",
                    tuple(data.values()))
                conn.commit()
                messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
                self.load_data()
            except Error as e:
                messagebox.showerror("Error", str(e))
            conn.close()

    def update(self):
        kode = self.entries["Kode Anggota"].get()
        if not kode:
            messagebox.showwarning("Validasi", "Masukkan kode anggota yang akan diupdate!")
            return
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE anggota 
                              SET nama=%s, alamat=%s, telepon=%s, email=%s 
                              WHERE kode_anggota=%s""",
                           (self.entries["Nama"].get(),
                            self.entries["Alamat"].get(),
                            self.entries["Telepon"].get(),
                            self.entries["Email"].get(),
                            kode))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data anggota berhasil diupdate!")
            self.load_data()

    def hapus(self):
        kode = self.entries["Kode Anggota"].get()
        if not kode:
            messagebox.showwarning("Validasi", "Masukkan kode anggota yang akan dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus anggota {kode}?"):
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM anggota WHERE kode_anggota=%s", (kode,))
                conn.commit()
                conn.close()
                self.load_data()

    def kembali(self):
        self.root.destroy()
        Dashboard(self.user)


# ====== EKSEKUSI ======
if __name__ == "__main__":
    LoginWindow()
