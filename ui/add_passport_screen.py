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
        outer_frame = ttk.Frame(self, padding=10, style="Rounded.TFrame")
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Back Button
        back_button = ttk.Button(outer_frame, text="رجوع", style="Blue.TButton", command=self.return_callback)
        back_button.grid(row=0, column=5, padx=5, pady=10, sticky="ew")  # تم تعديل sticky ليكون "ew" لتمديد الزر

        # Row 1
        self.name_entry = self.create_field(outer_frame, "اسم الزبون:", row=1, column=5)
        self.booking_date_entry = self.create_field(outer_frame, "تاريخ الحجز:", row=1, column=3, entry_var=self.booking_date)
        self.type_combobox = self.create_field(outer_frame, "النوع:", row=1, column=1, combobox_values=["عادي", "مستعجل بيومه", "مستعجل عدن"])

        # Row 2
        self.booking_price_entry = self.create_field(outer_frame, "التكلفة (سعر الحجز):", row=2, column=5)
        self.purchase_price_entry = self.create_field(outer_frame, "سعر الشراء:", row=2, column=3, entry_var=self.purchase_price)
        self.net_amount_label = self.create_field(outer_frame, "الصافي:", row=2, column=1, label_var=self.net_amount)

        # Row 3
        self.paid_amount_entry = self.create_field(outer_frame, "الواصل:", row=3, column=5)
        self.remaining_amount_label = self.create_field(outer_frame, "المتبقي:", row=3, column=3, label_var=self.remaining_amount)
        self.status_combobox = self.create_field(outer_frame, "حالة الجواز:", row=3, column=1, combobox_values=["في الطباعة", "مرفوض", "تم التسليم"])

        # Row 4
        self.receipt_date_entry = self.create_field(outer_frame, "تاريخ الاستلام:", row=4, column=5)
        self.receiver_name_entry = self.create_field(outer_frame, "اسم المستلم:", row=4, column=3)

        # Save Button
        save_button = ttk.Button(outer_frame, text="حفظ", style="Blue.TButton", width=50, command=self.save)
        save_button.grid(row=5, column=0, columnspan=5, pady=20)  # زيادة pady هنا

    def create_field(self, parent, label_text, row, column, entry_var=None, label_var=None, combobox_values=None):
        """Helper function to create a label and its corresponding widget."""
        ttk.Label(parent, text=label_text, style="Bold.TLabel").grid(row=row, column=column, padx=(10, 10), pady=10, sticky="ew")
        if combobox_values is None:
            if label_var is not None:
                widget = ttk.Label(parent, textvariable=label_var, style="Bold.TLabel", justify="center")  # محاذاة النص في المنتصف
                widget.grid( sticky="ew")
            else:
                widget = ttk.Entry(parent, font=("Arial", 12), width=30, style="Rounded.TEntry", textvariable=entry_var, justify="center")  # محاذاة النص في المنتصف
            widget.grid(row=row, column=column - 1, padx=(10, 10), pady=10, sticky="ew")  # تم تعديل sticky ليكون "ew" لتمديد الحقل
        else:
            widget = ttk.Combobox(parent, values=combobox_values, font=("Arial", 12), width=23, style="Rounded.TCombobox", justify="center")  # محاذاة النص في المنتصف
            widget.grid(row=row, column=column - 1, padx=(10, 10), pady=10, sticky="ew")  # تم تعديل sticky ليكون "ew" لتمديد الحقل
            widget.current(0)
        return widget

    def apply_styles(self):
        """Apply custom styles to the widgets."""
        style = ttk.Style(self)

        # Custom Frame Style (Rounded corners and shadow)
        style.configure("Rounded.TFrame", background="#f3f3f3", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=10)
        style.map("Rounded.TFrame", background=[("active", "#f3f3f3")])

        # Custom Label Style (Bold)
        style.configure("Bold.TLabel", background="#f3f3f3", font=("Arial", 12, 'bold'))

        # Custom Entry Style (Rounded corners)
        style.configure("Rounded.TEntry", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=5)
        style.map("Rounded.TEntry", background=[("active", "#f0f0f0")])

        # Custom Combobox Style (Rounded corners)
        style.configure("Rounded.TCombobox", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=5)
        style.map("Rounded.TCombobox", background=[("active", "#f0f0f0")])

        # Custom Button Style (Blue)
        style.configure("Blue.TButton", background="#007bff", foreground="black", font=("Arial", 12, 'bold'), padding=10, width=30)
        style.map("Blue.TButton", background=[("active", "#0056b3")])

    def calculate_net_amount(self, event=None):
        """Calculate the net amount based on purchase price and booking price."""
        try:
            purchase_price = float(self.purchase_price_entry.get())
            booking_price = float(self.booking_price_entry.get())
            net_amount = booking_price - purchase_price
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
        # Collect data from the form
        data = (
            len(self.master.table.get_children()) + 1,  # Auto-increment ID
            self.name_entry.get(),  # Name
            self.booking_date_entry.get(),  # Booking Date
            self.type_combobox.get(),  # Type
            self.booking_price_entry.get(),  # Booking Price
            self.purchase_price_entry.get(),  # Purchase Price
            self.net_amount.get(),  # Net Amount
            self.paid_amount_entry.get(),  # Paid Amount
            self.remaining_amount.get(),  # Remaining Amount
            self.status_combobox.get(),  # Status
            self.receipt_date_entry.get(),  # Receipt Date
            self.receiver_name_entry.get(),  # Receiver Name
        )

        # Add data to the table
        self.master.add_to_table(data)

        # Return to the main screen
        self.return_callback()