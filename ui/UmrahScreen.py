import tkinter as tk
from tkinter import ttk
from ui.add_umrah_screen import AddUmrahScreen
from services.umrah_service import UmrahService

class UmrahScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.service = UmrahService(self)  # إنشاء كائن من UmrahService

        # Search and Add New Section
        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        # Create Buttons and Search Bar
        self.create_buttons()

        # Data Table
        self.create_table_section()

        # Add New Screen (Initially hidden)
        self.add_umrah_screen = AddUmrahScreen(self, self.show_main_screen, self.service)
        self.add_umrah_screen.grid(row=1, column=0, sticky="nsew")
        self.add_umrah_screen.grid_remove()  # إخفاء واجهة الإضافة في البداية

        # Configure Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_buttons(self):
        """Create search bar, add new button, and export buttons."""
        # Search Bar
        self.search_label = tk.Label(self.top_frame, text="Search:", font=("Arial", 12), bg="white")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = tk.Entry(self.top_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Export Buttons
        self.export_pdf_button = tk.Button(self.top_frame, text="Export to PDF", bg="green", fg="white", font=("Arial", 12), command=self.service.export_to_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))

        self.export_excel_button = tk.Button(self.top_frame, text="Export to Excel", bg="green", fg="white", font=("Arial", 12), command=self.service.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT)

        # Add New Button
        self.add_button = tk.Button(self.top_frame, text="Add New", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.show_add_screen)
        self.add_button.pack(side=tk.LEFT, padx=(20, 10))

    def create_table_section(self):
        """Create a table to display data."""
        table_frame = tk.Frame(self, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew")

        # Scrollbars
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # Table
        self.table = ttk.Treeview(
            table_frame, columns=("ID", "Name", "Passport Number", "Phone Number", "Sponsor Name", "Sponsor Number", "Cost", "Paid", "Remaining", "Entry Date", "Exit Date", "Status",  "Days Left"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, show="headings"
        )

        # Configure Scrollbars
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Define Columns
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="اسم المعتمر")
        self.table.heading("Passport Number", text="رقم الجواز")
        self.table.heading("Phone Number", text="رقم الهاتف")
        self.table.heading("Sponsor Name", text="اسم الضمين")
        self.table.heading("Sponsor Number", text="رقم الضمين")
        self.table.heading("Cost", text="التكلفة")
        self.table.heading("Paid", text="الواصل")
        self.table.heading("Remaining", text="الباقي")
        self.table.heading("Entry Date", text="تاريخ الدخول")
        self.table.heading("Exit Date", text="تاريخ الخروج")
        self.table.heading("Days Left", text="عدد الأيام المتبقية")
        self.table.heading("Status", text="الحالة")

        self.table.column("ID", width=50)
        self.table.column("Name", width=150)
        self.table.column("Passport Number", width=100)
        self.table.column("Phone Number", width=100)
        self.table.column("Sponsor Name", width=150)
        self.table.column("Sponsor Number", width=100)
        self.table.column("Cost", width=100)
        self.table.column("Paid", width=100)
        self.table.column("Remaining", width=100)
        self.table.column("Entry Date", width=100)
        self.table.column("Exit Date", width=100)
        self.table.column("Days Left", width=100)
        self.table.column("Status", width=100)

        self.table.pack(fill=tk.BOTH, expand=True)

        # Load Data
        self.populate_table()

    def populate_table(self, data=None):
        """Populate the table with data from the service."""
        self.table.delete(*self.table.get_children())
        data = data if data is not None else self.service.get_all_data()

        for item in data:
            # print(item[13])
            # print(f"Item to insert: {item}")
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
        """Add a new row to the table with the provided data."""
        self.table.insert("", tk.END, values=data)

    def show_add_screen(self):
        """Show the add umrah screen."""
        self.table.master.grid_remove()  # إخفاء الجدول
        self.add_umrah_screen.grid()  # إظهار واجهة الإضافة
        self.hide_buttons_and_search()  # إخفاء الأزرار وشريط البحث

    def show_main_screen(self):
        """Show the main screen (table)."""
        self.add_umrah_screen.grid_remove()  # إخفاء واجهة الإضافة
        self.table.master.grid()  # إظهار الجدول
        self.show_buttons_and_search()  # إظهار الأزرار وشريط البحث

    def hide_buttons_and_search(self):
        """Hide the buttons and search bar when showing the add screen."""
        self.export_pdf_button.pack_forget()
        self.export_excel_button.pack_forget()
        self.add_button.pack_forget()
        self.search_label.pack_forget()
        self.search_entry.pack_forget()

    def show_buttons_and_search(self):
        """Show the buttons and search bar when returning to the main screen."""
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))
        self.export_excel_button.pack(side=tk.LEFT)
        self.add_button.pack(side=tk.LEFT, padx=(20, 10))