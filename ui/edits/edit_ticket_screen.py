import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from services.ticket_service import TicketService

class EditTicketScreen(tk.Frame):
    def __init__(self, master, return_callback, service, data):
        super().__init__(master, bg="#f5f5f5")
        self.return_callback = return_callback
        self.service = service
        self.data = data

        # Variables
        self.net_amount = tk.StringVar(value="0")
        self.paid_amount = tk.StringVar(value="0")
        self.remaining_amount = tk.StringVar(value="0")

        # Create Widgets
        self.create_widgets()
        self.populate_fields()

    def create_widgets(self):
        self.apply_styles()

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

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        back_button = ttk.Button(outer_frame, text="رجوع", style="Blue.TButton", command=self.return_callback)
        back_button.grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky="ew")

        # اسم الشخص
        self.name_entry = self.create_field(outer_frame, "الاسم", row=1, column=0)

        # رقم الجواز
        self.passport_number_entry = self.create_field(outer_frame, "رقم الجواز", row=1, column=2)

        # من مدينة
        self.from_place_entry = self.create_field(outer_frame, "من مدينة", row=2, column=0)

        # إلى مدينة
        self.to_place_entry = self.create_field(outer_frame, "إلى مدينة", row=2, column=2)

        # الشركة
        self.company_entry = self.create_field(outer_frame, "الشركة", row=3, column=0)

        # المبلغ
        self.amount_entry = self.create_field(outer_frame, "المبلغ", row=3, column=2)

        # العملة
        self.currency_combobox = self.create_field(outer_frame, "العملة", row=4, column=0, combobox_values=["ر.ي", "ر.س", "دولار"])

        # للوكيل
        self.agent_entry = self.create_field(outer_frame, "للوكيل", row=4, column=2)
        self.agent_entry.bind("<KeyRelease>", self.calculate_net)

        # الصافي
        self.net_amount_label = self.create_field(outer_frame, "الصافي", row=5, column=0, label_var=self.net_amount)

        # تاريخ الرحلة
        self.trip_date_entry = self.create_date_field(outer_frame, "تاريخ الرحلة", row=5, column=2)

        # المكتب
        self.office_combobox = self.create_field(outer_frame, "المكتب", row=6, column=0, combobox_values=["مكتبنا", "الوادي", "طايف"])

        # الحقول الجديدة
        self.paid_entry = self.create_field(outer_frame, "المدفوع", row=6, column=2, entry_var=self.paid_amount)
        self.remaining_amount_label = self.create_field(outer_frame, "المتبقي", row=7, column=0, label_var=self.remaining_amount)
        self.paid_entry.bind("<KeyRelease>", self.calculate_remaining_amount)

        # زر الحفظ
        save_button = ttk.Button(outer_frame, text="حفظ التعديلات", style="Blue.TButton", width=50, command=self.save)
        save_button.grid(row=8, column=0, columnspan=4, pady=20)

        for i in range(4):
            outer_frame.grid_columnconfigure(i, weight=1, uniform="col")

    def create_field(self, parent, label_text, row, column, entry_var=None, label_var=None, combobox_values=None):
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

        ttk.Label(parent, text=label_text, style="Bold.TLabel").grid(row=row, column=column + 1, padx=(10, 10), pady=10, sticky="ew")
        return widget

    def create_date_field(self, parent, label_text, row, column):
        widget = DateEntry(parent, font=("Arial", 12), width=25, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")

        ttk.Label(parent, text=label_text, style="Bold.TLabel").grid(row=row, column=column + 1, padx=(10, 10), pady=10, sticky="ew")
        return widget

    def apply_styles(self):
        style = ttk.Style(self)
        style.configure("Rounded.TFrame", background="#f3f3f3", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=10)
        style.configure("Bold.TLabel", background="#f3f3f3", font=("Arial", 12, 'bold'))
        style.configure("Rounded.TEntry", background="#ffffff", borderwidth=2, relief="solid", bordercolor="#cccccc", padding=5)
        style.configure("Blue.TButton", background="#007bff", font=("Arial", 12, 'bold'), padding=10, width=30)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_net(self, event=None):
        try:
            amount = float(self.amount_entry.get())
            agent = float(self.agent_entry.get())
            net = self.service.calculate_net_amount(amount, agent)
            self.net_amount.set(f"{net:.2f}")
            self.calculate_remaining_amount()
        except ValueError:
            self.net_amount.set("0.00")

    def calculate_remaining_amount(self, event=None):
        try:
            amount = float(self.amount_entry.get())
            paid = float(self.paid_amount.get())
            remaining = max(0, amount - paid)
            self.remaining_amount.set(f"{remaining:.2f}")
        except ValueError:
            self.remaining_amount.set("0.00")

    def populate_fields(self):
        if self.data:
            self.name_entry.insert(0, self.data[1])
            self.passport_number_entry.insert(0, self.data[2])
            self.from_place_entry.insert(0, self.data[3])
            self.to_place_entry.insert(0, self.data[4])
            self.company_entry.insert(0, self.data[5])
            self.amount_entry.insert(0, self.data[6])
            self.currency_combobox.set(self.data[7])
            self.agent_entry.insert(0, self.data[8])
            self.net_amount.set(self.data[9])
            self.trip_date_entry.set_date(self.data[10])
            self.office_combobox.set(self.data[11])
            self.paid_amount.set(self.data[12])
            self.remaining_amount.set(self.data[13])

    def save(self):
        if not self.validate_fields():
            return

        try:
            currency_map = {"ر.ي": "1", "ر.س": "2", "دولار": "3"}
            data = (
                self.data[0],  # ID
                self.name_entry.get(),
                self.passport_number_entry.get(),
                self.from_place_entry.get(),
                self.to_place_entry.get(),
                self.company_entry.get(),
                float(self.amount_entry.get()),
                currency_map.get(self.currency_combobox.get(), "1"),
                float(self.agent_entry.get()),
                float(self.net_amount.get()),
                self.trip_date_entry.get_date().strftime("%Y-%m-%d"),
                self.office_combobox.get(),
                float(self.paid_amount.get()),
                float(self.remaining_amount.get())
            )
        except ValueError as e:
            messagebox.showerror("خطأ", f"قيم غير صحيحة: {str(e)}")
            return

        success, message = self.service.update_ticket_data(data, self.master)
        if success:
            messagebox.showinfo("نجاح", message)
            self.return_callback()
        else:
            messagebox.showerror("خطأ", message)

    def validate_fields(self):
        required_fields = [
            (self.name_entry, "الاسم"),
            (self.passport_number_entry, "رقم الجواز"),
            (self.amount_entry, "المبلغ"),
            (self.paid_entry, "المدفوع")
        ]

        for field, name in required_fields:
            if not field.get().strip():
                messagebox.showerror("خطأ", f"يرجى ملء حقل {name}")
                return False
        return True