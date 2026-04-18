import os
import django
import tkinter as tk
from tkinter import ttk, messagebox

# --- IMPORTANT: INITIALIZE DJANGO BEFORE IMPORTS ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now import your model
from bookings.models import MasterBooking

class NexusReserve:
    def __init__(self, root):
        self.root = root
        self.root.title("NexusReserve Super-App")
        self.root.geometry("500x400")

        # UI Elements
        tk.Label(root, text="Customer Name:", font=('Arial', 12)).pack(pady=5)
        self.ent_name = tk.Entry(root)
        self.ent_name.pack()

        tk.Label(root, text="Select Category:", font=('Arial', 12)).pack(pady=5)
        self.cat_var = tk.StringVar(value="CAFE")
        self.drop = ttk.Combobox(root, textvariable=self.cat_var)
        self.drop['values'] = ("FLIGHT", "TRAIN", "MOVIE", "CAFE")
        self.drop.pack()

        self.deliv_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Is this a Delivery?", variable=self.deliv_var).pack(pady=10)

        tk.Button(root, text="Confirm Booking", bg="green", fg="white", 
                  command=self.save_to_db).pack(pady=20)

    def save_to_db(self):
        name = self.ent_name.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name!")
            return

        # Save to SQLite via Django ORM
        booking = MasterBooking(
            customer_name=name,
            category=self.cat_var.get(),
            details="General Booking",
            total_bill=0.0, # Logic for calculation goes here later
            is_delivery=self.deliv_var.get()
        )
        booking.save()
        messagebox.showinfo("Success", f"Booking saved for {name} in SQLite!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusReserve(root)
    root.mainloop()