import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from services.passport_service import PassportService

class EditPassportScreen(tk.Frame):
    def __init__(self, master, return_callback, service, data):
        super().__init__(master, bg="#f5f5f5")
        self.return_callback = return_callback
        self.service = service
        self.data = data

        # Variables
        self.booking_price = tk.StringVar(value="0")
        self.purchase_price = tk.StringVar(value="0")
        self.paid_amount = tk.StringVar(value="0")
        self.net_amount = tk.StringVar(value="0")
        self.remaining_amount = tk.StringVar(value="0")

        # Create Widgets
        self.create_widgets()
        self.populate_fields()  # تعبئة الحقول بالبيانات المحددة

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

        # التواريخ
        self.booking_date_entry = self.create_date_field(outer_frame, "تاريخ الحجز", row=1, column=2)
        self.receipt_date_entry = self.create_date_field(outer_frame, "تاريخ الاستلام", row=2, column=2)

        # نوع الجواز
        self.type_combobox = self.create_field(outer_frame, "نوع الجواز", row=2, column=0, combobox_values=["عادي", "مستعجل عدن", "مستعجل بيومه", "غير ذلك"])

        # الأسعار ونوع العملة
        self.booking_price_entry = self.create_field(outer_frame, "سعر الحجز", row=3, column=0, entry_var=self.booking_price)
        self.booking_price_entry.bind("<KeyRelease>", self.calculate_amounts)

        self.purchase_price_entry = self.create_field(outer_frame, "سعر الشراء", row=3, column=2, entry_var=self.purchase_price)
        self.purchase_price_entry.bind("<KeyRelease>", self.calculate_amounts)

        self.net_amount_label = self.create_field(outer_frame, "الصافي", row=4, column=0, label_var=self.net_amount)

        self.paid_amount_entry = self.create_field(outer_frame, "المبلغ المدفوع", row=4, column=2, entry_var=self.paid_amount)
        self.paid_amount_entry.bind("<KeyRelease>", self.calculate_amounts)

        self.remaining_amount_label = self.create_field(outer_frame, "المبلغ المتبقي", row=5, column=0, label_var=self.remaining_amount)

        self.currency_combobox = self.create_field(outer_frame, "العملة", row=5, column=2, combobox_values=["ر.ي", "ر.س", "دولار"])

        # حالة الجواز
        self.status_combobox = self.create_field(outer_frame, "حالة الجواز", row=6, column=0, combobox_values=["في الطابعة", "في المكتب", "تم الاستلام", "مرفوض"])

        # اسم المستلم
        self.receiver_name_entry = self.create_field(outer_frame, "اسم المستلم", row=6, column=2)

        # زر الحفظ
        save_button = ttk.Button(outer_frame, text="حفظ", style="Blue.TButton", width=50, command=self.save)
        save_button.grid(row=7, column=0, columnspan=4, pady=20)

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

    def calculate_amounts(self, event=None):
        """
        حساب الصافي والمبلغ المتبقي تلقائيًا.
        """
        try:
            booking_price = float(self.booking_price.get() or 0)
            purchase_price = float(self.purchase_price.get() or 0)
            paid_amount = float(self.paid_amount.get() or 0)

            # حساب الصافي
            net_amount = booking_price - purchase_price
            self.net_amount.set(f"{net_amount:.2f}")

            # حساب المبلغ المتبقي
            remaining_amount = booking_price - paid_amount
            self.remaining_amount.set(f"{remaining_amount:.2f}")
        except ValueError:
            # إذا كانت القيم غير صحيحة، يتم تعيين القيم إلى 0
            self.net_amount.set("0.00")
            self.remaining_amount.set("0.00")

    def populate_fields(self):
        """
        تعبئة الحقول بالبيانات المستردة من قاعدة البيانات.
        """
        type_map_reverse = {"1": "عادي", "2": "مستعجل عدن", "3": "مستعجل بيومه", "4": "غير ذلك"}
        status_map_reverse = {"1": "في الطابعة", "2": "في المكتب", "3": "تم الاستلام", "4": "مرفوض"}
        currency_map_reverse = {"1": "ر.ي", "2": "ر.س", "3": "دولار"}

        if self.data:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.data[1])  # الاسم
            
            self.booking_date_entry.set_date(self.data[2])  # تاريخ الحجز
            self.receipt_date_entry.set_date(self.data[10])  # تاريخ الاستلام
            
            # تحويل نوع الجواز من رقم إلى نص
            passport_type = str(self.data[3])
            self.type_combobox.set(type_map_reverse.get(passport_type, "عادي"))
            
            self.booking_price.set(str(self.data[4]))  # سعر الحجز
            self.purchase_price.set(str(self.data[5]))  # سعر الشراء
            self.paid_amount.set(str(self.data[7]))  # المبلغ المدفوع
            
            # تحويل العملة من رقم إلى نص
            currency = str(self.data[12])
            self.currency_combobox.set(currency_map_reverse.get(currency, "ر.ي"))
            
            # تحويل حالة الجواز من رقم إلى نص
            status = str(self.data[9])
            self.status_combobox.set(status_map_reverse.get(status, "في الطابعة"))
            
            self.receiver_name_entry.delete(0, tk.END)
            self.receiver_name_entry.insert(0, self.data[11])  # اسم المستلم
            
            # حساب القيم تلقائيًا بعد التحميل
            self.calculate_amounts()

    def save(self):
        currency_map = {"ر.ي": "1", "ر.س": "2", "دولار": "3"}
        status_map = {"في الطابعة": "1", "في المكتب": "2", "تم الاستلام": "3", "مرفوض": "4"}
        type_map = {"عادي": "1", "مستعجل عدن": "2", "مستعجل بيومه": "3", "غير ذلك": "4"}

        currency = currency_map.get(self.currency_combobox.get(), "1")
        status = status_map.get(self.status_combobox.get(), "1")
        type_ = type_map.get(self.type_combobox.get(), "1")

        data = (
            self.data[0],  # ID من self.data
            self.name_entry.get(),
            self.booking_date_entry.get_date().strftime("%Y-%m-%d"),
            type_,
            float(self.booking_price.get()),
            float(self.purchase_price.get()),
            float(self.net_amount.get()),
            float(self.paid_amount.get()),
            float(self.remaining_amount.get()),
            status,
            self.receipt_date_entry.get_date().strftime("%Y-%m-%d"),
            self.receiver_name_entry.get(),
            currency
        )

        success, message = self.service.update_passport_data(data, self.master)
        if success:
            messagebox.showinfo("نجاح", message)
            self.grid_remove()  # إخفاء واجهة التعديل
            self.return_callback()
        else:
            messagebox.showerror("خطأ", message)