import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from reportlab.lib.pagesizes import A6 # Small receipt size
from reportlab.pdfgen import canvas

class ReceiptWindow(tk.Toplevel):
    def __init__(self, parent, customer_name, items, total, email="Not Provided"):
        super().__init__(parent)
        self.title("NexusReserve - Digital Receipt")
        self.geometry("350x550")
        self.configure(bg="white")

        # Store data for PDF generation
        self.customer_name = customer_name
        self.items = items
        self.total = total
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- UI Display (The Window you already have) ---
        tk.Label(self, text="NEXUS RESERVE", font=("Courier", 18, "bold"), bg="white").pack(pady=10)
        tk.Label(self, text="--------------------------", bg="white").pack()
        tk.Label(self, text=f"Date: {self.timestamp}", font=("Courier", 8), bg="white").pack()
        tk.Label(self, text=f"Customer: {customer_name}", font=("Courier", 10), bg="white").pack(anchor="w", padx=20)
        tk.Label(self, text="--------------------------", bg="white").pack()

        item_frame = tk.Frame(self, bg="white")
        item_frame.pack(fill="both", expand=True, padx=20)

        item_list = items.split(", ")
        for item in item_list:
            tk.Label(item_frame, text=item, font=("Courier", 10), bg="white").pack(anchor="w")

        tk.Label(self, text="--------------------------", bg="white").pack()
        tk.Label(self, text=f"TOTAL: ₹{total:.2f}", font=("Courier", 12, "bold"), bg="white").pack(pady=10)

        # --- Action Buttons ---
        tk.Button(self, text="Save as PDF & Close", command=self.save_and_exit, 
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), padx=10).pack(pady=10)

    def generate_pdf(self):
        """Generates a physical PDF file"""
        filename = f"Receipt_{self.customer_name.replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.pdf"
        
        # Create a small A6 sized receipt PDF
        c = canvas.Canvas(filename, pagesize=A6)
        width, height = A6

        # Header
        c.setFont("Courier-Bold", 16)
        c.drawCentredString(width/2, height - 40, "NEXUS RESERVE")
        
        c.setFont("Courier", 10)
        c.drawCentredString(width/2, height - 55, "--------------------------")
        c.drawString(30, height - 80, f"Date: {self.timestamp}")
        c.drawString(30, height - 95, f"Customer: {self.customer_name}")
        c.drawCentredString(width/2, height - 110, "--------------------------")

        # Items
        y_position = height - 130
        item_list = self.items.split(", ")
        c.setFont("Courier", 9)
        for item in item_list:
            c.drawString(30, y_position, item)
            y_position -= 15
            if y_position < 50: # Simple page overflow check
                c.showPage()
                y_position = height - 50

        # Footer
        c.drawCentredString(width/2, y_position - 10, "--------------------------")
        c.setFont("Courier-Bold", 12)
        c.drawString(30, y_position - 30, f"TOTAL AMOUNT: Rs.{self.total:.2f}")
        
        c.setFont("Courier-Oblique", 8)
        c.drawCentredString(width/2, 30, "Thank you for choosing Nexus!")
        
        c.save()
        return filename

    def save_and_exit(self):
        try:
            pdf_path = self.generate_pdf()
            messagebox.showinfo("Success", f"Receipt generated successfully!\nFile: {pdf_path}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")