import tkinter as tk
from tkinter import ttk, messagebox

class ShowDebt(tk.Frame):
    def __init__(self, master, debt_id, debt_type, service, return_callback):
        super().__init__(master, bg="white")
        self.master = master
        self.service = service
        self.debt_id = debt_id
        self.debt_type = debt_type
        self.return_callback = return_callback  # دالة الرجوع للشاشة الرئيسية

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # زر الرجوع
        self.back_button = tk.Button(
            self,
            text="رجوع",
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            command=self.return_callback
        )
        self.back_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        # زر إضافة عملية جديدة
        self.add_payment_button = tk.Button(
            self,
            text="إضافة عملية جديدة",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            command=self.open_add_payment_window
        )
        self.add_payment_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        # إطار تفاصيل الدين
        self.details_frame = tk.LabelFrame(
            self,
            text="تفاصيل الدين",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        self.details_frame.pack(fill=tk.X, padx=20, pady=10)

        # إطار المدفوعات
        self.payments_frame = tk.LabelFrame(
            self,
            text="سجل المدفوعات",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        self.payments_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # إنشاء Treeview لعرض المدفوعات
        self.payments_tree = ttk.Treeview(
            self.payments_frame,
            columns=("المبلغ", "التاريخ", "الطريقة"),
            show="headings",
            height=6
        )

        # تنسيق الأعمدة
        self.payments_tree.heading("المبلغ", text="المبلغ")
        self.payments_tree.heading("التاريخ", text="التاريخ")
        self.payments_tree.heading("الطريقة", text="طريقة الدفع")

        self.payments_tree.column("المبلغ", width=150, anchor="center")
        self.payments_tree.column("التاريخ", width=200, anchor="center")
        self.payments_tree.column("الطريقة", width=200, anchor="center")

        # إضافة شريط التمرير
        self.scrollbar = ttk.Scrollbar(
            self.payments_frame,
            orient="vertical",
            command=self.payments_tree.yview
        )
        self.payments_tree.configure(yscrollcommand=self.scrollbar.set)

        # التخطيط
        self.payments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_data(self):
        # جلب بيانات الدين
        debt_data = self.service.get_by_id(self.debt_id, self.debt_type)
        if not debt_data:
            messagebox.showerror("خطأ", "لم يتم العثور على البيانات")
            self.destroy()
            return

        debt_data = debt_data[0]  # لأن get_by_id ترجع قائمة
        formatted_debt = self.service.format_record_data(self.debt_type, debt_data)

        # عرض تفاصيل الدين
        fields = [
            ("رقم الدين:", formatted_debt.get("id", "")),
            ("الاسم:", formatted_debt.get("name", "")),
            ("النوع:", formatted_debt.get("type", "")),
            ("التاريخ:", formatted_debt.get("date", "")),
            ("المبلغ اليمني:", formatted_debt.get("ym_paid", "")),
            ("المبلغ السعودي:", formatted_debt.get("sm_paid", "")),
            ("المتبقي:", formatted_debt.get("remaining", ""))
        ]

        for row, (label, value) in enumerate(fields):
            tk.Label(self.details_frame, text=label, font=("Arial", 12), bg="white").grid(
                row=row, column=0, sticky="e", padx=10, pady=5
            )
            tk.Label(self.details_frame, text=value, font=("Arial", 12, "bold"), bg="white").grid(
                row=row, column=1, sticky="w", padx=10, pady=5
            )

        # تعبئة المدفوعات
        self.load_payments()

    def load_payments(self):
        # تنظيف البيانات القديمة
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)

        # جلب البيانات الجديدة
        payments = self.service.get_payments(self.debt_type, self.debt_id)
        for payment in payments:
            self.payments_tree.insert("", "end", values=(
                f"{payment[3]} ريال",
                payment[4],
                payment[5]
            ))

    def open_add_payment_window(self):
        # نافذة إضافة عملية جديدة
        self.add_payment_window = tk.Toplevel(self)
        self.add_payment_window.title("إضافة عملية دفع")
        self.add_payment_window.geometry("400x300")

        # حقول الإدخال
        tk.Label(self.add_payment_window, text="المبلغ:").pack(pady=5)
        self.amount_entry = tk.Entry(self.add_payment_window)
        self.amount_entry.pack(pady=5)

        tk.Label(self.add_payment_window, text="التاريخ:").pack(pady=5)
        self.date_entry = tk.Entry(self.add_payment_window)
        self.date_entry.pack(pady=5)

        tk.Label(self.add_payment_window, text="طريقة الدفع:").pack(pady=5)
        self.method_entry = tk.Entry(self.add_payment_window)
        self.method_entry.pack(pady=5)

        # زر الحفظ
        save_button = tk.Button(
            self.add_payment_window,
            text="حفظ",
            command=self.save_payment
        )
        save_button.pack(pady=10)

    def save_payment(self):
        # التحقق من البيانات
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        method = self.method_entry.get()

        if not all([amount, date, method]):
            messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول")
            return

        # حفظ العملية
        try:
            self.service.db_manager.insert("Payments", {
                "debt_id": self.debt_id,
                "debt_type": self.debt_type,
                "amount": amount,
                "date": date,
                "method": method
            })

            messagebox.showinfo("نجاح", "تمت إضافة العملية بنجاح")
            self.add_payment_window.destroy()
            self.load_payments()  # تحديث قائمة المدفوعات
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {str(e)}")