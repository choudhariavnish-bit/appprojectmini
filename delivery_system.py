import customtkinter as ctk
from tkinter import messagebox
import tkintermapview # Ensure you ran: pip install tkintermapview
import random

COLORS = {
    "olive_dark": "#556B2F",
    "beige_bg": "#F5F5DC",
    "card_cream": "#FCFAED",
    "dark_text": "#1A1A1A",
}

class DeliveryPage(ctk.CTkToplevel):
    def __init__(self, parent, customer_name, total_bill):
        super().__init__(parent)
        
        self.title(f"Live Tracking | {customer_name}")
        self.geometry("1000x650")
        self.configure(fg_color=COLORS["beige_bg"])
        
        # Mock Data
        self.partner = random.choice(["Rajesh Kumar", "Amit Sharma", "Suresh V."])
        self.customer_name = customer_name
        self.total_bill = total_bill

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Left Panel: Order Details
        info_panel = ctk.CTkFrame(self, width=300, fg_color=COLORS["card_cream"], corner_radius=0)
        info_panel.grid(row=0, column=0, sticky="nsew", padx=2)

        ctk.CTkLabel(info_panel, text="NEXUS DELIVERY", font=("Georgia", 22, "bold"), 
                     text_color=COLORS["olive_dark"]).pack(pady=30)

        # Partner Info
        ctk.CTkLabel(info_panel, text="PARTNER ASSIGNED", font=("Helvetica", 10, "bold")).pack()
        ctk.CTkLabel(info_panel, text=self.partner, font=("Helvetica", 16), 
                     text_color=COLORS["dark_text"]).pack(pady=(0, 20))

        # Bill Display
        ctk.CTkLabel(info_panel, text=f"TOTAL BILL: ₹{self.total_bill}", 
                     font=("Helvetica", 18, "bold"), text_color="#B22222").pack(pady=20)

        # SMS Button
        ctk.CTkButton(info_panel, text="SEND SMS RECEIPT", fg_color=COLORS["olive_dark"],
                      command=self.send_sms_simulation).pack(side="bottom", pady=40, padx=20, fill="x")

        # Right Panel: Map
        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=15)
        self.map_widget.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Coordinates (Chhatrapati Sambhajinagar Example)
        cafe_loc = (19.8762, 75.3433)
        home_loc = (19.8950, 75.3750)
        
        self.map_widget.set_position(19.8850, 75.3550)
        self.map_widget.set_zoom(13)

        self.map_widget.set_marker(cafe_loc[0], cafe_loc[1], text="Nexus Cafe")
        self.map_widget.set_marker(home_loc[0], home_loc[1], text="Customer Home")
        
        self.partner_marker = self.map_widget.set_marker(cafe_loc[0], cafe_loc[1], 
                                                        text="Delivery Partner", 
                                                        marker_color_circle="red")
        
        self.animate_move(cafe_loc, home_loc)

    def animate_move(self, start, end):
        steps = 100
        def move(step=0):
            if step <= steps:
                lat = start[0] + (end[0] - start[0]) * (step / steps)
                lng = start[1] + (end[1] - start[1]) * (step / steps)
                self.partner_marker.set_position(lat, lng)
                self.after(200, lambda: move(step + 1))
            else:
                messagebox.showinfo("Delivery Update", "Your order has arrived!")
        move()

    def send_sms_simulation(self):
        msg = f"SUCCESS: SMS sent to {self.customer_name}.\nContent: 'Your Nexus order bill of ₹{self.total_bill} is paid. {self.partner} is at your door.'"
        messagebox.showinfo("SMS Gateway", msg)