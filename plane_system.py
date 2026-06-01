import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import random

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class MockReceiptWindow(ctk.CTkToplevel):
    def __init__(self, parent, passenger, details, seat_num, final_price):
        super().__init__(parent)
        self.title("Nexus Go - Booking Confirmation")
        self.geometry("460x480")
        self.configure(fg_color="#ffffff")
        self.resizable(False, False)
        self.grab_set() 
        
        header = ctk.CTkFrame(self, fg_color="#001c71", height=65, corner_radius=0)
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text="Flight E-Ticket / Receipt", font=("Helvetica", 16, "bold"), text_color="white").pack(pady=18)
        
        content = ctk.CTkFrame(self, fg_color="#f8fafc", corner_radius=12, border_width=1, border_color="#e2e8f0")
        content.pack(fill="both", expand=True, padx=24, pady=24)
        
        ctk.CTkLabel(content, text="🎉 Booking Successful!", font=("Helvetica", 16, "bold"), text_color="#001c71").pack(pady=12)
        
        self.add_field(content, "Passenger Name:", passenger)
        self.add_field(content, "Trip Itinerary:", details.split("|")[0].strip())
        self.add_field(content, "Flight Details:", details.split("|")[1].strip())
        self.add_field(content, "Assigned Seat:", f"💺 Seat {seat_num}")
        self.add_field(content, "Class & Date:", details.split("|")[2].strip() + " | " + details.split("|")[3].strip())
        self.add_field(content, "Total Amount Paid:", f"₹{final_price:,.2f}")
        
        ctk.CTkButton(
            self, text="Close & Exit", fg_color="#ff6f00", hover_color="#e65c00", 
            height=42, font=("Helvetica", 13, "bold"), corner_radius=6, command=self.quit
        ).pack(pady=(0, 20))

    def add_field(self, parent, label_text, val_text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(f, text=label_text, font=("Helvetica", 11, "bold"), text_color="#64748b", anchor="w").pack(side="left")
        ctk.CTkLabel(f, text=val_text, font=("Helvetica", 11), text_color="#0f172a", wraplength=230, justify="left", anchor="e").pack(side="right", fill="x", expand=True)


class SeatSelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent, passenger, details, travel_class, current_price):
        super().__init__(parent)
        self.parent = parent
        self.passenger = passenger
        self.details = details
        self.travel_class = travel_class
        self.base_price = current_price
        self.selected_seat = None
        self.seat_addons = 0
        
        self.title(f"Nexus Go - Seat Map ({travel_class})")
        
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = 520 if travel_class == "Business" else 480
        win_h = max(700, min(int(screen_h * 0.88), 840))
        pos_x = int((screen_w - win_w) / 2)
        pos_y = int((screen_h - win_h) / 2)
        
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.configure(fg_color="#f8fafc")
        self.grab_set()

        if travel_class == "Business":
            self.theme_color = "#d4af37"       
            self.banner_bg = "#1e293b"         
            self.seat_hover = "#fef08a"        
        elif travel_class == "Premium":
            self.theme_color = "#0284c7"       
            self.banner_bg = "#0f172a"         
            self.seat_hover = "#bae6fd"
        else:
            self.theme_color = "#001c71"       
            self.banner_bg = "#001c71"         
            self.seat_hover = "#bfdbfe"

        self.rowconfigure(2, weight=1) 
        self.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=self.banner_bg, height=85, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text=f"Cabin Map — {travel_class}", font=("Helvetica", 18, "bold"), text_color="white").pack(pady=(12, 2))
        caption_text = "👑 Luxury Seating with Complementary Perks Unleashed" if travel_class == "Business" else "Select your preferred layout configuration option below"
        ctk.CTkLabel(header, text=caption_text, font=("Helvetica", 11), text_color="#94a3b8").pack()

        if travel_class == "Business":
            perk_card = ctk.CTkFrame(self, fg_color="#fffbeb", border_width=1, border_color="#fef08a", corner_radius=10)
            perk_card.grid(row=1, column=0, sticky="ew", padx=25, pady=(15, 0))
            
            ctk.CTkLabel(perk_card, text="👑 Premium Business Class Inclusions Unlocked:", font=("Helvetica", 11, "bold"), text_color="#b48900").pack(anchor="w", padx=15, pady=(8, 2))
            perks_list = "• Free Hot Gourmet Meals  • Lounge Access Pass  • Priority Boarding"
            ctk.CTkLabel(perk_card, text=perks_list, font=("Helvetica", 11), text_color="#71717a", wraplength=450, justify="left").pack(anchor="w", padx=15, pady=(0, 8))

        cabin_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#e2e8f0")
        cabin_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=20)

        columns_layout = [("A", 55), ("Aisle", 70), ("B", 55)] if travel_class == "Business" else [("A", 42), ("B", 34), ("Aisle", 60), ("C", 34), ("D", 42)]
        
        lbl_frame = ctk.CTkFrame(cabin_frame, fg_color="transparent")
        lbl_frame.pack(fill="x", pady=(15, 5))
        for col_name, px in columns_layout:
            ctk.CTkLabel(lbl_frame, text=col_name, font=("Helvetica", 11, "bold"), text_color="#94a3b8", width=px).pack(side="left", expand=True)

        scroll_cabin = ctk.CTkScrollableFrame(cabin_frame, fg_color="transparent")
        scroll_cabin.pack(fill="both", expand=True, padx=5, pady=5)

        if travel_class == "Business":
            total_rows = 3
            seat_cols = ["A", "Aisle", "B"]
        elif travel_class == "Premium":
            total_rows = 5
            seat_cols = ["A", "B", "Aisle", "C", "D"]
        else:
            total_rows = 12
            seat_cols = ["A", "B", "Aisle", "C", "D"]

        self.seat_buttons = {}
        for row in range(1, total_rows + 1):
            row_frame = ctk.CTkFrame(scroll_cabin, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row_frame, text=str(row), font=("Helvetica", 11, "bold"), text_color="#64748b", width=25).pack(side="left", padx=5)

            for col in seat_cols:
                if col == "Aisle":
                    ctk.CTkFrame(row_frame, fg_color="transparent", width=35, height=20).pack(side="left", expand=True)
                    continue
                
                seat_id = f"{row}{col}"
                is_occupied = random.choice([True, False, False, False])
                seat_cost = 1500 if travel_class == "Business" else (600 if row <= 2 else 0)

                if is_occupied:
                    btn = ctk.CTkButton(row_frame, text=seat_id, width=48, height=34, fg_color="#cbd5e1", text_color="#94a3b8", state="disabled", corner_radius=6)
                else:
                    btn = ctk.CTkButton(
                        row_frame, text=seat_id, width=48, height=34, 
                        fg_color="#f1f5f9", hover_color=self.seat_hover, text_color="#0f172a",
                        font=("Helvetica", 11, "bold"), corner_radius=6,
                        command=lambda sid=seat_id, cost=seat_cost: self.select_seat(sid, cost)
                    )
                btn.pack(side="left", padx=4, expand=True)
                self.seat_buttons[seat_id] = btn

        self.billing_strip = ctk.CTkFrame(self, fg_color="#ffffff", height=80, corner_radius=0, border_width=1, border_color="#e2e8f0")
        self.billing_strip.grid(row=3, column=0, sticky="ew")
        self.billing_strip.pack_propagate(False)

        self.lbl_summary = ctk.CTkLabel(self.billing_strip, text="Selected Seat: None", font=("Helvetica", 12, "bold"), text_color="#0f172a", justify="left")
        self.lbl_summary.pack(side="left", padx=25)

        self.btn_confirm = ctk.CTkButton(
            self.billing_strip, text="Confirm Seating", fg_color=self.theme_color if travel_class != "Business" else "#0f172a", 
            hover_color=self.banner_bg, text_color="white",
            width=160, height=40, font=("Helvetica", 13, "bold"), corner_radius=6, state="disabled",
            command=self.finalize_booking
        )
        self.btn_confirm.pack(side="right", padx=25)

    def select_seat(self, seat_id, cost):
        if self.selected_seat and self.selected_seat in self.seat_buttons:
            self.seat_buttons[self.selected_seat].configure(fg_color="#f1f5f9", text_color="#0f172a")

        self.selected_seat = seat_id
        self.seat_addons = cost
        self.seat_buttons[seat_id].configure(fg_color="#10b981", text_color="white") 

        running_total = self.base_price + self.seat_addons
        addon_msg = f" (+₹{cost})" if cost > 0 else " (Included)"
        self.lbl_summary.configure(text=f"Seat {seat_id}{addon_msg}\nTotal Bill: ₹{running_total:,}")
        self.btn_confirm.configure(state="normal")

    def finalize_booking(self):
        final_bill = self.base_price + self.seat_addons
        
        # Integrate back with Django models if available
        try:
            from bookings.models import MasterBooking
            new_booking = MasterBooking(
                customer_name=self.passenger,
                category="FLIGHT",
                details=f"{self.details} | Seat: {self.selected_seat}",
                total_bill=final_bill,
                is_delivery=False
            )
            new_booking.save()
        except Exception:
            print("[Standalone Mode]: Skipping Django core persistent DB write.")

        MockReceiptWindow(self.parent, self.passenger, self.details, self.selected_seat, final_bill)
        self.destroy()


class FlightSelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent, passenger, origin, destination, travel_class, travel_date, pass_count, base_price):
        super().__init__(parent)
        self.parent = parent
        self.passenger = passenger
        self.origin = origin
        self.destination = destination
        self.travel_class = travel_class
        self.travel_date = travel_date
        self.pass_count = pass_count
        self.base_price = base_price
        
        self.title("Nexus Go - Available Flights")
        
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = max(540, min(int(screen_w * 0.4), 600))
        win_h = max(580, min(int(screen_h * 0.8), 750))
        pos_x = int((screen_w - win_w) / 2)
        pos_y = int((screen_h - win_h) / 2)
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.configure(fg_color="#f8fafc") 
        self.grab_set()

        header = ctk.CTkFrame(self, fg_color="#001c71", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"{origin} ➔ {destination}", font=("Helvetica", 15, "bold"), text_color="white").pack(pady=(14, 2))
        ctk.CTkLabel(header, text="Select your preferred flight departure time below", font=("Helvetica", 11), text_color="#93c5fd").pack()

        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=24, pady=15)

        num_flights = random.randint(3, 4)
        hours = [6, 10, 14, 19]
        random.shuffle(hours)

        for i in range(num_flights):
            flight_num = f"NX-{random.randint(100, 999)}"
            dep_hour = hours[i]
            dep_min = random.choice([0, 15, 30, 45])
            duration_hrs = random.randint(1, 3)
            duration_mins = random.choice([0, 15, 30, 45])
            
            time_dep = f"{dep_hour:02d}:{dep_min:02d}"
            time_arr = f"{(dep_hour + duration_hrs) % 24:02d}:{(dep_min + duration_mins) % 60:02d}"
            
            price_variant = int(base_price * random.uniform(0.85, 1.15))
            total_flight_bill = price_variant * pass_count

            card = ctk.CTkFrame(scroll_frame, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#e2e8f0")
            card.pack(fill="x", pady=10, padx=4)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=18, pady=18)

            ctk.CTkLabel(info_frame, text=flight_num, font=("Helvetica", 12, "bold"), text_color="#ff6f00").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"🕒 {time_dep} ➔ {time_arr}", font=("Helvetica", 14, "bold"), text_color="#0f172a").pack(anchor="w", pady=(2, 1))
            ctk.CTkLabel(info_frame, text=f"Non-Stop • {travel_class} • {duration_hrs}h {duration_mins}m", font=("Helvetica", 11), text_color="#64748b").pack(anchor="w")

            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side="right", padx=18, pady=18)

            ctk.CTkLabel(action_frame, text=f"₹{total_flight_bill:,.2f}", font=("Helvetica", 16, "bold"), text_color="#001c71").pack(anchor="e", pady=(0, 4))
            
            details_str = f"From: {origin} -> To: {destination} | Flight: {flight_num} ({time_dep}-{time_arr}) | Class: {travel_class} | Date: {travel_date}"
            
            btn_select = ctk.CTkButton(
                action_frame, text="Select Flight", width=95, height=30, 
                fg_color="#001c71", hover_color="#0000a0",
                font=("Helvetica", 11, "bold"), corner_radius=6,
                command=lambda d=details_str, p=total_flight_bill: self.forward_to_seats(d, p)
            )
            btn_select.pack(anchor="e")

    def forward_to_seats(self, flight_details, total_flight_bill):
        SeatSelectionWindow(self.parent, self.passenger, flight_details, self.travel_class, total_flight_bill)
        self.destroy()


class FlightWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nexus Go - Book Flights")
        
        scr_w = self.winfo_screenwidth()
        scr_h = self.winfo_screenheight()
        win_w, win_h = 560, 730
        pos_x = int((scr_w - win_w) / 2)
        pos_y = int((scr_h - win_h) / 2)
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        
        self.indigo_navy = "#001c71"    
        self.indigo_blue = "#002060"    
        self.bg_light = "#f8fafc"       
        self.card_bg = "#ffffff"        
        self.text_dark = "#0f172a"      
        
        self.configure(fg_color=self.bg_light)
        self.grab_set()

        self.header_frame = ctk.CTkFrame(self, fg_color=self.indigo_navy, height=75, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        ctk.CTkLabel(self.header_frame, text="Nexus Go", font=("Helvetica", 24, "bold"), text_color="#ffffff").pack(side="left", padx=25, pady=20)

        self.main_card = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=14, border_width=1, border_color="#e2e8f0")
        self.main_card.pack(fill="both", expand=True, padx=30, pady=30)

        self.trip_var = ctk.StringVar(value="one_way")
        self.trip_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.trip_frame.pack(fill="x", padx=24, pady=(24, 15))
        
        self.rad_one_way = ctk.CTkRadioButton(self.trip_frame, text="One Way Ticket", variable=self.trip_var, value="one_way", font=("Helvetica", 12, "bold"), text_color=self.text_dark, fg_color=self.indigo_navy)
        self.rad_one_way.pack(side="left", padx=(0, 24))
        self.rad_round = ctk.CTkRadioButton(self.trip_frame, text="Round Trip Flight", variable=self.trip_var, value="round_trip", font=("Helvetica", 12, "bold"), text_color=self.text_dark, fg_color=self.indigo_navy)
        self.rad_round.pack(side="left")

        self.route_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.route_frame.pack(fill="x", padx=24, pady=8)
        self.route_frame.columnconfigure(0, weight=1)
        self.route_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(self.route_frame, text="DEPARTURE CITY (FROM)", font=("Helvetica", 10, "bold"), text_color="#64748b").grid(row=0, column=0, sticky="w", padx=2)
        self.from_var = ctk.StringVar(value="Delhi (DEL)")
        self.from_drop = ctk.CTkOptionMenu(self.route_frame, variable=self.from_var, values=["Chhatrapati Sambhajinagar (IXU)", "Mumbai (BOM)", "Delhi (DEL)", "Bangalore (BLR)"], fg_color="#f1f5f9", text_color=self.text_dark, button_color="#cbd5e1")
        self.from_drop.grid(row=1, column=0, sticky="ew", pady=(4, 12), padx=(0, 12))
        
        ctk.CTkLabel(self.route_frame, text="ARRIVAL DESTINATION (TO)", font=("Helvetica", 10, "bold"), text_color="#64748b").grid(row=0, column=1, sticky="w", padx=2)
        self.dest_var = ctk.StringVar(value="Bangalore (BLR)")
        self.dest_drop = ctk.CTkOptionMenu(self.route_frame, variable=self.dest_var, values=["Delhi (DEL)", "Mumbai (BOM)", "Bangalore (BLR)", "London (LHR)", "Dubai (DXB)"], fg_color="#1e293b", text_color="#ffffff", button_color="#334155")
        self.dest_drop.grid(row=1, column=1, sticky="ew", pady=(4, 12), padx=(12, 0))

        self.details_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.details_frame.pack(fill="x", padx=24, pady=4)
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.details_frame, text="DEPARTURE DATE", font=("Helvetica", 10, "bold"), text_color="#64748b").grid(row=0, column=0, sticky="w")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d %b %Y")
        self.ent_date = ctk.CTkEntry(self.details_frame, placeholder_text=tomorrow, font=("Helvetica", 12), height=35, fg_color="#f1f5f9", text_color=self.text_dark, border_width=1, border_color="#cbd5e1")
        self.ent_date.insert(0, tomorrow)
        self.ent_date.grid(row=1, column=0, sticky="ew", pady=(4, 12), padx=(0, 12))
        
        ctk.CTkLabel(self.details_frame, text="TOTAL PASSENGERS", font=("Helvetica", 10, "bold"), text_color="#64748b").grid(row=0, column=1, sticky="w")
        self.pass_count_var = ctk.StringVar(value="1 Passenger")
        self.pass_drop = ctk.CTkOptionMenu(self.details_frame, variable=self.pass_count_var, values=["1 Passenger", "2 Passengers", "3 Passengers"], fg_color="#f1f5f9", text_color=self.text_dark, button_color="#cbd5e1")
        self.pass_drop.grid(row=1, column=1, sticky="ew", pady=(4, 12), padx=(12, 0))

        ctk.CTkLabel(self.main_card, text="SELECT CABIN SEATING CLASS", font=("Helvetica", 10, "bold"), text_color="#64748b").pack(anchor="w", padx=24, pady=(8, 2))
        self.class_var = ctk.StringVar(value="Regular Economy")
        self.class_frame = ctk.CTkFrame(self.main_card, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0", corner_radius=10)
        self.class_frame.pack(fill="x", padx=24, pady=4)
        
        classes = [("Regular Economy", "Economy"), ("6E Premium", "Premium"), ("Business Class", "Business")]
        for text, val in classes:
            ctk.CTkRadioButton(self.class_frame, text=text, variable=self.class_var, value=val, font=("Helvetica", 11, "normal"), text_color=self.text_dark, fg_color=self.indigo_navy).pack(side="left", padx=16, pady=14, expand=True)

        ctk.CTkLabel(self.main_card, text="PRIMARY PASSENGER FULL NAME", font=("Helvetica", 10, "bold"), text_color="#64748b").pack(anchor="w", padx=24, pady=(14, 2))
        self.ent_passenger = ctk.CTkEntry(self.main_card, placeholder_text="Enter identity legal name as per Passport/ID", height=42, font=("Helvetica", 12), fg_color="#ffffff", text_color=self.text_dark, border_width=1, border_color="#cbd5e1", corner_radius=8)
        self.ent_passenger.pack(fill="x", padx=24, pady=(0, 20))

        self.prices = {"Delhi (DEL)": 5000, "Mumbai (BOM)": 4500, "Bangalore (BLR)": 5500, "London (LHR)": 65000, "Dubai (DXB)": 25000}

        self.btn_book = ctk.CTkButton(
            self.main_card, text="Search & Book Flight Matrix", command=self.book_flight, 
            fg_color="#ff6f00", hover_color="#e65c00", height=52, 
            font=("Helvetica", 14, "bold"), text_color="white", corner_radius=8
        )
        self.btn_book.pack(fill="x", padx=24, pady=(10, 24))

    def book_flight(self):
        passenger = self.ent_passenger.get().strip()
        origin = self.from_var.get()
        destination = self.dest_var.get()
        travel_class = self.class_var.get()
        date_of_travel = self.ent_date.get()
        
        if origin == destination:
            messagebox.showwarning("Route Error", "Origin and Destination choices cannot be identical.")
            return
        if not passenger:
            messagebox.showwarning("Input Error", "Please fill in the Primary Passenger Name field.")
            return

        base_price = self.prices.get(destination, 5000)
        if travel_class == "Premium":
            base_price *= 1.4
        elif travel_class == "Business":
            base_price *= 2.0
            
        passenger_count = int(self.pass_count_var.get().split()[0])

        FlightSelectionWindow(self, passenger, origin, destination, travel_class, date_of_travel, passenger_count, base_price)
        self.withdraw()


if __name__ == "__main__":
    app = FlightWindow(None)
    app.mainloop()