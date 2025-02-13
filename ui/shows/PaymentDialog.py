import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # استيراد مكون التقويم

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
                                command=self.on_back_clicked)
        self.back_btn.place(x=20, y=15)

        # Form Section
        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=30, padx=50)

        # حقول القراءة فقط
        self.add_readonly_field(form_frame, 'نوع الدين:', self.debt_type, 0)
        self.add_readonly_field(form_frame, 'رقم الدين:', self.debt_id, 1)
        
        # الحقول القابلة للتعديل
        fields = [
            ("المبلغ:", "amount"),
            ("تاريخ السداد:", "payment_date"),
            ("طريقة الدفع:", "payment_method")
        ]
        
        self.entries = {}
        row = 2  # بدء من الصف الثالث بعد الحقول الثابتة
        for (label, field) in fields:  # التصحيح هنا
            lbl = tk.Label(form_frame, 
                          text=label,
                          font=("Arial", 14),
                          bg="#f0f4f7")
            lbl.grid(row=row, column=0, pady=15, sticky="e")
            
            if field == "payment_date":
                entry = DateEntry(form_frame,
                                font=("Arial", 14),
                                width=25,
                                bg="white",
                                date_pattern='yyyy-mm-dd')
            else:
                entry = tk.Entry(form_frame,
                                font=("Arial", 14),
                                width=25,
                                bg="white",
                                relief=tk.GROOVE)
            
            entry.grid(row=row, column=1, padx=20, pady=15)
            self.entries[field] = entry
            row += 1

        # Save Button
        save_btn = tk.Button(self,
                           text="حفظ العملية",
                           bg="#27ae60",
                           fg="white",
                           font=("Arial", 16, "bold"),
                           command=self.save_payment)
        save_btn.pack(pady=30)

    def add_readonly_field(self, parent, label, value, row):
        """إضافة حقل قراءة فقط"""
        tk.Label(parent,
               text=label,
               font=("Arial", 14),
               bg="#f0f4f7").grid(row=row, column=0, pady=15, sticky="e")
        
        entry = tk.Entry(parent,
            font=("Arial", 14),
            width=25,
            bg="#f0f4f7",
            relief=tk.FLAT)
        entry.insert(0, str(value))  # تحويل القيمة لنص
        entry.config(state='readonly')  # تعيين القراءة فقط بعد الإدخال
        entry.grid(row=row, column=1, padx=20, pady=15)

    def save_payment(self):
        try:
            # جمع البيانات من الحقول مباشرة مع التحقق من القيم
            amount = self.entries["amount"].get()
            payment_date = self.entries["payment_date"].get()
            payment_method = self.entries["payment_method"].get()

            # التحقق من عدم وجود حقول فارغة
            if not all([amount, payment_date, payment_method]):
                messagebox.showwarning("خطأ", "جميع الحقول مطلوبة")
                return

            # استدعاء خدمة الإضافة مع تمرير البارامترات بشكل صحيح
            self.service.add_payment(
                debt_type=self.debt_type,
                debt_id=self.debt_id,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method
            )
            
            messagebox.showinfo("نجاح", "تمت إضافة العملية بنجاح")
            self.return_callback()
            
        except ValueError as e:
            messagebox.showerror("خطأ", f"قيمة غير صحيحة: {str(e)}")
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
        
        # 2. إعادة عرض الشاشة السابقة
        self.return_callback()
        
# لا تستدعي self.return_callback() هنا