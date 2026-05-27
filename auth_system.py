import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import hashlib

# --- DB SETUP ---
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()


# --- PASSWORD HASH ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# --- SIGNUP WINDOW ---
class SignupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Signup")
        self.geometry("350x300")

        ctk.CTkLabel(self, text="Create Account", font=("Arial", 20, "bold")).pack(pady=20)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Signup", command=self.signup).pack(pady=20)

    def signup(self):
        user = self.username.get()
        pwd = hash_password(self.password.get())

        if not user or not pwd:
            messagebox.showwarning("Error", "Fill all fields")
            return

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            messagebox.showinfo("Success", "Account created!")
            self.destroy()
        except:
            messagebox.showerror("Error", "Username already exists")


# --- LOGIN WINDOW ---
class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.title("Login - NexusReserve")
        self.geometry("400x350")

        self.on_success = on_success

        ctk.CTkLabel(self, text="Login", font=("Arial", 22, "bold")).pack(pady=30)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=15)
        ctk.CTkButton(self, text="Create Account", command=self.open_signup).pack()

    def login(self):
        user = self.username.get()
        pwd = hash_password(self.password.get())

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            self.destroy()
            self.on_success()   # 👉 open main app
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_signup(self):
        SignupWindow(self)