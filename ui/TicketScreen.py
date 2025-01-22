import tkinter as tk
from tkinter import ttk, messagebox
from ui.adds.add_ticket_screen import AddTicketScreen
from services.ticket_service import TicketService
from ui.edits.edit_ticket_screen import EditTicketScreen

class TicketScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.service = TicketService(self)  # إنشاء كائن الخدمة

        #  جعل الإطار الرئيسي يتكيف مع حجم النافذة
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        
        # جعل أعمدة top_frame تتكيف مع العرض
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(3, weight=1)

        self.create_buttons()
        self.create_table_section()

        self.add_ticket_screen = AddTicketScreen(self, self.show_main_screen, self.service)
        self.add_ticket_screen.grid(row=1, column=0, sticky="nsew")
        self.add_ticket_screen.grid_remove()

        self.edit_ticket_screen = None

    def create_buttons(self):
        self.search_label = tk.Label(self.top_frame, text="بحث:", font=("Arial", 12), bg="white")
        self.search_label.grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.search_entry = tk.Entry(
            self.top_frame, font=("Arial", 12),
            width=30,
            highlightbackground="cyan",
            highlightthickness=2,
            relief=tk.FLAT
            )

        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # أزرار التعديل والحذف (مخفية بشكل افتراضي)
        self.edit_button = tk.Button(self.top_frame, text="تعديل", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.edit_row)
        self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
        self.edit_button.grid_remove()

        self.delete_button = tk.Button(self.top_frame, text="حذف", bg="red", fg="white", font=("Arial", 12), width=20, command=self.delete_row)
        self.delete_button.grid(row=0, column=3, padx=10, sticky="e")
        self.delete_button.grid_remove()


        self.add_button = tk.Button(self.top_frame, text="إضافة حجز جديد", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.show_add_screen)
        self.add_button.grid(row=0, column=4, padx=(20, 10), sticky="e")

        self.export_excel_button = tk.Button(self.top_frame, text="تصدير إلى Excel", bg="green", fg="white", font=("Arial", 12), width=20, command=self.service.export_to_excel)
        self.export_excel_button.grid(row=0, column=5, padx=(10, 20), sticky="e")
    def create_table_section(self):
        table_frame = tk.Frame(self, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew")

        # جعل الجدول يتكيف مع حجم النافذة
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "الاسم", "رقم الجواز", "من", "إلى", "الشركة", "المبلغ", "للوكيل", "الصافي", "تاريخ الرحلة", "المكتب"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show="headings"
        )

        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)

        # تخصيص ألوان الصفوف الزوجية والفردية
        self.table.tag_configure("oddrow", background="#f0f0f0")  # لون الصفوف الفردية
        self.table.tag_configure("evenrow", background="#ffffff")  # لون الصفوف الزوجية

        # تخصيص لون رأس الجدول
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", background='#568CC6', foreground='white', font=("Arial", 12, "bold"))
        
        # تخصيص لون رأس الجدول عند تحريك الماوس فوقه (hover)
        style.map("Treeview.Heading",
                background=[("active", "#295686")],  # لون الخلفية عند hover
                foreground=[("active", "white")]     # لون النص عند hover
                )

        self.table.pack(fill=tk.BOTH, expand=True)
        self.populate_table()
        
        # ربط حدث النقر على صف في الجدول
        self.table.bind("<ButtonRelease-1>", self.show_buttons)

    def populate_table(self, data=None):
        """
        تعبئة الجدول بالبيانات.
        """
        self.table.delete(*self.table.get_children())
        data = data if data is not None else self.service.get_all_data()
        for index, item in enumerate(data):  # استخدام المولد لاسترجاع البيانات
            if index % 2 == 0:
                self.table.insert("", tk.END, values=item, tags=("evenrow",))
            else:
                self.table.insert("", tk.END, values=item, tags=("oddrow",))

    def show_buttons(self, event=None):
        """
        عرض أزرار التعديل والحذف عند النقر على صف.
        """
        selected_item = self.table.selection()
        if selected_item:
            self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
            self.delete_button.grid(row=0, column=3, padx=10, sticky="e")
        else:
            self.edit_button.grid_remove()
            self.delete_button.grid_remove()
        
    def edit_row(self):
        """
        عرض واجهة التعديل عند النقر على زر التعديل.
        """
        selected_item = self.table.selection()
        if selected_item:
            # جلب id الصف المحدد
            item_id = self.table.item(selected_item, "values")[0]

            # البحث في قاعدة البيانات باستخدام id
            data = self.service.get_ticket_by_id(item_id)

            if data:
                # فتح واجهة التعديل مع البيانات المستردة
                self.edit_ticket_screen = EditTicketScreen(self, self.show_main_screen, self.service, data)
                self.edit_ticket_screen.grid(row=1, column=0, sticky="nsew")
                self.table.master.grid_remove()
                self.hide_buttons_and_search()
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على البيانات!")
    
    def delete_row(self):
        """
        دالة الحذف.
        """
        selected_item = self.table.selection()
        if selected_item:
            item_values = self.table.item(selected_item, "values")
            item_id = item_values[0]
            person_name = item_values[1]

            # حذف البيانات من قاعدة البيانات
            confirm = messagebox.askyesno("تاكيد الحذف", f"هل انت متاكد من حذف البيانات للمستخدم: {person_name}?")
            if confirm:
                success, message = self.service.delete_ticket_data(item_id)
                if success:
                    self.table.delete(selected_item)
                    messagebox.showinfo("نجاح", "تم حذف البيانات بنجاح!")
                else:
                    messagebox.showerror("خطأ", message)


    def on_search(self, event=None):
        """
        البحث عند تغيير نص حقل البحث.
        """
        search_term = self.search_entry.get().strip()
        if search_term:
            results = self.service.search_data(search_term)
        else:
            results = self.service.get_all_data()
        self.populate_table(results)

    def add_to_table(self, data):
        formatted_data = self.service.merge_currency_with_amounts(data)  # دمج العملة مع الأعمدة
        formatted_data = formatted_data[:6] + formatted_data[7:]  # إزالة العمود رقم 6 (العملة)
        self.table.insert("", tk.END, values=formatted_data)

    def show_add_screen(self):
        self.table.master.grid_remove()
        self.add_ticket_screen.grid()
        self.hide_buttons_and_search()

    def show_main_screen(self):
        if self.add_ticket_screen:
            self.add_ticket_screen.grid_remove()
        if self.edit_ticket_screen:
            self.edit_ticket_screen.grid_remove()
        self.table.master.grid()
        self.show_buttons_and_search()
        self.populate_table()

    def hide_buttons_and_search(self):
        self.export_excel_button.pack_forget()
        self.add_button.pack_forget()
        self.search_label.pack_forget()
        self.search_entry.pack_forget()
        self.edit_button.grid_remove()
        self.delete_button.grid_remove()

    def show_buttons_and_search(self):
        self.search_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.export_excel_button.grid(row=0, column=5, padx=(10, 20), sticky="e")
        self.add_button.grid(row=0, column=4, padx=(20, 10), sticky="e")

        selected_item = self.table.selection()
        if selected_item:
            self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
            self.delete_button.grid(row=0, column=3, padx=10, sticky="e")