import json
import os
from datetime import datetime

USER_FILE = "users.json"
LOG_FILE = "log.txt"

# Muat data user
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# Simpan data user
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Log aktivitas user
def log_activity(username, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {username}: {action}\n")

# Registrasi user
def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username sudah terdaftar."
    users[username] = {"password": password, "role": "user"}
    save_users(users)
    log_activity(username, "registered")
    return True, "Registrasi berhasil."

# Autentikasi user
def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        log_activity(username, "login")
        return True, users[username]["role"]
    return False, None

# Reset password (sederhana)
def reset_password(username):
    users = load_users()
    if username in users:
        users[username]["password"] = "password123"
        save_users(users)
        log_activity(username, "reset password")
        return True, "Password direset ke 'password123'."
    return False, "Username tidak ditemukan."

# Ambil semua user
def get_all_users():
    return load_users()

# Hapus user
def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        log_activity(username, "dihapus oleh admin")
        return True
    return False

# Baca log aktivitas
def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            return log.read()
    return "Belum ada aktivitas."
