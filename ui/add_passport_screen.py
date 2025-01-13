import tkinter as tk
from tkinter import ttk
from datetime import datetime

class AddPassportScreen(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, bg="#f5f5f5")  # خلفية رمادية فاتحة
        self.return_callback = return_callback  # Callback للرجوع إلى الشاشة السابقة

        # Variables
        self.booking_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.remaining_amount = tk.StringVar(value="0")
        self.purchase_price = tk.StringVar(value="0")  # سعر الشراء
        self.net_amount = tk.StringVar(value="0")  # الصافي

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        """Create all the widgets for the add customer screen."""
        # Apply custom styles
        self.apply_styles()

        # Outer Frame
        outer_frame = ttk.Frame(self, padding=20, style="Rounded.TFrame")
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Back Button
        back_button = ttk.Button(outer_frame, text="رجوع", style="Blue.TButton", command=self.return_callback)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Name
        ttk.Label(outer_frame, text="اسم الزبون:", style="Bold.TLabel").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = ttk.Entry(outer_frame, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Booking Date
        ttk.Label(outer_frame, text="تاريخ الحجز:", style="Bold.TLabel").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.booking_date_entry = ttk.Entry(outer_frame, textvariable=self.booking_date, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.booking_date_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Type (Dropdown)
        ttk.Label(outer_frame, text="النوع:", style="Bold.TLabel").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.type_combobox = ttk.Combobox(outer_frame, values=["عادي", "مستعجل بيومه", "مستعجل عدن"], font=("Arial", 12), width=23, style="Rounded.TCombobox")
        self.type_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.type_combobox.current(0)

        # Booking Price
        ttk.Label(outer_frame, text="التكلفة (سعر الحجز):", style="Bold.TLabel").grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.booking_price_entry = ttk.Entry(outer_frame, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.booking_price_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        self.booking_price_entry.bind("<KeyRelease>", self.calculate_net_amount)

        # Purchase Price
        ttk.Label(outer_frame, text="سعر الشراء:", style="Bold.TLabel").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.purchase_price_entry = ttk.Entry(outer_frame, textvariable=self.purchase_price, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.purchase_price_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.purchase_price_entry.bind("<KeyRelease>", self.calculate_net_amount)

        # Net Amount
        ttk.Label(outer_frame, text="الصافي:", style="Bold.TLabel").grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.net_amount_label = ttk.Label(outer_frame, textvariable=self.net_amount, style="Bold.TLabel")
        self.net_amount_label.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        # Paid Amount
        ttk.Label(outer_frame, text="الواصل:", style="Bold.TLabel").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.paid_amount_entry = ttk.Entry(outer_frame, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.paid_amount_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.paid_amount_entry.bind("<KeyRelease>", self.calculate_remaining)

        # Remaining Amount
        ttk.Label(outer_frame, text="المتبقي:", style="Bold.TLabel").grid(row=4, column=2, padx=10, pady=10, sticky="e")
        self.remaining_amount_label = ttk.Label(outer_frame, textvariable=self.remaining_amount, style="Bold.TLabel")
        self.remaining_amount_label.grid(row=4, column=3, padx=10, pady=10, sticky="w")

        # Passport Status (Dropdown)
        ttk.Label(outer_frame, text="حالة الجواز:", style="Bold.TLabel").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.status_combobox = ttk.Combobox(outer_frame, values=["في الطباعة", "مرفوض", "تم التسليم"], font=("Arial", 12), width=23, style="Rounded.TCombobox")
        self.status_combobox.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.status_combobox.current(0)

        # Receipt Date
        ttk.Label(outer_frame, text="تاريخ الاستلام:", style="Bold.TLabel").grid(row=5, column=2, padx=10, pady=10, sticky="e")
        self.receipt_date_entry = ttk.Entry(outer_frame, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.receipt_date_entry.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        # Receiver Name (Optional)
        ttk.Label(outer_frame, text="اسم المستلم:", style="Bold.TLabel").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.receiver_name_entry = ttk.Entry(outer_frame, font=("Arial", 12), width=25, style="Rounded.TEntry")
        self.receiver_name_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Save Button
        save_button = ttk.Button(outer_frame, text="حفظ", style="Blue.TButton", width=30, command=self.save)
        save_button.grid(row=7, column=0, columnspan=4, pady=20)

    def apply_styles(self):
        """Apply custom styles to the widgets."""
        style = ttk.Style(self)

        # Custom Frame Style (Rounded corners and shadow)
        style.configure("Rounded.TFrame", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=10)
        style.map("Rounded.TFrame", background=[("active", "#f0f0f0")])

        # Custom Label Style (Bold)
        style.configure("Bold.TLabel", background="#ffffff", font=("Arial", 12, 'bold'))

        # Custom Entry Style (Rounded corners)
        style.configure("Rounded.TEntry", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=5)
        style.map("Rounded.TEntry", background=[("active", "#f0f0f0")])

        # Custom Combobox Style (Rounded corners)
        style.configure("Rounded.TCombobox", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=5)
        style.map("Rounded.TCombobox", background=[("active", "#f0f0f0")])

        # Custom Button Style (Blue)
        style.configure("Blue.TButton", background="#007bff", foreground="white", font=("Arial", 12, 'bold'), padding=10, width=30)
        style.map("Blue.TButton", background=[("active", "#0056b3")])

    def calculate_net_amount(self, event=None):
        """Calculate the net amount based on purchase price and booking price."""
        try:
            purchase_price = float(self.purchase_price_entry.get())
            booking_price = float(self.booking_price_entry.get())
            net_amount =   booking_price - purchase_price
            self.net_amount.set(f"{net_amount:.2f}")
        except ValueError:
            self.net_amount.set("0.00")

    def calculate_remaining(self, event=None):
        """Calculate the remaining amount based on booking price and paid amount."""
        try:
            booking_price = float(self.booking_price_entry.get())
            paid_amount = float(self.paid_amount_entry.get())
            remaining = booking_price - paid_amount
            self.remaining_amount.set(f"{remaining:.2f}")
        except ValueError:
            self.remaining_amount.set("0.00")

    def save(self):
        """Handle saving the new customer data."""
        # Here you can add the logic to save the data to a database or file
        print("Data Saved Successfully!")
        self.return_callback()  # العودة إلى الشاشة السابقة بعد الحفظ