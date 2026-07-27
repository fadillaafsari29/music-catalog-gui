import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import pygame
import os
from PIL import Image, ImageTk

# Inisialisasi pygame mixer
pygame.mixer.init()

# Definisi kelas Lagu untuk menyimpan informasi tentang setiap lagu
class Lagu:
    def __init__(self, judul, artis, tahun_rilis, genre, file_path):
        self.judul = judul
        self.artis = artis
        self.tahun_rilis = tahun_rilis
        self.genre = genre
        self.file_path = file_path

    def __repr__(self):
        return f"Lagu(judul='{self.judul}', artis='{self.artis}', tahun_rilis={self.tahun_rilis}, genre='{self.genre}', file_path='{self.file_path}')"

# Fungsi untuk memuat data dari file Excel
def muat_data():
    global katalog
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        data = pd.read_excel(file_path)
        if all(column in data.columns for column in ['Judul', 'Artis', 'Tahun Rilis', 'Genre', 'File Path']):
            katalog = [Lagu(row['Judul'], row['Artis'], row['Tahun Rilis'], row['Genre'], row['File Path']) for index, row in data.iterrows()]
            update_katalog_listbox()
        else:
            messagebox.showerror("Error", "Format file Excel tidak valid. Pastikan memiliki kolom 'Judul', 'Artis', 'Tahun Rilis', 'Genre', dan 'File Path'.")

# Fungsi untuk menyimpan data ke file Excel
def simpan_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        data = pd.DataFrame([vars(lagu) for lagu in katalog])
        data.to_excel(file_path, index=False)
        messagebox.showinfo("Berhasil", "Data berhasil disimpan.")

# Fungsi untuk mengupdate listbox katalog
def update_katalog_listbox():
    listbox_katalog.delete(0, tk.END)
    for lagu in katalog:
        listbox_katalog.insert(tk.END, f"{lagu.judul} - {lagu.artis} ({lagu.tahun_rilis}, {lagu.genre})")

# Fungsi untuk menambah lagu
def tambah_lagu():
    judul = entry_judul.get()
    artis = entry_artis.get()
    tahun_rilis = entry_tahun_rilis.get()
    genre = entry_genre.get()

    selected_file = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.mp3;*.wav")]
    )

    if judul and artis and tahun_rilis and genre and selected_file:
        try:
            tahun_rilis = int(tahun_rilis)

            # Simpan hanya nama file (bukan path laptop)
            file_path = os.path.basename(selected_file)

            lagu_baru = Lagu(
                judul,
                artis,
                tahun_rilis,
                genre,
                file_path
            )

            katalog.append(lagu_baru)
            update_katalog_listbox()

            entry_judul.delete(0, tk.END)
            entry_artis.delete(0, tk.END)
            entry_tahun_rilis.delete(0, tk.END)
            entry_genre.delete(0, tk.END)

            messagebox.showinfo(
                "Berhasil",
                "Lagu berhasil ditambahkan."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Tahun rilis harus berupa angka."
            )

    else:
        messagebox.showerror(
            "Error",
            "Semua field harus diisi."
        )

# Fungsi untuk menghapus lagu
def hapus_lagu():
    selected_index = listbox_katalog.curselection()
    if selected_index:
        index = selected_index[0]
        del katalog[index]
        update_katalog_listbox()
        messagebox.showinfo("Berhasil", "Lagu berhasil dihapus.")
    else:
        messagebox.showerror("Error", "Pilih lagu yang ingin dihapus.")

# Fungsi untuk mengurutkan katalog
def urutkan_katalog(sort_by):
    n = len(katalog)
    for i in range(n):
        for j in range(0, n-i-1):
            if getattr(katalog[j], sort_by) > getattr(katalog[j+1], sort_by):
                katalog[j], katalog[j+1] = katalog[j+1], katalog[j]
    update_katalog_listbox()

# Fungsi untuk mencari lagu
def cari_lagu():
    keyword = entry_cari.get().lower()
    search_by = cari_option.get()
    results = [lagu for lagu in katalog if keyword in str(getattr(lagu, search_by)).lower()]
    
    if results:
        if search_by == "artis":
            message = f"Lagu oleh {keyword.capitalize()}:\n" + "\n".join([lagu.judul for lagu in results])
        else:
            message = f"Lagu ditemukan: {results[0]}"
        messagebox.showinfo("Lagu Ditemukan", message)
    else:
        messagebox.showinfo("Lagu Tidak Ditemukan", f"Lagu dengan {search_by} '{keyword}' tidak ditemukan.")

# Fungsi untuk memutar lagu
def putar_lagu():
    selected_index = listbox_katalog.curselection()

    if selected_index:
        index = selected_index[0]
        lagu = katalog[index]

        # Folder music berada di dalam project
        music_path = os.path.join("music", lagu.file_path)

        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play()

                messagebox.showinfo(
                    "Memutar Lagu",
                    f"Memutar lagu: {lagu.judul} oleh {lagu.artis}"
                )

            except pygame.error as e:
                messagebox.showerror(
                    "Error",
                    f"Tidak dapat memutar lagu:\n{e}"
                )

        else:
            messagebox.showerror(
                "Error",
                f"File lagu '{lagu.file_path}' tidak ditemukan di folder 'music'."
            )

    else:
        messagebox.showerror(
            "Error",
            "Pilih lagu yang ingin diputar."
        )

