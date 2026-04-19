import os
import django
import tkinter as tk
from tkinter import ttk, messagebox
import billing_system
import cafe_system

# Example: Calling a function from your billing system
# billing_system.calculate_total()

# --- IMPORTANT: INITIALIZE DJANGO BEFORE IMPORTS ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now import your model
from cafe_system import CafeWindow
from bookings.models import MasterBooking

class NexusReserve:
    def __init__(self, root):
        self.root = root
        self.root.title("NexusReserve Super-App")
        self.root.geometry("450x450")
        
        
        # 1. Create a Main Container with padding
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # 2. Customer Name Row
        tk.Label(main_frame, text="Customer Name:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=10)
        self.ent_name = tk.Entry(main_frame, width=25)
        self.ent_name.grid(row=0, column=1, pady=10)

        # 3. Category Dropdown Row
        tk.Label(main_frame, text="Category:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky="w", pady=10)
        self.cat_var = tk.StringVar(value="CAFE")
        self.drop = ttk.Combobox(main_frame, textvariable=self.cat_var, width=22)
        self.drop['values'] = ("FLIGHT", "TRAIN", "MOVIE", "CAFE")
        self.drop.grid(row=1, column=1, pady=10)

        # 4. Delivery Checkbox Row
        self.deliv_var = tk.BooleanVar()
        tk.Checkbutton(main_frame, text="Is this a Delivery?", variable=self.deliv_var).grid(row=2, column=0, columnspan=2, pady=10)

        # 5. Buttons Row
        tk.Button(main_frame, text="Confirm Booking", bg="#2ecc71", fg="white", font=('Arial', 10, 'bold'), 
                  command=self.save_to_db, width=20).grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(main_frame, text="View All Bookings", bg="#3498db", fg="white", font=('Arial', 10, 'bold'),
                  command=self.show_records, width=20).grid(row=4, column=0, columnspan=2, pady=5)
        # Update your button to this:
        tk.Button(main_frame, text="Open Cafe Ordering ☕", 
          bg="#e67e22", fg="white", font=('Arial', 10, 'bold'),
          command=lambda: CafeWindow(root), # This opens the new file's window
          width=20).grid(row=5, column=0, columnspan=2, pady=5)

        # This line changes the 'theme' of the whole app
        style = ttk.Style()
        style.theme_use('clam') # Options: 'clam', 'alt', 'default', 'classic'

        # You can even change the button color globally
        style.configure("TButton", foreground="white", background="#2c3e50", font=('Helvetica', 10, 'bold'))

    def save_to_db(self):
        name = self.ent_name.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name!")
            return
        # Temporarily change button color to show it's working
        self.root.config(cursor="watch") # Changes mouse to a loading spinner
        self.root.update()
        # (After saving...)
        self.root.config(cursor="") # Changes mouse back to normal
        # Save to SQLite via Django ORM
        booking = MasterBooking(
            customer_name=name,
            category=self.cat_var.get(),
            details="General Booking",
            total_bill=0.0, # Logic for calculation goes here later
            is_delivery=self.deliv_var.get()
        )
        booking.save()
        messagebox.showinfo("Success", f"Booking saved for {name} in SQLite!")

     # Add this method inside your NexusReserve class
    def show_records(self):
        # 1. Create a new popup window
        view_window = tk.Toplevel(self.root)
        view_window.title("All Bookings")
        view_window.geometry("600x300")

        # 2. Create the Treeview table
        tree = ttk.Treeview(view_window, columns=("Name", "Category", "Bill", "Delivery"), show='headings')
        tree.heading("Name", text="Customer Name")
        tree.heading("Category", text="Category")
        tree.heading("Bill", text="Total Bill")
        tree.heading("Delivery", text="Delivery?")
        tree.pack(fill="both", expand=True)

        # 3. Pull data from Django and insert into the table
        for b in MasterBooking.objects.all():
            tree.insert("", "end", values=(b.customer_name, b.category, b.total_bill, b.is_delivery))

    def open_cafe_page(self):
        # 1. Create a new window for the Cafe
        self.cafe_window = tk.Toplevel(self.root)
        self.cafe_window.title("Cafe Management Dashboard")
        self.cafe_window.geometry("600x400")
        self.cafe_window.configure(bg="#ffffff")

        # 2. Title for the page
        tk.Label(self.cafe_window, text="☕ Cafe Bookings List", 
                 font=('Helvetica', 16, 'bold'), bg="white", fg=self.primary_color).pack(pady=10)

        # 3. Create the Treeview (Table)
        columns = ("Name", "Total Bill", "Delivery")
        tree = ttk.Treeview(self.cafe_window, columns=columns, show='headings')
        
        # Set column headers
        tree.heading("Name", text="Customer Name")
        tree.heading("Total Bill", text="Bill Amount")
        tree.heading("Delivery", text="Is Delivery?")
        
        # 4. FILTER: Fetch ONLY "CAFE" bookings from Django
        cafe_data = MasterBooking.objects.filter(category="CAFE")

        for b in cafe_data:
            delivery_status = "Yes" if b.is_delivery else "No"
            tree.insert("", "end", values=(b.customer_name, f"₹{b.total_bill}", delivery_status))

        tree.pack(fill="both", expand=True, padx=20, pady=20)          

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusReserve(root)
    root.mainloop()