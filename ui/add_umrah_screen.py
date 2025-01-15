import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # استيراد DateEntry
from services.umrah_service import UmrahService

class AddUmrahScreen(tk.Frame):
    def __init__(self, master, return_callback, service):
        super().__init__(master, bg="#f5f5f5")
        self.return_callback = return_callback
        self.service = service  # كائن الخدمة

        # Variables
        self.remaining_amount = tk.StringVar(value="0")

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        """Create all the widgets for the add umrah screen."""
        # Apply custom styles
        self.apply_styles()

        # Outer Frame with Scrollbars
        self.canvas = tk.Canvas(self, bg="#f5f5f5", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        scroll_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        scroll_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        outer_frame = ttk.Frame(self.canvas, padding=10, style="Rounded.TFrame")
        self.canvas.create_window((0, 0), window=outer_frame, anchor="nw")

        # Bind Mouse Wheel for Scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Back Button
        back_button = ttk.Button(outer_frame, text="رجوع", style="Blue.TButton", command=self.return_callback)
        back_button.grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky="ew")

        # Row 1
        self.name_entry = self.create_field(outer_frame, "اسم المعتمر", row=1, column=0)
        self.passport_number_entry = self.create_field(outer_frame, "رقم الجواز", row=1, column=2)

        # Row 2
        self.phone_number_entry = self.create_field(outer_frame, "رقم الهاتف", row=2, column=0)
        self.sponsor_name_entry = self.create_field(outer_frame, "اسم الضمين", row=2, column=2)

        # Row 3
        self.sponsor_number_entry = self.create_field(outer_frame, "رقم الضمين", row=3, column=0)
        self.cost_entry = self.create_field(outer_frame, "التكلفة", row=3, column=2)
        self.cost_entry.bind("<KeyRelease>", self.calculate_remaining)  # ربط حدث لحساب الباقي

        # Row 4
        self.paid_entry = self.create_field(outer_frame, "الواصل", row=4, column=0)
        self.paid_entry.bind("<KeyRelease>", self.calculate_remaining)  # ربط حدث لحساب الباقي
        self.remaining_amount_label = self.create_field(outer_frame, "الباقي", row=4, column=2, label_var=self.remaining_amount)

        # Row 5
        self.entry_date_entry = self.create_date_field(outer_frame, "تاريخ الدخول", row=5, column=0)
        self.exit_date_entry = self.create_date_field(outer_frame, "تاريخ الخروج", row=5, column=2)

        # Row 6
        self.status_combobox = self.create_field(outer_frame, "الحالة", row=6, column=0, combobox_values=["مهم", "غير مهم"])

        # Save Button
        save_button = ttk.Button(outer_frame, text="حفظ", style="Blue.TButton", width=50, command=self.save)
        save_button.grid(row=7, column=0, columnspan=4, pady=20)

        # Configure Grid Columns to be Responsive
        for i in range(4):  # 4 columns
            outer_frame.grid_columnconfigure(i, weight=1, uniform="col")

    def create_field(self, parent, label_text, row, column, entry_var=None, label_var=None, combobox_values=None):
        """Helper function to create a label and its corresponding widget."""
        if combobox_values is None:
            if label_var is not None:
                widget = ttk.Label(parent, textvariable=label_var, style="Bold.TLabel", justify="center")
                widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")
            else:
                widget = ttk.Entry(parent, font=("Arial", 12), width=25, style="Rounded.TEntry", textvariable=entry_var, justify="center")
                widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")
        else:
            widget = ttk.Combobox(parent, values=combobox_values, font=("Arial", 12), width=23, style="Rounded.TCombobox", justify="center")
            widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")
            widget.current(0)

        # وضع الـ Label على اليمين من الحقل
        ttk.Label(parent, text=label_text, style="Bold.TLabel").grid(row=row, column=column + 1, padx=(10, 10), pady=10, sticky="ew")
        return widget

    def create_date_field(self, parent, label_text, row, column):
        """Helper function to create a date entry field."""
        widget = DateEntry(parent, font=("Arial", 12), width=25, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")

        # وضع الـ Label على اليمين من الحقل
        ttk.Label(parent, text=label_text, style="Bold.TLabel").grid(row=row, column=column + 1, padx=(10, 10), pady=10, sticky="ew")
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

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_remaining(self, event=None):
        """Calculate the remaining amount based on cost and paid amount."""
        try:
            cost = float(self.cost_entry.get())
            paid = float(self.paid_entry.get())
            remaining = self.service.calculate_remaining_amount(cost, paid)
            self.remaining_amount.set(f"{remaining:.2f}")
            # print(type(self.remaining_amount))
        except ValueError:
            self.remaining_amount.set("0.00")

    def save(self):
        """Handle saving the new umrah data."""
        # Collect data from the form
        data = (
            len(self.master.table.get_children()) + 1,  # Auto-increment ID
            self.name_entry.get(),  # Name
            self.passport_number_entry.get(),  # Passport Number
            self.phone_number_entry.get(),  # Phone Number
            self.sponsor_name_entry.get(),  # Sponsor Name
            self.sponsor_number_entry.get(),  # Sponsor Number
            float(self.cost_entry.get()),  # Cost
            float(self.paid_entry.get()),  # Paid
            float(self.remaining_amount.get()),  # Remaining
            self.entry_date_entry.get_date().strftime("%Y-%m-%d"),  # Entry Date
            self.exit_date_entry.get_date().strftime("%Y-%m-%d"),  # Exit Date
            self.status_combobox.get(),  # Status
        )

        # Save data using the service
        success, message = self.service.save_umrah_data(data, self.master)
        if success:
            messagebox.showinfo("نجاح", message)
            self.return_callback()  # العودة إلى الشاشة الرئيسية
        else:
            messagebox.showerror("خطأ", message)