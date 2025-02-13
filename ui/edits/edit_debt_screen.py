import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from services.debt_service import DebtService

class EditDebtScreen(tk.Frame):
    def __init__(self, master, return_callback, debt_service, debt_id, debt_type):
        super().__init__(master, bg="#f5f5f5")
        self.return_callback = return_callback
        self.debt_service = debt_service
        self.debt_id = debt_id
        self.debt_type = debt_type

        # Variables
        self.remaining_amount = tk.StringVar(value="0")
        self.paid_amount = tk.StringVar(value="0")

        # Load Debt Data
        self.debt_data = self.debt_service.get_by_id(debt_id, debt_type)
        # print(f"Debt Data: {self.debt_data}") 
        if not self.debt_data:
            messagebox.showerror("خطأ", "لم يتم العثور على الدين المحدد.")
            self.return_callback()

        # Create Widgets
        self.create_widgets()

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

        # Debt Details
        self.name_entry = self.create_field(outer_frame, "الاسم", row=1, column=0, entry_var=tk.StringVar(value=self.debt_data[1]))
        self.date_entry = self.create_date_field(outer_frame, "التاريخ", row=1, column=2, initial_date=self.debt_data[2])

        self.remaining_amount_label = self.create_field(outer_frame, "المتبقي", row=2, column=0, label_var=self.remaining_amount)
        self.paid_entry = self.create_field(outer_frame, "المدفوع", row=2, column=2, entry_var=self.paid_amount)

        self.paid_entry.bind("<KeyRelease>", self.calculate_remaining_amount)

        # Payment Method
        self.payment_method_combobox = self.create_field(outer_frame, "طريقة الدفع", row=3, column=0, combobox_values=["نقدي", "تحويل بنكي"])

        save_button = ttk.Button(outer_frame, text="حفظ التعديل", style="Blue.TButton", width=50, command=self.save)
        save_button.grid(row=4, column=0, columnspan=4, pady=20)

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

    def create_date_field(self, parent, label_text, row, column, initial_date=None):
        widget = DateEntry(parent, font=("Arial", 12), width=25, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        widget.grid(row=row, column=column, padx=(5, 5), pady=10, sticky="ew")
        if initial_date:
            widget.set_date(initial_date)

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

    def calculate_remaining_amount(self, event=None):
        try:
            remaining = float(self.debt_data[8]) - float(self.paid_amount.get())
            self.remaining_amount.set(f"{remaining:.2f}")
        except ValueError:
            self.remaining_amount.set("0.00")

    def save(self):
        try:
            paid_amount = float(self.paid_amount.get())
            if paid_amount <= 0:
                messagebox.showerror("خطأ", "المبلغ المدفوع يجب أن يكون أكبر من الصفر.")
                return

            # Update Debt Remaining Amount
            remaining_amount = float(self.remaining_amount.get())
            success, message = self.debt_service.mark_debt_as_paid(self.debt_id, self.debt_type)
            if not success:
                messagebox.showerror("خطأ", message)
                return

            # Add Payment to Payments Table
            payment_data = (
                self.debt_type,
                self.debt_id,
                paid_amount,
                self.date_entry.get_date().strftime("%Y-%m-%d"),
                self.payment_method_combobox.get()
            )
            self.debt_service.add_payment(payment_data)

            messagebox.showinfo("نجاح", "تم تحديث الدين وإضافة الدفع بنجاح.")
            self.return_callback()
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم رقمية صحيحة.")