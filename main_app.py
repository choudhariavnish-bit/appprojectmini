import os
import django
import tkinter as tk
from tkinter import ttk, messagebox

# --- IMPORTANT: INITIALIZE DJANGO BEFORE IMPORTS ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now import your model
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

        # Theme Colors
        self.bg_color = "#094be6"  # Light Grayish Blue
        self.primary_color = "#f372c8" # Dark Blue
        self.root.configure(bg=self.bg_color)

        # 4. Delivery Checkbox Row
        self.deliv_var = tk.BooleanVar()
        tk.Checkbutton(main_frame, text="Is this a Delivery?", variable=self.deliv_var).grid(row=2, column=0, columnspan=2, pady=10)

        # 5. Buttons Row
        tk.Button(main_frame, text="Confirm Booking", bg="#2ecc71", fg="white", font=('Arial', 10, 'bold'), 
                  command=self.save_to_db, width=20).grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(main_frame, text="View All Bookings", bg="#3498db", fg="white", font=('Arial', 10, 'bold'),
                  command=self.show_records, width=20).grid(row=4, column=0, columnspan=2, pady=5)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusReserve(root)
    root.mainloop()