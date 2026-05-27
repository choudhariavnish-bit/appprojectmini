import os
import django
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox

# ✅ ASYNC PIPELINES
import threading
from email_service import send_booking_email
from billing_system import ReceiptWindow   
from sms_service import send_booking_sms       # 🆕 ADDED FOR SMS

# --- DJANGO INITIALIZATION ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# --- IMPORTS FOR SUB-SYSTEMS ---
from train_system import TrainWindow
from cafe_system import CafeWindow
from plane_system import FlightWindow
from movie_system import MovieWindow
from bookings.models import MasterBooking
from django.db.models import Sum

# Professional Beige & Olive Palette
COLORS = {
    "sidebar": "#3B3D37",
    "olive_dark": "#556B2F",
    "olive_light": "#808000",
    "beige_bg": "#F5F5DC",
    "card_cream": "#FCFAED",
    "dark_text": "#1A1A1A",
    "muted_text": "#4A4A4A",
    "FLIGHT": "#A9BA9D",
    "TRAIN": "#BCB88A",
    "MOVIE": "#D2B48C",
    "CAFE": "#6B8E23"
}

# ✅ UPDATED COMMON NOTIFICATION ROUTINE (ASYNC VIA THREADS)
def process_notifications_async(app, email, phone, name, category, amount):
    # Process PDF Generation synchronously on the UI Thread boundary safely
    receipt = ReceiptWindow(app, name, f"{category} Booking", amount)
    pdf_path = receipt.generate_pdf()
    receipt.destroy()

    # Dispatch external API Network requests asynchronously to prevent UI application freezing
    def background_task():
        # 1. Dispatch Email
        send_booking_email(email, name, category, pdf_path, amount)
        # 2. Dispatch SMS (🆕 ADDED FOR SMS)
        send_booking_sms(phone, name, category, amount)

    threading.Thread(target=background_task, daemon=True).start()


