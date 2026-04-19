import tkinter as tk
from tkinter import ttk

class ReceiptWindow(tk.Toplevel):
    def __init__(self, parent, customer_name, items, total):
        super().__init__(parent)
        self.title("NexusReserve - Cafe Receipt")
        self.geometry("350x500")
        self.configure(bg="white")

        # --- Receipt Header ---
        tk.Label(self, text="NEXUS CAFE", font=("Courier", 18, "bold"), bg="white").pack(pady=10)
        tk.Label(self, text="--------------------------", bg="white").pack()
        tk.Label(self, text=f"Customer: {customer_name}", font=("Courier", 10), bg="white").pack(anchor="w", padx=20)
        tk.Label(self, text="--------------------------", bg="white").pack()

        # --- Items List ---
        item_frame = tk.Frame(self, bg="white")
        item_frame.pack(fill="both", expand=True, padx=20)

        # Split the items string back into a list to display
        item_list = items.split(", ")
        for item in item_list:
            tk.Label(item_frame, text=item, font=("Courier", 10), bg="white").pack(anchor="w")

        # --- Footer ---
        tk.Label(self, text="--------------------------", bg="white").pack()
        tk.Label(self, text=f"TOTAL AMOUNT: ₹{total:.2f}", font=("Courier", 12, "bold"), bg="white").pack(pady=10)
        tk.Label(self, text="Thank you for visiting!", font=("Courier", 9, "italic"), bg="white").pack(pady=5)
        
        tk.Button(self, text="Close & Print", command=self.destroy, bg="#2c3e50", fg="white").pack(pady=10)