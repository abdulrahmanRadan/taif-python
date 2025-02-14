import tkinter as tk
from tkinter import ttk, messagebox
from ui.shows.PaymentDialog import PaymentDialog

class ShowDebt(tk.Frame):
    def __init__(self, master, debt_id, debt_type, service, return_callback):
        super().__init__(master, bg="#f0f4f7")
        self.master = master
        self.service = service
        self.debt_id = debt_id
        self.debt_type = debt_type
        self.return_callback = return_callback
        self.additional_labels = {}  # لتخزين الحقول الإضافية

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Header Section
        header_frame = tk.Frame(self, bg="#295686", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Back Button (في اليسار تمامًا)
        self.back_btn = tk.Button(header_frame,
                                text="← رجوع للقائمة",
                                bg="#e74c3c",
                                fg="white",
                                font=("Arial", 14),
                                width=12,
                                command=self.return_callback)
        self.back_btn.pack(side=tk.LEFT, padx=10, anchor="w")

        # Title Label (في الوسط)
        title_lbl = tk.Label(header_frame,
                            text="تفاصيل الدين",
                            font=("Arial", 20, "bold"),
                            bg="#295686",
                            fg="white")
        title_lbl.pack(side=tk.LEFT, expand=True, padx=10, anchor="center")

        # Add Payment Button (في اليمين تمامًا)
        self.add_btn_header = tk.Button(header_frame,
                                        text="+ إضافة عملية جديدة",
                                        bg="#27ae60",
                                        fg="white",
                                        font=("Arial", 14),
                                        width=18,
                                        command=self.show_payment_dialog)
        self.add_btn_header.pack(side=tk.RIGHT, padx=10, anchor="e")

        # Debt Details Section
        details_frame = tk.LabelFrame(self,
                                    text="معلومات الدين",
                                    font=("Arial", 14, "bold"),
                                    bg="white",
                                    fg="#2c3e50")
        details_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # الحقول الأساسية والإضافية في عمودين
        self.details_labels = {}
        base_fields = [
            ("رقم الدين:", "id"),
            ("الاسم:", "name"),
            ("النوع:", "type"),
            ("التاريخ:", "date"),
            ("المتبقي:", "remaining")
        ]
        
        # الحقول الإضافية
        additional_fields = self.get_additional_fields()
        all_fields = base_fields + additional_fields

        # تقسيم الحقول إلى عمودين
        half = len(all_fields) // 2
        if len(all_fields) % 2 != 0:
            half += 1

        # العمود الأول
        for row, (label, key) in enumerate(all_fields[:half]):
            lbl = tk.Label(details_frame, text=label, font=("Arial", 12), bg="white")
            lbl.grid(row=row, column=0, padx=20, pady=10, sticky="e")
            
            val = tk.Label(details_frame, font=("Arial", 12, "bold"), bg="white")
            val.grid(row=row, column=1, padx=20, pady=10, sticky="w")
            self.details_labels[key] = val

        # العمود الثاني
        for row, (label, key) in enumerate(all_fields[half:], start=0):
            lbl = tk.Label(details_frame, text=label, font=("Arial", 12), bg="white")
            lbl.grid(row=row, column=2, padx=20, pady=10, sticky="e")
            
            val = tk.Label(details_frame, font=("Arial", 12, "bold"), bg="white")
            val.grid(row=row, column=3, padx=20, pady=10, sticky="w")
            self.details_labels[key] = val

        # Payments Section
        payments_frame = tk.LabelFrame(self,
                                    text="سجل المدفوعات",
                                    font=("Arial", 14, "bold"),
                                    bg="white",
                                    fg="#2c3e50")
        payments_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(payments_frame,
                            columns=("id", "amount", "payment_date", "payment_method"),
                            show="headings",
                            style="Custom.Treeview")
        
        # Configure Columns
        columns = [
            ("id", "رقم العملية", 100),
            ("amount", "المبلغ", 150),
            ("payment_date", "تاريخ السداد", 200),
            ("payment_method", "طريقة الدفع", 200)
        ]
        
        for col_id, text, width in columns:
            self.tree.heading(col_id, text=text)
            self.tree.column(col_id, width=width, anchor="center")
        
        # Scrollbar
        scroll = ttk.Scrollbar(payments_frame, 
                            orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def get_additional_fields(self):
        """إرجاع الحقول الإضافية حسب نوع الدين"""
        fields_mapping = {
            "Passports": [
                ("سعر الحجز", "booking_price"),
                ("العملة", "currency")
            ],
            "Umrah": [
                ("رقم الجواز", "passport_number"),
                ("رقم الهاتف", "phone_number")
            ],
            "Trips": [
                ("مكان المغادرة", "from_place"),
                ("مكان الوصول", "to_place")
            ]
        }
        return fields_mapping.get(self.debt_type, [])

    def load_data(self):
        # جلب البيانات الخام
        raw_data = self.service.get_by_id(self.debt_id, self.debt_type)
        if raw_data and len(raw_data) > 0:
            record = raw_data[0]
            
            # تعبئة الحقول الأساسية
            self.details_labels["id"].config(text=record[0])
            self.details_labels["name"].config(text=record[1])
            self.details_labels["type"].config(text=self.debt_type)
            self.details_labels["date"].config(text=record[2] if self.debt_type == "Passports"  else record[9])
            self.details_labels["remaining"].config(text=record[8] if self.debt_type == "Passports" else record[7])
            
            # تعبئة الحقول الإضافية
            additional_fields = self.get_additional_fields()
            for _, key in additional_fields:
                if self.debt_type == "Passports":
                    if key == "booking_price":
                        self.details_labels[key].config(text=record[4])
                    elif key == "currency":
                        self.details_labels[key].config(text=record[11])
                elif self.debt_type == "Umrah":
                    if key == "passport_number":
                        self.details_labels[key].config(text=record[2])
                    elif key == "phone_number":
                        self.details_labels[key].config(text=record[3])
                elif self.debt_type == "Trips":
                    if key == "from_place":
                        self.details_labels[key].config(text=record[3])
                    elif key == "to_place":
                        self.details_labels[key].config(text=record[4])

        # تحميل المدفوعات
        self.tree.delete(*self.tree.get_children())
        payments = self.service.get_payments(self.debt_type, self.debt_id)
        for payment in payments:
            self.tree.insert("", "end", values=(
                payment["id"],
                f"{payment['amount']} ريال",
                payment["payment_date"],
                payment["payment_method"] or "غير محدد"
            ))

    def show_payment_dialog(self):
        self.pack_forget()
        self.payment_dialog = PaymentDialog(
            self.master,
            self.debt_type,
            self.debt_id,
            self.service,
            self.on_payment_dialog_closed
        )

    def return_to_show_debt(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.load_data()

    def on_payment_dialog_closed(self):
        """الدالة التي تُستدعى عند الرجوع من PaymentDialog"""
        self.pack(fill=tk.BOTH, expand=True)
        self.load_data()
# 