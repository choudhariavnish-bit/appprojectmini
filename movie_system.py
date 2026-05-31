import tkinter as tk
from tkinter import ttk, messagebox
# 1. Import the Billing system file
from billing_system import ReceiptWindow

class MovieWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Movie Booking")
        self.geometry("900x750")  # Expanded width to accommodate the seat layout
        self.configure(bg="#ffffff") # Clean white background as requested
        
        # --- Movie & Pricing Data ---
        self.movies = {
            "The Batman": 250,
            "Oppenheimer": 300,
            "Inception": 200,
            "Avatar": 350,
            "Dune: Part Two": 300
        }
        
        # Track selected seats: e.g., {"Row A - 05": seat_button_reference}
        self.selected_seats = {} 
        self.base_price = 250

        # --- UI Header ---
        header_frame = tk.Frame(self, bg="#e74c3c", height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="🎬 NEXUS CINEMAS", font=("Helvetica", 18, "bold"), 
                 fg="white", bg="#e74c3c").pack(pady=10)

        # Main Layout split into Left (Seats) and Right (Controls/Summary)
        main_container = tk.Frame(self, bg="#ffffff")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_container, bg="#ffffff")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        right_frame = tk.Frame(main_container, bg="#f8f9fa", bd=1, relief="solid")
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # --- Dropdown Selector (Right Side) ---
        movie_select_frame = tk.Frame(right_frame, bg="#f8f9fa", padx=15, pady=15)
        movie_select_frame.pack(fill="x")
        
        tk.Label(movie_select_frame, text="Select Movie:", font=("Arial", 10, "bold"), bg="#f8f9fa").pack(anchor="w")
        self.movie_var = tk.StringVar()
        self.movie_drop = ttk.Combobox(movie_select_frame, textvariable=self.movie_var, 
                                       values=list(self.movies.keys()), state="readonly")
        self.movie_drop.pack(fill="x", pady=5)
        self.movie_drop.current(0)
        self.movie_drop.bind("<<ComboboxSelected>>", self.on_movie_change)
        
        # --- Visual Seat Map Layout (Left Side) ---
        seat_title_frame = tk.Frame(left_frame, bg="#ffffff")
        seat_title_frame.pack(fill="x", pady=5)
        
        # Screen Indicator
        screen_label = tk.Label(seat_title_frame, text="✨ SCREEN THIS WAY ✨", font=("Arial", 10, "italic"), bg="#e0e0e0", fg="#555555")
        screen_label.pack(fill="x", pady=5)
        
        prime_label = tk.Label(seat_title_frame, text="₹270 PRIME ROWS (Rows A-C) | Normal Base (Rows D-G)", font=("Arial", 9, "bold"), bg="#ffffff", fg="#27ae60")
        prime_label.pack(pady=5)

        # Container scrollable frame canvas logic if window size gets tight
        self.seats_grid_frame = tk.Frame(left_frame, bg="#ffffff")
        self.seats_grid_frame.pack(expand=True)
        
        self.generate_seat_map()

        # --- Legend Indicator ---
        legend_frame = tk.Frame(left_frame, bg="#ffffff")
        legend_frame.pack(pady=10)
        
        self.create_legend_item(legend_frame, "#ffffff", "#27ae60", "Available")
        self.create_legend_item(legend_frame, "#27ae60", "#27ae60", "Selected")
        self.create_legend_item(legend_frame, "#e0e0e0", "#e0e0e0", "Sold / Unavailable")

        # --- Booking Summary (Right Side) ---
        summary_frame = tk.LabelFrame(right_frame, text=" Booking Summary ", font=("Arial", 10, "bold"), padx=10, pady=10, bg="#f8f9fa")
        summary_frame.pack(padx=15, pady=10, fill="both", expand=True)

        self.order_listbox = tk.Listbox(summary_frame, font=("Courier", 10), height=12, bg="#ffffff", fg="#333333")
        self.order_listbox.pack(fill="both", expand=True)

        self.total_label = tk.Label(summary_frame, text="Total: ₹0.00", font=("Arial", 14, "bold"), 
                                    bg="#f8f9fa", fg="#c0392b")
        self.total_label.pack(pady=10)

        # --- Action Buttons (Right Side) ---
        btn_frame = tk.Frame(right_frame, bg="#f8f9fa", pady=10)
        btn_frame.pack(fill="x", padx=15)

        tk.Button(btn_frame, text="Clear Layout", command=self.clear_order, bg="#7f8c8d", fg="white", relief="flat", width=12).pack(side="left", padx=5, expand=True)
        tk.Button(btn_frame, text="Confirm", command=self.place_order, 
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), relief="flat", width=12).pack(side="right", padx=5, expand=True)

    def create_legend_item(self, parent, bg_color, border_color, text):
        item_frame = tk.Frame(parent, bg="#ffffff", padx=10)
        item_frame.pack(side="left")
        box = tk.Label(item_frame, width=2, height=1, bg=bg_color, relief="solid", bd=1, highlightbackground=border_color)
        box.pack(side="left", padx=2)
        lbl = tk.Label(item_frame, text=text, bg="#ffffff", font=("Arial", 9))
        lbl.pack(side="left")

    def generate_seat_map(self):
        # Rows configurations (Row ID, Number of seats, Is Prime status)
        row_configs = [
            ("A", 20, True), ("B", 20, True), ("C", 20, True),
            ("D", 16, False), ("E", 16, False), ("F", 16, False), ("G", 16, False)
        ]
        
        # Hardcoded simulated 'Already Occupied/Sold' seats to mimic gray blocks in your image
        sold_seats = ["B-07", "B-08", "B-09", "B-10", "C-06", "C-07"]

        for row_idx, (row_name, total_seats, is_prime) in enumerate(row_configs):
            row_label = tk.Label(self.seats_grid_frame, text=row_name, font=("Arial", 10, "bold"), bg="#ffffff")
            row_label.grid(row=row_idx, column=0, padx=10, pady=4)
            
            for seat_num in range(1, total_seats + 1):
                seat_id = f"{row_name}-{seat_num:02d}"
                
                # Handling custom spacing breaks for seat blocks (simulating walkways)
                col_offset = seat_num
                if total_seats == 20:
                    if seat_num > 4: col_offset += 1
                    if seat_num > 16: col_offset += 1
                elif total_seats == 16:
                    if seat_num > 4: col_offset += 1
                    
                if seat_id in sold_seats:
                    # Disabled/Sold seat style
                    btn = tk.Button(self.seats_grid_frame, text=f"{seat_num:02d}", font=("Arial", 7),
                                    width=3, height=1, bg="#e0e0e0", fg="#aaaaaa", state="disabled", relief="flat")
                else:
                    # Clear, interactive custom flat buttons mimicking your snapshot UI layout
                    btn = tk.Button(self.seats_grid_frame, text=f"{seat_num:02d}", font=("Arial", 7),
                                    width=3, height=1, bg="#ffffff", fg="#27ae60", 
                                    activebackground="#27ae60", activeforeground="#ffffff",
                                    relief="solid", bd=1, highlightcolor="#27ae60")
                    
                    # Binding click actions cleanly using explicit default arguments closures
                    btn.config(command=lambda b=btn, sid=seat_id, ip=is_prime: self.toggle_seat(b, sid, ip))
                
                btn.grid(row=row_idx, column=col_offset, padx=2, pady=2)

    def on_movie_change(self, event=None):
        movie = self.movie_var.get()
        self.base_price = self.movies[movie]
        self.update_summary_and_total()

    def toggle_seat(self, button, seat_id, is_prime):
        if seat_id in self.selected_seats:
            # Deselect execution
            button.config(bg="#ffffff", fg="#27ae60")
            del self.selected_seats[seat_id]
        else:
            # Select execution
            button.config(bg="#27ae60", fg="#ffffff")
            self.selected_seats[seat_id] = is_prime
            
        self.update_summary_and_total()

    def update_summary_and_total(self):
        self.order_listbox.delete(0, tk.END)
        total = 0
        movie = self.movie_var.get()
        
        for seat_id, is_prime in self.selected_seats.items():
            # Prime calculation matches your layout surcharge criteria (Dynamic modifier setup)
            seat_cost = 270 if is_prime else self.base_price
            total += seat_cost
            
            seat_type_str = "Prime Row" if is_prime else "Normal"
            self.order_listbox.insert(tk.END, f"{movie} [{seat_id}] ({seat_type_str}) - ₹{seat_cost}")
            
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def clear_order(self):
        # Resets UI layout references smoothly back to fresh state configurations
        for seat_id, btn in list(self.selected_seats.items()):
            # We don't save references directly, easiest approach is to regenerate or loop over children widgets
            pass
            
        self.selected_seats.clear()
        
        # Reset colors of all non-disabled grid buttons
        for widget in self.seats_grid_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget['state'] == 'normal':
                widget.config(bg="#ffffff", fg="#27ae60")
                
        self.update_summary_and_total()

    def place_order(self):
        # 2. Local import for Django Model
        from bookings.models import MasterBooking 

        if not self.selected_seats:
            messagebox.showwarning("Empty Selection", "Please click and select at least one seat from the matrix visual chart!")
            return

        tickets_list = self.order_listbox.get(0, tk.END)
        all_tickets_string = " | ".join([t.strip() for t in tickets_list])
        
        # Re-verify dynamic price sum evaluations
        total = 0
        for seat_id, is_prime in self.selected_seats.items():
            total += (270 if is_prime else self.base_price)

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
            
            # 5. Hide the window cleanly without crashing the application thread loop
            self.withdraw() 
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save booking: {e}")