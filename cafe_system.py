# cafe_system.py
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os

# Import the Billing system file
from billing_system import ReceiptWindow

class CafeWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Cyber Cafe System")
        self.geometry("500x700")
        self.resizable(False, False)
        
        # Enforce keeping window on top of main background matrix viewport
        self.attributes("-topmost", True)

        # --- Menu Data ---
        self.menu = {
            "Espresso": 120,
            "Cold Coffee": 180,
            "Club Sandwich": 250,
            "Garlic Bread": 150,
            "Chocolate Muffin": 120
        }
        self.current_order = []
        
        # --- Video System State Engine ---
        self.video_path = "136613662307-uhd_3840_2160_25fps.mp4"
        self.video_cap = None
        self.is_running = True

        # Base layout container
        self.root_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#05070A")
        self.root_container.pack(fill="both", expand=True)

        # 🎥 Layer 0: Video Display Viewport
        self.video_label = tk.Label(self.root_container, bg="#05070A", borderwidth=0, highlightthickness=0)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 🌌 Layer 1: Dark Translucent Glass Filter Panel
        self.glass_overlay = ctk.CTkFrame(self.root_container, corner_radius=12, 
                                          fg_color="#0A0F14", border_width=1, border_color="#1A2633")
        self.glass_overlay.place(relx=0.5, rely=0.5, anchor="center", width=440, height=640)

        # --- UI Sub-components ---
        self.title_label = ctk.CTkLabel(self.glass_overlay, text="☕ NEXUS CAFE OPERATOR", 
                                         font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
                                         text_color="#00E5FF")
        self.title_label.pack(pady=(30, 5))
        
        self.status_label = ctk.CTkLabel(self.glass_overlay, text="LIQUID REFRESHMENT LAYER LIVE", 
                                          font=("Courier", 10), text_color="#00FF66")
        self.status_label.pack(pady=(0, 20))

        # Selection Interface Box
        menu_frame = ctk.CTkFrame(self.glass_overlay, fg_color="#121B22", border_width=1, border_color="#1A2633")
        menu_frame.pack(padx=25, pady=10, fill="x")

        ctk.CTkLabel(menu_frame, text="SELECT MENU DISPATCH:", font=("Courier", 11, "bold"), 
                     text_color="#E0E6ED").pack(pady=(10, 2), padx=15, anchor="w")
        
        self.item_var = tk.StringVar()
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("CyberCafe.TCombobox", background="#1A2633", fieldbackground="#121B22", 
                        foreground="#FFFFFF", arrowcolor="#00E5FF", bordercolor="#1A2633")
        
        self.menu_drop = ttk.Combobox(menu_frame, textvariable=self.item_var, 
                                      values=list(self.menu.keys()), state="readonly", 
                                      style="CyberCafe.TCombobox")
        self.menu_drop.pack(padx=15, pady=5, fill="x")
        self.menu_drop.current(0)

        self.add_btn = ctk.CTkButton(menu_frame, text="ADD DATA TO CART", fg_color="#006644", 
                                     hover_color="#00FF66", font=("Courier", 12, "bold"),
                                     command=self.add_to_cart, corner_radius=4)
        self.add_btn.pack(padx=15, pady=12, fill="x")

        # Cart Matrix Box
        summary_frame = ctk.CTkFrame(self.glass_overlay, fg_color="#121B22", border_width=1, border_color="#1A2633")
        summary_frame.pack(padx=25, pady=10, fill="both", expand=True)

        ctk.CTkLabel(summary_frame, text="CURRENT TRANSACTION STACK:", font=("Courier", 11, "bold"), 
                     text_color="#E0E6ED").pack(pady=(8, 2), padx=15, anchor="w")

        self.order_listbox = tk.Listbox(summary_frame, font=("Courier", 11), bg="#0A0F14", 
                                        fg="#00FF66", borderwidth=0, highlightthickness=0,
                                        selectbackground="#1A2633")
        self.order_listbox.pack(padx=15, pady=5, fill="both", expand=True)

        self.total_label = ctk.CTkLabel(summary_frame, text="TOTAL: ₹0.00", 
                                         font=ctk.CTkFont(family="Courier", size=16, weight="bold"), 
                                         text_color="#FF9900")
        self.total_label.pack(pady=10)

        # Control terminal action panel buttons
        btn_frame = ctk.CTkFrame(self.glass_overlay, fg_color="transparent")
        btn_frame.pack(pady=(10, 25), fill="x", padx=25)

        self.clear_btn = ctk.CTkButton(btn_frame, text="CLEAR STACK", fg_color="#331A1A", 
                                       hover_color="#FF3333", text_color="#FFFFFF",
                                       command=self.clear_order, width=170, corner_radius=4)
        self.clear_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        self.place_btn = ctk.CTkButton(btn_frame, text="EXECUTE PURCHASE", fg_color="#005577", 
                                       hover_color="#00E5FF", text_color="#FFFFFF",
                                       font=("Courier", 12, "bold"),
                                       command=self.place_order, width=170, corner_radius=4)
        self.place_btn.pack(side="right", fill="x", expand=True)

        # Close handler
        self.protocol("WM_DELETE_WINDOW", self.terminate_window)

        # Start Video Background Stream Loop Execution
        self.initialize_video_pipeline()

    def initialize_video_pipeline(self):
        """Initializes OpenCV video decode system streams safely."""
        if os.path.exists(self.video_path):
            self.video_cap = cv2.VideoCapture(self.video_path)
            self.play_video_frame()
        else:
            print(f"🚨 Critical Fallback: Video data missing at path target location: '{self.video_path}'")
            self.status_label.configure(text="VIDEO FLOW PATH DETACHED (FILE NOT FOUND)", text_color="#FF3333")

    def play_video_frame(self):
        """Processes video frame array updates asynchronously while managing memory locks."""
        if not self.is_running or self.video_cap is None:
            return

        ret, frame = self.video_cap.read()
        
        # Auto wrap video index pointer back to index 0 on EOF
        if not ret:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_cap.read()

        if ret:
            try:
                # Downscale resolution constraints explicitly matching container geometries
                frame = cv2.resize(frame, (500, 700))
                
                # Transform OpenCV space (BGR) array to standard processing array layout (RGB)
                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(cv2_image)
                tk_img = ImageTk.PhotoImage(image=pil_img)

                # 🛠️ CRITICAL FIX: Save an explicit memory pointer directly on the widget
                # This breaks garbage collection and keeps the frames visible on screen
                self.video_label.configure(image=tk_img)
                self.video_label.image = tk_img 
                
            except Exception as e:
                print(f"[Frame Raster Render Intercept Failure Fault]: {e}")

        # Re-queue update task loop tick every 35ms (~28 FPS output fluid synchronization)
        self.after(35, self.play_video_frame)

    def add_to_cart(self):
        item = self.item_var.get()
        price = self.menu[item]
        self.current_order.append(price)
        self.order_listbox.insert(tk.END, f" 🧬 {item.upper():<18} -> ₹{price}")
        self.update_total()

    def update_total(self):
        total = sum(self.current_order)
        self.total_label.configure(text=f"TOTAL: ₹{total:.2f}")

    def clear_order(self):
        self.current_order = []
        self.order_listbox.delete(0, tk.END)
        self.update_total()

    def place_order(self):
        from bookings.models import MasterBooking 

        total = sum(self.current_order)
        if total == 0:
            messagebox.showwarning("Empty Vector", "Select dynamic food data packets first!")
            return

        items_list = self.order_listbox.get(0, tk.END)
        all_items_string = ", ".join([item.replace(" 🧬 ", "").strip() for item in items_list])

        try:
            new_booking = MasterBooking(
                customer_name="Cafe Guest",
                category="CAFE",
                details=all_items_string, 
                total_bill=total,
                is_delivery=False
            )
            new_booking.save()

            ReceiptWindow(self, "Cafe Guest", all_items_string, total)
            self.terminate_window() 
            
        except Exception as e:
            messagebox.showerror("Data Loss Fault", f"Failed to sync central storage block: {e}")

    def terminate_window(self):
        """Releases capture handles and kills window context smoothly."""
        self.is_running = False
        if self.video_cap is not None:
            self.video_cap.release()
        self.destroy()