import tkinter as tk
from tkinter import ttk, messagebox
# 1. Import the Billing system file
from billing_system import ReceiptWindow

class MovieWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Movie Booking")
        self.geometry("450x650")
        self.configure(bg="#121212") # Dark Cinema Theme
        
        # --- Movie & Pricing Data ---
        # Format: "Movie Name": Base Ticket Price
        self.movies = {
            "The Batman": 250,
            "Oppenheimer": 300,
            "Inception": 200,
            "Avatar": 350,
            "Dune: Part Two": 300
        }
        self.current_tickets = []

        # --- UI Header ---
        header_frame = tk.Frame(self, bg="#e74c3c", height=60) # Red theme for Movies
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="🎬 NEXUS CINEMAS", font=("Helvetica", 18, "bold"), 
                 fg="white", bg="#e74c3c").pack(pady=10)

        # --- Movie Selection ---
        movie_frame = tk.LabelFrame(self, text=" Select Show & Seats ", padx=10, pady=10, 
                                    bg="#1e1e1e", fg="white")
        movie_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(movie_frame, text="Select Movie:", bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w")
        self.movie_var = tk.StringVar()
        self.movie_drop = ttk.Combobox(movie_frame, textvariable=self.movie_var, 
                                       values=list(self.movies.keys()), state="readonly")
        self.movie_drop.grid(row=0, column=1, padx=10, pady=5)
        self.movie_drop.current(0)

        tk.Label(movie_frame, text="Seat Type:", bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w")
        self.seat_type = tk.StringVar(value="Normal")
        self.seat_drop = ttk.Combobox(movie_frame, textvariable=self.seat_type, 
                                      values=["Normal", "Executive (+₹100)", "Recliner (+₹250)"], state="readonly")
        self.seat_drop.grid(row=1, column=1, padx=10, pady=5)
        self.seat_drop.current(0)

        tk.Button(movie_frame, text="Add Ticket", command=self.add_to_cart, 
                  bg="#e74c3c", fg="white", relief="flat", width=12).grid(row=2, column=1, pady=10)

        # --- Booking Summary ---
        summary_frame = tk.LabelFrame(self, text=" Booking Summary ", padx=10, pady=10, bg="#1e1e1e", fg="white")
        summary_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.order_listbox = tk.Listbox(summary_frame, font=("Courier", 10), height=8, bg="#2c2c2c", fg="white")
        self.order_listbox.pack(fill="both", expand=True)

        self.total_label = tk.Label(summary_frame, text="Total: ₹0.00", font=("Arial", 12, "bold"), 
                                    bg="#1e1e1e", fg="#f1c40f")
        self.total_label.pack(pady=10)

        # --- Action Buttons ---
        btn_frame = tk.Frame(self, bg="#121212")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cancel All", command=self.clear_order, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Confirm Booking", command=self.place_order, 
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left", padx=5)

    def add_to_cart(self):
        movie = self.movie_var.get()
        base_price = self.movies[movie]
        
        # Calculate seat surcharge
        surcharge = 0
        seat = self.seat_type.get()
        if "Executive" in seat: surcharge = 100
        elif "Recliner" in seat: surcharge = 250
        
        final_price = base_price + surcharge
        self.current_tickets.append(final_price)
        self.order_listbox.insert(tk.END, f"{movie} ({seat}) - ₹{final_price}")
        self.update_total()

    def update_total(self):
        total = sum(self.current_tickets)
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def clear_order(self):
        self.current_tickets = []
        self.order_listbox.delete(0, tk.END)
        self.update_total()

    def place_order(self):
        # 2. Local import for Django Model
        from bookings.models import MasterBooking 

        total = sum(self.current_tickets)
        
        if total == 0:
            messagebox.showwarning("Empty", "Please select a movie and seat first!")
            return

        # Prepare string for database
        tickets_list = self.order_listbox.get(0, tk.END)
        all_tickets_string = " | ".join([t.strip() for t in tickets_list])

        try:
            # 3. SAVE TO DJANGO DATABASE
            new_booking = MasterBooking(
                customer_name="Movie Fan",
                category="MOVIE",
                details=all_tickets_string, 
                total_bill=total,
                is_delivery=False
            )
            new_booking.save()

            # 4. TRIGGER BILLING RECEIPT
            ReceiptWindow(self, "Movie Fan", all_tickets_string, total)
            
            # 5. Hide the window
            self.withdraw() 
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save booking: {e}")