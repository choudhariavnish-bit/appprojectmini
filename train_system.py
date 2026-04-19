import tkinter as tk
from tkinter import ttk, messagebox

class TrainWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve Rail Connect")
        self.geometry("500x550")
        self.configure(bg="#fef9e7")
        
        # UI Header
        tk.Label(self, text="🚆 Train Reservation", font=('Helvetica', 18, 'bold'), 
                 bg="#fef9e7", fg="#d35400").pack(pady=15)

        # Route Selection
        tk.Label(self, text="Select Route:", bg="#fef9e7").pack()
        self.route_var = ttk.Combobox(self, values=["Nagpur to Mumbai", "Nagpur to Delhi", "Nagpur to Pune"], state="readonly")
        self.route_var.pack(pady=5)

        # Class Selection
        tk.Label(self, text="Class:", bg="#fef9e7").pack(pady=5)
        self.class_var = tk.StringVar(value="Sleeper")
        ttk.Radiobutton(self, text="Sleeper", variable=self.class_var, value="Sleeper").pack()
        ttk.Radiobutton(self, text="AC 3-Tier", variable=self.class_var, value="AC3").pack()

        # Passenger Name
        tk.Label(self, text="Passenger Name:", bg="#fef9e7").pack(pady=5)
        self.ent_passenger = tk.Entry(self)
        self.ent_passenger.pack(pady=5)

        # Booking Button
        tk.Button(self, text="Book Train & Print Ticket", command=self.book_train, 
                  bg="#d35400", fg="white", font=('Arial', 12, 'bold')).pack(pady=30)

    def book_train(self):
        from bookings.models import MasterBooking
        from billing_system import ReceiptWindow

        name = self.ent_passenger.get()
        route = self.route_var.get()
        coach = self.class_var.get()

        if not name or not route:
            messagebox.showwarning("Error", "Please fill all fields!")
            return

        # Simple Pricing Logic
        price = 500 if coach == "Sleeper" else 1200
        details = f"Route: {route} | Coach: {coach}"

        try:
            new_booking = MasterBooking(
                customer_name=name,
                category="TRAIN",
                details=details,
                total_bill=price,
                is_delivery=False
            )
            new_booking.save()

            # Trigger Receipt
            ReceiptWindow(self, name, details, price)
            self.withdraw()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")