# Fungsi untuk menghentikan lagu
def stop_lagu():
    pygame.mixer.music.stop()
    messagebox.showinfo("Stop Lagu", "Lagu telah dihentikan.")

# Program Utama
katalog = []

# Membuat window utama
root = tk.Tk()
root.title("Katalog Musik")

# Menambahkan gambar latar belakang
bg_image_path = "background.jpg"

if os.path.exists(bg_image_path):
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

# Membuat frame input
frame_input = tk.Frame(root, bg='#ffffff')  # Set background untuk menghindari transparansi
frame_input.pack(pady=10)

button_muat = tk.Button(frame_input, text="Muat Data dari Excel", command=muat_data)
button_muat.grid(row=0, columnspan=3, pady=10)

label_judul = tk.Label(frame_input, text="Judul:", bg='#ffffff')
label_judul.grid(row=1, column=0)
entry_judul = tk.Entry(frame_input)
entry_judul.grid(row=1, column=1)

label_artis = tk.Label(frame_input, text="Artis:", bg='#ffffff')
label_artis.grid(row=2, column=0)
entry_artis = tk.Entry(frame_input)
entry_artis.grid(row=2, column=1)

label_tahun_rilis = tk.Label(frame_input, text="Tahun Rilis:", bg='#ffffff')
label_tahun_rilis.grid(row=3, column=0)
entry_tahun_rilis = tk.Entry(frame_input)
entry_tahun_rilis.grid(row=3, column=1)

label_genre = tk.Label(frame_input, text="Genre:", bg='#ffffff')
label_genre.grid(row=4, column=0)
entry_genre = tk.Entry(frame_input)
entry_genre.grid(row=4, column=1)

button_tambah = tk.Button(frame_input, text="Tambah Lagu", command=tambah_lagu)
button_tambah.grid(row=5, columnspan=3, pady=10)

# Membuat frame katalog
frame_katalog = tk.Frame(root, bg='#ffffff')  # Set background untuk menghindari transparansi
frame_katalog.pack(pady=10)

listbox_katalog = tk.Listbox(frame_katalog, width=50)
listbox_katalog.pack()

# Menggabungkan tombol urutkan dengan pilihan
sort_option = tk.StringVar(value="judul")

def show_sort_menu(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Judul", command=lambda: urutkan_katalog("judul"))
    menu.add_command(label="Artis", command=lambda: urutkan_katalog("artis"))
    menu.add_command(label="Tahun Rilis", command=lambda: urutkan_katalog("tahun_rilis"))
    menu.add_command(label="Genre", command=lambda: urutkan_katalog("genre"))
    menu.post(event.x_root, event.y_root)

button_urutkan = tk.Button(frame_katalog, text="Urutkan Katalog")
button_urutkan.bind("<Button-1>", show_sort_menu)
button_urutkan.pack(side=tk.LEFT, padx=5)

button_hapus = tk.Button(frame_katalog, text="Hapus Lagu", command=hapus_lagu)
button_hapus.pack(side=tk.LEFT, padx=5)

button_putar = tk.Button(frame_katalog, text="Putar Lagu", command=putar_lagu)
button_putar.pack(side=tk.LEFT, padx=5)

button_stop = tk.Button(frame_katalog, text="Stop Lagu", command=stop_lagu)
button_stop.pack(side=tk.LEFT, padx=5)

# Membuat frame pencarian
frame_cari = tk.Frame(root, bg='#ffffff')  # Set background untuk menghindari transparansi
frame_cari.pack(pady=10)

label_cari = tk.Label(frame_cari, text="Cari:", bg='#ffffff')
label_cari.grid(row=0, column=0)
entry_cari = tk.Entry(frame_cari)
entry_cari.grid(row=0, column=1)

cari_option = tk.StringVar(value="judul")

def show_cari_menu(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Judul", command=lambda: cari_lagu_berdasarkan("judul"))
    menu.add_command(label="Artis", command=lambda: cari_lagu_berdasarkan("artis"))
    menu.add_command(label="Tahun Rilis", command=lambda: cari_lagu_berdasarkan("tahun_rilis"))
    menu.add_command(label="Genre", command=lambda: cari_lagu_berdasarkan("genre"))
    menu.post(event.x_root, event.y_root)

button_cari = tk.Button(frame_cari, text="Cari Lagu")
button_cari.bind("<Button-1>", show_cari_menu)
button_cari.grid(row=0, column=3, padx=5)

def cari_lagu_berdasarkan(cari_by):
    keyword = entry_cari.get().lower()
    results = [lagu for lagu in katalog if keyword in str(getattr(lagu, cari_by)).lower()]
    
    if results:
        if cari_by == "artis":
            message = f"Lagu oleh {keyword.capitalize()}:\n" + "\n".join([lagu.judul for lagu in results])
        else:
            message = f"Lagu ditemukan: {results[0]}"
        messagebox.showinfo("Lagu Ditemukan", message)
    else:
        messagebox.showinfo("Lagu Tidak Ditemukan", f"Lagu dengan {cari_by} '{keyword}' tidak ditemukan.")

# Membuat frame simpan
frame_simpan = tk.Frame(root, bg='#ffffff')  # Set background untuk menghindari transparansi
frame_simpan.pack(pady=10)

button_simpan = tk.Button(frame_simpan, text="Simpan Data ke Excel", command=simpan_data)
button_simpan.pack()

# Menjalankan aplikasi
root.mainloop()