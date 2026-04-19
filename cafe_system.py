import tkinter as tk
from tkinter import ttk, messagebox
from bookings.models import MasterBooking # Import your Django model

class CafeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Cafe Ordering")
        self.geometry("500x500")
        self.configure(bg="#f8f9fa")

        # 1. Menu and Pricing
        self.menu = {"Coffee": 120, "Sandwich": 150, "Tea": 50, "Cake": 200}
        self.order_items = []

        tk.Label(self, text="☕ Cafe Ordering System", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=10)

        # 2. Dropdown for Menu
        tk.Label(self, text="Select Item:", bg="#f8f9fa").pack()
        self.item_var = tk.StringVar(value="Coffee")
        self.menu_drop = ttk.Combobox(self, textvariable=self.item_var, values=list(self.menu.keys()))
        self.menu_drop.pack(pady=5)

        tk.Button(self, text="Add to Order", command=self.add_item, bg="#3498db", fg="white").pack(pady=5)

        # 3. Order Summary Listbox
        self.listbox = tk.Listbox(self, width=40, height=5)
        self.listbox.pack(pady=10)

        # 4. Final Confirmation Button
        tk.Button(self, text="Place Final Order", bg="#27ae60", fg="white", 
                  font=("Arial", 10, "bold"), command=self.place_order).pack(pady=20)

    def add_item(self):
        item = self.item_var.get()
        price = self.menu[item]
        self.order_items.append(price)
        self.listbox.insert(tk.END, f"{item} - ₹{price}")

    def place_order(self):
        total = sum(self.order_items)
        if total == 0:
            messagebox.showwarning("Empty", "No items added!")
            return

        # Save to Django Database
        new_order = MasterBooking(
            customer_name="Cafe Customer", # You can pass a name here later
            category="CAFE",
            details="Items ordered from Cafe Menu",
            total_bill=total,
            is_delivery=False
        )
        new_order.save()
        messagebox.showinfo("Success", f"Order Placed! Total: ₹{total}")
        self.destroy() # Closes the cafe window