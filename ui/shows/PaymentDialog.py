import tkinter as tk
from tkinter import ttk, messagebox

class PaymentDialog(tk.Frame):
    def __init__(self, master, debt_type, debt_id, service, return_callback):
        super().__init__(master, bg="#f0f4f7")
        self.master = master
        self.debt_type = debt_type
        self.debt_id = debt_id
        self.service = service
        self.return_callback = return_callback
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Header Section
        header_frame = tk.Frame(self, bg="#2980b9", height=80)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame,
                text="إضافة عملية سداد جديدة",
                font=("Arial", 20, "bold"),
                bg="#2980b9",
                fg="white").pack(pady=15)
        
        # Back Button
        self.back_btn = tk.Button(header_frame,
                                text="← رجوع",
                                bg="#e74c3c",
                                fg="white",
                                font=("Arial", 14),
                                command=self.on_back_clicked)  # استدعاء return_callback مباشرة
        self.back_btn.place(x=20, y=15)

        # Form Section
        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=30, padx=50)
        
        # Form Fields
        fields = [
            ("المبلغ:", "amount"),
            ("تاريخ السداد:", "payment_date"),
            ("طريقة الدفع:", "payment_method")
        ]
        
        self.entries = {}
        for row, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, 
                          text=label,
                          font=("Arial", 14),
                          bg="#f0f4f7")
            lbl.grid(row=row, column=0, pady=15, sticky="e")
            
            entry = tk.Entry(form_frame,
                            font=("Arial", 14),
                            width=25,
                            bg="white",
                            relief=tk.GROOVE)
            entry.grid(row=row, column=1, padx=20, pady=15)
            self.entries[field] = entry

        # Save Button
        save_btn = tk.Button(self,
                           text="حفظ العملية",
                           bg="#27ae60",
                           fg="white",
                           font=("Arial", 16, "bold"),
                           command=self.save_payment)
        save_btn.pack(pady=30)

    def save_payment(self):
        data = {
            "debt_type": self.debt_type,
            "debt_id": self.debt_id,
            "amount": self.entries["amount"].get(),
            "payment_date": self.entries["payment_date"].get(),
            "payment_method": self.entries["payment_method"].get()
        }
        
        if not all(data.values()):
            messagebox.showwarning("خطأ", "جميع الحقول مطلوبة")
            return
            
        try:
            self.service.add_payment(data)
            messagebox.showinfo("نجاح", "تمت إضافة العملية بنجاح")
            self.return_callback()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في الحفظ: {str(e)}")

    def return_callback(self):    
        # إزالة المرتبطين
        self.unbind_all("<MouseWheel>")
        
        # تدمير الإطار الحالي
        self.destroy()
    
    def on_back_clicked(self):
        """الدالة التي تُستدعى عند النقر على زر الرجوع"""
        # 1. تدمير الإطار الحالي
        self.unbind_all("<MouseWheel>")
        self.destroy()
        
        # 2. إعادة عرض شاشة ShowDebt
        self.return_callback()
        
# لا تستدعي self.return_callback() هنا