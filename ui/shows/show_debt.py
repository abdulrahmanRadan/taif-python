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
        self.return_callback = return_callback  # دالة الرجوع للشاشة الرئيسية

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
        self.back_btn.pack(side=tk.LEFT, padx=10, anchor="w")  # في اليسار تمامًا

        # Title Label (في الوسط)
        title_lbl = tk.Label(header_frame,
                            text="تفاصيل الدين",
                            font=("Arial", 20, "bold"),
                            bg="#295686",
                            fg="white")
        title_lbl.pack(side=tk.LEFT, expand=True, padx=10, anchor="center")  # في الوسط

        # Add Payment Button (في اليمين تمامًا)
        self.add_btn_header = tk.Button(header_frame,
                                        text="+ إضافة عملية جديدة",
                                        bg="#27ae60",
                                        fg="white",
                                        font=("Arial", 14),
                                        width=18,
                                        command=self.show_payment_dialog)
        self.add_btn_header.pack(side=tk.RIGHT, padx=10, anchor="e")  # في اليمين تمامًا


        # Debt Details Section
        details_frame = tk.LabelFrame(self,
                                    text="معلومات الدين",
                                    font=("Arial", 14, "bold"),
                                    bg="white",
                                    fg="#2c3e50")
        details_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Details Grid
        self.details_labels = {}
        fields = [
            ("رقم الدين:", "id"),
            ("الاسم:", "name"),
            ("النوع:", "type"),
            ("التاريخ:", "date"),
            ("المتبقي:", "remaining")
        ]
        
        for row, (label, key) in enumerate(fields):
            lbl = tk.Label(details_frame, 
                        text=label, 
                        font=("Arial", 12),
                        bg="white")
            lbl.grid(row=row, column=0, padx=20, pady=10, sticky="e")
            
            val = tk.Label(details_frame, 
                        font=("Arial", 12, "bold"),
                        bg="white")
            val.grid(row=row, column=1, padx=20, pady=10, sticky="w")
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

    def load_data(self):
        # Load Debt Details
        debt_data = self.service.get_by_id(self.debt_id, self.debt_type)
        if debt_data:
            formatted = self.service.format_record_data(self.debt_type, debt_data[0])
            for key, label in self.details_labels.items():
                label.config(text=formatted.get(key, ""))
        
        # Load Payments
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
        
        # 2. إنشاء نافذة الدفعة مع تحديد دالة الرجوع
        self.payment_dialog = PaymentDialog(
            self.master,
            self.debt_type,
            self.debt_id,
            self.service,
            self.on_payment_dialog_closed  # دالة تُستدعى عند إغلاق PaymentDialog
        )

    def return_to_show_debt(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.load_data()

    def on_payment_dialog_closed(self):
        """الدالة التي تُستدعى عند الرجوع من PaymentDialog"""
        # 1. إعادة عرض شاشة ShowDebt
        self.pack(fill=tk.BOTH, expand=True)
        
        # 2. تحديث البيانات إذا لزم الأمر
        self.load_data()