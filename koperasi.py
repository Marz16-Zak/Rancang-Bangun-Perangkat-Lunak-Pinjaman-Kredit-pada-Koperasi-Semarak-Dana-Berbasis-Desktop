import sqlite3
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import ttk
from datetime import date

DB_NAME = "koperasi_semarak_dana.db"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Koperasi Semarak Dana")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.style = tb.Style("superhero")
        self.create_table()
        self.login_screen()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user (
                        username TEXT PRIMARY KEY,
                        password TEXT,
                        role TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS pengajuan (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT,
                        nik TEXT,
                        alamat TEXT,
                        pekerjaan TEXT,
                        penghasilan REAL,
                        jumlah_pinjam REAL,
                        jaminan TEXT,
                        tanggal TEXT)''')
        c.execute("SELECT COUNT(*) FROM user")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO user VALUES ('anggota1', '123', 'anggota')")
            c.execute("INSERT INTO user VALUES ('pimpinan1', 'admin', 'pimpinan')")
        conn.commit()
        conn.close()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tb.Frame(self.root, padding=30)
        frame.pack(pady=80)

        tb.Label(frame, text="\U0001F510 Login Koperasi", font=("Segoe UI", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        tb.Label(frame, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tb.Entry(frame, width=30, bootstyle="info")
        self.username_entry.grid(row=1, column=1, pady=5)

        tb.Label(frame, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tb.Entry(frame, show="*", width=30, bootstyle="info")
        self.password_entry.grid(row=2, column=1, pady=5)

        tb.Button(frame, text="Login", width=25, bootstyle="success", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username=? AND password=?", (user, pw))
        result = c.fetchone()
        conn.close()
        if result:
            role = result[2]
            if role == "anggota":
                self.anggota_menu()
            elif role == "pimpinan":
                self.pimpinan_menu()
        else:
            messagebox.showerror("Error", "Username atau password salah!")

    def anggota_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tb.Frame(self.root, padding=20)
        frame.pack(pady=10)

        tb.Label(frame, text="\U0001F4DD Formulir Pengajuan Pinjaman", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Nama", "NIK", "Alamat", "Pekerjaan", "Penghasilan", "Jumlah Pinjaman", "Jaminan"]
        self.entries = {}

        for idx, label in enumerate(labels):
            tb.Label(frame, text=label).grid(row=idx+1, column=0, sticky="w", pady=5)
            entry = tb.Entry(frame, width=40, bootstyle="primary")
            entry.grid(row=idx+1, column=1, pady=5)
            self.entries[label.lower()] = entry

        tb.Button(frame, text="Ajukan Pinjaman", bootstyle="success", width=25, command=self.ajukan_pinjaman).grid(row=9, column=0, columnspan=2, pady=15)
        tb.Button(frame, text="Logout", bootstyle="danger-outline", width=10, command=self.login_screen).grid(row=10, column=0, columnspan=2)

    def pimpinan_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tb.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        tb.Label(frame, text="\U0001F4CA Data Pengajuan Pinjaman", font=("Segoe UI", 18, "bold")).pack(pady=10)

        columns = ("ID", "Nama", "NIK", "Alamat", "Pekerjaan", "Penghasilan", "Jumlah Pinjaman", "Jaminan", "Tanggal")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM pengajuan")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            tree.insert('', 'end', values=row)

        tb.Button(frame, text="Logout", bootstyle="danger-outline", width=10, command=self.login_screen).pack(pady=10)

    def ajukan_pinjaman(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Validasi", "Semua data harus diisi.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''INSERT INTO pengajuan (nama, nik, alamat, pekerjaan, penghasilan, jumlah_pinjam, jaminan, tanggal)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (data['nama'], data['nik'], data['alamat'], data['pekerjaan'],
                       float(data['penghasilan']), float(data['jumlah pinjaman']),
                       data['jaminan'], date.today().isoformat()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Berhasil", "Pengajuan berhasil diajukan!")
            for entry in self.entries.values():
                entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data.\n{str(e)}")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = App(root)
    root.mainloop()