class NexusReserve(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NexusReserve | Executive Dashboard")
        self.geometry("1100(800") # Height gently scaled to accommodate phone bar cleanly
        self.geometry("1100x780")
        self.configure(fg_color=COLORS["beige_bg"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.show_home()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLORS["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="NEXUS\nRESERVE", 
                                 font=ctk.CTkFont(family="Georgia", size=26, weight="bold"),
                                 text_color=COLORS["beige_bg"])
        self.logo.grid(row=0, column=0, padx=20, pady=40)

        self.add_nav_btn("🏠 Dashboard", self.show_home, 1)
        self.add_nav_btn("✈️ Flight System", lambda: FlightWindow(self), 2)
        self.add_nav_btn("🚆 Train System", self.open_train_booking, 3)
        self.add_nav_btn("🎬 Movie System", lambda: MovieWindow(self), 4)
        self.add_nav_btn("☕ Cafe System", lambda: CafeWindow(self), 5)
        self.add_nav_btn("📊 Records", self.show_records, 6)

    def add_nav_btn(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar, text=text, height=45, corner_radius=8,
                            fg_color="transparent", text_color="#E0E0E0",
                            hover_color=COLORS["olive_dark"], anchor="w",
                            font=ctk.CTkFont(size=14, weight="bold"), command=command)
        btn.grid(row=row, column=0, padx=15, pady=10, sticky="ew")

    def show_home(self):
        if hasattr(self, 'main_view'): self.main_view.destroy()
        
        self.main_view = ctk.CTkFrame(self, corner_radius=15, fg_color=COLORS["card_cream"],
                                      border_width=1, border_color="#D1D1BC")
        self.main_view.grid(row=0, column=1, padx=40, pady=30, sticky="nsew")

        ctk.CTkLabel(self.main_view, text="Executive Reservation", 
                     font=ctk.CTkFont(family="Georgia", size=32, weight="bold"), 
                     text_color=COLORS["dark_text"]).pack(pady=(30, 10))

        form_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        form_frame.pack(padx=60, pady=5, fill="x")

        # NAME
        ctk.CTkLabel(form_frame, text="CUSTOMER NAME", 
                     font=("Helvetica", 11, "bold"), text_color=COLORS["dark_text"]).pack(pady=(10, 0))
        self.ent_name = ctk.CTkEntry(form_frame, placeholder_text="e.g. Avnish Choudhari", 
                                     width=380, height=45, corner_radius=5,
                                     fg_color="#FFFFFF", text_color=COLORS["dark_text"],
                                     border_color="#BDB76B")
        self.ent_name.pack(pady=5)

        # EMAIL FIELD
        ctk.CTkLabel(form_frame, text="CUSTOMER EMAIL", 
                     font=("Helvetica", 11, "bold"), text_color=COLORS["dark_text"]).pack(pady=(10, 0))
        self.ent_email = ctk.CTkEntry(form_frame, placeholder_text="e.g. example@gmail.com", 
                                     width=380, height=45, corner_radius=5,
                                     fg_color="#FFFFFF", text_color=COLORS["dark_text"],
                                     border_color="#BDB76B")
        self.ent_email.pack(pady=5)

        # 🆕 PHONE NUMBER FIELD (ADDED FOR SMS)
        ctk.CTkLabel(form_frame, text="CUSTOMER PHONE NUMBER", 
                     font=("Helvetica", 11, "bold"), text_color=COLORS["dark_text"]).pack(pady=(10, 0))
        self.ent_phone = ctk.CTkEntry(form_frame, placeholder_text="e.g. +919876543210", 
                                     width=380, height=45, corner_radius=5,
                                     fg_color="#FFFFFF", text_color=COLORS["dark_text"],
                                     border_color="#BDB76B")
        self.ent_phone.pack(pady=5)

        # CATEGORY
        ctk.CTkLabel(form_frame, text="SERVICE CATEGORY", 
                     font=("Helvetica", 11, "bold"), text_color=COLORS["dark_text"]).pack(pady=(10, 0))
        self.cat_var = ctk.StringVar(value="CAFE")
        self.drop = ctk.CTkOptionMenu(form_frame, variable=self.cat_var, 
                                      values=["FLIGHT", "TRAIN", "MOVIE", "CAFE"],
                                      fg_color=COLORS["olive_dark"], button_color=COLORS["olive_light"],
                                      width=380, height=45, corner_radius=5,
                                      command=self.update_category_ui)
        self.drop.pack(pady=5)

        self.deliv_var = tk.BooleanVar()
        self.check = ctk.CTkCheckBox(form_frame, text="Apply Priority Delivery?", variable=self.deliv_var,
                                     text_color=COLORS["dark_text"], fg_color=COLORS["olive_dark"])
        self.check.pack(pady=15)

        self.btn_confirm = ctk.CTkButton(self.main_view, text="CONFIRM BOOKING", 
                                         fg_color=COLORS["olive_dark"], hover_color=COLORS["olive_light"],
                                         height=55, width=300, corner_radius=5,
                                         font=ctk.CTkFont(size=15, weight="bold"),
                                         command=self.save_to_db)
        self.btn_confirm.pack(pady=15)

    def update_category_ui(self, choice):
        new_color = COLORS.get(choice, COLORS["olive_dark"])
        self.drop.configure(fg_color=new_color)

    def save_to_db(self):
        name = self.ent_name.get().strip()
        customer_email = self.ent_email.get().strip()
        customer_phone = self.ent_phone.get().strip() # 🆕 ADDED FOR SMS
        category = self.cat_var.get()
        
        # Validation checks
        if not name or not customer_email or not customer_phone:
            messagebox.showwarning("Incomplete", "Please provide Customer Name, Email, and Phone Number!")
            return

        try:
            # Assumes your MasterBooking Django table supports phone tracking, or it will execute locally 
            booking = MasterBooking(
                customer_name=name,
                category=category,
                details=f"Digital booking for {category}",
                total_bill=0.0,
                is_delivery=self.deliv_var.get()
            )
            booking.save()

            # ✅ ASYNC DISPATCH (Dispatches both background operations)
            process_notifications_async(self, customer_email, customer_phone, name, category, 0.0)

            messagebox.showinfo("Success", f"Booking Confirmed!\nReceipt emailed and SMS dispatched to {customer_phone}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process: {e}")

        # Redirect triggers to child systems
        if category == "TRAIN": 
            self.open_train_booking()
        elif category == "CAFE": 
            CafeWindow(self)
        elif category == "FLIGHT":
            FlightWindow(self)
        elif category == "MOVIE":
            MovieWindow(self)

    def show_records(self):
        records_win = ctk.CTkToplevel(self)
        records_win.title("Nexus Database Audit")
        records_win.geometry("850x550")
        records_win.configure(fg_color=COLORS["beige_bg"])
        records_win.attributes("-topmost", True)

        ctk.CTkLabel(records_win, text="Active Reservations", 
                     font=("Georgia", 24, "bold"), text_color=COLORS["dark_text"]).pack(pady=20)

        tree = ttk.Treeview(records_win, columns=("ID", "Name", "Cat", "Bill"), show='headings')
        tree.heading("ID", text="Ref ID")
        tree.heading("Name", text="Customer")
        tree.heading("Cat", text="Service")
        tree.heading("Bill", text="Amount")
        
        for b in MasterBooking.objects.all():
            tree.insert("", "end", values=(b.id, b.customer_name, b.category, f"₹{b.total_bill}"))
        
        tree.pack(fill="both", expand=True)

    def open_train_booking(self):
        TrainWindow(self)
    
    def get_total_revenue(self):
        report = MasterBooking.objects.aggregate(Sum('total_bill'))
        total = report['total_bill__sum'] or 0.0
        return f"Total Revenue: ₹{total:,.2f}"


if __name__ == "__main__":
    from auth_system import LoginWindow

    def start_main_app():
        app = NexusReserve()
        app.mainloop()

    login = LoginWindow(start_main_app)
    login.mainloop()