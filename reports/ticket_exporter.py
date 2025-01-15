import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
import os
from database.database_manager import DatabaseManager

class TicketExporter:
    def __init__(self, master):
        self.master = master
        self.table_name = "Trips"  # اسم الجدول
        self.db_manager = DatabaseManager()

        # إنشاء نافذة التصدير
        self.export_window = tk.Toplevel(master)
        self.export_window.title("تصدير بيانات التذاكر إلى Excel")
        self.export_window.geometry("500x400")
        self.export_window.grab_set()  # جعل النافذة إجبارية
        self.center_window()

        # المتغيرات
        self.filename = tk.StringVar(value="تصدير_التذاكر")
        self.export_option = tk.StringVar(value="جميع البيانات")
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        # إنشاء الواجهة
        self.create_widgets()

    def center_window(self):
        """
        وضع النافذة في وسط الشاشة.
        """
        self.export_window.update_idletasks()
        width = self.export_window.winfo_width()
        height = self.export_window.winfo_height()
        x = (self.export_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.export_window.winfo_screenheight() // 2) - (height // 2)
        self.export_window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # إطار النموذج
        form_frame = ttk.Frame(self.export_window, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # حقل اسم الملف
        ttk.Label(form_frame, text="اسم الملف:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        filename_entry = ttk.Entry(form_frame, textvariable=self.filename, width=30)
        filename_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # قائمة منسدلة لخيارات التصدير
        ttk.Label(form_frame, text="خيارات التصدير:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        export_options = ttk.Combobox(
            form_frame,
            textvariable=self.export_option,
            values=["جميع البيانات", "حسب التاريخ", "بيانات بها مبالغ متبقية", "آخر 30 يوم", "آخر أسبوع"],
            state="readonly"
        )
        export_options.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        export_options.bind("<<ComboboxSelected>>", self.toggle_date_fields)

        # حقول التاريخ (مخفية بشكل افتراضي)
        self.start_date_label = ttk.Label(form_frame, text="تاريخ البداية:")
        self.start_date_entry = DateEntry(form_frame, textvariable=self.start_date, date_pattern="yyyy-mm-dd")
        self.end_date_label = ttk.Label(form_frame, text="تاريخ النهاية:")
        self.end_date_entry = DateEntry(form_frame, textvariable=self.end_date, date_pattern="yyyy-mm-dd")

        # زر التصدير
        export_button = ttk.Button(form_frame, text="تصدير", command=self.export_data)
        export_button.grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_date_fields(self, event=None):
        """
        إظهار أو إخفاء حقول التاريخ بناءً على الخيار المحدد.
        """
        if self.export_option.get() == "حسب التاريخ":
            self.start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            self.end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        else:
            self.start_date_label.grid_remove()
            self.start_date_entry.grid_remove()
            self.end_date_label.grid_remove()
            self.end_date_entry.grid_remove()

    def export_data(self):
        """
        تصدير البيانات إلى ملف Excel بناءً على الخيارات المحددة.
        """
        try:
            # بناء الاستعلام بناءً على الخيار المحدد
            query = f"SELECT * FROM {self.table_name}"
            conditions = []

            if self.export_option.get() == "حسب التاريخ":
                if not self.start_date.get() or not self.end_date.get():
                    messagebox.showwarning("تحذير", "يجب تحديد تاريخ البداية والنهاية.")
                    return
                conditions.append(f"trip_date BETWEEN '{self.start_date.get()}' AND '{self.end_date.get()}'")

            elif self.export_option.get() == "بيانات بها مبالغ متبقية":
                conditions.append("remaining_amount > 0")

            elif self.export_option.get() == "آخر 30 يوم":
                conditions.append("trip_date >= date('now', '-30 days')")

            elif self.export_option.get() == "آخر أسبوع":
                conditions.append("trip_date >= date('now', '-7 days')")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # جلب البيانات من قاعدة البيانات
            data = self.db_manager.execute_read_query(query)

            if not data:
                messagebox.showinfo("معلومات", "لا توجد بيانات للتصدير.")
                return

            # تحويل البيانات إلى DataFrame
            columns = [description[0] for description in self.db_manager.cursor.description]
            df = pd.DataFrame(data, columns=columns)

            # تحويل أسماء الأعمدة إلى العربية
            arabic_columns = {
                "id": "المعرف",
                "name": "الاسم",
                "passport_number": "رقم الجواز",
                "from_place": "من",
                "to_place": "إلى",
                "booking_company": "الشركة",
                "amount": "المبلغ",
                "currency": "العملة",
                "agent": "الوكيل",
                "net_amount": "الصافي",
                "trip_date": "تاريخ الرحلة",
                "office_name": "المكتب"
            }
            df.rename(columns=arabic_columns, inplace=True)

            # تحديد مسار حفظ الملف
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(downloads_path, f"{self.filename.get()}.xlsx")

            # تصدير البيانات إلى Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("نجاح", f"تم تصدير البيانات بنجاح إلى: {file_path}")

            # إغلاق النافذة بعد التصدير
            self.export_window.destroy()

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")