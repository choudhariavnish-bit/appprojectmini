# cafe_system.py
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import cv2
import numpy as np
import random
import time
from PIL import Image, ImageTk
import os

try:
    from billing_system import ReceiptWindow
except ImportError:
    ReceiptWindow = None

class CafeWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("NexusReserve - Cyber Cafe System")
        self.geometry("500x700")
        self.resizable(False, False)
        
        self.attributes("-topmost", True)

        self.menu = {
            "Espresso": 120,
            "Cold Coffee": 180,
            "Club Sandwich": 250,
            "Garlic Bread": 150,
            "Chocolate Muffin": 120
        }
        self.current_order = []
        
        self.video_path = r"C:\appproject\13662307-uhd_3840_2160_25fps.mp4"
        self.video_cap = None
        self.is_running = True
        
        self.frame_count = 0
        self.start_time = time.time()
        self.glitch_active = False
        self.glitch_duration = 0

        self.root_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#05070A")
        self.root_container.pack(fill="both", expand=True)

        # 🎥 Layer 0: High-Exposure Video Viewport
        self.video_label = tk.Label(self.root_container, bg="#05070A", borderwidth=0, highlightthickness=0)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 🌌 Layer 1: Futuristic Wireframe HUD (Removed heavy dark background color so video shines through)
        self.glass_overlay = ctk.CTkFrame(self.root_container, width=440, height=640, corner_radius=12, 
                                          fg_color="transparent", border_width=2, border_color="#00E5FF")
        self.glass_overlay.place(relx=0.5, rely=0.5, anchor="center")

        # --- UI Sub-components ---
        self.title_label = ctk.CTkLabel(self.glass_overlay, text="⚡ NEXUS CAFE OPERATOR", 
                                         font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
                                         text_color="#00E5FF")
        self.title_label.pack(pady=(30, 5))
        
        self.status_label = ctk.CTkLabel(self.glass_overlay, text="INITIALIZING DATA CHANNELS...", 
                                          font=("Courier", 10), text_color="#00FF66")
        self.status_label.pack(pady=(0, 20))

        # Selection Interface Box
        menu_frame = ctk.CTkFrame(self.glass_overlay, fg_color="#090F14", border_width=1, border_color="#1A2633")
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
        summary_frame = ctk.CTkFrame(self.glass_overlay, fg_color="#090F14", border_width=1, border_color="#1A2633")
        summary_frame.pack(padx=25, pady=10, fill="both", expand=True)

        ctk.CTkLabel(summary_frame, text="CURRENT TRANSACTION STACK:", font=("Courier", 11, "bold"), 
                     text_color="#E0E6ED").pack(pady=(8, 2), padx=15, anchor="w")

        self.order_listbox = tk.Listbox(summary_frame, font=("Courier", 11), bg="#05070A", 
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

        self.protocol("WM_DELETE_WINDOW", self.terminate_window)

        self.lift()
        self.focus_force()
        self.update()
        
        self.after(100, self.initialize_video_pipeline)

    def initialize_video_pipeline(self):
        if not self.is_running:
            return
            
        if os.path.exists(self.video_path):
            try:
                self.video_cap = cv2.VideoCapture(self.video_path)
                if self.video_cap.isOpened():
                    self.status_label.configure(text="AI-NATIVE FLOW ENGINE RUNNING", text_color="#00FF66")
                    self.play_video_frame()
                    return
            except Exception as e:
                print(f"OpenCV Initialization Error: {e}")
                
        self.handle_video_failure("FILE PATH NOT LOCATED")

    def handle_video_failure(self, reason):
        self.status_label.configure(text=f"VIDEO STREAM DEGRADED ({reason})", text_color="#FF3333")
        try:
            static_bg = np.zeros((700, 500, 3), dtype=np.uint8)
            for y in range(0, 700, 35):
                cv2.line(static_bg, (0, y), (500, y), (20, 30, 25), 1)
            cv2_image = cv2.cvtColor(static_bg, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv2_image)
            tk_img = ImageTk.PhotoImage(image=pil_img)
            self.video_label.configure(image=tk_img)
            self.video_label.image = tk_img
        except Exception as e:
            print(f"Failed to render static grid layout: {e}")

    def play_video_frame(self):
        if not self.is_running or self.video_cap is None:
            return

        try:
            ret, frame = self.video_cap.read()
            if not ret:
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video_cap.read()

            if ret:
                self.frame_count += 1
                
                # 🛠️ NEW STYLING GAIN: Algorithmic exposure amplifier. 
                # Multiplies color data array matrices to pull the dark milk-pouring highlights into crisp clarity.
                frame = cv2.convertScaleAbs(frame, alpha=1.4, beta=25)
                
                h, w, _ = frame.shape
                
                # --- EFFECT 1: Dynamic Rhythmic Camera Pulse Zoom ---
                elapsed = time.time() - self.start_time
                pulse = np.sin(elapsed * 4.5)
                
                if pulse > 0.7:  
                    zoom_factor = 1.25
                elif 0.2 < pulse <= 0.7:
                    zoom_factor = 1.08
                else:
                    zoom_factor = 1.0
                
                if zoom_factor > 1.0:
                    nw, nh = int(w / zoom_factor), int(h / zoom_factor)
                    x1, y1 = (w - nw) // 2, (h - nh) // 2
                    frame = frame[y1:y1+nh, x1:x1+nw]

                frame = cv2.resize(frame, (500, 700))

                # --- EFFECT 2: Occasional Digital Chromatic/Glitch Jumps ---
                if self.frame_count % 45 == 0:
                    self.glitch_active = True
                    self.glitch_duration = random.randint(2, 5)

                if self.glitch_active and self.glitch_duration > 0:
                    self.glitch_duration -= 1
                    glitch_type = random.choice(["slice", "chromatic", "invert"])
                    
                    if glitch_type == "slice":
                        for _ in range(3):
                            y_start = random.randint(100, 600)
                            h_slice = random.randint(10, 40)
                            shift = random.randint(-20, 20)
                            frame[y_start:y_start+h_slice, :] = np.roll(frame[y_start:y_start+h_slice, :], shift, axis=1)
                    
                    elif glitch_type == "chromatic":
                        b, g, r = cv2.split(frame)
                        b = np.roll(b, 8, axis=1)
                        r = np.roll(r, -8, axis=1)
                        frame = cv2.merge([b, g, r])
                        
                    elif glitch_type == "invert":
                        frame = cv2.bitwise_not(frame)

                    if self.glitch_duration <= 0:
                        self.glitch_active = False

                # --- EFFECT 3: "AI-Native" Corporate Typography Overlay ---
                cv2.rectangle(frame, (0, 0), (500, 65), (5, 7, 10), -1)
                
                if (self.frame_count // 30) % 3 == 0:
                    text_str = "REINVENTING THE FUTURE OF REFRESHMENT"
                    color_text = (0, 229, 255)
                elif (self.frame_count // 30) % 3 == 1:
                    text_str = "AGENTIC COFFEE WORKFLOW DISPATCHERS: ON"
                    color_text = (102, 255, 0)
                else:
                    text_str = "INTELLIGENT SYSTEM MATRIX // LIQUID LAYER"
                    color_text = (0, 153, 255)
                
                cv2.putText(frame, text_str, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.45, color_text, 1, cv2.LINE_AA)
                
                cv2.line(frame, (0, 64), (500, 64), (26, 38, 51), 1)

                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(cv2_image)
                tk_img = ImageTk.PhotoImage(image=pil_img)

                self.video_label.configure(image=tk_img)
                self.video_label.image = tk_img 
            else:
                self.handle_video_failure("STREAM INTERRUPTED")
                return
        except Exception as e:
            print(f"[FX Pipeline Exception]: {e}")

        self.after(33, self.play_video_frame)

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
        try:
            from bookings.models import MasterBooking
        except ImportError:
            messagebox.showerror("Configuration Error", "Django Database Models Unavailable.")
            return

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

            if ReceiptWindow is not None:
                ReceiptWindow(self, "Cafe Guest", all_items_string, total)
            else:
                messagebox.showinfo("Success", f"Order Logged! Total: ₹{total}")
                
            self.terminate_window() 
            
        except Exception as e:
            messagebox.showerror("Data Loss Fault", f"Failed to sync central storage block: {e}")

    def terminate_window(self):
        self.is_running = False
        if self.video_cap is not None:
            self.video_cap.release()
            self.video_cap = None
        self.destroy()