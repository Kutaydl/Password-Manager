import tkinter as tk
import cryptography.fernet
import customtkinter as ctk
from cryptography.fernet import Fernet
import pyperclip
import os

class PassManager:

    def __init__(self):
        self.key = None
        self.pass_file = None
        self.pass_dict = {}

    def generate_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def load_pass_file(self, path):
        self.pass_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.pass_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def append_pass(self, site, password):
        self.pass_dict[site] = password

        if self.pass_file is not None:
            with open(self.pass_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

        tk.messagebox.showinfo("Şifre Ekleme", "İşlem başarı ile gerçekleşti")

    def get_pass(self, site):
        try:
            pyperclip.copy(self.pass_dict[site])
            tk.messagebox.showinfo("Şifre", f"\"{site}\" başlığına ait şifreniz: {self.pass_dict[site]} panoya kopyalanmıştır")
        except KeyError:
            tk.messagebox.showerror("Başlık Bulunamadı", f"Girilen {site} isimli başlık bulunamadı")

def corrupted_file():
    pm = PassManager()
    tk.messagebox.showerror("Geçersiz Anahtar", "Anahtar dosyası değiştirilmiş veya bozuk. Var olan dosyalarınız yeniden oluşturulacak")
    fp = open("key/key.key", "w")
    pm.generate_key("key/key.key")
    fp1 = open("password/pass.pass", "w")

def main():
    pm = PassManager()

    keyFileName = "key.key"
    passFileName = "pass.pass"
    path_key = "key/"
    path_pass = "password/"

    if not os.path.exists(path_key):
        os.makedirs(path_key)

    if not os.path.exists(path_pass):
        os.makedirs(path_pass)

    if not os.path.isfile(path_key + keyFileName):
        fp = open(path_key + keyFileName, "x")
        pm.generate_key(path_key + keyFileName)

    if not os.path.isfile(path_pass + passFileName):
        fp = open(path_pass + passFileName, "x")


    pm.load_key(path_key + keyFileName)
    pm.load_pass_file(path_pass + passFileName)

    ctk.set_default_color_theme("dark-blue")
    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.geometry("700x400")
    root.title("Şifre Yöneticisi")

    frame = ctk.CTkFrame(root, width=350, height=500, corner_radius=10)
    frame.pack(padx=(20, 10), pady=20, side="left")


    label1_text = tk.StringVar(value="Yeni şifre ekle")
    label1 = ctk.CTkLabel(frame, textvariable=label1_text)
    label1.pack(padx=120, pady=(55, 20), side="top")

    title = ctk.CTkEntry(frame, placeholder_text="Şifre başlığı giriniz", corner_radius=10, border_width=2)
    title.pack(padx=50, pady=20, side="top")

    passw = ctk.CTkEntry(frame, placeholder_text="Şifrenizi giriniz", corner_radius=10, border_width=2)
    passw.pack(padx=50, pady=20, side="top")


    button_add = ctk.CTkButton(frame, corner_radius=5, text="Şifre Ekle", command=lambda:pm.append_pass(title.get(),passw.get()))
    button_add.pack(padx=50, pady=(20, 75), side="top")

    frame2 = ctk.CTkFrame(root, width=350, height=500, corner_radius=10)
    frame2.pack(padx=(10, 20), pady=20, side="right")

    label2_text = tk.StringVar(value="Şifre Görüntüle")
    label2 = ctk.CTkLabel(frame2, textvariable=label2_text)
    label2.pack(padx=115, pady=(90, 10), side="top")

    show_pass = ctk.CTkEntry(frame2, placeholder_text="Şifre başlığınızı giriniz", corner_radius=10, border_width=2)
    show_pass.pack(padx=50, pady=20, side="top")

    button_show = ctk.CTkButton(frame2, corner_radius=5, text="Şifre Gör", command=lambda:pm.get_pass(show_pass.get()))
    button_show.pack(padx=50, pady=(20, 120), side="top")

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except cryptography.fernet.InvalidToken:
        corrupted_file()
        main()
