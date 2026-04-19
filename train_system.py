import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from billing_system import ReceiptWindow

# DB setup
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS train_orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    train TEXT,
    route TEXT,
    seats INTEGER,
    total INTEGER
)
""")
conn.commit()


class TrainWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Train Booking")
        self.geometry("520x650")
        self.configure(bg="#eef7ff")

        # Train data
        self.trains = {
            "Rajdhani Express": 1200,
            "Shatabdi Express": 1000,
            "Duronto Express": 900,
            "Garib Rath": 600
        }

        # Header
        tk.Label(self, text="🚆 TRAIN BOOKING", font=("Arial", 18, "bold"),
                 bg="#2980b9", fg="white").pack(fill="x", pady=10)

        # Booking Frame
        frame = tk.LabelFrame(self, text="Book Ticket", bg="white")
        frame.pack(padx=20, pady=10, fill="x")

        tk.Label(frame, text="Train:", bg="white").grid(row=0, column=0)
        self.train_var = tk.StringVar()
        self.combo = ttk.Combobox(frame, textvariable=self.train_var,
                                 values=list(self.trains.keys()), state="readonly")
        self.combo.grid(row=0, column=1)
        self.combo.current(0)

        tk.Label(frame, text="From:", bg="white").grid(row=1, column=0)
        self.from_entry = tk.Entry(frame)
        self.from_entry.grid(row=1, column=1)

        tk.Label(frame, text="To:", bg="white").grid(row=2, column=0)
        self.to_entry = tk.Entry(frame)
        self.to_entry.grid(row=2, column=1)

        tk.Label(frame, text="Seats:", bg="white").grid(row=3, column=0)
        self.seat_var = tk.IntVar(value=1)
        tk.Entry(frame, textvariable=self.seat_var, width=5).grid(row=3, column=1)

        tk.Button(frame, text="Add Booking", bg="#27ae60", fg="white",
                  command=self.add_booking).grid(row=4, column=0, columnspan=2, pady=10)

        # Listbox
        self.listbox = tk.Listbox(self, height=10)
        self.listbox.pack(padx=20, pady=10, fill="both")

        self.total_label = tk.Label(self, text="Total: ₹0", font=("Arial", 14, "bold"),
                                   fg="#c0392b", bg="#eef7ff")
        self.total_label.pack()

        # Buttons
        btn_frame = tk.Frame(self, bg="#eef7ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Confirm Booking", bg="#e67e22", fg="white",
                  command=self.place_order).pack(side="left", padx=5)

        self.orders = []

    def add_booking(self):
        train = self.train_var.get()
        from_loc = self.from_entry.get()
        to_loc = self.to_entry.get()
        seats = self.seat_var.get()

        if not from_loc or not to_loc:
            messagebox.showerror("Error", "Enter route details")
            return

        if seats <= 0:
            messagebox.showerror("Error", "Seats must be > 0")
            return

        price = self.trains[train]
        total_price = price * seats

        self.orders.append((train, from_loc, to_loc, seats, total_price))
        self.listbox.insert(tk.END,
            f"{train} | {from_loc}→{to_loc} | Seats:{seats} = ₹{total_price}")

        self.update_total()

    def update_total(self):
        total = sum(o[4] for o in self.orders)
        self.total_label.config(text=f"Total: ₹{total}")

    def clear(self):
        self.orders = []
        self.listbox.delete(0, tk.END)
        self.update_total()

    def place_order(self):
        total = sum(o[4] for o in self.orders)

        if total == 0:
            messagebox.showwarning("Empty", "Add booking first")
            return

        all_details = ", ".join(
            [f"{o[0]} {o[1]}→{o[2]} x{o[3]}" for o in self.orders]
        )

        try:
            for o in self.orders:
                cursor.execute("""
                INSERT INTO train_orders(customer, train, route, seats, total)
                VALUES (?, ?, ?, ?, ?)
                """, ("Train User", o[0], f"{o[1]}-{o[2]}", o[3], o[4]))

            conn.commit()

            # Receipt
            ReceiptWindow(self, "Train User", all_details, total)

            self.withdraw()

        except Exception as e:
            messagebox.showerror("Error", str(e))