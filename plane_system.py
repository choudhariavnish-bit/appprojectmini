import tkinter as tk
from tkinter import ttk, messagebox

class FlightWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve Sky-High Bookings")
        self.geometry("500x600")
        self.configure(bg="#f0f4f8")
        
        self.primary_color = "#2c3e50"
        
        # --- UI Header ---
        tk.Label(self, text="✈️ Flight Reservation", font=('Helvetica', 18, 'bold'), 
                 bg="#f0f4f8", fg=self.primary_color).pack(pady=15)

        # --- Destination Selection ---
        tk.Label(self, text="Select Destination:", bg="#f0f4f8").pack()
        self.dest_var = tk.StringVar(value="Mumbai (BOM)")
        self.dest_drop = ttk.Combobox(self, textvariable=self.dest_var, state="readonly")
        self.dest_drop['values'] = ("Delhi (DEL)", "Mumbai (BOM)", "Bangalore (BLR)", "London (LHR)", "Dubai (DXB)")
        self.dest_drop.pack(pady=5)

        # --- Class Selection ---
        tk.Label(self, text="Travel Class:", bg="#f0f4f8").pack(pady=5)
        self.class_var = tk.StringVar(value="Economy")
        tk.Radiobutton(self, text="Economy", variable=self.class_var, value="Economy", bg="#f0f4f8").pack()
        tk.Radiobutton(self, text="Business", variable=self.class_var, value="Business", bg="#f0f4f8").pack()

        # --- Passenger Name ---
        tk.Label(self, text="Passenger Name:", bg="#f0f4f8").pack(pady=5)
        self.ent_passenger = tk.Entry(self, font=('Arial', 12))
        self.ent_passenger.pack(pady=5)

        # --- Price Logic ---
        # Base prices for destinations
        self.prices = {
            "Delhi (DEL)": 5000,
            "Mumbai (BOM)": 4500,
            "Bangalore (BLR)": 5500,
            "London (LHR)": 65000,
            "Dubai (DXB)": 25000
        }

        # --- Booking Button ---
        tk.Button(self, text="Book Ticket & Save", command=self.book_flight, 
                  bg="#e67e22", fg="white", font=('Arial', 12, 'bold'), height=2).pack(pady=30, fill="x", padx=50)

    def book_flight(self):
        # 1. Django Import
        from bookings.models import MasterBooking
        from billing_system import ReceiptWindow # Use your existing billing file

        passenger = self.ent_passenger.get()
        destination = self.dest_var.get()
        travel_class = self.class_var.get()

        if not passenger:
            messagebox.showwarning("Input Error", "Please enter passenger name!")
            return

        # 2. Calculate Price
        base_price = self.prices.get(destination, 0)
        final_price = base_price * 2 if travel_class == "Business" else base_price

        details = f"Flight to {destination} | Class: {travel_class}"

        try:
            # 3. Save to Django
            new_booking = MasterBooking(
                customer_name=passenger,
                category="FLIGHT",
                details=details,
                total_bill=final_price,
                is_delivery=False
            )
            new_booking.save()

            # 4. Trigger Receipt
            ReceiptWindow(self, passenger, details, final_price)
            self.withdraw()

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save flight: {e}")