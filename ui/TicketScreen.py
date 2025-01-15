import tkinter as tk
from tkinter import ttk
from ui.add_ticket_screen import AddTicketScreen
from services.ticket_service import TicketService

class TicketScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.service = TicketService(self)  # إنشاء كائن الخدمة

        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        self.create_buttons()
        self.create_table_section()

        self.add_ticket_screen = AddTicketScreen(self, self.show_main_screen, self.service)
        self.add_ticket_screen.grid(row=1, column=0, sticky="nsew")
        self.add_ticket_screen.grid_remove()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_buttons(self):
        self.search_label = tk.Label(self.top_frame, text="بحث:", font=("Arial", 12), bg="white")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = tk.Entry(self.top_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.export_pdf_button = tk.Button(self.top_frame, text="تصدير إلى PDF", bg="green", fg="white", font=("Arial", 12), command=self.service.export_to_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))

        self.export_excel_button = tk.Button(self.top_frame, text="تصدير إلى Excel", bg="green", fg="white", font=("Arial", 12), command=self.service.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.top_frame, text="إضافة حجز جديد", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.show_add_screen)
        self.add_button.pack(side=tk.LEFT, padx=(20, 10))

    def create_table_section(self):
        table_frame = tk.Frame(self, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew")

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

        self.table.pack(fill=tk.BOTH, expand=True)
        self.populate_table()

    def populate_table(self, data=None):
        """
        تعبئة الجدول بالبيانات.
        """
        self.table.delete(*self.table.get_children())
        data = data if data is not None else self.service.get_all_data()
        for item in data:  # استخدام المولد لاسترجاع البيانات
            self.table.insert("", tk.END, values=item)

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
        self.add_ticket_screen.grid_remove()
        self.table.master.grid()
        self.show_buttons_and_search()

    def hide_buttons_and_search(self):
        self.export_pdf_button.pack_forget()
        self.export_excel_button.pack_forget()
        self.add_button.pack_forget()
        self.search_label.pack_forget()
        self.search_entry.pack_forget()

    def show_buttons_and_search(self):
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))
        self.export_excel_button.pack(side=tk.LEFT)
        self.add_button.pack(side=tk.LEFT, padx=(20, 10))