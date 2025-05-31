import customtkinter as ctk
from tkinter import messagebox
from utils import (
    register_user,
    authenticate_user,
    reset_password,
    get_all_users,
    delete_user,
    read_log
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Login Modern")
        self.geometry("500x500")
        self.resizable(False, False)
        self.current_user = None
        self.current_role = None
        self.create_login_frame()  # Tampilkan frame login saat aplikasi dibuka

    def clear_frame(self):
        # Menghapus semua widget dari window utama
        for widget in self.winfo_children():
            widget.destroy()

    def create_login_frame(self):
        # Membuat tampilan login
        self.clear_frame()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="LOGIN", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)
        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=6)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=6)

        ctk.CTkButton(frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(frame, text="Register", command=self.create_register_frame).pack()
        ctk.CTkButton(frame, text="Lupa Password", command=self.forgot_password).pack(pady=5)

        # Switch untuk dark mode
        self.mode_switch = ctk.CTkSwitch(frame, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.pack(pady=5)
        self.mode_switch.select()

    def toggle_mode(self):
        # Mengubah mode tampilan (dark/light)
        if self.mode_switch.get():
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def create_register_frame(self):
        # Membuat tampilan register
        self.clear_frame()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Register", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)
        self.new_username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.new_username_entry.pack(pady=6)

        self.new_password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.new_password_entry.pack(pady=6)

        ctk.CTkButton(frame, text="Daftar", command=self.register).pack(pady=10)
        ctk.CTkButton(frame, text="Kembali", command=self.create_login_frame).pack()

    def forgot_password(self):
        # Membuat tampilan reset password
        self.clear_frame()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Reset Password", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)
        self.reset_user_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.reset_user_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Reset", command=self.reset_password_action).pack(pady=5)
        ctk.CTkButton(frame, text="Kembali", command=self.create_login_frame).pack(pady=5)

    def reset_password_action(self):
        # Proses reset password
        username = self.reset_user_entry.get()
        success, msg = reset_password(username)
        if success:
            messagebox.showinfo("Berhasil", msg)
            self.create_login_frame()
        else:
            messagebox.showerror("Gagal", msg)

    def login(self):
        # Proses login user
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Gagal", "Username dan password tidak boleh kosong.")
            return
        success, role = authenticate_user(username, password)
        if success:
            self.current_user = username
            self.current_role = role
            if role == "admin":
                self.show_admin_tab()  # Jika admin, tampilkan admin panel
            else:
                self.show_home()       # Jika user biasa, tampilkan home
        else:
            messagebox.showerror("Gagal", "Username atau password salah.")

    def register(self):
        # Proses registrasi user baru
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if not username or not password:
            messagebox.showerror("Gagal", "Username dan password tidak boleh kosong.")
            return
        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.create_login_frame()
        else:
            messagebox.showerror("Gagal", msg)

    def show_home(self):
        # Tampilan beranda untuk user biasa
        self.clear_frame()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)
        ctk.CTkLabel(frame, text=f"Halo, {self.current_user}!", font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkButton(frame, text="Logout", command=self.create_login_frame).pack(pady=5)

    def show_admin_tab(self):
        # Tampilan admin panel (data user & log aktivitas)
        self.clear_frame()
        tabview = ctk.CTkTabview(self, width=480, height=460)
        tabview.pack(padx=10, pady=10)

        tab1 = tabview.add("Data User")
        tab2 = tabview.add("Log Aktivitas")

        # Tab Data User
        user_frame = ctk.CTkScrollableFrame(tab1, width=450, height=370)
        user_frame.pack(padx=10, pady=10)

        users = get_all_users()
        for u in users:
            row = ctk.CTkFrame(user_frame)
            row.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(row, text=f"{u} ({users[u]['role']})", width=200, anchor="w").pack(side="left")
            if u != self.current_user:
                # Tombol hapus user (tidak bisa hapus diri sendiri)
                ctk.CTkButton(row, text="Hapus", width=100,
                              command=lambda user=u: self.confirm_delete(user)).pack(side="right")

        ctk.CTkButton(tab1, text="Kembali ke Beranda", command=self.show_home).pack(pady=8)

        # Tab Log
        log_text = read_log()
        log_box = ctk.CTkTextbox(tab2, width=450, height=370)
        log_box.pack(padx=10, pady=10)
        log_box.insert("0.0", log_text)
        log_box.configure(state="disabled")

        ctk.CTkButton(tab2, text="Kembali ke Beranda", command=self.show_home).pack(pady=8)

    def confirm_delete(self, username):
        # Konfirmasi dan proses hapus user
        if messagebox.askyesno("Konfirmasi", f"Hapus user '{username}'?"):
            if delete_user(username):
                messagebox.showinfo("Berhasil", f"User '{username}' dihapus.")
                self.show_admin_tab()
            else:
                messagebox.showerror("Gagal", "Gagal menghapus user.")

if __name__ == "__main__":
    # Entry point aplikasi
    app = LoginApp()
    app.mainloop()
