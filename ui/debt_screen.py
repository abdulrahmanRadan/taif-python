import tkinter as tk
from tkinter import ttk, messagebox
from services.debt_service import DebtService
from ui.shows.show_debt import ShowDebt 
import math


class DebtScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.service = DebtService(master)
        self.columns = ("ID", "الاسم", "النوع", "التاريخ", "المبلغ باليمني", "المبلغ بالسعودي","\u0627\u0644\u0645\u062a\u0628\u0642\u064a", "\u0627\u0644\u0648\u0627\u0635\u0644", "\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0648\u0627\u0635\u0644", "\u0646\u0648\u0639 \u0627\u0644\u0648\u0627\u0635\u0644")
        
        self.current_page = 1
        self.rows_per_page = 10
        self.buttons_visible = False
        self.previous_selected_item = None

        self.configure_grid()
        self.create_top_section()
        self.create_table_section()
        self.create_pagination_controls()
        
    def configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_top_section(self):
        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        
        # Search Section
        self.search_label = tk.Label(self.top_frame, text="بحث:", font=("Arial", 12), bg="white")
        self.search_label.grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.search_entry = tk.Entry(
            self.top_frame,
            font=("Arial", 12),
            width=30,
            highlightbackground="black",
            highlightthickness=2,
            relief=tk.FLAT
        )
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Edit Button
        self.view_button  = tk.Button(
            self.top_frame, 
            text="عرض التفاصيل", 
            bg="#295686", 
            fg="white", 
            font=("Arial", 12), 
            width=15,
            command=self.show_debt_details
        )
        self.view_button.grid(row=0, column=2, padx=10, sticky="e")
        self.view_button.grid_remove()

        # Export Button
        self.export_button = tk.Button(
            self.top_frame,
            text="تصدير إلى Excel",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            width=15,
            command=self.service.export_to_excel
        )
        self.export_button.grid(row=0, column=3, padx=(10, 20), sticky="e")

    def create_table_section(self):
        table_frame = tk.Frame(self, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew")

        # Scrollbars
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # Configure Treeview
        reversed_columns = list(reversed(self.columns))
        self.table = ttk.Treeview(
            table_frame,
            columns=reversed_columns,
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show="headings",
            style="Custom.Treeview"
        )

        # Configure Scrollbars
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Columns
        for col in reversed_columns:
            self.table.heading(col, text=col)
            width = 50 if col == "ID" else 150  # تصغير حجم عمود ID
            self.table.column(col, anchor="center", width=width)

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Custom.Treeview.Heading", 
            background="#568CC6", 
            foreground="white", 
            font=("Arial", 12, "bold"))
        self.style.map("Custom.Treeview.Heading", 
                background=[("active", "#295686")])

        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<ButtonRelease-1>", self.show_buttons)
        self.table.bind("<Double-Button-1>", self.on_double_click)

        self.refresh_table()

    def create_pagination_controls(self):
        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)

        # Pagination Buttons
        self.previous_button = tk.Button(
            self.bottom_frame,
            text="السابق",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.go_to_previous_page
        )
        self.previous_button.grid(row=0, column=0, padx=10, sticky="e")

        self.page_label = tk.Label(
            self.bottom_frame,
            text=f"الصفحة: {self.current_page}",
            font=("Arial", 12),
            bg="white"
        )
        self.page_label.grid(row=0, column=1)

        self.next_button = tk.Button(
            self.bottom_frame,
            text="التالي",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.go_to_next_page
        )
        self.next_button.grid(row=0, column=2, padx=10, sticky="w")

        self.update_pagination_controls()

    def refresh_table(self, data=None):
        # حذف البيانات القديمة من الجدول
        self.table.delete(*self.table.get_children())
        all_data = data if data else self.service.get_all_data()

        # إعداد الأعمدة الديناميكية
        base_columns = ["ID", "الاسم", "النوع", "التاريخ", "المبلغ باليمني", "المبلغ بالسعودي", "المتبقي"]
        max_payment_count = max((len(debt["payments"]) for debt in all_data), default=0)

        payment_columns = [
            f"المبلغ {i + 1}" for i in range(max_payment_count)
        ] + [
            f"تاريخ {i + 1}" for i in range(max_payment_count)
        ] + [
            f"نوع {i + 1}" for i in range(max_payment_count)
        ]

        dynamic_columns = base_columns + payment_columns
        self.table["columns"] = list(reversed(dynamic_columns))

        # تحديث رؤوس الأعمدة
        for col in reversed(dynamic_columns):
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=50 if col == "ID" else 150)

        # تعبئة الجدول
        for idx, debt in enumerate(all_data):
            row_data = [
                debt.get("id", ""),
                debt.get("name", ""),
                debt.get("type", ""),
                debt.get("date", ""),
                debt.get("ym_paid", 0),
                debt.get("sm_paid", 0),
                debt.get("remaining", 0),
            ]

            # إضافة المدفوعات الديناميكية
            for payment in debt.get("payments", []):
                row_data.extend([
                    payment.get("amount", ""),
                    payment.get("date", ""),
                    payment.get("method", ""),
                ])

            # تعبئة باقي الأعمدة الفارغة
            row_data.extend([""] * (len(dynamic_columns) - len(row_data)))

            # إدراج الصف
            self.table.insert("", tk.END, values=list(reversed(row_data)))

    def update_pagination_controls(self):
        total_rows = len(self.service.get_all_data())
        total_pages = math.ceil(total_rows / self.rows_per_page)
        
        self.previous_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)
        self.page_label.config(text=f"الصفحة: {self.current_page}")

    def on_double_click(self, event):
        selected_item = self.table.selection()
        if selected_item:
            self.show_debt_details()

    def show_buttons(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            self.view_button.grid()
        else:
            self.view_button.grid_remove()

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()
            self.update_pagination_controls()

    def go_to_next_page(self):
        total_rows = len(self.service.get_all_data())
        total_pages = math.ceil(total_rows / self.rows_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_table()
            self.update_pagination_controls()

    def on_search(self, event=None):
        search_term = self.search_entry.get().strip()
        results = self.service.search_data(search_term) if search_term else self.service.get_all_data()
        self.refresh_table(results)

    def show_debt_details(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("تحذير", "يرجى تحديد دين أولاً")
            return

        item_values = self.table.item(selected_item, "values")
        debt_id = item_values[-1]
        debt_type = item_values[-3]

        # إخفاء الإطار الرئيسي
        self.pack_forget()

        # عرض شاشة التفاصيل
        self.show_debt_screen = ShowDebt(
            self.master,
            debt_id,
            debt_type,
            self.service,
            self.return_to_main_screen
        )

    def return_to_main_screen(self):
        # إخفاء شاشة التفاصيل وإظهار الشاشة الرئيسية
        if hasattr(self, 'show_debt_screen'):
            self.show_debt_screen.destroy()
        self.pack(fill=tk.BOTH, expand=True)
        self.refresh_table()

    def return_to_debt_screen(self):
        self.pack(fill=tk.BOTH, expand=True)  # إعادة عرض الشاشة الرئيسية
        self.refresh_table()  # تحديث الجدول لعرض التغييرات


    
#