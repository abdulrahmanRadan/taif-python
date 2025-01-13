import tkinter as tk
from tkinter import ttk
from ui.add_passport_screen import AddPassportScreen

class PassportScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master

        # Search and Add New Section
        self.top_frame = tk.Frame(self, bg="white")
        self.top_frame.pack(fill=tk.X, pady=10, padx=10)

        # Create Buttons and Search Bar
        self.create_buttons()

        # Data Table
        self.create_table_section()

        # Add New Screen (Initially hidden)
        self.add_passport_screen = AddPassportScreen(self, self.show_main_screen)
        self.add_passport_screen.pack_forget()  # إخفاء واجهة الإضافة في البداية

    def create_buttons(self):
        """Create search bar, add new button, and export buttons."""
        # Search Bar
        self.search_label = tk.Label(self.top_frame, text="Search:", font=("Arial", 12), bg="white")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = tk.Entry(self.top_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export Buttons
        self.export_pdf_button = tk.Button(self.top_frame, text="Export to PDF", bg="green", fg="white", font=("Arial", 12), command=self.export_to_pdf)
        self.export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))

        self.export_excel_button = tk.Button(self.top_frame, text="Export to Excel", bg="green", fg="white", font=("Arial", 12), command=self.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT)

        # Add New Button
        self.add_button = tk.Button(self.top_frame, text="Add New", bg="blue", fg="white", font=("Arial", 12), width=20, command=self.show_add_screen)
        self.add_button.pack(side=tk.LEFT, padx=(20, 10))

    def create_table_section(self):
        """Create a table to display data."""
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Scrollbars
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # Table
        self.table = ttk.Treeview(
            table_frame, columns=("ID", "Name", "Passport Number", "Status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, show="headings"
        )

        # Configure Scrollbars
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Define Columns
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Passport Number", text="Passport Number")
        self.table.heading("Status", text="Status")

        self.table.column("ID", width=50)
        self.table.column("Name", width=200)
        self.table.column("Passport Number", width=150)
        self.table.column("Status", width=100)

        self.table.pack(fill=tk.BOTH, expand=True)

        # Dummy Data
        self.populate_table()

    def populate_table(self):
        """Populate the table with dummy data."""
        data = [
            (1, "John Doe", "P1234567", "Valid"),
            (2, "Jane Smith", "P7654321", "Expired"),
            (3, "Ali Ahmed", "P2345678", "Valid"),
            (4, "Fatima Khan", "P8765432", "Pending"),
        ]

        for item in data:
            self.table.insert("", tk.END, values=item)

    def show_add_screen(self):
        """Show the add passport screen."""
        self.table.pack_forget()  # إخفاء الجدول
        self.add_passport_screen.pack(fill=tk.BOTH, expand=True)  # إظهار واجهة الإضافة
        self.hide_buttons_and_search()  # إخفاء الأزرار وشريط البحث

    def show_main_screen(self):
        """Show the main screen (table)."""
        self.add_passport_screen.pack_forget()  # إخفاء واجهة الإضافة
        self.table.pack(fill=tk.BOTH, expand=True)  # إظهار الجدول
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

    def export_to_pdf(self):
        """Handle exporting data to PDF."""
        print("Export to PDF - Functionality not implemented yet.")

    def export_to_excel(self):
        """Handle exporting data to Excel."""
        print("Export to Excel - Functionality not implemented yet.")