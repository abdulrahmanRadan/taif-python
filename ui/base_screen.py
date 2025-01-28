import tkinter as tk
from tkinter import ttk, messagebox
import math

class BaseScreen(tk.Frame):
    def __init__(self, master, service, add_screen_class, edit_screen_class, columns):
        super().__init__(master, bg="white")
        self.master = master
        self.service = service
        self.add_screen_class = add_screen_class
        self.edit_screen_class = edit_screen_class
        self.columns = columns

        self.current_page =1
        self.rows_per_page = 10

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)

        for i in range(6):
            self.top_frame.grid_columnconfigure(i, weight=1)

        self.create_buttons()
        self.create_table_section()
        self.create_pagination_controls()

        self.add_screen = self.add_screen_class(self, self.show_main_screen, self.service)
        self.add_screen.grid(row=1, column=0, sticky="nsew")
        self.add_screen.grid_remove()

        self.edit_screen = None
        self.buttons_visible = False
        self.previous_selected_item = None

    def create_pagination_controls(self):
        # إضافة مرونة لتوسيع الإطار العلوي والسفلي بشكل ديناميكي
        self.grid_rowconfigure(1, weight=1)  # لإضافة مساحة فارغة أسفل الأزرار

        # الأزرار السفلية داخل إطار سفلي
        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 20))

        # إضافة توزيع الأزرار في منتصف الشاشة أفقيًا
        self.bottom_frame.grid_columnconfigure(0, weight=1)  # فراغ على اليسار
        self.bottom_frame.grid_columnconfigure(1, weight=1)  # العمود الخاص بالأزرار
        self.bottom_frame.grid_columnconfigure(2, weight=1)  # فراغ على اليمين

        # زر السابق
        self.previous_button = tk.Button(
            self.bottom_frame,
            text="السابق",
            font=("Arial", 12),
            command=self.go_to_previous_page,
            state=tk.DISABLED,
            bg="#4CAF50",  # لون الخلفية
            fg="white",    # لون النص
            relief=tk.RAISED,
            bd=2
        )
        self.previous_button.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        # صفحة حالية
        self.page_label = tk.Label(
            self.bottom_frame, 
            text=f"الصفحة: {self.current_page}", 
            font=("Arial", 12),
            bg="white"
        )
        self.page_label.grid(row=0, column=1, pady=5)

        # زر التالي
        self.next_button = tk.Button(
            self.bottom_frame,
            text="التالي",
            font=("Arial", 12),
            command=self.go_to_next_page,
            bg="#4CAF50",  # لون الخلفية
            fg="white",    # لون النص
            relief=tk.RAISED,
            bd=2
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    
    def go_to_previous_page(self):
        if self.current_page >1:
            self.current_page -= 1
            self.update_pagination_controls()
            self.refresh_table()

    def go_to_next_page(self):
        total_rows = len(self.service.get_all_data())
        total_pages = math.ceil(total_rows / self.rows_per_page)

        if self.current_page < total_pages:
            self.current_page += 1
            self.update_pagination_controls()
            self.refresh_table()
    
    def update_pagination_controls(self):
        total_rows = len(self.service.get_all_data())
        total_pages = math.ceil(total_rows / self.rows_per_page)

        self.page_label.config(text=f"الصفحة: {self.current_page}")

        if self.current_page == 1:
            self.previous_button.config(state=tk.DISABLED)
        else:
            self.previous_button.config(state=tk.NORMAL)

        if self.current_page == total_pages:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)
        
    def refresh_table(self):
        all_data = self.service.get_all_data()
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        self.populate_table(all_data[start_index:end_index])
    

    def create_buttons(self):
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

        self.edit_button = tk.Button(self.top_frame, text="تعديل", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.edit_row)
        self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
        self.edit_button.grid_remove()

        self.delete_button = tk.Button(self.top_frame, text="حذف", bg="red", fg="white", font=("Arial", 12), width=20, command=self.delete_row)
        self.delete_button.grid(row=0, column=3, padx=10, sticky="e")
        self.delete_button.grid_remove()

        self.add_button = tk.Button(self.top_frame, text="إضافة جديد", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.show_add_screen)
        self.add_button.grid(row=0, column=4, padx=(20, 10), sticky="e")

        self.export_excel_button = tk.Button(self.top_frame, text="تصدير إلى Excel", bg="green", fg="white", font=("Arial", 12), width=20, command=self.service.export_to_excel)
        self.export_excel_button.grid(row=0, column=5, padx=(10, 20), sticky="e")

    def create_table_section(self):
        table_frame = tk.Frame(self, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # عكس ترتيب الأعمدة
        reversed_columns = list(reversed(self.columns))

        self.table = ttk.Treeview(
            table_frame,
            columns=reversed_columns,  # استخدام الأعمدة المعكوسة
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            show="headings"
        )

        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        total_columns = len(reversed_columns)
        table_width = table_frame.winfo_width()

        for col in reversed_columns:
            if col == "ID":
                # print("ID", col)
                self.table.column(col, width=30, minwidth=10, stretch=False, anchor="center")
            else:
                self.table.column(col, width=int((table_width - 50) / (total_columns - 1)), anchor="center")
            self.table.heading(col, text=col)

        self.table.tag_configure("oddrow", background="#f0f0f0")
        self.table.tag_configure("evenrow", background="#ffffff")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", background='#568CC6', foreground='white', font=("Arial", 12, "bold"))
        style.map("Treeview.Heading", background=[("active", "#295686")], foreground=[("active", "white")])

        self.table.pack(fill=tk.BOTH, expand=True)

        self.refresh_table()

        self.table.bind("<ButtonRelease-1>", self.show_buttons)
        self.table.bind("<Double-Button-1>", self.on_double_click)

    def on_double_click(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            self.edit_button.grid_remove()
            self.delete_button.grid_remove()

            item_id = self.table.item(selected_item, "values")[-1]
            # print("item",item_id)
            data = self.service.get_by_id(item_id)
            # print(data)

            if data:
                self.edit_screen = self.edit_screen_class(self, self.show_main_screen, self.service, data)
                self.edit_screen.grid(row=1, column=0, sticky="nsew")
                self.table.master.grid_remove()
                self.hide_buttons_and_search()
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على البيانات!")

    def populate_table(self, data=None):
        self.table.delete(*self.table.get_children())
        data = data if data is not None else self.service.get_all_data()
        for index, item in enumerate(data):
            reversed_item = list(reversed(item))
            if index % 2 == 0:
                self.table.insert("", tk.END, values=reversed_item, tags=("evenrow",))
            else:
                self.table.insert("", tk.END, values=reversed_item, tags=("oddrow",))

    def show_buttons(self, event=None):
        selected_item = self.table.selection()
        if selected_item:
            if selected_item == self.previous_selected_item:
                if self.buttons_visible:
                    self.edit_button.grid_remove()
                    self.delete_button.grid_remove()
                    self.buttons_visible = False
                else:
                    self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
                    self.delete_button.grid(row=0, column=3, padx=10, sticky="e")
                    self.buttons_visible = True
            else:
                if not self.buttons_visible:
                    self.edit_button.grid(row=0, column=2, padx=10, sticky="e")
                    self.delete_button.grid(row=0, column=3, padx=10, sticky="e")
                    self.buttons_visible = True

            self.previous_selected_item = selected_item
        else:
            self.edit_button.grid_remove()
            self.delete_button.grid_remove()
            self.buttons_visible = False
            self.previous_selected_item = None

    def edit_row(self):
        selected_item = self.table.selection()
        if selected_item:
            item_id = self.table.item(selected_item, "values")[-1]
            data = self.service.get_by_id(item_id)

            if data:
                self.edit_screen = self.edit_screen_class(self, self.show_main_screen, self.service, data)
                self.edit_screen.grid(row=1, column=0, sticky="nsew")
                self.table.master.grid_remove()
                self.hide_buttons_and_search()
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على البيانات!")

    def delete_row(self):
        selected_item = self.table.selection()
        if selected_item:
            item_values = self.table.item(selected_item, "values")
            item_id = item_values[-1]
            person_name = item_values[-2]

            confirm = messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف البيانات للمستخدم: {person_name}?")
            if confirm:
                success, message = self.service.delete_data(item_id)
                if success:
                    self.table.delete(selected_item)
                    messagebox.showinfo("نجاح", "تم حذف البيانات بنجاح!")
                else:
                    messagebox.showerror("خطأ", message)

    def on_search(self, event=None):
        search_term = self.search_entry.get().strip()
        if search_term:
            results = self.service.search_data(search_term)
        else:
            results = self.service.get_all_data()
        self.populate_table(results)

    def show_add_screen(self):
        self.table.master.grid_remove()
        self.add_screen.grid()
        self.hide_buttons_and_search()

    def show_main_screen(self):
        if self.add_screen:
            self.add_screen.grid_remove()
        if self.edit_screen:
            self.edit_screen.grid_remove()
        self.table.master.grid()
        self.show_buttons_and_search()
        self.populate_table()

    def hide_buttons_and_search(self):
        self.export_excel_button.grid_remove()
        self.add_button.grid_remove()
        self.search_label.grid_remove()
        self.search_entry.grid_remove()
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