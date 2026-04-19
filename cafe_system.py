import tkinter as tk
from tkinter import ttk, messagebox
# 1. Import the Billing system file
from billing_system import ReceiptWindow

class CafeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Cafe Ordering")
        self.geometry("450x600")
        self.configure(bg="#fdfdfd")
        
        # --- Menu Data ---
        self.menu = {
            "Espresso": 120,
            "Cold Coffee": 180,
            "Club Sandwich": 250,
            "Garlic Bread": 150,
            "Chocolate Muffin": 120
        }
        self.current_order = []

        # --- UI Header ---
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="☕ NEXUS CAFE", font=("Helvetica", 18, "bold"), 
                 fg="white", bg="#2c3e50").pack(pady=10)

        # --- Menu Selection ---
        menu_frame = tk.LabelFrame(self, text=" Select Items ", padx=10, pady=10, bg="white")
        menu_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(menu_frame, text="Menu Item:", bg="white").grid(row=0, column=0, sticky="w")
        self.item_var = tk.StringVar()
        self.menu_drop = ttk.Combobox(menu_frame, textvariable=self.item_var, values=list(self.menu.keys()), state="readonly")
        self.menu_drop.grid(row=0, column=1, padx=10)
        self.menu_drop.current(0)

        tk.Button(menu_frame, text="Add to Cart", command=self.add_to_cart, 
                  bg="#3498db", fg="white", relief="flat").grid(row=0, column=2, padx=10)

        # --- Order Summary List ---
        summary_frame = tk.LabelFrame(self, text=" Your Order ", padx=10, pady=10, bg="white")
        summary_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.order_listbox = tk.Listbox(summary_frame, font=("Courier", 10), height=8)
        self.order_listbox.pack(fill="both", expand=True)

        self.total_label = tk.Label(summary_frame, text="Total: ₹0.00", font=("Arial", 12, "bold"), bg="white", fg="#e67e22")
        self.total_label.pack(pady=10)

        # --- Action Buttons ---
        btn_frame = tk.Frame(self, bg="#fdfdfd")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Clear Order", command=self.clear_order, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Place Final Order", command=self.place_order, 
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left", padx=5)

    def add_to_cart(self):
        item = self.item_var.get()
        price = self.menu[item]
        self.current_order.append(price)
        self.order_listbox.insert(tk.END, f"{item} - ₹{price}")
        self.update_total()

    def update_total(self):
        total = sum(self.current_order)
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def clear_order(self):
        self.current_order = []
        self.order_listbox.delete(0, tk.END)
        self.update_total()

    def place_order(self):
        # 2. Local import for Django Model
        from bookings.models import MasterBooking 

        total = sum(self.current_order)
        
        if total == 0:
            messagebox.showwarning("Empty", "Add items first!")
            return

        # Prepare string of all items for the database
        items_list = self.order_listbox.get(0, tk.END)
        all_items_string = ", ".join([item.strip() for item in items_list])

        try:
            # 3. SAVE TO DJANGO DATABASE
            new_booking = MasterBooking(
                customer_name="Cafe Guest",
                category="CAFE",
                details=all_items_string, 
                total_bill=total,
                is_delivery=False
            )
            new_booking.save()

            # 4. TRIGGER BILLING RECEIPT
            # Instead of a simple alert, this shows the receipt window
            ReceiptWindow(self, "Cafe Guest", all_items_string, total)
            
            # 5. Hide the ordering window
            self.withdraw() 
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")