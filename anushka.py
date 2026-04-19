import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

# ---------------- DATABASE ----------------
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    username TEXT,
    category TEXT,
    item TEXT,
    price INTEGER,
    qty INTEGER
)
""")

conn.commit()

# ---------------- APP ----------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Pro App")
        self.root.geometry("950x600")
        self.root.config(bg="#1e1e2f")

        self.username = ""

        # ---------------- LOAD IMAGES ----------------
        self.images = {
            "Coffee": self.load_img("images/coffee.png"),
            "Burger": self.load_img("images/burger.png"),
            "Pizza": self.load_img("images/pizza.png"),
            "Pasta": self.load_img("images/pasta.png"),
            "Avengers": self.load_img("images/avengers.png"),
            "Pushpa 2": self.load_img("images/pushpa.png"),
            "Inception": self.load_img("images/inception.png"),
            "Goa Trip": self.load_img("images/goa.png"),
            "Manali": self.load_img("images/manali.png"),
            "Kashmir": self.load_img("images/kashmir.png"),
            "T-Shirt": self.load_img("images/tshirt.png"),
            "Shoes": self.load_img("images/shoes.png"),
            "Watch": self.load_img("images/watch.png"),
        }

        self.login_screen()

    # ---------------- IMAGE LOADER ----------------
    def load_img(self, path):
        try:
            img = Image.open(path)
            img = img.resize((80, 80))
            return ImageTk.PhotoImage(img)
        except:
            return None

    # ---------------- STYLE ----------------
    def title(self, text):
        return tk.Label(self.root, text=text,
                        font=("Helvetica", 22, "bold"),
                        bg="#1e1e2f", fg="white")

    def btn(self, text, cmd, color="#4CAF50"):
        return tk.Button(self.root, text=text, command=cmd,
                         font=("Arial", 11, "bold"),
                         bg=color, fg="white",
                         width=18, height=2, bd=0)

    # ---------------- LOGIN ----------------
    def login_screen(self):
        self.clear()

        self.title("Login").pack(pady=20)

        frame = tk.Frame(self.root, bg="#2c2c3e", padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Username", bg="#2c2c3e", fg="white").pack()
        self.user = tk.Entry(frame)
        self.user.pack()

        tk.Label(frame, text="Password", bg="#2c2c3e", fg="white").pack()
        self.passw = tk.Entry(frame, show="*")
        self.passw.pack()

        self.btn("Login", self.login).pack(pady=10)
        self.btn("Signup", self.signup_screen, "#2196F3").pack()

    def login(self):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (self.user.get(), self.passw.get()))
        if cursor.fetchone():
            self.username = self.user.get()
            self.home()
        else:
            messagebox.showerror("Error", "Invalid login")

    # ---------------- SIGNUP ----------------
    def signup_screen(self):
        self.clear()

        self.title("Signup").pack(pady=20)

        frame = tk.Frame(self.root, bg="#2c2c3e", padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Username", bg="#2c2c3e", fg="white").pack()
        self.new_user = tk.Entry(frame)
        self.new_user.pack()

        tk.Label(frame, text="Password", bg="#2c2c3e", fg="white").pack()
        self.new_pass = tk.Entry(frame, show="*")
        self.new_pass.pack()

        self.btn("Create", self.signup).pack(pady=10)
        self.btn("Back", self.login_screen, "#f44336").pack()

    def signup(self):
        cursor.execute("INSERT INTO users VALUES (?,?)",
                       (self.new_user.get(), self.new_pass.get()))
        conn.commit()
        messagebox.showinfo("Success", "Account Created!")
        self.login_screen()

    # ---------------- HOME ----------------
    def home(self):
        self.clear()

        self.title(f"Welcome {self.username} 👋").pack(pady=15)

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack()

        self.btn("☕ Cafe", lambda: self.category("Cafe"), "#ff9800").grid(row=0, column=0, padx=10, pady=10)
        self.btn("🎬 Movies", lambda: self.category("Movie"), "#9c27b0").grid(row=0, column=1, padx=10, pady=10)
        self.btn("✈ Travel", lambda: self.category("Travel"), "#03a9f4").grid(row=1, column=0, padx=10, pady=10)
        self.btn("🛍 Shopping", lambda: self.category("Shopping"), "#4caf50").grid(row=1, column=1, padx=10, pady=10)

        self.btn("🛒 View Cart", self.view_cart, "#009688").pack(pady=20)
        self.btn("💳 View Bill", self.bill, "#e91e63").pack()

    # ---------------- CATEGORY ----------------
    def category(self, cat):
        self.clear()

        self.title(cat).pack(pady=10)

        items = {
            "Cafe": [("Coffee",100),("Burger",150),("Pizza",250),("Pasta",200)],
            "Movie": [("Avengers",300),("Pushpa 2",250),("Inception",200)],
            "Travel": [("Goa Trip",5000),("Manali",7000),("Kashmir",10000)],
            "Shopping": [("T-Shirt",400),("Shoes",800),("Watch",1500)]
        }

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack()

        row, col = 0, 0

        for item, price in items[cat]:
            card = tk.Frame(frame, bg="#2c2c3e", padx=10, pady=10)
            card.grid(row=row, column=col, padx=10, pady=10)

            if item in self.images and self.images[item]:
                tk.Label(card, image=self.images[item], bg="#2c2c3e").pack()

            tk.Label(card, text=item, bg="#2c2c3e", fg="white").pack()
            tk.Label(card, text=f"₹{price}", bg="#2c2c3e", fg="#00e676").pack()

            tk.Button(card, text="Add",
                      command=lambda i=item, p=price: self.add_to_cart(cat, i, p),
                      bg="#4caf50", fg="white").pack()

            col += 1
            if col > 2:
                col = 0
                row += 1

        self.btn("Back", self.home, "#f44336").pack(pady=20)

    # ---------------- ADD TO CART ----------------
    def add_to_cart(self, cat, item, price):
        cursor.execute("SELECT qty FROM cart WHERE username=? AND item=?",
                       (self.username, item))
        data = cursor.fetchone()

        if data:
            cursor.execute("UPDATE cart SET qty = qty + 1 WHERE username=? AND item=?",
                           (self.username, item))
        else:
            cursor.execute("INSERT INTO cart VALUES (?,?,?,?,?)",
                           (self.username, cat, item, price, 1))

        conn.commit()
        messagebox.showinfo("Added", f"{item} added!")

    # ---------------- CART ----------------
    def view_cart(self):
        self.clear()

        self.title("Your Cart 🛒").pack(pady=10)

        cursor.execute("SELECT item, price, qty FROM cart WHERE username=?", (self.username,))
        data = cursor.fetchall()

        for item, price, qty in data:
            tk.Label(self.root,
                     text=f"{item} x{qty} = ₹{price*qty}",
                     bg="#1e1e2f", fg="white").pack()

        tk.Button(self.root, text="Clear Cart",
                  command=self.clear_cart,
                  bg="red", fg="white").pack(pady=10)

        self.btn("Back", self.home).pack()

    def clear_cart(self):
        cursor.execute("DELETE FROM cart WHERE username=?", (self.username,))
        conn.commit()
        messagebox.showinfo("Done", "Cart Cleared")
        self.home()

    # ---------------- BILL ----------------
    def bill(self):
        self.clear()

        self.title("Final Bill 💳").pack(pady=10)

        cursor.execute("SELECT item, price, qty FROM cart WHERE username=?", (self.username,))
        data = cursor.fetchall()

        total = 0

        for item, price, qty in data:
            subtotal = price * qty
            total += subtotal

            tk.Label(self.root,
                     text=f"{item} x{qty} = ₹{subtotal}",
                     bg="#1e1e2f", fg="white").pack()

        tk.Label(self.root,
                 text=f"Total = ₹{total}",
                 bg="#1e1e2f", fg="#00e676",
                 font=("Arial", 14, "bold")).pack(pady=10)

        self.btn("Back", self.home).pack(pady=20)

    # ---------------- UTIL ----------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN ----------------
root = tk.Tk()
app = App(root)
root.mainloop()